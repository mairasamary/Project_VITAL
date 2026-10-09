# Project VITAL — Assignment 4 Benchmark and Validation Report

**Instructor reference | October 9, 2026**  
**Assignment:** A4 — Data Testing: Quality, Integrity, and Scale  
**System under test:** OpenEMR 8.2.0 with MariaDB 11.8.8, deployed through Docker Compose

## 1. Executive summary

The Project VITAL A4 synthetic-data pipeline was validated at three scales: 200, 2,000, and 20,000 patients. Generation and pre-load validation completed successfully in three repetitions per scale. Separate, isolated OpenEMR environments accepted all three datasets; post-load counts and the three tested relationship checks passed. Transaction rollback was verified through a simulated loader failure, and an insertion-order experiment demonstrated that MariaDB could accept an encounter referencing a nonexistent patient.

A performance investigation found that an orphan-appointment integrity query used a block nested-loop join when it cast the indexed patient identifier to text. Rewriting the join to cast the appointment identifier to an integer enabled indexed patient lookups. In three-run end-to-end integrity benchmarks on the large dataset, mean verification time decreased from **38.658 s to 0.676 s** (approximately **57.2× faster**, or **98.25% less time**). A separate MariaDB profile measured the individual appointment query at **41.388 s before** and **0.174 s after** (approximately **238.5× faster**).

These findings demonstrate that data correctness, transactional behavior, and verification performance are distinct testing concerns.

## 2. Environment and scope

- Repository: `Project_VITAL`; A4 scripts under `environment/data-testing/scripts/`.
- Application: OpenEMR 8.2.0; database: MariaDB 11.8.8; orchestration: Docker Compose.
- Synthetic fixture format: CSV schema v1; deterministic generation with seed `42`.
- Datasets: `.project-vital/data/{small,medium,large}`.
- Generation command: `generate_data.py --level {small,medium,large} --seed 42 --output <directory>`.
- Validation command: `validate_data.py --input <directory>`.
- Loading command: `load_data.py --input <directory> --apply --confirm vital-a4` in a dedicated Docker network with `VITAL_A4_LOADER=yes`.
- Benchmarking utilities: `benchmark_a4.py` (generation and validation), `benchmark_db_a4.py` (loading and database integrity).
- Existing original OpenEMR environment and completed Small, Medium, and Large A4 environments were kept separate from the disposable `vital-a4-bench` Compose project.

**Measurement definition:** Generation and validation times are Python subprocess wall-clock times. Database load times include `docker run`, container startup, PyMySQL installation, fixture validation, transactional insertion, and commit. Database integrity times include the script's SQL count and relationship checks, along with invocation overhead. Reset/reinitialization time is not included in reported load time. All measurements were taken in the user's local development environment; detailed CPU, memory, storage, and concurrent workload characteristics were not recorded.

## 3. Fixture sizes and successful load counts

| Database table / fixture | Small | Medium | Large |
|---|---:|---:|---:|
| `patient_data` / patients | 200 | 2,000 | 20,000 |
| `form_encounter` / encounters | 294 | 2,913 | 29,736 |
| `openemr_postcalendar_events` / appointments | 196 | 2,002 | 20,081 |
| `form_vitals` / vitals | 237 | 2,352 | 23,836 |
| `forms` / vital registrations | 237 | 2,352 | 23,836 |
| **Total committed database rows** | **1,164** | **11,619** | **117,489** |

The loader reported `LOAD PASS — committed` at all three scales. Independent SQL checks returned the expected counts and zero orphan encounters, zero orphan appointments, and zero invalid vital-form links for each dataset. These checks cover the relationships tested, not every possible OpenEMR invariant.

## 4. Generation and pre-load validation benchmark

Three runs per dataset, seed `42`. Values are seconds, rounded to three decimals.

| Dataset | Generation runs (s) | Mean generation (s) | Validation runs (s) | Mean validation (s) |
|---|---|---:|---|---:|
| Small | 0.087, 0.071, 0.088 | 0.082 | 0.076, 0.065, 0.063 | 0.068 |
| Medium | 0.126, 0.180, 0.161 | 0.156 | 0.184, 0.145, 0.124 | 0.151 |
| Large | 0.943, 0.862, 1.003 | 0.936 | 0.790, 0.435, 0.512 | 0.579 |

All nine generation-and-validation experiments passed. Process startup is included in these measurements.

## 5. Database loading and integrity benchmarks

Each series used three runs per dataset. The dedicated `vital-a4-bench` Compose project was reset to an empty, initialized database between repetitions. The first series used the original appointment relationship query; the second used the optimized query. Values are seconds, rounded to three decimals.

### 5.1 Original query: three-run baseline

| Dataset | Load runs (s) | Mean load (s) | Integrity runs (s) | Mean integrity (s) |
|---|---|---:|---|---:|
| Small | 3.069, 2.951, 3.051 | 3.024 | 0.340, 0.364, 0.353 | 0.352 |
| Medium | 5.827, 6.035, 5.593 | 5.818 | 0.677, 0.863, 0.683 | 0.741 |
| Large | 41.712, 47.627, 40.025 | 43.121 | 43.194, 38.551, 34.229 | 38.658 |

### 5.2 Optimized query: three-run follow-up

| Dataset | Load runs (s) | Mean load (s) | Integrity runs (s) | Mean integrity (s) |
|---|---|---:|---|---:|
| Small | 4.673, 4.291, 3.645 | 4.203 | 0.507, 0.454, 0.417 | 0.459 |
| Medium | 9.750, 9.009, 7.553 | 8.771 | 0.471, 0.481, 0.613 | 0.522 |
| Large | 42.949, 44.493, 44.245 | 43.896 | 0.633, 0.717, 0.678 | 0.676 |

### 5.3 Comparison of integrity verification means

| Dataset | Original (s) | Optimized (s) | Interpretation |
|---|---:|---:|---|
| Small | 0.352 | 0.459 | Slightly slower in the follow-up; overhead and run-to-run variation matter at this scale |
| Medium | 0.741 | 0.522 | About 1.42× faster |
| Large | 38.658 | 0.676 | About **57.2× faster**, a **98.25% reduction** |

**Caution:** The original and optimized series were performed at different times, so changes in load times cannot be attributed to the integrity-query rewrite. No confidence intervals or controlled system-load measurements were collected. The large integrity improvement is additionally supported by same-database SQL profiling and execution plans below.

## 6. Root cause and SQL optimization

The original orphan-appointment query was:

```sql
SELECT COUNT(*) AS orphan_appointments
FROM openemr_postcalendar_events a
LEFT JOIN patient_data p
  ON a.pc_pid = CAST(p.pid AS CHAR)
WHERE p.pid IS NULL;
```

On the Large dataset, `EXPLAIN` showed a full appointment scan and a patient index scan with a block nested-loop join (`Using join buffer (flat, BNL join)`), rather than an indexed lookup for each appointment. The reported estimates were approximately 20,084 appointment rows and 19,814 patient index rows.

The optimized query was:

```sql
SELECT COUNT(*) AS orphan_appointments
FROM openemr_postcalendar_events a
LEFT JOIN patient_data p
  ON CAST(a.pc_pid AS UNSIGNED) = p.pid
WHERE p.pid IS NULL;
```

The revised `EXPLAIN` showed `type=eq_ref`, `key=pid`, and `rows=1` for `patient_data`, eliminating the block nested-loop join in the observed plan.

MariaDB session profiling against the same Large benchmark database returned:

| Query | Result (orphan appointments) | Profiled duration |
|---|---:|---:|
| Original | 0 | 41.38778846 s |
| Optimized | 0 | 0.17352001 s |

The optimized query was approximately **238.5× faster** in this single paired profiling experiment. Both queries returned the same count, but a zero orphan count alone does not prove equivalence for every possible input.

**Data semantics caveat:** `CAST(a.pc_pid AS UNSIGNED)` is appropriate for the numeric patient IDs in these generated fixtures. On production data, malformed, nonnumeric, signed, or specially formatted identifiers could be converted unexpectedly. Validate identifier formats and consider schema-appropriate joins before applying this rewrite outside the controlled A4 dataset.

## 7. Correctness, integrity, and transaction experiments

### 7.1 Pre-load fixture validation

All datasets passed independent CSV validation prior to loading. The validation script checks fixture structure and supported data relationships. The successful outcomes were recorded in terminal output for each scale.

### 7.2 Post-load relationship checks

The independent SQL verification examined:

1. Encounters without a matching `patient_data.pid`.
2. Appointments without a matching patient identifier.
3. Vital-form registrations lacking a matching vital record or clinical encounter for the same patient.

Each check returned **0** for Small, Medium, and Large datasets. The vital-form check joins `forms.encounter` to the clinical `form_encounter.encounter` value, not the encounter table's auto-increment `id`.

### 7.3 Automatic rollback on injected loader failure

A disposable, empty database was used to invoke `load_data.py --simulate-failure` with the Small dataset. The loader inserted patients within a transaction, intentionally raised an error before commit, and executed rollback. Independent SQL queries confirmed that all five target tables remained empty. This demonstrates rollback at the tested failure point, not every possible failure mode.

### 7.4 Insertion-order / orphan experiment

A test inserted an encounter referencing nonexistent patient `99999999` inside a transaction. MariaDB accepted the insert; a subsequent orphan-detection query returned **1**. After `ROLLBACK`, the encounter count was **0**. This shows that successful insertion alone did not enforce the tested semantic relationship in this database configuration.

## 8. Reproduction guide

Run from the Project VITAL repository root. Review scripts and the target Docker Compose project before running commands that write to a database.

### 8.1 Generation and validation (no database writes)

```bash
python3 environment/data-testing/scripts/benchmark_a4.py --runs 3
```

Expected artifacts:

- `.project-vital/benchmarks/benchmark_results.csv`
- `.project-vital/benchmarks/benchmark_report.md`

### 8.2 Database loading and integrity benchmark (destructive to benchmark volumes)

```bash
python3 environment/data-testing/scripts/benchmark_db_a4.py \
  --runs 3 \
  --allow-benchmark-reset
```

**Warning:** The database benchmark resets the `vital-a4-bench` Compose project and removes its dedicated volumes between runs. Do not run it if those volumes contain data you need. Confirm that the container and volume ownership labels are `com.docker.compose.project=vital-a4-bench` and that the configured project and container names have not been changed. The original OpenEMR environment and other A4 datasets must remain outside this project.

Expected artifacts:

- `.project-vital/benchmarks/database_benchmark_results.csv`
- `.project-vital/benchmarks/database_benchmark_report.md`

### 8.3 Inspect query plans without changing data

```bash
docker exec -i vital-a4-bench-db \
  mariadb -uroot -p -D openemr <<'SQL'
EXPLAIN
SELECT COUNT(*)
FROM openemr_postcalendar_events a
LEFT JOIN patient_data p
  ON CAST(a.pc_pid AS UNSIGNED) = p.pid
WHERE p.pid IS NULL;
SQL
```

The MariaDB client will prompt for the root password. The benchmark database must still contain the Large dataset to reproduce the Large-dataset execution plan.

## 9. Limitations and threats to validity

- Only three repetitions per scale were recorded; results are indicative rather than statistically conclusive.
- The experiments ran on a single development machine. CPU, RAM, disk performance, thermal state, and competing workloads were not documented.
- End-to-end loading includes dependency installation and Docker startup; it does not isolate database insertion latency.
- Fresh database initialization was performed between runs, but cache and host-state effects were not controlled.
- The original and optimized benchmark series were collected sequentially, not interleaved or randomized.
- Relationship verification covers three selected checks, not all OpenEMR integrity constraints or application workflows.
- The optimized numeric cast assumes numeric synthetic appointment patient identifiers.
- A single injected failure and a single insertion-order scenario do not establish comprehensive transactional or referential-integrity coverage.
- The previously generated CSV and Markdown benchmark outputs may have been overwritten by subsequent runs. The baseline measurements in this report were transcribed from the recorded terminal outputs.

## 10. Instructor use and suggested student work

**Instructor-validated reference:** The results above document successful synthetic-data generation, loading, selected relationship checks, rollback behavior, and an observed SQL query optimization. They should not be presented as results independently obtained by students.

**Student reproduction opportunities:**

1. Generate and validate datasets using the documented seed and record fixture counts.
2. Load into a fresh isolated OpenEMR database and independently verify table counts.
3. Write and run relationship checks for encounters, appointments, and vital registrations.
4. Demonstrate an intentionally invalid insertion inside a rollback-protected transaction.
5. Measure generation, validation, loading, and integrity-check durations at multiple scales.
6. Compare original and optimized appointment joins with `EXPLAIN` and timed queries, explaining why the execution plans differ.
7. Discuss measurement overhead, dataset assumptions, and risks of applying fixture-specific casts to production data.

**Suggested submission evidence:** commands executed, seed and dataset metadata, CSV or Markdown benchmark output, SQL query results, execution plans, short interpretation, and a limitations paragraph.

## 11. Conclusion

Project VITAL A4 successfully exercised a deterministic synthetic-data workflow from generation through database verification at 200, 2,000, and 20,000 patients. The most consequential finding was that an integrity query can be logically correct yet scale poorly: moving a type conversion off the indexed patient identifier changed the MariaDB plan from a block nested-loop join to an indexed lookup and reduced the Large dataset's measured integrity-check time substantially. This provides a concrete teaching example connecting data testing, database design, performance analysis, and evidence-based optimization.
