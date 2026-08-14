#!/usr/bin/env python3
"""
Teaching experiment: demonstrates an important distinction.

The inspected OpenEMR schema indexes pid/encounter relationships but does not
declare SQL FOREIGN KEY constraints for the selected tables. Therefore a
wrong-order/orphan insert may be accepted by MariaDB. This experiment inserts
an orphan encounter inside a transaction, detects it semantically, then rolls
the transaction back.
"""
import subprocess, sys, uuid
from pathlib import Path

def main():
    repo=Path(__file__).resolve().parents[2]; env=repo/"environment"
    marker=("ORDER-"+uuid.uuid4().hex[:10])[:20]
    pid=999999991; enc=999999991
    sql=f"""
START TRANSACTION;
INSERT INTO form_encounter
(uuid,date,reason,facility,facility_id,pid,encounter,pc_catid,provider_id,billing_facility,external_id,class_code)
VALUES (UNHEX(REPLACE(UUID(),'-','')),NOW(),'Controlled wrong-order experiment',
'Project VITAL',0,{pid},{enc},5,0,0,'{marker}','AMB');
SELECT COUNT(*) AS orphan_count
FROM form_encounter e LEFT JOIN patient_data p ON p.pid=e.pid
WHERE e.external_id='{marker}' AND p.pid IS NULL;
ROLLBACK;
"""
    shell=("set -a; source .env; set +a; "
           'docker compose exec -T mysql mariadb -N -B -uroot "-p${MYSQL_ROOT_PASSWORD}" openemr')
    r=subprocess.run(["bash","-lc",shell],cwd=env,input=sql,text=True,capture_output=True)
    if r.returncode:
        print(r.stderr,file=sys.stderr); return r.returncode
    lines=[x.strip() for x in r.stdout.splitlines() if x.strip()]
    print("Database orphan count during transaction:", lines[-1] if lines else "unknown")
    print("Transaction rolled back.")
    if lines and lines[-1]=="1":
        print("INSERTION-ORDER EXPERIMENT PASSED.")
        print("Finding: the database accepted the orphan row; semantic validation detected it.")
        return 0
    print("Unexpected experiment result.")
    return 1
if __name__=="__main__": sys.exit(main())
