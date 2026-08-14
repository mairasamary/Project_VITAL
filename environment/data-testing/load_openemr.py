#!/usr/bin/env python3
"""
Project VITAL — hardened OpenEMR synthetic-data loader.

Improvements over the initial Stage 2 prototype:
- rejects duplicate batch names before loading;
- allocates patient/encounter IDs from currently available ranges;
- checks the planned ID ranges for collisions before inserting;
- preserves transactional rollback on any SQL error;
- prints the chosen ID ranges before loading.

Target: the isolated/local Project VITAL OpenEMR course environment.
"""
import argparse
import csv
import subprocess
import sys
import uuid
from pathlib import Path

PATIENT_FLOOR = 9_000_000
ENCOUNTER_FLOOR = 9_100_000


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sql_quote(value):
    if value is None:
        return "NULL"
    s = str(value)
    return "'" + s.replace("\\", "\\\\").replace("'", "''") + "'"


def db_shell():
    return (
        "set -a; source .env; set +a; "
        'docker compose exec -T mysql '
        'mariadb -N -B -uroot "-p${MYSQL_ROOT_PASSWORD}" openemr'
    )


def query(env_dir, sql):
    r = subprocess.run(
        ["bash", "-lc", db_shell()],
        cwd=env_dir,
        input=sql,
        text=True,
        capture_output=True,
    )
    if r.returncode:
        print(r.stderr, file=sys.stderr)
        raise SystemExit(r.returncode)
    return r.stdout.strip()


def execute(env_dir, sql):
    shell = (
        "set -a; source .env; set +a; "
        'docker compose exec -T mysql '
        'mariadb -uroot "-p${MYSQL_ROOT_PASSWORD}" openemr'
    )
    return subprocess.run(
        ["bash", "-lc", shell],
        cwd=env_dir,
        input=sql,
        text=True,
        capture_output=True,
    )


def as_int(value, default=0):
    value = (value or "").strip()
    return int(value) if value else default


def batch_marker(batch):
    if len(batch) > 20:
        raise ValueError(
            "Batch names must be 20 characters or fewer because the current "
            "OpenEMR external_id field is varchar(20)."
        )
    return batch


def choose_ranges(env_dir, patient_count, encounter_count):
    current_max_pid = as_int(query(env_dir, "SELECT COALESCE(MAX(pid),0) FROM patient_data;"))
    current_max_enc = as_int(query(env_dir, "SELECT COALESCE(MAX(encounter),0) FROM form_encounter;"))

    patient_start = max(PATIENT_FLOOR, current_max_pid) + 1
    encounter_start = max(ENCOUNTER_FLOOR, current_max_enc) + 1

    patient_end = patient_start + max(patient_count - 1, 0)
    encounter_end = encounter_start + max(encounter_count - 1, 0)

    return patient_start, patient_end, encounter_start, encounter_end


def preflight(env_dir, batch, patient_start, patient_end, encounter_start, encounter_end):
    b = batch.replace("'", "''")

    duplicate_batch = as_int(query(
        env_dir,
        f"""SELECT COUNT(*) FROM patient_data
            WHERE genericname1='project_vital_batch'
              AND genericval1='{b}';"""
    ))
    if duplicate_batch:
        raise RuntimeError(
            f"Batch {batch!r} already exists ({duplicate_batch} patient row(s)). "
            "Use a new batch name or reset the existing batch first."
        )

    patient_collision = as_int(query(
        env_dir,
        f"SELECT COUNT(*) FROM patient_data WHERE pid BETWEEN {patient_start} AND {patient_end};"
    )) if patient_end >= patient_start else 0

    encounter_collision = as_int(query(
        env_dir,
        f"SELECT COUNT(*) FROM form_encounter "
        f"WHERE encounter BETWEEN {encounter_start} AND {encounter_end};"
    )) if encounter_end >= encounter_start else 0

    if patient_collision or encounter_collision:
        raise RuntimeError(
            "Preflight ID collision detected. "
            f"patient collisions={patient_collision}, encounter collisions={encounter_collision}"
        )


def build_sql(patients, encounters, vitals, batch, patient_start, encounter_start, fail_after=None):
    patient_pid = {
        p["patient_key"]: patient_start + i
        for i, p in enumerate(patients)
    }
    encounter_id = {
        e["encounter_key"]: encounter_start + i
        for i, e in enumerate(encounters)
    }
    vitals_by_encounter = {v["encounter_key"]: v for v in vitals}

    out = ["SET autocommit=0;", "START TRANSACTION;"]

    for p in patients:
        pid = patient_pid[p["patient_key"]]
        out.append(
            "INSERT INTO patient_data "
            "(uuid,fname,lname,DOB,sex,email,phone_cell,city,state,postal_code,"
            "country_code,pubpid,pid,regdate,genericname1,genericval1) VALUES ("
            "UNHEX(REPLACE(UUID(),'-','')),"
            f"{sql_quote(p['first_name'])},{sql_quote(p['last_name'])},"
            f"{sql_quote(p['date_of_birth'])},{sql_quote(p['sex'])},"
            f"{sql_quote(p['email'])},{sql_quote(p['phone'])},"
            f"{sql_quote(p['city'])},{sql_quote(p['state'])},{sql_quote(p['postal_code'])},"
            f"'US',{sql_quote('VITAL-'+p['patient_key'])},{pid},NOW(),"
            f"'project_vital_batch',{sql_quote(batch)});"
        )

    if fail_after == "patients":
        out.append(
            "SIGNAL SQLSTATE '45000' "
            "SET MESSAGE_TEXT='Project VITAL controlled failure after patients';"
        )

    for e in encounters:
        pid = patient_pid[e["patient_key"]]
        enc = encounter_id[e["encounter_key"]]
        out.append(
            "INSERT INTO form_encounter "
            "(uuid,date,reason,facility,facility_id,pid,encounter,pc_catid,provider_id,"
            "billing_facility,external_id,class_code) VALUES ("
            "UNHEX(REPLACE(UUID(),'-','')),"
            f"{sql_quote(e['encounter_datetime'])},{sql_quote(e['reason'])},"
            f"'Project VITAL',0,{pid},{enc},5,0,0,{sql_quote(batch)},'AMB');"
        )

    if fail_after == "encounters":
        out.append(
            "SIGNAL SQLSTATE '45000' "
            "SET MESSAGE_TEXT='Project VITAL controlled failure after encounters';"
        )

    for e in encounters:
        v = vitals_by_encounter.get(e["encounter_key"])
        if not v:
            continue

        pid = patient_pid[e["patient_key"]]
        enc = encounter_id[e["encounter_key"]]

        out.append(
            "INSERT INTO form_vitals "
            "(uuid,date,pid,user,groupname,authorized,activity,bps,bpd,weight,height,"
            "temperature,pulse,oxygen_saturation,external_id) VALUES ("
            "UNHEX(REPLACE(UUID(),'-','')),"
            f"{sql_quote(v['recorded_datetime'])},{pid},'project-vital','Default',1,1,"
            f"{sql_quote(v['systolic'])},{sql_quote(v['diastolic'])},"
            f"{v['weight_lb']},{v['height_in']},{v['temperature_f']},"
            f"{v['pulse']},{v['oxygen_saturation']},{sql_quote(batch)});"
        )
        out.append(
            "INSERT INTO forms "
            "(date,encounter,form_name,form_id,pid,user,groupname,authorized,deleted,formdir,provider_id) VALUES ("
            f"{sql_quote(v['recorded_datetime'])},{enc},'Vitals',LAST_INSERT_ID(),{pid},"
            "'project-vital','Default',1,0,'vitals',0);"
        )

    if fail_after == "vitals":
        out.append(
            "SIGNAL SQLSTATE '45000' "
            "SET MESSAGE_TEXT='Project VITAL controlled failure after vitals';"
        )

    out.append("COMMIT;")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset")
    ap.add_argument("--limit-patients", type=int)
    ap.add_argument("--batch")
    ap.add_argument("--fail-after", choices=["patients", "encounters", "vitals"])
    ap.add_argument("--yes", action="store_true")
    args = ap.parse_args()

    dataset = Path(args.dataset).resolve()
    repo = Path(__file__).resolve().parents[2]
    env_dir = repo / "environment"

    validator = Path(__file__).with_name("validate_data.py")
    vr = subprocess.run([sys.executable, str(validator), str(dataset)])
    if vr.returncode:
        print("Refusing to load: intermediate dataset failed validation.", file=sys.stderr)
        return 2

    patients = read_csv(dataset / "patients.csv")
    encounters = read_csv(dataset / "encounters.csv")
    vitals = read_csv(dataset / "vitals.csv")

    if args.limit_patients:
        keep = {p["patient_key"] for p in patients[:args.limit_patients]}
        patients = [p for p in patients if p["patient_key"] in keep]
        encounters = [e for e in encounters if e["patient_key"] in keep]
        enc_keep = {e["encounter_key"] for e in encounters}
        vitals = [
            v for v in vitals
            if v["patient_key"] in keep and v["encounter_key"] in enc_keep
        ]

    batch = args.batch or ("VITAL-" + uuid.uuid4().hex[:12])
    try:
        batch_marker(batch)
    except ValueError as exc:
        print(f"PREFLIGHT FAILED: {exc}", file=sys.stderr)
        return 3

    p_start, p_end, e_start, e_end = choose_ranges(
        env_dir, len(patients), len(encounters)
    )

    try:
        preflight(env_dir, batch, p_start, p_end, e_start, e_end)
    except RuntimeError as exc:
        print(f"PREFLIGHT FAILED: {exc}", file=sys.stderr)
        return 3

    print(f"Batch:             {batch}")
    print(f"Patients:          {len(patients)}")
    print(f"Encounters:        {len(encounters)}")
    print(f"Vitals:            {len(vitals)}")
    print(f"Patient ID range:  {p_start}..{p_end}")
    print(f"Encounter range:   {e_start}..{e_end}")
    if args.fail_after:
        print(f"CONTROLLED FAILURE: after {args.fail_after}")

    if not args.yes:
        answer = input("Load this synthetic dataset into the local OpenEMR database? [y/N] ")
        if answer.lower() not in {"y", "yes"}:
            print("Cancelled.")
            return 0

    sql = build_sql(
        patients, encounters, vitals, batch,
        p_start, e_start, args.fail_after
    )
    r = execute(env_dir, sql)

    if r.returncode:
        if r.stdout:
            print(r.stdout)
        if r.stderr:
            print(r.stderr, file=sys.stderr)
        print("LOAD FAILED — transaction should have rolled back.", file=sys.stderr)
        return r.returncode

    print("LOAD COMMITTED")
    print(
        "Validate with:\n"
        f"  python3 environment/data-testing/validate_openemr_load.py --batch {batch}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
