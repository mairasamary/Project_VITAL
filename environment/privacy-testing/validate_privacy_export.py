#!/usr/bin/env python3
import argparse, csv, json, sys
from collections import Counter
from pathlib import Path

PROHIBITED = {
    "patient_key","first_name","last_name","date_of_birth","email","phone",
    "city","postal_code","encounter_key","vitals_key","encounter_datetime",
    "recorded_datetime"
}
QIS = ("age_band","sex","state","postal_prefix")

def rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def headers(path):
    with path.open(newline="", encoding="utf-8") as f:
        return set(next(csv.reader(f)))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset")
    ap.add_argument("--min-k", type=int, default=1)
    args = ap.parse_args()
    d = Path(args.dataset)

    needed = ["patients.csv","encounters.csv","vitals.csv","privacy-manifest.json"]
    missing = [x for x in needed if not (d/x).exists()]
    if missing:
        print("PRIVACY VALIDATION FAILED")
        print("Missing:", ", ".join(missing))
        return 1

    problems = []
    for name in ("patients.csv","encounters.csv","vitals.csv"):
        leaked = sorted(headers(d/name) & PROHIBITED)
        if leaked:
            problems.append(f"{name}: prohibited columns: {', '.join(leaked)}")

    p, e, v = rows(d/"patients.csv"), rows(d/"encounters.csv"), rows(d/"vitals.csv")
    pids = {r["subject_id"] for r in p}
    eids = {r["encounter_id"] for r in e}
    orphan_e = sum(r["subject_id"] not in pids for r in e)
    orphan_vp = sum(r["subject_id"] not in pids for r in v)
    orphan_ve = sum(r["encounter_id"] not in eids for r in v)
    if orphan_e: problems.append(f"orphan encounters: {orphan_e}")
    if orphan_vp: problems.append(f"vitals with unknown subject: {orphan_vp}")
    if orphan_ve: problems.append(f"vitals with unknown encounter: {orphan_ve}")

    classes = Counter(tuple(r[q] for q in QIS) for r in p)
    min_k = min(classes.values()) if classes else 0
    unique = sum(n for n in classes.values() if n == 1)
    below = sum(n for n in classes.values() if n < args.min_k)

    print(f"Patients:                 {len(p)}")
    print(f"Encounters:               {len(e)}")
    print(f"Vitals:                   {len(v)}")
    print(f"Orphan encounters:        {orphan_e}")
    print(f"Unknown-subject vitals:   {orphan_vp}")
    print(f"Unknown-encounter vitals: {orphan_ve}")
    print(f"Quasi-identifiers:        {', '.join(QIS)}")
    print(f"Minimum equivalence k:    {min_k}")
    print(f"Records with k=1:         {unique}")
    print(f"Records with k<{args.min_k}:        {below}")

    if min_k < args.min_k:
        problems.append(f"minimum k={min_k}, required k>={args.min_k}")

    if problems:
        print("\nPRIVACY VALIDATION FAILED")
        for x in problems:
            print(" -", x)
        return 1

    print("\nPRIVACY VALIDATION PASSED")
    return 0

if __name__ == "__main__":
    sys.exit(main())
