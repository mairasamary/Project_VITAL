#!/usr/bin/env python3
import argparse, csv
from collections import Counter
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("patients_csv")
    ap.add_argument("--fields", nargs="+", required=True)
    ap.add_argument("--threshold", type=int, default=3)
    args=ap.parse_args()

    with Path(args.patients_csv).open(newline="",encoding="utf-8") as f:
        data=list(csv.DictReader(f))
    if not data:
        raise SystemExit("No rows.")
    missing=[x for x in args.fields if x not in data[0]]
    if missing:
        raise SystemExit("Missing quasi-identifier field(s): "+", ".join(missing))

    classes=Counter(tuple(r[x] for x in args.fields) for r in data)
    min_k=min(classes.values())
    below=sum(n for n in classes.values() if n < args.threshold)
    unique=sum(n for n in classes.values() if n==1)

    print("Fields:", ", ".join(args.fields))
    print("Patients:", len(data))
    print("Equivalence classes:", len(classes))
    print("Minimum k:", min_k)
    print("Patients with k=1:", unique)
    print(f"Patients with k<{args.threshold}:", below)
    print("Threshold:", args.threshold)
    print("K-THRESHOLD:", "PASS" if min_k >= args.threshold else "FAIL")
    return 0 if min_k >= args.threshold else 1

if __name__=="__main__":
    raise SystemExit(main())
