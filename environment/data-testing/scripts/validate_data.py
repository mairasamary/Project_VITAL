#!/usr/bin/env python3
"""Independent pre-load validator for Project VITAL A4 CSV fixtures (schema v1)."""
import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from datetime import date, datetime, time
from pathlib import Path

LEVELS = {'small': 200, 'medium': 2000, 'large': 20000}
FIELDS = {
    'patients': ['pid','pubpid','fname','lname','DOB','sex','city','state'],
    'encounters': ['encounter','pid','date','reason'],
    'appointments': ['appointment_id','pc_pid','pc_eventDate','pc_startTime','pc_endTime','pc_duration','pc_catid','pc_apptstatus'],
    'vitals': ['vital_id','pid','encounter','date','bps','bpd','pulse','weight','height'],
}


def validate(folder, max_errors=25):
    errors = []
    def fail(msg):
        if len(errors) < max_errors:
            errors.append(msg)

    meta_path = folder / 'metadata.json'
    try:
        meta = json.loads(meta_path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        return {'status':'FAIL','errors':[f'metadata.json: {exc}'],'counts':{}}
    if not isinstance(meta, dict):
        return {'status': 'FAIL', 'errors': ['metadata.json: root must be a JSON object'], 'counts': {}}
    for field in ('sha256', 'counts'):
        if not isinstance(meta.get(field), dict):
            return {'status': 'FAIL', 'errors': [f'metadata.json: {field} must be a JSON object'], 'counts': {}}
    if meta.get('schema_version') != 1:
        fail('Unsupported schema_version; expected 1')
    level = meta.get('level')
    if level not in LEVELS:
        fail(f'Unknown level: {level!r}')
    if not isinstance(meta.get('seed'), int):
        fail('Missing or noninteger seed')
    counts = {}
    patients, encounters = set(), {}
    for name, fields in FIELDS.items():
        path = folder / f'{name}.csv'
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != meta.get('sha256', {}).get(name):
                fail(f'{name}: SHA-256 differs from metadata (file may be modified)')
            with path.open(newline='', encoding='utf-8') as fh:
                reader = csv.DictReader(fh)
                if reader.fieldnames != fields:
                    fail(f'{name}: unexpected CSV header {reader.fieldnames!r}')
                    continue
                seen = set()
                count = 0
                for row in reader:
                    count += 1
                    loc = f'{name}.csv row {count + 1}'
                    key = {'patients':'pid','encounters':'encounter','appointments':'appointment_id','vitals':'vital_id'}[name]
                    try:
                        record_id = int(row[key])
                        if record_id <= 0: raise ValueError('nonpositive ID')
                        if record_id in seen: fail(f'{loc}: duplicate {key}={record_id}')
                        seen.add(record_id)
                        if name == 'patients':
                            patients.add(record_id)
                            if row['pubpid'] != f'VITAL-{record_id:07d}': fail(f'{loc}: pubpid inconsistent with pid')
                            if not row['fname'].strip() or not row['lname'].strip(): fail(f'{loc}: missing name')
                            date.fromisoformat(row['DOB'])
                            if row['sex'] not in ('Male', 'Female'): fail(f'{loc}: unexpected sex category')
                        elif name == 'encounters':
                            pid = int(row['pid'])
                            datetime.fromisoformat(row['date'])
                            encounters[record_id] = pid
                        elif name == 'appointments':
                            pid = int(row['pc_pid'])
                            if pid not in patients: fail(f'{loc}: orphan appointment patient {pid}')
                            date.fromisoformat(row['pc_eventDate'])
                            start = time.fromisoformat(row['pc_startTime'])
                            end = time.fromisoformat(row['pc_endTime'])
                            if start >= end: fail(f'{loc}: appointment end is not after start')
                            if int(row['pc_duration']) <= 0: fail(f'{loc}: nonpositive duration')
                            int(row['pc_catid'])
                        else:
                            pid = int(row['pid'])
                            encounter = int(row['encounter'])
                            if pid not in patients: fail(f'{loc}: orphan vitals patient {pid}')
                            if encounter not in encounters: fail(f'{loc}: orphan vitals encounter {encounter}')
                            elif encounters[encounter] != pid: fail(f'{loc}: vitals patient does not match encounter patient')
                            datetime.fromisoformat(row['date'])
                            for col in ('bps','bpd','pulse','weight','height'):
                                if not math.isfinite(float(row[col])) or float(row[col]) <= 0: fail(f'{loc}: {col} must be positive in this fixture specification')
                            if float(row['bps']) <= float(row['bpd']): fail(f'{loc}: systolic <= diastolic in this fixture specification')
                    except (ValueError, TypeError, KeyError, OverflowError) as exc:
                        fail(f'{loc}: invalid value ({exc})')
                counts[name] = count
        except (OSError, UnicodeError, csv.Error) as exc:
            fail(f'{name}: cannot read CSV ({exc})')
    for encounter, pid in encounters.items():
        if pid not in patients: fail(f'encounters: orphan encounter {encounter} references patient {pid}')
    for name in FIELDS:
        if counts.get(name) != meta.get('counts', {}).get(name):
            fail(f'{name}: count {counts.get(name)} differs from metadata {meta.get("counts", {}).get(name)}')
    if level in LEVELS and counts.get('patients') != LEVELS[level]:
        fail(f'patients: expected {LEVELS[level]} for {level}, got {counts.get("patients")}')
    return {'status':'PASS' if not errors else 'FAIL','level':level,'seed':meta.get('seed'),'counts':counts,'errors':errors,'max_errors_displayed':max_errors}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path, required=True, help='Folder with CSVs and metadata.json')
    p.add_argument('--max-errors', type=int, default=25)
    args = p.parse_args()
    result = validate(args.input, max(1, args.max_errors))
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
