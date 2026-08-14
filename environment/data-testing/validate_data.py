#!/usr/bin/env python3
import argparse, csv, json, sys
from datetime import date, datetime
from pathlib import Path

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def dt(value):
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset")
    args = ap.parse_args()
    root = Path(args.dataset)
    errors = []

    required = ["patients.csv","encounters.csv","vitals.csv","manifest.json"]
    for name in required:
        if not (root/name).exists():
            errors.append(f"missing file: {name}")
    if errors:
        for e in errors: print("ERROR:", e)
        return 1

    patients = read_csv(root/"patients.csv")
    encounters = read_csv(root/"encounters.csv")
    vitals = read_csv(root/"vitals.csv")
    manifest = json.loads((root/"manifest.json").read_text(encoding="utf-8"))

    def keys_unique(rows, key, label):
        values = [r.get(key,"") for r in rows]
        blanks = sum(not v for v in values)
        if blanks: errors.append(f"{label}: {blanks} blank {key} value(s)")
        if len(set(values)) != len(values): errors.append(f"{label}: duplicate {key} value(s)")

    keys_unique(patients, "patient_key", "patients")
    keys_unique(encounters, "encounter_key", "encounters")
    keys_unique(vitals, "vitals_key", "vitals")

    pmap = {r["patient_key"]: r for r in patients}
    emap = {r["encounter_key"]: r for r in encounters}

    allowed_sex = {"Female","Male","Other"}

    for i,p in enumerate(patients, 2):
        if not p["first_name"].strip() or not p["last_name"].strip():
            errors.append(f"patients.csv line {i}: patient name is required")
        try:
            d = date.fromisoformat(p["date_of_birth"])
            if d > date.today():
                errors.append(f"patients.csv line {i}: DOB is in the future")
        except Exception:
            errors.append(f"patients.csv line {i}: invalid DOB")
        if p["sex"] not in allowed_sex:
            errors.append(f"patients.csv line {i}: unsupported sex value {p['sex']!r}")

    for i,e in enumerate(encounters, 2):
        if e["patient_key"] not in pmap:
            errors.append(f"encounters.csv line {i}: orphan patient_key {e['patient_key']}")
        try: dt(e["encounter_datetime"])
        except Exception: errors.append(f"encounters.csv line {i}: invalid encounter_datetime")

    for i,v in enumerate(vitals, 2):
        if v["patient_key"] not in pmap:
            errors.append(f"vitals.csv line {i}: orphan patient_key {v['patient_key']}")
        if v["encounter_key"] not in emap:
            errors.append(f"vitals.csv line {i}: orphan encounter_key {v['encounter_key']}")
        elif emap[v["encounter_key"]]["patient_key"] != v["patient_key"]:
            errors.append(f"vitals.csv line {i}: patient does not match encounter")
        try: dt(v["recorded_datetime"])
        except Exception: errors.append(f"vitals.csv line {i}: invalid recorded_datetime")
        ranges = {
            "systolic": (60,260), "diastolic": (30,160), "pulse": (20,220),
            "temperature_f": (90,110), "weight_lb": (2,1000),
            "height_in": (10,100), "oxygen_saturation": (50,100)
        }
        for field,(lo,hi) in ranges.items():
            try:
                x=float(v[field])
                if not lo <= x <= hi:
                    errors.append(f"vitals.csv line {i}: {field}={x} outside course range {lo}..{hi}")
            except Exception:
                errors.append(f"vitals.csv line {i}: {field} is not numeric")

    expected = manifest.get("counts", {})
    actual = {"patients":len(patients),"encounters":len(encounters),"vitals":len(vitals)}
    for k,n in actual.items():
        if expected.get(k) != n:
            errors.append(f"manifest count mismatch for {k}: expected {expected.get(k)}, actual {n}")

    print(f"Patients:   {len(patients)}")
    print(f"Encounters: {len(encounters)}")
    print(f"Vitals:     {len(vitals)}")
    if errors:
        print(f"\nVALIDATION FAILED ({len(errors)} issue(s))")
        for e in errors[:50]:
            print(" -", e)
        if len(errors) > 50:
            print(f" - ... {len(errors)-50} additional issue(s)")
        return 1

    print("\nVALIDATION PASSED")
    return 0

if __name__ == "__main__":
    sys.exit(main())
