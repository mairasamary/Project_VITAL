# Project VITAL — Stage 2 OpenEMR Loader Validation

This stage validates the actual OpenEMR load path using the schema captured from the pinned course instance.

## Important schema finding

For this OpenEMR baseline:

```text
patient_data
    ↓ pid
form_encounter
    ↓ encounter relationship
form_vitals
    ↓ form_vitals.id
forms
    ├── form_id → form_vitals.id
    ├── pid
    ├── encounter
    └── formdir = vitals
```

`form_vitals` does not itself contain an encounter column. The `forms` table registers the vitals form with the encounter.

Also important: the inspected tables use indexes but do not declare SQL foreign-key constraints for these relationships. Consequently, database acceptance alone is not sufficient evidence of relational validity. Project VITAL performs explicit post-load relationship validation.

---

# Step 1 — Confirm Docker

```bash
cd environment
docker compose ps
cd ..
```

OpenEMR and MariaDB should be running.

---

# Step 2 — Five-Patient Validation

Run:

```bash
bash environment/data-testing/run_loader_validation.sh
```

Expected sequence:

```text
generate 5
validate CSV
reset prior STAGE2-FIVE batch
load transaction
validate database relationships
PASS
```

Do not proceed to 200 until this succeeds.

---

# Step 3 — Inspect Through OpenEMR

Log in to the local OpenEMR UI.

Search for synthetic patients whose public patient IDs begin with:

```text
VITAL-P
```

Open several patients.

For patients with encounters/vitals, inspect whether the encounter and Vitals form are visible and whether the values are interpretable in the UI.

Record any mismatch between:

```text
database-valid
```

and:

```text
application-visible / application-correct
```

This distinction is an important testing lesson.

---

# Step 4 — Reset

```bash
python3 environment/data-testing/reset_loaded_data.py \
  --batch STAGE2-FIVE
```

Then validate that the batch is gone:

```bash
python3 environment/data-testing/validate_openemr_load.py \
  --batch STAGE2-FIVE
```

The validator should no longer report a valid loaded batch.

---

# Step 5 — Atomicity Experiment

Generate a small source dataset if needed:

```bash
python3 environment/data-testing/generate_data.py \
  --size small --patients 5 --seed 42 \
  --output .project-vital/data-testing/atomicity
```

Run:

```bash
python3 environment/data-testing/test_atomicity.py \
  .project-vital/data-testing/atomicity
```

The loader intentionally fails after patients and encounters have been inserted but before commit.

Expected:

```text
LOAD FAILED
Rows remaining after failed transaction: (0, 0, 0)
ATOMICITY TEST PASSED
```

This demonstrates that the transaction prevents a partially loaded batch.

---

# Step 6 — Wrong Insertion-Order Experiment

Run:

```bash
python3 environment/data-testing/test_insertion_order.py
```

This deliberately inserts an encounter referencing a nonexistent patient inside a transaction.

For the inspected OpenEMR schema, MariaDB may accept this because the relationship is not enforced by a SQL FOREIGN KEY constraint.

Project VITAL then detects the orphan relationship and rolls the experiment back.

Expected lesson:

> Correct insertion order is an application/data-integrity requirement even when the database does not physically enforce it.

---

# Step 7 — Only After All Checks Pass: 200

Generate:

```bash
python3 environment/data-testing/generate_data.py \
  --size small --seed 42 \
  --output .project-vital/data-testing/small
```

Load with a unique batch:

```bash
python3 environment/data-testing/load_openemr.py \
  .project-vital/data-testing/small \
  --batch VITAL-SMALL-42
```

Validate:

```bash
python3 environment/data-testing/validate_openemr_load.py \
  --batch VITAL-SMALL-42
```

Inspect samples in the UI.

Reset when finished:

```bash
python3 environment/data-testing/reset_loaded_data.py \
  --batch VITAL-SMALL-42
```

---

# Do Not Run Medium/High Yet

Do not load 2,000 or 20,000 patients until:

- five-patient DB validation passes;
- UI inspection passes;
- reset works;
- atomic rollback works;
- insertion-order experiment behaves as documented;
- the 200-patient load passes.

The 2,000 and 20,000 stages should be treated as later scale-validation milestones.
