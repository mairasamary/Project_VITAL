#!/usr/bin/env python3
import argparse, csv
from pathlib import Path

def read(path):
    with path.open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write(path, rows, fields=None):
    if fields is None:
        fields=list(rows[0].keys())
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader(); w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("dataset")
    ap.add_argument("--defect",required=True,choices=[
        "leak-email","break-encounter-subject","break-vitals-encounter"
    ])
    args=ap.parse_args()
    d=Path(args.dataset)

    if args.defect=="leak-email":
        p=read(d/"patients.csv")
        fields=list(p[0].keys())+["email"]
        for i,r in enumerate(p):
            r["email"]=f"leaked{i+1}@example.invalid"
        write(d/"patients.csv",p,fields)
    elif args.defect=="break-encounter-subject":
        e=read(d/"encounters.csv")
        e[0]["subject_id"]="UNKNOWN-SUBJECT"
        write(d/"encounters.csv",e)
    elif args.defect=="break-vitals-encounter":
        v=read(d/"vitals.csv")
        v[0]["encounter_id"]="UNKNOWN-ENCOUNTER"
        write(d/"vitals.csv",v)

    print("Introduced privacy defect:",args.defect)

if __name__=="__main__":
    main()
