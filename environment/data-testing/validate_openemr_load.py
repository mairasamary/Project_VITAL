#!/usr/bin/env python3
"""
Validate one Project VITAL batch already loaded into OpenEMR.

Exit codes:
  0 = batch exists and is valid
  1 = batch exists but is invalid
  4 = batch not found
"""
import argparse
import subprocess
import sys
from pathlib import Path


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    args = ap.parse_args()

    if len(args.batch) > 20:
        print("INVALID BATCH NAME — must be 20 characters or fewer.")
        return 2

    repo = Path(__file__).resolve().parents[2]
    env = repo / "environment"
    b = args.batch.replace("'", "''")

    raw = query(env, f"""
SELECT
 (SELECT COUNT(*) FROM patient_data
    WHERE genericname1='project_vital_batch' AND genericval1='{b}'),
 (SELECT COUNT(*) FROM form_encounter WHERE external_id='{b}'),
 (SELECT COUNT(*) FROM form_vitals WHERE external_id='{b}'),
 (SELECT COUNT(*) FROM forms f
    JOIN form_vitals v ON v.id=f.form_id
   WHERE f.formdir='vitals' AND v.external_id='{b}');
""")
    parts = raw.split("\t") if raw else []
    if len(parts) != 4:
        print("Unexpected database result:", raw)
        return 2

    p, e, v, f = map(int, parts)

    print(f"Patients:             {p}")
    print(f"Encounters:           {e}")
    print(f"Vitals:               {v}")
    print(f"Vitals form links:    {f}")

    if p == 0 and e == 0 and v == 0 and f == 0:
        print("\nBATCH NOT FOUND")
        return 4

    orphan_enc = int(query(env, f"""
SELECT COUNT(*) FROM form_encounter e
LEFT JOIN patient_data p ON p.pid=e.pid
WHERE e.external_id='{b}' AND p.pid IS NULL;
""") or 0)

    orphan_forms = int(query(env, f"""
SELECT COUNT(*) FROM forms f
JOIN form_vitals v ON v.id=f.form_id
LEFT JOIN form_encounter e ON e.encounter=f.encounter AND e.pid=f.pid
WHERE f.formdir='vitals' AND v.external_id='{b}' AND e.id IS NULL;
""") or 0)

    unregistered_vitals = int(query(env, f"""
SELECT COUNT(*) FROM form_vitals v
LEFT JOIN forms f ON f.form_id=v.id AND f.formdir='vitals' AND f.pid=v.pid
WHERE v.external_id='{b}' AND f.id IS NULL;
""") or 0)

    wrong_patient_vitals = int(query(env, f"""
SELECT COUNT(*) FROM forms f
JOIN form_vitals v ON v.id=f.form_id
WHERE f.formdir='vitals'
  AND v.external_id='{b}'
  AND f.pid <> v.pid;
""") or 0)

    print(f"Orphan encounters:    {orphan_enc}")
    print(f"Broken form links:    {orphan_forms}")
    print(f"Unregistered vitals:  {unregistered_vitals}")
    print(f"Patient mismatches:   {wrong_patient_vitals}")

    ok = (
        p > 0
        and orphan_enc == 0
        and orphan_forms == 0
        and unregistered_vitals == 0
        and wrong_patient_vitals == 0
        and v == f
    )

    if ok:
        print("\nBATCH VALID")
        return 0

    print("\nBATCH INVALID")
    return 1


if __name__ == "__main__":
    sys.exit(main())
