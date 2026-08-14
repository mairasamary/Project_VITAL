#!/usr/bin/env python3
import argparse, csv
from pathlib import Path

def read(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write(path, rows):
    if not rows:
        raise SystemExit(f"Cannot rewrite empty file {path}")
    with path.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("dataset")
    ap.add_argument("--defect", required=True, choices=[
        "missing-patient-name","duplicate-patient-id","orphan-encounter",
        "orphan-vitals","invalid-blood-pressure","invalid-dob"])
    a=ap.parse_args()
    root=Path(a.dataset)
    patients=read(root/"patients.csv")
    encounters=read(root/"encounters.csv")
    vitals=read(root/"vitals.csv")

    if a.defect=="missing-patient-name":
        patients[0]["first_name"]=""
        write(root/"patients.csv",patients)
    elif a.defect=="duplicate-patient-id":
        patients[1]["patient_key"]=patients[0]["patient_key"]
        write(root/"patients.csv",patients)
    elif a.defect=="orphan-encounter":
        encounters[0]["patient_key"]="P-NOT-EXIST"
        write(root/"encounters.csv",encounters)
    elif a.defect=="orphan-vitals":
        vitals[0]["encounter_key"]="E-NOT-EXIST"
        write(root/"vitals.csv",vitals)
    elif a.defect=="invalid-blood-pressure":
        vitals[0]["systolic"]="999"
        write(root/"vitals.csv",vitals)
    elif a.defect=="invalid-dob":
        patients[0]["date_of_birth"]="2999-01-01"
        write(root/"patients.csv",patients)

    print(f"Introduced controlled defect: {a.defect}")

if __name__=="__main__":
    main()
