#!/usr/bin/env python3
"""Project VITAL A4: guarded, transactional OpenEMR CSV loader.

Run only inside the isolated vital-a4 Docker network. Dry-run by default.
"""
import argparse
import csv
import json
import os
import pathlib
import subprocess
import sys
import uuid
from collections import Counter

import pymysql

FILES = {
    'patients': ('patients.csv', {'pid','pubpid','fname','lname','DOB','sex','city','state'}),
    'encounters': ('encounters.csv', {'encounter','pid','date','reason'}),
    'appointments': ('appointments.csv', {'appointment_id','pc_pid','pc_eventDate','pc_startTime','pc_endTime','pc_duration','pc_catid','pc_apptstatus'}),
    'vitals': ('vitals.csv', {'vital_id','pid','encounter','date','bps','bpd','pulse','weight','height'}),
}
TABLES = ('patient_data','form_encounter','openemr_postcalendar_events','form_vitals','forms')


def read_csvs(directory):
    data = {}
    for kind, (filename, required) in FILES.items():
        with (directory / filename).open(newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or not required.issubset(reader.fieldnames):
                raise ValueError(f'{filename}: missing columns {sorted(required-set(reader.fieldnames or []))}')
            data[kind] = list(reader)
    return data


def check_relationships(data):
    patients = [p['pid'] for p in data['patients']]
    encounters = [e['encounter'] for e in data['encounters']]
    appts = [a['appointment_id'] for a in data['appointments']]
    vitals = [v['vital_id'] for v in data['vitals']]
    for name, ids in [('patients',patients),('encounters',encounters),('appointments',appts),('vitals',vitals)]:
        if len(ids) != len(set(ids)):
            raise ValueError(f'Duplicate fixture IDs in {name}')
    patient_ids = set(patients)
    encounter_owner = {e['encounter']:e['pid'] for e in data['encounters']}
    for e in data['encounters']:
        if e['pid'] not in patient_ids:
            raise ValueError(f"Encounter {e['encounter']} references missing patient")
    for a in data['appointments']:
        if a['pc_pid'] not in patient_ids:
            raise ValueError(f"Appointment {a['appointment_id']} references missing patient")
    for v in data['vitals']:
        if v['pid'] not in patient_ids or encounter_owner.get(v['encounter']) != v['pid']:
            raise ValueError(f"Vital {v['vital_id']} has invalid patient/encounter link")


def verify_a4_database(cursor):
    """Refuse databases without the dedicated A4 identity marker."""
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = DATABASE()
          AND table_name = 'vital_environment_identity'
    """)
    if cursor.fetchone()[0] != 1:
        raise RuntimeError(
            "Missing A4 database identity marker; refusing to load"
        )

    cursor.execute("""
        SELECT environment_name
        FROM vital_environment_identity
    """)
    identities = [row[0] for row in cursor.fetchall()]

    if identities != ['vital-a4']:
        raise RuntimeError(
            "Incorrect A4 database identity; refusing to load"
        )


def db_counts(cursor):
    result = {}
    for table in TABLES:
        cursor.execute(f'SELECT COUNT(*) FROM `{table}`')
        result[table] = cursor.fetchone()[0]
    return result


def insert(cursor, sql, args):
    cursor.execute(sql, args)
    return cursor.lastrowid


def load(cursor, data):
    # Fixture IDs are used as clinical identifiers in this empty, dedicated DB.
    # Database auto-increment primary keys remain database-assigned.
    for p in data['patients']:
        insert(cursor, '''INSERT INTO patient_data
            (pid,pubpid,fname,lname,DOB,sex,city,state,uuid)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
            (p['pid'],p['pubpid'],p['fname'],p['lname'],p['DOB'] or None,
             p['sex'],p['city'],p['state'],uuid.uuid4().bytes))

    for e in data['encounters']:
        insert(cursor, '''INSERT INTO form_encounter
            (encounter,pid,date,reason,uuid) VALUES (%s,%s,%s,%s,%s)''',
            (e['encounter'],e['pid'],e['date'],e['reason'],uuid.uuid4().bytes))

    for a in data['appointments']:
        # pc_eid is an internal auto-increment PK; fixture appointment_id is not copied.
        insert(cursor, '''INSERT INTO openemr_postcalendar_events
            (pc_pid,pc_eventDate,pc_startTime,pc_endTime,pc_duration,pc_catid,
             pc_apptstatus,pc_multiple,uuid)
            VALUES (%s,%s,%s,%s,%s,%s,%s,0,%s)''',
            (a['pc_pid'],a['pc_eventDate'],a['pc_startTime'],a['pc_endTime'],
             a['pc_duration'],a['pc_catid'],a['pc_apptstatus'],uuid.uuid4().bytes))

    for v in data['vitals']:
        vital_pk = insert(cursor, '''INSERT INTO form_vitals
            (pid,date,bps,bpd,pulse,weight,height,uuid)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',
            (v['pid'],v['date'],v['bps'],v['bpd'],v['pulse'],v['weight'],
             v['height'],uuid.uuid4().bytes))
        insert(cursor, '''INSERT INTO forms
            (pid,encounter,form_id,formdir,form_name)
            VALUES (%s,%s,%s,'vitals','Vitals')''',
            (v['pid'],v['encounter'],vital_pk))


def verify(cursor, data):
    expected = {
        'patient_data':len(data['patients']),
        'form_encounter':len(data['encounters']),
        'openemr_postcalendar_events':len(data['appointments']),
        'form_vitals':len(data['vitals']),
        'forms':len(data['vitals']),
    }
    actual = db_counts(cursor)
    if actual != expected:
        raise ValueError(f'Count mismatch: expected {expected}; actual {actual}')
    cursor.execute('''SELECT COUNT(*) FROM forms f
        LEFT JOIN form_vitals v ON v.id=f.form_id AND v.pid=f.pid
        LEFT JOIN form_encounter e ON e.encounter=f.encounter AND e.pid=f.pid
        WHERE f.formdir='vitals' AND (v.id IS NULL OR e.id IS NULL)''')
    if cursor.fetchone()[0]:
        raise ValueError('Invalid vital-to-encounter registry links')
    cursor.execute('''SELECT COUNT(*) FROM form_encounter e
        LEFT JOIN patient_data p ON p.pid=e.pid WHERE p.pid IS NULL''')
    if cursor.fetchone()[0]:
        raise ValueError('Encounter references missing patient')
    cursor.execute('''SELECT COUNT(*) FROM openemr_postcalendar_events a
        LEFT JOIN patient_data p ON p.pid=CAST(a.pc_pid AS UNSIGNED)
        WHERE p.pid IS NULL''')
    if cursor.fetchone()[0]:
        raise ValueError('Appointment references missing patient')
    return actual


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', required=True, type=pathlib.Path)
    ap.add_argument('--apply', action='store_true', help='Actually write records (default: dry-run)')
    ap.add_argument('--confirm', choices=['vital-a4'], help='Required for --apply')
    ap.add_argument('--simulate-failure', action='store_true',
                    help='Instructor test: fail after inserting patients, before commit')
    args = ap.parse_args()
    if args.simulate_failure and not args.apply:
        ap.error('--simulate-failure requires --apply')
    if args.apply and args.confirm != 'vital-a4':
        ap.error('--apply requires --confirm vital-a4')
    if os.environ.get('VITAL_A4_LOADER') != 'yes' or os.environ.get('MYSQL_HOST') != 'mysql':
        ap.error('Run in dedicated A4 Docker network with VITAL_A4_LOADER=yes and MYSQL_HOST=mysql')

    data = read_csvs(args.input)
    check_relationships(data)
    # Use the already-validated course script to check manifest hashes and fixture rules.
    validator = pathlib.Path(__file__).with_name('validate_data.py')
    if not validator.is_file():
        raise FileNotFoundError(f'Missing validator: {validator}')
    proc = subprocess.run([sys.executable,str(validator),'--input',str(args.input)],
                          capture_output=True,text=True)
    if proc.returncode != 0:
        raise RuntimeError('Fixture validation failed:\n' + proc.stdout + proc.stderr)
    report = json.loads(proc.stdout)
    if report.get('status') != 'PASS':
        raise ValueError('Fixture validator did not return PASS')
    print('Fixture validation: PASS')
    print('Rows:', {key:len(rows) for key,rows in data.items()})

    conn = pymysql.connect(host='mysql',port=3306,user='root',
                           password=os.environ['MYSQL_ROOT_PASSWORD'],
                           database='openemr',autocommit=False,
                           connect_timeout=10,charset='utf8mb4')
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT @@hostname, DATABASE()')
            hostname, database = cur.fetchone()
            print('Connected database:',database,'server:',hostname)
            # Container hostname may be a Docker-generated ID, not container_name.
            # Isolation depends on running with --network vital-a4_default.
            if database != 'openemr':
                raise RuntimeError('Unexpected database name')
            verify_a4_database(cur)
            initial = db_counts(cur)
            print('Baseline counts:',initial)
            if any(initial.values()):
                raise RuntimeError('Refusing nonempty database; restore A4 baseline first')
            if not args.apply:
                print('DRY RUN PASS — no database writes performed')
                return
            print('Inserting records in one transaction...')
            if args.simulate_failure:
                for p in data['patients']:
                    insert(cur, '''INSERT INTO patient_data
                        (pid,pubpid,fname,lname,DOB,sex,city,state,uuid)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                        (p['pid'],p['pubpid'],p['fname'],p['lname'],p['DOB'] or None,
                         p['sex'],p['city'],p['state'],uuid.uuid4().bytes))
                print('INJECTED FAILURE: after inserting patients; rolling back', flush=True)
                raise RuntimeError('Simulated loader failure before commit')
            load(cur,data)
            final = verify(cur,data)
            conn.commit()
            print('LOAD PASS — committed:',final)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        sys.exit(1)
