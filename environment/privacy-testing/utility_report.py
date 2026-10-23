#!/usr/bin/env python3
import argparse, csv, json
from collections import Counter
from pathlib import Path

def read(path):
    with path.open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("export")
    args=ap.parse_args()
    s,e=Path(args.source),Path(args.export)

    sp,se,sv=read(s/"patients.csv"),read(s/"encounters.csv"),read(s/"vitals.csv")
    ep,ee,ev=read(e/"patients.csv"),read(e/"encounters.csv"),read(e/"vitals.csv")

    checks = {
        "patient_count_preserved": len(sp)==len(ep),
        "encounter_count_preserved": len(se)==len(ee),
        "vitals_count_preserved": len(sv)==len(ev),
        "reason_distribution_preserved": Counter(r["reason"] for r in se)==Counter(r["reason"] for r in ee),
        "vitals_numeric_values_preserved": (
            sum(float(r["systolic"]) for r in sv)==sum(float(r["systolic"]) for r in ev)
            and sum(float(r["pulse"]) for r in sv)==sum(float(r["pulse"]) for r in ev)
        )
    }

    manifest=json.loads((e/"privacy-manifest.json").read_text())
    print("Privacy configuration:",manifest["configuration"])
    print()
    for k,v in checks.items():
        print(f"{k}: {'YES' if v else 'NO'}")
    print()
    print("Available patient analytical fields:", ", ".join(ep[0].keys()))
    print("Available encounter analytical fields:", ", ".join(ee[0].keys()))
    print("Available vitals analytical fields:", ", ".join(ev[0].keys()))
if __name__=="__main__":
    main()
