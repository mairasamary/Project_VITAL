#!/usr/bin/env python3
import argparse, csv, json, random, shutil, time
from datetime import date, datetime, timedelta
from pathlib import Path

SIZES = {"small": 200, "medium": 2000, "high": 20000}

FIRST = ["Alex","Jordan","Taylor","Morgan","Casey","Riley","Cameron","Avery","Quinn","Parker",
         "Sam","Jamie","Drew","Reese","Rowan","Skyler","Emerson","Hayden","Dakota","Finley"]
LAST = ["Rivera","Patel","Nguyen","Garcia","Smith","Johnson","Brown","Lee","Kim","Martinez",
        "Wilson","Davis","Anderson","Thomas","Moore","Jackson","White","Harris","Clark","Lewis"]
CITIES = [("Boston","MA","02108"),("Cambridge","MA","02139"),("Newton","MA","02458"),
          ("Brookline","MA","02445"),("Quincy","MA","02169"),("Somerville","MA","02143")]
REASONS = ["Annual physical","Follow-up","Blood pressure check","Medication review",
           "Preventive visit","Minor illness","Routine evaluation"]

def iso_dt(d):
    return d.strftime("%Y-%m-%d %H:%M:%S")

def dob(rng):
    today = date.today()
    age_days = rng.randint(18*365, 90*365)
    d = today - timedelta(days=age_days)
    return d.isoformat()

def write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", choices=SIZES, default="small")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--output", required=True)
    ap.add_argument("--patients", type=int, help="override preset patient count")
    args = ap.parse_args()

    count = args.patients or SIZES[args.size]
    rng = random.Random(args.seed)
    out = Path(args.output)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    start = time.perf_counter()
    patients, encounters, vitals = [], [], []
    base = datetime(2025, 1, 1, 8, 0, 0)

    for i in range(1, count + 1):
        pkey = f"P{i:07d}"
        first = rng.choice(FIRST)
        last = rng.choice(LAST)
        city, state, postal = rng.choice(CITIES)
        sex = rng.choice(["Female","Male","Other"])
        patients.append({
            "patient_key": pkey,
            "first_name": first,
            "last_name": last,
            "date_of_birth": dob(rng),
            "sex": sex,
            "email": f"{pkey.lower()}@synthetic.invalid",
            "phone": f"555-{rng.randint(100,999):03d}-{rng.randint(1000,9999):04d}",
            "city": city,
            "state": state,
            "postal_code": postal,
        })

        # 0–3 encounters/patient, deterministic from seed
        n_enc = rng.randint(0, 3)
        for e in range(1, n_enc + 1):
            ekey = f"E{i:07d}-{e:02d}"
            when = base + timedelta(days=rng.randint(0, 540), hours=rng.randint(0, 8), minutes=rng.choice([0,15,30,45]))
            encounters.append({
                "encounter_key": ekey,
                "patient_key": pkey,
                "encounter_datetime": iso_dt(when),
                "reason": rng.choice(REASONS),
            })

            # roughly 85% of encounters have a vitals record
            if rng.random() < 0.85:
                vkey = f"V{i:07d}-{e:02d}"
                height = round(rng.uniform(58, 77), 1)
                weight = round(rng.uniform(105, 280), 1)
                systolic = rng.randint(90, 165)
                diastolic = rng.randint(55, 105)
                vitals.append({
                    "vitals_key": vkey,
                    "encounter_key": ekey,
                    "patient_key": pkey,
                    "recorded_datetime": iso_dt(when + timedelta(minutes=rng.randint(1, 20))),
                    "systolic": systolic,
                    "diastolic": diastolic,
                    "pulse": rng.randint(50, 110),
                    "temperature_f": round(rng.uniform(96.5, 100.8), 1),
                    "weight_lb": weight,
                    "height_in": height,
                    "oxygen_saturation": rng.randint(92, 100),
                })

    write_csv(out/"patients.csv",
              ["patient_key","first_name","last_name","date_of_birth","sex","email","phone","city","state","postal_code"],
              patients)
    write_csv(out/"encounters.csv",
              ["encounter_key","patient_key","encounter_datetime","reason"],
              encounters)
    write_csv(out/"vitals.csv",
              ["vitals_key","encounter_key","patient_key","recorded_datetime","systolic","diastolic","pulse",
               "temperature_f","weight_lb","height_in","oxygen_saturation"],
              vitals)

    elapsed = time.perf_counter() - start
    manifest = {
        "project": "Project VITAL",
        "synthetic": True,
        "size": args.size,
        "seed": args.seed,
        "counts": {"patients": len(patients), "encounters": len(encounters), "vitals": len(vitals)},
        "generation_seconds": round(elapsed, 6),
        "note": "All records are synthetic and do not represent real people."
    }
    (out/"manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
