# Project VITAL — Data Testing Benchmark Utility

The benchmark utility records the time required for four distinct Assignment 4 operations:

```text
Synthetic generation
        ↓
Intermediate validation
        ↓
OpenEMR database load
        ↓
Post-load database validation
```

This separation is important because different operations may scale differently.

## Run One Scale

Small:

```bash
python3 environment/data-testing/benchmark.py \
  --size small \
  --seed 42
```

Medium:

```bash
python3 environment/data-testing/benchmark.py \
  --size medium \
  --seed 42
```

High:

```bash
python3 environment/data-testing/benchmark.py \
  --size high \
  --seed 42
```

By default, the temporary benchmark batch is automatically removed after successful validation.

## Run All Three Scales

```bash
python3 environment/data-testing/benchmark.py \
  --all \
  --seed 42
```

Recommended instructor validation order:

```text
small
  ↓
medium
  ↓
high
```

Do not begin with `--all` until the utility has been validated at Small scale.

## Keep a Dataset Loaded

For UI inspection:

```bash
python3 environment/data-testing/benchmark.py \
  --size small \
  --seed 42 \
  --keep-loaded
```

The batch name is printed during the run and recorded in the results file.

Reset it afterward with:

```bash
python3 environment/data-testing/reset_loaded_data.py \
  --batch <BATCH-NAME>
```

## Output

Results are written under:

```text
.project-vital/data-testing/benchmark-results/
├── benchmark-results.csv
└── benchmark-results.md
```

These files are local experiment artifacts and should normally not be committed.

Students may instead copy selected results into their Assignment 4 report.

## What Is Measured?

The utility records:

- size;
- seed;
- batch;
- patients;
- encounters;
- vitals;
- generation wall-clock time;
- intermediate validation wall-clock time;
- database load wall-clock time;
- database validation wall-clock time;
- reset wall-clock time;
- status.

## Interpretation

This is a **data-scale experiment**, not a rigorous performance benchmark.

Results may vary because of:

- CPU and memory;
- Docker Desktop/Engine resource allocation;
- storage speed;
- current database size;
- background processes;
- operating system;
- warm/cold caches.

Students should compare the behavior of the different pipeline stages rather than treating the times as universal OpenEMR performance numbers.

## Recommended Assignment 4 Question

After running the three scales, students should answer:

> Which stage scaled most noticeably as the dataset increased: generation, validation, database loading, or post-load validation? What evidence supports your conclusion?

This keeps the activity focused on data testing and prepares students for later formal performance testing.
