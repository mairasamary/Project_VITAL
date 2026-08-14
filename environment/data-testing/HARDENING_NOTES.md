# Project VITAL — Stage 2 Loader Hardening

This revision was prompted by a real validation failure.

The original five-patient loader used fixed ID ranges:

```text
patient pid:  9000001...
encounter:    9100001...
```

After the five-patient validation batch remained loaded, a later 200-patient
load correctly failed with a duplicate patient PID.

The failure was safely rolled back, but it revealed that the loader should not
depend on the instructor remembering to delete previous batches.

## Improvements

The hardened loader now:

1. reads the current maximum patient `pid`;
2. reads the current maximum encounter number;
3. chooses the next available high-range identifiers;
4. checks the planned ranges for collisions before loading;
5. rejects a duplicate Project VITAL batch name before loading;
6. keeps the complete load inside one transaction;
7. limits batch names to 20 characters because the selected OpenEMR
   `external_id` field is `varchar(20)`.

The validator now has three semantic outcomes:

```text
BATCH VALID
BATCH INVALID
BATCH NOT FOUND
```

`BATCH NOT FOUND` uses exit code `4`, which is useful after a reset or rollback.

## Required validation before 2,000 records

With the existing 200-patient `VITAL-SMALL-42` batch still loaded, run:

```bash
python3 environment/data-testing/test_batch_coexistence.py
```

The test should prove that:

```text
existing 200-patient batch remains loaded
        +
COEXIST-A loads successfully
        +
COEXIST-B loads successfully
        ↓
both small batches validate independently
        ↓
reset COEXIST-B
        ↓
COEXIST-A remains valid
```

This demonstrates that new batches no longer reuse the original fixed ID range.

## Duplicate-batch preflight

Also test:

```bash
python3 environment/data-testing/load_openemr.py \
  .project-vital/data-testing/small \
  --batch VITAL-SMALL-42
```

Because that batch already exists, the loader should stop *before insertion*
with a message beginning:

```text
PREFLIGHT FAILED
```

This is preferable to discovering a duplicate during the transaction.
