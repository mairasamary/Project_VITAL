#!/usr/bin/env python3
"""
Project VITAL privacy transformation experiment.

This tool creates progressively more generalized research exports from the
synthetic Project VITAL source data. It is a teaching tool for comparing
privacy risk with data utility. It does NOT certify anonymity or legal
de-identification.
"""
import argparse, csv, hashlib, hmac, json, shutil
from datetime import date, datetime
from pathlib import Path

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def token(secret, namespace, value):
    return hmac.new(
        secret.encode(),
        f"{namespace}:{value}".encode(),
        hashlib.sha256
    ).hexdigest()[:20]

def age_years(dob, ref=date(2026,1,1)):
    born = date.fromisoformat(dob)
    return ref.year - born.year - ((ref.month, ref.day) < (born.month, born.day))

def age_band(dob, width):
    age = age_years(dob)
    lo = max(0, (age // width) * width)
    return f"{lo}-{lo + width - 1}"

def time_generalize(value, mode):
    dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    if mode == "month":
        return dt.strftime("%Y-%m")
    if mode == "year":
        return dt.strftime("%Y")
    return ""

def geo_value(row, mode):
    if mode == "postal3":
        return row["postal_code"][:3] + "**"
    if mode == "state":
        return row["state"]
    return ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--output", required=True)
    ap.add_argument("--secret", required=True)
    ap.add_argument("--age-band", type=int, choices=[5,10,20], default=10)
    ap.add_argument("--geo", choices=["postal3","state","none"], default="postal3")
    ap.add_argument("--time", choices=["month","year","none"], default="month")
    ap.add_argument("--suppress-sex", action="store_true")
    args = ap.parse_args()

    src, out = Path(args.source), Path(args.output)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    patients = read_csv(src/"patients.csv")
    encounters = read_csv(src/"encounters.csv")
    vitals = read_csv(src/"vitals.csv")

    pmap = {r["patient_key"]: token(args.secret, "patient", r["patient_key"]) for r in patients}
    emap = {r["encounter_key"]: token(args.secret, "encounter", r["encounter_key"]) for r in encounters}

    patient_fields = ["subject_id","age_band"]
    if not args.suppress_sex:
        patient_fields.append("sex")
    if args.geo != "none":
        patient_fields.append("geography")

    pout = []
    for r in patients:
        row = {
            "subject_id": pmap[r["patient_key"]],
            "age_band": age_band(r["date_of_birth"], args.age_band),
        }
        if not args.suppress_sex:
            row["sex"] = r["sex"]
        if args.geo != "none":
            row["geography"] = geo_value(r,args.geo)
        pout.append(row)

    encounter_fields = ["encounter_id","subject_id"]
    if args.time != "none":
        encounter_fields.append("encounter_period")
    encounter_fields.append("reason")

    eout=[]
    for r in encounters:
        row={
            "encounter_id": emap[r["encounter_key"]],
            "subject_id": pmap[r["patient_key"]],
            "reason": r["reason"],
        }
        if args.time != "none":
            row["encounter_period"] = time_generalize(r["encounter_datetime"], args.time)
        eout.append(row)

    vitals_fields=["vitals_id","encounter_id","subject_id"]
    if args.time != "none":
        vitals_fields.append("recorded_period")
    vitals_fields += ["systolic","diastolic","pulse","temperature_f","weight_lb","height_in","oxygen_saturation"]

    vout=[]
    for r in vitals:
        row={
            "vitals_id": token(args.secret,"vitals",r["vitals_key"]),
            "encounter_id": emap[r["encounter_key"]],
            "subject_id": pmap[r["patient_key"]],
            "systolic": r["systolic"], "diastolic": r["diastolic"],
            "pulse": r["pulse"], "temperature_f": r["temperature_f"],
            "weight_lb": r["weight_lb"], "height_in": r["height_in"],
            "oxygen_saturation": r["oxygen_saturation"],
        }
        if args.time != "none":
            row["recorded_period"] = time_generalize(r["recorded_datetime"], args.time)
        vout.append(row)

    write_csv(out/"patients.csv",patient_fields,pout)
    write_csv(out/"encounters.csv",encounter_fields,eout)
    write_csv(out/"vitals.csv",vitals_fields,vout)

    manifest={
        "project":"Project VITAL",
        "privacy_stage":"generalization-experiment",
        "synthetic_source":True,
        "counts":{"patients":len(pout),"encounters":len(eout),"vitals":len(vout)},
        "configuration":{
            "age_band_width":args.age_band,
            "geography":args.geo,
            "time_granularity":args.time,
            "sex_suppressed":args.suppress_sex,
        },
        "warning":"Teaching privacy transformation only; passing a k threshold does not certify anonymity."
    }
    (out/"privacy-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2))

if __name__=="__main__":
    main()
