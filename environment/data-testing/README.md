# Project VITAL — Data Testing Environment

This directory supports **Assignment 4: Data Testing**.

The first validated slice uses three logical entities:

```text
Patient
   │
   └── Encounter
           │
           └── Vitals
```

OpenEMR 8.2.0 uses `patient_data` for patient demographics, `form_encounter` for encounters, and `form_vitals` for vitals data. The course generator first creates a **portable synthetic intermediate dataset** before anything is loaded into OpenEMR.

This separation is intentional:

```text
Synthetic Generator
        ↓
CSV intermediate data
        ↓
Data Validators
        ↓
Validated Dataset
        ↓
OpenEMR Loader
```

The generator/validator can therefore be tested independently of the database loader.

## Why Stage 1?

Before finalizing the OpenEMR loader, the instructor should inspect the **actual schema in the pinned running course container**. This avoids hard-coding assumptions that may differ across OpenEMR releases.

Stage 1 provides:

- deterministic synthetic generation;
- 200 / 2,000 / 20,000 presets;
- patient → encounter → vitals relationships;
- automated validation;
- intentional corruption experiments;
- schema-inspection helpers.

After the schema output is validated against the pinned course environment, the OpenEMR loader can be finalized.

---

## Prerequisites

From the Project VITAL root, the normal OpenEMR environment should already run:

```bash
cd environment
docker compose up -d
docker compose ps
```

You also need Python 3:

```bash
python3 --version
```

The generator uses only the Python standard library.

---

# 1. Generate a Small Dataset

From the Project VITAL root:

```bash
python3 environment/data-testing/generate_data.py \
  --size small \
  --seed 42 \
  --output .project-vital/data-testing/small
```

Expected primary-record count:

```text
200 patients
```

The generator also creates related encounters and vitals.

Generated files:

```text
.project-vital/data-testing/small/
├── patients.csv
├── encounters.csv
├── vitals.csv
└── manifest.json
```

`.project-vital/` should already be ignored by Git.

---

# 2. Validate the Dataset

```bash
python3 environment/data-testing/validate_data.py \
  .project-vital/data-testing/small
```

A successful run ends with:

```text
VALIDATION PASSED
```

---

# 3. Reproducibility Check

Generate the same seed twice:

```bash
python3 environment/data-testing/generate_data.py \
  --size small --seed 42 \
  --output .project-vital/data-testing/repro-a

python3 environment/data-testing/generate_data.py \
  --size small --seed 42 \
  --output .project-vital/data-testing/repro-b
```

Compare:

```bash
diff -rq \
  .project-vital/data-testing/repro-a \
  .project-vital/data-testing/repro-b
```

There should be no differences.

Generate a different seed:

```bash
python3 environment/data-testing/generate_data.py \
  --size small --seed 99 \
  --output .project-vital/data-testing/repro-c
```

Now the logical data should differ.

---

# 4. Intentional Corruption

Copy a valid dataset:

```bash
cp -R .project-vital/data-testing/small \
      .project-vital/data-testing/broken
```

Introduce a controlled defect:

```bash
python3 environment/data-testing/corrupt_data.py \
  .project-vital/data-testing/broken \
  --defect orphan-vitals
```

Validate again:

```bash
python3 environment/data-testing/validate_data.py \
  .project-vital/data-testing/broken
```

The validator should fail.

Supported controlled defects:

```text
missing-patient-name
duplicate-patient-id
orphan-encounter
orphan-vitals
invalid-blood-pressure
invalid-dob
```

---

# 5. Generate Medium and High Datasets

```bash
python3 environment/data-testing/generate_data.py \
  --size medium --seed 42 \
  --output .project-vital/data-testing/medium

python3 environment/data-testing/generate_data.py \
  --size high --seed 42 \
  --output .project-vital/data-testing/high
```

Preset patient counts:

```text
small   =    200
medium  =  2,000
high    = 20,000
```

---

# 6. Inspect the Actual OpenEMR 8.2.0 Schema

Make sure the normal OpenEMR Docker environment is running.

From `environment/`:

```bash
docker compose ps
```

Then, from the Project VITAL root:

```bash
bash environment/data-testing/inspect_openemr_schema.sh
```

The script writes:

```text
.project-vital/data-testing/schema/
├── patient_data.txt
├── form_encounter.txt
├── form_vitals.txt
├── forms.txt
└── row-counts.txt
```

These files capture the schema from the **actual running course database**.

Review them before introducing a direct database loader.

---

# 7. Why We Inspect `forms`

OpenEMR clinical forms may involve both a form-specific table and metadata that associates the form with an encounter.

For example, simply inserting a row into a clinical form table does not automatically prove that the OpenEMR UI will recognize the record as part of an encounter.

For Project VITAL, we will validate the exact relationship before finalizing the loader.

---

# 8. Current Data Model

The intermediate dataset intentionally uses stable course-level identifiers rather than pretending they are already OpenEMR database IDs.

## patients.csv

```text
patient_key
first_name
last_name
date_of_birth
sex
email
phone
city
state
postal_code
```

## encounters.csv

```text
encounter_key
patient_key
encounter_datetime
reason
```

## vitals.csv

```text
vitals_key
encounter_key
patient_key
recorded_datetime
systolic
diastolic
pulse
temperature_f
weight_lb
height_in
oxygen_saturation
```

The OpenEMR loader will map these synthetic identifiers to the real OpenEMR identifiers.

This allows the generator to remain independent from database implementation details.

---

# 9. Data Rules Enforced by the Validator

The reference validator checks:

- required identifiers;
- unique patient/encounter/vitals keys;
- valid date formats;
- no future date of birth;
- supported sex values;
- encounter → patient relationship;
- vitals → patient relationship;
- vitals → encounter relationship;
- consistency between the patient on an encounter and the patient on its vitals;
- configurable physiological ranges;
- manifest row counts.

These are **course testing rules**, not a claim that every boundary is an official clinical OpenEMR constraint.

Students should distinguish:

```text
database constraint
application validation
course test-data rule
clinical/domain rule
```

---

# 10. Next Validation Step

After adding this directory to Project VITAL:

1. Run the generator.
2. Run the validator.
3. Run controlled corruption.
4. Generate all three sizes.
5. Run `inspect_openemr_schema.sh`.
6. Share the schema output with the instructor/course maintainer.
7. Finalize and validate the OpenEMR loader.

Do not provide students a direct loader until it has been validated against the exact semester OpenEMR baseline.
