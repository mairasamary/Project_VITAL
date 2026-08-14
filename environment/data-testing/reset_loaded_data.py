#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--yes", action="store_true")
    args = ap.parse_args()

    if len(args.batch) > 20:
        print("Batch name must be 20 characters or fewer.", file=sys.stderr)
        return 2

    repo = Path(__file__).resolve().parents[2]
    env = repo / "environment"
    b = args.batch.replace("'", "''")

    if not args.yes:
        ans = input(f"Delete Project VITAL synthetic batch {args.batch}? [y/N] ")
        if ans.lower() not in {"y", "yes"}:
            print("Cancelled.")
            return 0

    sql = f"""
START TRANSACTION;

DELETE f FROM forms f
JOIN form_vitals v ON v.id=f.form_id
WHERE f.formdir='vitals' AND v.external_id='{b}';

DELETE FROM form_vitals
WHERE external_id='{b}';

DELETE FROM form_encounter
WHERE external_id='{b}';

DELETE FROM patient_data
WHERE genericname1='project_vital_batch'
  AND genericval1='{b}';

COMMIT;
"""

    shell = (
        "set -a; source .env; set +a; "
        'docker compose exec -T mysql '
        'mariadb -uroot "-p${MYSQL_ROOT_PASSWORD}" openemr'
    )

    r = subprocess.run(
        ["bash", "-lc", shell],
        cwd=env,
        input=sql,
        text=True,
    )
    if r.returncode:
        return r.returncode

    print("RESET COMPLETE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
