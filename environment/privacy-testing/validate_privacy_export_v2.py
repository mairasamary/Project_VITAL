#!/usr/bin/env python3
import argparse, csv, sys
from collections import Counter
from pathlib import Path

PROHIBITED={"patient_key","first_name","last_name","date_of_birth","email","phone",
            "city","postal_code","encounter_key","vitals_key","encounter_datetime",
            "recorded_datetime"}

def read(path):
    with path.open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def header(path):
    with path.open(newline="",encoding="utf-8") as f:
        return set(next(csv.reader(f)))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("dataset")
    ap.add_argument("--qi",nargs="*",default=[])
    ap.add_argument("--min-k",type=int,default=1)
    args=ap.parse_args()
    d=Path(args.dataset)
    problems=[]

    for name in ["patients.csv","encounters.csv","vitals.csv"]:
        leaked=sorted(header(d/name)&PROHIBITED)
        if leaked: problems.append(f"{name}: prohibited columns: {', '.join(leaked)}")

    p,e,v=read(d/"patients.csv"),read(d/"encounters.csv"),read(d/"vitals.csv")
    pids={r["subject_id"] for r in p}; eids={r["encounter_id"] for r in e}
    oe=sum(r["subject_id"] not in pids for r in e)
    ovp=sum(r["subject_id"] not in pids for r in v)
    ove=sum(r["encounter_id"] not in eids for r in v)
    if oe: problems.append(f"orphan encounters: {oe}")
    if ovp: problems.append(f"vitals with unknown subject: {ovp}")
    if ove: problems.append(f"vitals with unknown encounter: {ove}")

    print("Patients:",len(p))
    print("Encounters:",len(e))
    print("Vitals:",len(v))
    print("Orphan encounters:",oe)
    print("Unknown-subject vitals:",ovp)
    print("Unknown-encounter vitals:",ove)

    if args.qi:
        missing=[x for x in args.qi if x not in p[0]]
        if missing:
            problems.append("missing quasi-identifiers: "+", ".join(missing))
        else:
            c=Counter(tuple(r[x] for x in args.qi) for r in p)
            min_k=min(c.values()) if c else 0
            below=sum(n for n in c.values() if n<args.min_k)
            print("Quasi-identifiers:",", ".join(args.qi))
            print("Minimum k:",min_k)
            print(f"Patients with k<{args.min_k}:",below)
            if min_k<args.min_k:
                problems.append(f"minimum k={min_k}; required >= {args.min_k}")

    if problems:
        print("\nPRIVACY VALIDATION FAILED")
        for x in problems: print(" -",x)
        return 1
    print("\nPRIVACY VALIDATION PASSED")
    return 0

if __name__=="__main__":
    sys.exit(main())
