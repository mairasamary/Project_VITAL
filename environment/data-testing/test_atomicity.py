#!/usr/bin/env python3
import argparse, subprocess, sys, uuid
from pathlib import Path

def count_batch(repo,batch):
    env=repo/"environment"; b=batch.replace("'","''"); m=b[:20]
    sql=f"""SELECT
(SELECT COUNT(*) FROM patient_data WHERE genericname1='project_vital_batch' AND genericval1='{b}'),
(SELECT COUNT(*) FROM form_encounter WHERE external_id='{m}'),
(SELECT COUNT(*) FROM form_vitals WHERE external_id='{m}');
"""
    shell=("set -a; source .env; set +a; "
           'docker compose exec -T mysql mariadb -N -B -uroot "-p${MYSQL_ROOT_PASSWORD}" openemr')
    r=subprocess.run(["bash","-lc",shell],cwd=env,input=sql,text=True,capture_output=True,check=True)
    return tuple(map(int,r.stdout.strip().split("\t")))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("dataset"); a=ap.parse_args()
    repo=Path(__file__).resolve().parents[2]
    loader=Path(__file__).with_name("load_openemr.py")
    batch="ATOMIC-"+uuid.uuid4().hex[:10]
    print("Controlled batch:",batch)
    r=subprocess.run([sys.executable,str(loader),a.dataset,"--limit-patients","5",
                      "--batch",batch,"--fail-after","encounters","--yes"])
    if r.returncode==0:
        print("ERROR: controlled load unexpectedly succeeded"); return 1
    counts=count_batch(repo,batch)
    print("Rows remaining after failed transaction:",counts)
    if counts==(0,0,0):
        print("ATOMICITY TEST PASSED — rollback left no partial batch.")
        return 0
    print("ATOMICITY TEST FAILED — partial rows remain.")
    return 1
if __name__=="__main__": sys.exit(main())
