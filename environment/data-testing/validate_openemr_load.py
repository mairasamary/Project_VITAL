#!/usr/bin/env python3
import argparse, subprocess, sys
from pathlib import Path

def query(env_dir, sql):
    shell=("set -a; source .env; set +a; "
           'docker compose exec -T mysql mariadb -N -B -uroot "-p${MYSQL_ROOT_PASSWORD}" openemr')
    r=subprocess.run(["bash","-lc",shell],cwd=env_dir,input=sql,text=True,capture_output=True)
    if r.returncode:
        print(r.stderr,file=sys.stderr); raise SystemExit(r.returncode)
    return r.stdout.strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    args=ap.parse_args()
    repo=Path(__file__).resolve().parents[2]
    env=repo/"environment"
    b=args.batch.replace("'","''")
    marker=b[:20].replace("'","''")

    sql=f"""
SELECT
 (SELECT COUNT(*) FROM patient_data WHERE genericname1='project_vital_batch' AND genericval1='{b}'),
 (SELECT COUNT(*) FROM form_encounter WHERE external_id='{marker}'),
 (SELECT COUNT(*) FROM form_vitals WHERE external_id='{marker}'),
 (SELECT COUNT(*) FROM forms f
    JOIN form_vitals v ON v.id=f.form_id
   WHERE f.formdir='vitals' AND v.external_id='{marker}');
"""
    raw=query(env,sql)
    parts=raw.split("\t") if raw else []
    if len(parts)!=4:
        print("Unexpected database result:",raw); return 2
    p,e,v,f=map(int,parts)
    print(f"Patients:             {p}")
    print(f"Encounters:           {e}")
    print(f"Vitals:               {v}")
    print(f"Vitals form links:    {f}")

    orphan_enc=int(query(env,f"""
SELECT COUNT(*) FROM form_encounter e
LEFT JOIN patient_data p ON p.pid=e.pid
WHERE e.external_id='{marker}' AND p.pid IS NULL;
""") or 0)

    orphan_forms=int(query(env,f"""
SELECT COUNT(*) FROM forms f
JOIN form_vitals v ON v.id=f.form_id
LEFT JOIN form_encounter e ON e.encounter=f.encounter AND e.pid=f.pid
WHERE f.formdir='vitals' AND v.external_id='{marker}' AND e.id IS NULL;
""") or 0)

    bad_form_link=int(query(env,f"""
SELECT COUNT(*) FROM form_vitals v
LEFT JOIN forms f ON f.form_id=v.id AND f.formdir='vitals' AND f.pid=v.pid
WHERE v.external_id='{marker}' AND f.id IS NULL;
""") or 0)

    print(f"Orphan encounters:    {orphan_enc}")
    print(f"Broken form links:    {orphan_forms}")
    print(f"Unregistered vitals:  {bad_form_link}")

    ok = p>0 and orphan_enc==0 and orphan_forms==0 and bad_form_link==0 and v==f
    print("\nOPENEMR LOAD VALIDATION " + ("PASSED" if ok else "FAILED"))
    return 0 if ok else 1

if __name__=="__main__":
    sys.exit(main())
