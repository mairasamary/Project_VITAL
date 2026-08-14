# Instructor Validation — Benchmark Utility

Validate the benchmark utility before exposing it to students.

## 1. Small scale

Run:

```bash
bash environment/data-testing/run_benchmark_validation.sh
```

Expected:

- 200 patients generated;
- intermediate validator passes;
- database load commits;
- database validator reports `BATCH VALID`;
- benchmark batch is reset automatically;
- CSV and Markdown reports are created;
- script ends with `BENCHMARK UTILITY VALIDATION PASSED`.

## 2. Confirm reset behavior

Find the generated batch name in:

```text
.project-vital/data-testing/benchmark-results/benchmark-results.csv
```

Then:

```bash
python3 environment/data-testing/validate_openemr_load.py \
  --batch <BATCH-NAME>
```

Expected:

```text
BATCH NOT FOUND
```

because the benchmark removes its batch by default.

## 3. Medium

After Small passes:

```bash
python3 environment/data-testing/benchmark.py \
  --size medium \
  --seed 42
```

Review the report.

## 4. High

Only after Medium passes:

```bash
python3 environment/data-testing/benchmark.py \
  --size high \
  --seed 42
```

Review the report.

## 5. Optional all-scale run

After each individual scale has been validated:

```bash
python3 environment/data-testing/benchmark.py \
  --all \
  --seed 42
```

## 6. Record instructor baseline

Do not treat baseline timing as a grading target.

Record it as an instructor reference containing:

- hardware/OS;
- Docker version;
- OpenEMR Project VITAL semester baseline;
- seed;
- generated counts;
- observed timing;
- notable UI behavior.

The assignment should ask students to interpret their own measurements, not match the instructor's timing.
