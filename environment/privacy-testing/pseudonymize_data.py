#!/usr/bin/env python3
import argparse, csv, hashlib, hmac, json, shutil
from datetime import date, datetime
from pathlib import Path

PATIENT_OUT = ["subject_id","age_band","sex","state","postal_prefix"]
ENCOUNTER_OUT = ["encounter_id","subject_id","encounter_month","reason"]
VITALS_OUT = ["vitals_id","encounter_id","subject_id","recorded_month",
              "systolic","diastolic","pulse","temperature_f","weight_lb",
              "height_in","oxygen_saturation"]

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def token(secret, namespace, value):
    digest = hmac.new(secret.encode(), f"{namespace}:{value}".encode(),
                      hashlib.sha256).hexdigest()
    return digest[:20]

def age_band(dob):
    born = date.fromisoformat(dob)
    # Fixed reference date makes the export reproducible across semesters/runs.
    ref = date(2026, 1, 1)
    age = ref.year - born.year - ((ref.month, ref.day) < (born.month, born.day))
    lo = max(0, (age // 10) * 10)
    return f"{lo}-{lo+9}"

def month_only(value):
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--output", required=True)
    ap.add_argument("--secret", required=True,
                    help="local experiment secret; never commit a real re-identification key")
    args = ap.parse_args()

    src, out = Path(args.source), Path(args.output)
    required = ["patients.csv","encounters.csv","vitals.csv","manifest.json"]
    missing = [x for x in required if not (src/x).exists()]
    if missing:
        raise SystemExit("Missing source files: " + ", ".join(missing))

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    patients = read_csv(src/"patients.csv")
    encounters = read_csv(src/"encounters.csv")
    vitals = read_csv(src/"vitals.csv")

    pmap = {r["patient_key"]: token(args.secret, "patient", r["patient_key"])
            for r in patients}
    emap = {r["encounter_key"]: token(args.secret, "encounter", r["encounter_key"])
            for r in encounters}

    pout = [{
        "subject_id": pmap[r["patient_key"]],
        "age_band": age_band(r["date_of_birth"]),
        "sex": r["sex"],
        "state": r["state"],
        "postal_prefix": r["postal_code"][:3] + "**",
    } for r in patients]

    eout = [{
        "encounter_id": emap[r["encounter_key"]],
        "subject_id": pmap[r["patient_key"]],
        "encounter_month": month_only(r["encounter_datetime"]),
        "reason": r["reason"],
    } for r in encounters]

    vout = [{
        "vitals_id": token(args.secret, "vitals", r["vitals_key"]),
        "encounter_id": emap[r["encounter_key"]],
        "subject_id": pmap[r["patient_key"]],
        "recorded_month": month_only(r["recorded_datetime"]),
        "systolic": r["systolic"], "diastolic": r["diastolic"],
        "pulse": r["pulse"], "temperature_f": r["temperature_f"],
        "weight_lb": r["weight_lb"], "height_in": r["height_in"],
        "oxygen_saturation": r["oxygen_saturation"],
    } for r in vitals]

    write_csv(out/"patients.csv", PATIENT_OUT, pout)
    write_csv(out/"encounters.csv", ENCOUNTER_OUT, eout)
    write_csv(out/"vitals.csv", VITALS_OUT, vout)

    manifest = {
        "project": "Project VITAL",
        "privacy_stage": "pseudonymized-research-export",
        "synthetic_source": True,
        "counts": {"patients": len(pout), "encounters": len(eout), "vitals": len(vout)},
        "transformations": {
            "direct_identifiers": "removed",
            "patient_keys": "HMAC pseudonyms",
            "encounter_keys": "HMAC pseudonyms",
            "vitals_keys": "HMAC pseudonyms",
            "date_of_birth": "10-year age band using fixed reference date 2026-01-01",
            "postal_code": "3-digit prefix + suppression",
            "timestamps": "month only"
        },
        "warning": "This is a teaching pseudonymization pipeline, not a certification that data are anonymous."
    }
    (out/"privacy-manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
