# Project VITAL — Assignment 4: Data Testing — Quality, Integrity, and Scale

**Team Assignment | OpenEMR | Synthetic Data | Python | MariaDB**

## Purpose

In Assignment 1, you explored **what OpenEMR does**. In Assignment 2, you investigated **how a workflow is implemented**. In Assignment 3, you tested a small part of that implementation independently.

Assignment 4 asks:

> **How can we determine whether the data used by and stored in a software system is correct, consistent, reproducible, and usable at different scales?**

Your team will generate reproducible **synthetic data**, develop and apply data-quality rules, load data into an **isolated** OpenEMR database, investigate deliberately introduced defects and database behavior, and compare three dataset sizes.

The goal is not simply to generate thousands of records or obtain a `PASS` message. The goal is:

**data specification → reproducible generation → validation → controlled loading → evidence → experiments → interpretation**

## Start Here

Your private team repository contains an Assignment 4 workspace and starter infrastructure under `environment/data-testing/`.

1. Pull the latest version of your team repository (`git pull`).
2. Read this assignment and `environment/data-testing/README.md` before running Docker commands.
3. Confirm that Docker is running. **Do not reset or delete your A1–A3 OpenEMR environment.**
4. Start by generating and validating the **small** dataset; do not begin with 20,000 patients.
5. Keep team-developed scripts, tests, and reports under `assignment-04/`.

The environment README contains the full, tested commands for **dedicated Docker Compose projects, identity initialization, dry runs, and confirmed loads**. Never substitute an existing course database for the dedicated A4 database.

## Connection to Previous Assignments

Revisit the workflow your team investigated in Assignment 2: **Patient Registration, Appointment Scheduling, or Recording Vital Signs**. Its architecture, data model, URL trace, and related observations will help you decide which fields, relationships, and data expectations to investigate.

Assignment 3 showed that passing unit tests cannot establish that complete workflows and their stored data are correct. Here you will explicitly test data quality **before** and **after** database insertion.

> **Database acceptance is not proof of semantic correctness.** A row may be inserted successfully and still violate an application-level expectation.

## Learning Objectives

By the end of this assignment, your team should be able to:

1. Distinguish data testing from functional testing.
2. Define evidence-based data-quality properties.
3. Generate reproducible synthetic relational data.
4. Validate completeness, validity, uniqueness, consistency, and referential integrity.
5. Distinguish database acceptance from semantically correct data.
6. Verify loaded data with database evidence and selected UI observations.
7. Show that a validator detects known defects.
8. Investigate atomicity and insertion-order behavior.
9. Compare data-testing behavior across dataset sizes without confusing data volume with workload.
10. Document evidence, assumptions, uncertainty, and AI-assisted work.

## Standard Project VITAL Data Levels

| Level | Patients | Primary purpose in Assignment 4 |
|---|---:|---|
| **Small** | **200** | Correctness, debugging, validation |
| **Medium** | **2,000** | Comparison at moderate scale |
| **Large** | **20,000** | High-volume integrity and pipeline behavior |

Use **seed 42** for submitted datasets. Course validation may use another seed, such as **314159**. Running the generator twice with the same level and seed should produce equivalent dataset contents, including related encounters, appointments, and vital-sign records.

**Data volume is not workload.** A database containing 20,000 patients is not the same as 20,000 simultaneous requests. Record execution times as baseline observations, not as rigorous proof of performance or scalability.

## Part 0 — Validate Your Environment

Start from the **root of your team repository**. Generate the small fixture, then validate it:

```bash
python3 environment/data-testing/scripts/generate_data.py --level small --seed 42 --output .project-vital/data/small
python3 environment/data-testing/scripts/validate_data.py --input .project-vital/data/small
```

A valid small fixture should report `PASS` and **200 patients**, with related record counts recorded in its manifest and validator output. A `PASS` result demonstrates only the properties checked by the supplied validator; it is **not** your completed data-testing assignment.

The provided `generate_data.py`, `validate_data.py`, and `load_data.py` are **starter infrastructure**, not the finished graded deliverables. Your team must document adaptations and implement its own additional validation, tests, experiments, and analysis.

### Set up the isolated A4 database

Follow `environment/data-testing/README.md` to start the dedicated Compose project (`vital-a4-student`), initialize the identity marker **only in a new, empty A4 database**, run the loader in dry-run mode, and then run a confirmed load when the environment is verified. Follow that document's instructions for separate environments for medium and large loads.

**Do not run `docker compose down -v` on the original A1–A3 project.** Never load real patient information, reuse an existing clinical database, or reset a database to make an experiment easier. Do not commit `.project-vital/`, database dumps, passwords, tokens, or generated datasets.

## Part A — Define the Data Specification

Complete `assignment-04/data-specification.md` **before evaluating the datasets**.

Document the entities/tables represented; important fields and identifiers; required versus optional fields; relationships; categories; date/time relationships; and domain constraints to test. Label each rule as **supported by evidence** or **a hypothesis that still needs verification**.

Use evidence from OpenEMR schema/source code, observed UI behavior, your Assignment 2 artifacts, or the course fixture specification. **AI-generated statements alone are not evidence.**

## Part B — Reproducible Synthetic Data Generation

Use the supplied framework to generate each of the three levels with a configurable seed. Include consistent **patients, encounters, appointments, and vital-sign records**, not merely different numbers of patient rows.

Run the generator twice with the same level and seed; demonstrate reproducibility. Explain how your code or configuration creates identifiers, relationships, categories, dates, and measurements. Synthetic vital CSVs use **pounds** for weight and **inches** for height, as documented in the environment README.

Store the code needed to recreate fixtures, **not** large generated CSVs. Record any changes your team makes to starter scripts.

## Part C — Design a Data-Quality Test Plan

Complete `assignment-04/validation-plan.md` before inspecting validation outcomes. Address:

- **Completeness:** required identifiers, records, or relationships are present.
- **Validity:** representations, types, categories, and supported constraints are respected.
- **Uniqueness:** fields actually expected to be unique contain no unexpected duplicates.
- **Consistency:** related or derived fields do not contradict one another.
- **Referential integrity:** dependent records reference appropriate existing records.

For every important rule, specify its justification, evidence, test method, and expected result.

| Property / rule | Why it matters | Evidence supporting expectation | Test method / expected result |
|---|---|---|---|
| ... | ... | ... | ... |

Do not assume that a column is unique or mandatory based solely on its name.

## Part D — Perform Pre-Load Validation

Run the validator on **small, medium, and large** fixtures before loading them. Record level, seed, expected and actual patient and related-record counts, rules run, failures, and overall result.

Describe **what the validator does not check** and add team-designed validation/tests needed to address important documented rules. A successful generator execution does not prove data quality.

## Part E — Load Data into Isolated OpenEMR

Use the controlled loader and exact safety workflow in `environment/data-testing/README.md`. For each level, record attempted, committed, and rejected records; warnings/errors; and loading duration.

The loader is protected against loading a populated database. For separate levels use separate **new A4 Compose projects and volumes** with distinct container names and ports. Do not delete another experiment's database or load another fixture into a populated one.

## Part F — Validate the Loaded Database

Check actual database state against the fixture and your specification. Investigate counts, missing values, uniqueness, references, expected relationships, and selected stored field values. Save relevant SQL queries and results.

Explain any differences between **what the loader accepted** and **what the data specification requires**.

## Part G — Perform UI Spot Checks

For each level, inspect a small, purposeful sample using OpenEMR. Can you locate generated patients? Do relevant details match the database? Are associated encounters, appointments, or vital-sign records visible where expected?

Record a few meaningful examples and limitations. Do **not** manually inspect thousands of records or treat a few screenshots as proof of full correctness.

## Part H — Show the Validator Detects a Defect (GREEN → RED → GREEN)

Complete `assignment-04/defect-injection.md`:

1. **GREEN:** validate known-valid synthetic data.
2. **RED:** intentionally introduce **one controlled defect** (e.g., duplicate ID, missing required value, orphan reference, invalid category, or inconsistent relationship).
3. **GREEN:** repair or regenerate the data and confirm validation passes again.

Document the defect, the evidence establishing why it is invalid, commands, outputs, and interpretation. A deliberate `RED` result is **successful testing evidence**. Leave the final submission in a valid state.

## Part I — Investigate Atomicity

Complete `assignment-04/atomicity-experiment.md`. Attempt a controlled multi-record operation in the isolated A4 environment with failure partway through. Explain:

1. What operation and records were intended?
2. Where/how was failure introduced, and what was predicted?
3. What records remained after the failure?
4. Did the operation behave atomically?
5. What SQL/output evidence supports your conclusion, and why would partial completion matter?

Do not run destructive experiments against the original course environment.

## Part J — Investigate Insertion Order and Referential Integrity

Complete `assignment-04/insertion-order-experiment.md`. Use the provided safe framework to attempt a dependent record before its expected parent.

Record the relationship, expected order, abnormal order, database response, semantic validator response, and conclusion. If SQL accepts an orphan or out-of-order row, explain why database acceptance alone is insufficient. Document any rollback or cleanup.

## Part K — Compare All Three Data Levels

Complete `assignment-04/scale-analysis.md` and implement a reproducible `assignment-04/scripts/benchmark.py` (or equivalent) to collect the results.

| Metric | Small | Medium | Large |
|---|---:|---:|---:|
| Patient count | | | |
| Encounter count | | | |
| Appointment count | | | |
| Vital-record count | | | |
| Generation time | | | |
| Load time | | | |
| Validation time | | | |
| Validation errors | | | |

Discuss scaling of related records, consistency of validation rules, resource limits, new errors at larger sizes, and which findings merit later performance testing.

**Do not claim rigorous scalability conclusions from a single run.** Proper performance experiments also consider repetitions, workload, warm-up, distributions, and other controls.

## Part L — Return to Your Assignment 2 Workflow

Investigate data concerns specific to your team's workflow:

- **Patient Registration:** identifiers, demographics, optional/required values, duplicates, and registration consistency.
- **Appointment Scheduling:** patient references, provider/facility/category relationships, date/time representations, status categories, and scheduling consistency.
- **Recording Vital Signs:** patient/encounter/form relationships, absent measurements, numeric representation, derived values, and supported range expectations.

Use system evidence for your expectations. Label unsupported domain rules as hypotheses rather than treating them as facts.

## Part M — Verify AI-Assisted Claims

If your team uses generative AI, complete `assignment-04/ai-verification-log.md` for **at least two substantive claims or suggestions**.

| AI claim / suggestion | How we verified it | Evidence | Accepted, modified, or rejected? |
|---|---|---|---|
| ... | ... | ... | ... |

A strong log may include a suggestion your team rejected after inspecting the actual system. Never submit private credentials, real patient data, or unverified AI assumptions as evidence.

## Required Deliverables

1. Data specification with evidence and assumptions.
2. Reproducible synthetic data generator/configuration for all three levels.
3. Data-quality validation plan and implemented tests.
4. Pre-load validation evidence for each level.
5. Controlled loading and post-load database evidence for each level.
6. Selected OpenEMR UI spot-check evidence.
7. Defect-injection **GREEN → RED → GREEN** report.
8. Atomicity experiment report.
9. Insertion-order/referential-integrity experiment report.
10. Three-level scale measurements, benchmark script, and analysis.
11. Workflow-specific data investigation.
12. AI Verification Log **if AI was used**.
13. Reproduction instructions, commands, and clearly stated limitations.

## Recommended Repository Structure

```text
assignment-04/
├── README.md
├── data-specification.md
├── validation-plan.md
├── defect-injection.md
├── atomicity-experiment.md
├── insertion-order-experiment.md
├── scale-analysis.md
├── ai-verification-log.md
├── scripts/
│   ├── generate_data.py
│   ├── validate_data.py
│   ├── load_data.py
│   └── benchmark.py
├── tests/
├── datasets/
│   └── README.md
└── results/
    ├── validation/
    └── benchmarks/
```

Place team-developed scripts and tests under `assignment-04/`. You may adapt the course-provided scripts from `environment/data-testing/scripts/` with attribution, but identify your team's own contributions. Use `datasets/README.md` to explain how to recreate the datasets, rather than committing generated patient CSVs.

## Evaluation

| Criterion | Points |
|---|---:|
| Data specification & reproducibility | **10** |
| Synthetic-data generation | **15** |
| Data-quality testing & validation | **20** |
| Loading & post-load verification | **10** |
| Controlled defect GREEN → RED → GREEN | **10** |
| Atomicity experiment | **10** |
| Insertion-order / integrity experiment | **10** |
| Three-level scale experiment & analysis | **10** |
| Evidence, communication & AI verification | **5** |
| **Total** | **100** |

You are evaluated on justified test rules, meaningful evidence, reproducibility, and your analysis—not on obtaining a particular execution time or making every experimental operation succeed.

## Use of Generative AI

You may use AI as an investigation and learning aid subject to the course policy—for example, to propose validation ideas, interpret error messages, or explain code. Your team remains responsible for checking those suggestions against evidence.

> **An AI-generated rule or test is not proof that an OpenEMR requirement exists.**

Verify rules with source, schema, observed behavior, or the explicit assignment specification; document at least two meaningful AI-assisted claims if AI was used.

## Submission

Work in your assigned private Project VITAL team repository. Before submitting, confirm that the required reports and code are committed; the standard datasets can be regenerated with seed `42`; deliberate defects have been repaired; tests and evidence are reproducible; and no real patient information, credentials, large generated datasets, or database dumps are committed.

Tag the completed submission:

```bash
git tag -a assignment-04 -m "Assignment 4 submission"
git push origin assignment-04
```

Submit your team repository reference and tag `assignment-04` through the LMS. **Do not submit a separate ZIP** unless your instructor requests one.

## Workflow Summary

```text
Review Assignment 2 workflow evidence
        ↓
Define and justify data-quality rules
        ↓
Generate small / medium / large synthetic fixtures
        ↓
Validate before loading
        ↓
Load in separate isolated A4 databases
        ↓
Verify database and UI observations
        ↓
Controlled defect: GREEN → RED → GREEN
        ↓
Atomicity + insertion-order investigations
        ↓
Compare 200 / 2,000 / 20,000 patients
        ↓
Interpret limitations and verify AI claims
        ↓
Tag assignment-04
```

## Final Perspective

A program can run successfully while operating on incorrect data. A database can accept a row while leaving the system in a semantically incorrect state. A validator can pass a small fixture while omitting important properties or assumptions.

Assignment 4 asks you to treat **data itself as a testable artifact**: specify its expected properties, investigate those properties with reproducible evidence, and explain what your results do—and do not—establish.
