#!/usr/bin/env python3
"""
Project VITAL Stage 2 loader.

Loads a previously validated synthetic CSV dataset into the running OpenEMR
MariaDB container. The loader sends SQL to the database through docker compose,
so students do not need a local Python MariaDB driver.

The loader is transactional: any SQL error causes the transaction to roll back.
Rows are marked with a Project VITAL batch token so they can be validated/reset.
"""
import argparse, csv, json, subprocess, sys, uuid
from pathlib import Path

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def sql_quote(value):
    if value is None:
        return "NULL"
    s = str(value)
    return "'" + s.replace("\\", "\\\\").replace("'", "''") + "'"

def run_mariadb(env_dir, sql, capture=False):
    cmd = [
        "docker", "compose", "exec", "-T", "mysql",
        "mariadb", "-uroot", "-p${MYSQL_ROOT_PASSWORD}", "openemr"
    ]
    # Password expansion is needed inside a shell after sourcing .env.
    shell = (
        "set -a; source .env; set +a; "
        "docker compose exec -T mysql "
        'mariadb -uroot "-p${MYSQL_ROOT_PASSWORD}" openemr'
    )
    return subprocess.run(
        ["bash", "-lc", shell],
        cwd=env_dir,
        input=sql,
        text=True,
        capture_output=capture,
    )

def build_sql(patients, encounters, vitals, batch, fail_after=None):
    # Stable numeric IDs for this isolated teaching environment.
    # We derive them from row order and start in a high range to avoid ordinary UI IDs.
    patient_pid = {p["patient_key"]: 9000000 + i for i,p in enumerate(patients, 1)}
    encounter_id = {e["encounter_key"]: 9100000 + i for i,e in enumerate(encounters, 1)}

    vitals_by_encounter = {v["encounter_key"]: v for v in vitals}

    out = [
        "SET autocommit=0;",
        "START TRANSACTION;",
    ]

    for p in patients:
        pid = patient_pid[p["patient_key"]]
        # external marker: pubpid is visible and useful; genericname/value mark the batch.
        out.append(
            "INSERT INTO patient_data "
            "(uuid,fname,lname,DOB,sex,email,phone_cell,city,state,postal_code,"
            "country_code,pubpid,pid,regdate,genericname1,genericval1) VALUES ("
            f"UNHEX(REPLACE(UUID(),'-','')),"
            f"{sql_quote(p['first_name'])},{sql_quote(p['last_name'])},{sql_quote(p['date_of_birth'])},"
            f"{sql_quote(p['sex'])},{sql_quote(p['email'])},{sql_quote(p['phone'])},"
            f"{sql_quote(p['city'])},{sql_quote(p['state'])},{sql_quote(p['postal_code'])},"
            f"'US',{sql_quote('VITAL-'+p['patient_key'])},{pid},NOW(),'project_vital_batch',{sql_quote(batch)}"
            ");"
        )

    if fail_after == "patients":
        out.append("SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Project VITAL controlled failure after patients';")

    for e in encounters:
        pid = patient_pid[e["patient_key"]]
        enc = encounter_id[e["encounter_key"]]
        out.append(
            "INSERT INTO form_encounter "
            "(uuid,date,reason,facility,facility_id,pid,encounter,pc_catid,provider_id,"
            "billing_facility,external_id,class_code) VALUES ("
            f"UNHEX(REPLACE(UUID(),'-','')),{sql_quote(e['encounter_datetime'])},{sql_quote(e['reason'])},"
            f"'Project VITAL',0,{pid},{enc},5,0,0,{sql_quote(batch[:20])},'AMB');"
        )

    if fail_after == "encounters":
        out.append("SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Project VITAL controlled failure after encounters';")

    for e in encounters:
        v = vitals_by_encounter.get(e["encounter_key"])
        if not v:
            continue
        pid = patient_pid[e["patient_key"]]
        enc = encounter_id[e["encounter_key"]]
        # Use LAST_INSERT_ID() immediately in forms.form_id.
        out.append(
            "INSERT INTO form_vitals "
            "(uuid,date,pid,user,groupname,authorized,activity,bps,bpd,weight,height,"
            "temperature,pulse,oxygen_saturation,external_id) VALUES ("
            f"UNHEX(REPLACE(UUID(),'-','')),{sql_quote(v['recorded_datetime'])},{pid},"
            f"'project-vital','Default',1,1,{sql_quote(v['systolic'])},{sql_quote(v['diastolic'])},"
            f"{v['weight_lb']},{v['height_in']},{v['temperature_f']},{v['pulse']},"
            f"{v['oxygen_saturation']},{sql_quote(batch[:20])});"
        )
        out.append(
            "INSERT INTO forms "
            "(date,encounter,form_name,form_id,pid,user,groupname,authorized,deleted,formdir,provider_id) VALUES ("
            f"{sql_quote(v['recorded_datetime'])},{enc},'Vitals',LAST_INSERT_ID(),{pid},"
            "'project-vital','Default',1,0,'vitals',0);"
        )

    if fail_after == "vitals":
        out.append("SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Project VITAL controlled failure after vitals';")

    out += ["COMMIT;"]
    return "\n".join(out) + "\n"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("dataset")
    ap.add_argument("--limit-patients", type=int)
    ap.add_argument("--batch")
    ap.add_argument("--fail-after", choices=["patients","encounters","vitals"])
    ap.add_argument("--yes", action="store_true")
    args=ap.parse_args()

    root=Path(args.dataset).resolve()
    repo=Path(__file__).resolve().parents[2]
    env_dir=repo/"environment"

    # Pre-load validation.
    validator=Path(__file__).with_name("validate_data.py")
    vr=subprocess.run([sys.executable,str(validator),str(root)])
    if vr.returncode:
        print("Refusing to load: intermediate dataset failed validation.", file=sys.stderr)
        return 2

    patients=read_csv(root/"patients.csv")
    encounters=read_csv(root/"encounters.csv")
    vitals=read_csv(root/"vitals.csv")

    if args.limit_patients:
        keep={p["patient_key"] for p in patients[:args.limit_patients]}
        patients=[p for p in patients if p["patient_key"] in keep]
        encounters=[e for e in encounters if e["patient_key"] in keep]
        enc_keep={e["encounter_key"] for e in encounters}
        vitals=[v for v in vitals if v["patient_key"] in keep and v["encounter_key"] in enc_keep]

    batch=args.batch or ("VITAL-" + uuid.uuid4().hex[:12])
    print(f"Batch:      {batch}")
    print(f"Patients:   {len(patients)}")
    print(f"Encounters: {len(encounters)}")
    print(f"Vitals:     {len(vitals)}")
    if args.fail_after:
        print(f"CONTROLLED FAILURE: after {args.fail_after}")

    if not args.yes:
        answer=input("Load this synthetic dataset into the local OpenEMR database? [y/N] ")
        if answer.lower() not in {"y","yes"}:
            print("Cancelled.")
            return 0

    sql=build_sql(patients,encounters,vitals,batch,args.fail_after)
    r=run_mariadb(env_dir,sql,capture=True)
    if r.returncode:
        print(r.stdout)
        print(r.stderr, file=sys.stderr)
        print("LOAD FAILED — transaction should have rolled back.", file=sys.stderr)
        return r.returncode

    print("LOAD COMMITTED")
    print(f"Validate with:\n  python3 environment/data-testing/validate_openemr_load.py --batch {batch}")
    return 0

if __name__=="__main__":
    sys.exit(main())
