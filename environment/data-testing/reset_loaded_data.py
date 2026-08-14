#!/usr/bin/env python3
import argparse, subprocess, sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--yes", action="store_true")
    a=ap.parse_args()
    repo=Path(__file__).resolve().parents[2]
    env=repo/"environment"
    b=a.batch.replace("'","''")
    marker=b[:20].replace("'","''")

    if not a.yes:
        ans=input(f"Delete Project VITAL synthetic batch {a.batch}? [y/N] ")
        if ans.lower() not in {"y","yes"}: return 0

    # Delete children before parents. Transactional reset.
    sql=f"""
START TRANSACTION;
DELETE f FROM forms f
JOIN form_vitals v ON v.id=f.form_id
WHERE f.formdir='vitals' AND v.external_id='{marker}';
DELETE FROM form_vitals WHERE external_id='{marker}';
DELETE FROM form_encounter WHERE external_id='{marker}';
DELETE FROM patient_data
 WHERE genericname1='project_vital_batch' AND genericval1='{b}';
COMMIT;
"""
    shell=("set -a; source .env; set +a; "
           'docker compose exec -T mysql mariadb -uroot "-p${MYSQL_ROOT_PASSWORD}" openemr')
    r=subprocess.run(["bash","-lc",shell],cwd=env,input=sql,text=True)
    if r.returncode: return r.returncode
    print("RESET COMPLETE")
    return 0

if __name__=="__main__":
    sys.exit(main())
