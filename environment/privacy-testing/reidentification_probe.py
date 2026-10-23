#!/usr/bin/env python3
import argparse, csv
from collections import Counter
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(description="Measure equivalence classes for selected quasi-identifiers.")
    ap.add_argument("patients_csv")
    ap.add_argument("--fields", nargs="+", default=["age_band","sex","state","postal_prefix"])
    args = ap.parse_args()

    with Path(args.patients_csv).open(newline="", encoding="utf-8") as f:
        data = list(csv.DictReader(f))
    if not data:
        raise SystemExit("No patient rows.")
    unknown = [x for x in args.fields if x not in data[0]]
    if unknown:
        raise SystemExit("Unknown fields: " + ", ".join(unknown))

    c = Counter(tuple(r[x] for x in args.fields) for r in data)
    hist = Counter(c.values())
    print("Quasi-identifiers:", ", ".join(args.fields))
    print("Patients:", len(data))
    print("Equivalence classes:", len(c))
    print("Minimum k:", min(c.values()))
    print("Patients unique on these fields:", sum(n for n in c.values() if n == 1))
    print("\nClass-size distribution:")
    for k in sorted(hist)[:15]:
        print(f"  k={k}: {hist[k]} class(es)")
if __name__ == "__main__":
    main()
