# Assignment 4 — Data Testing: Quality, Integrity, and Scale

**Team Assignment | OpenEMR | Synthetic Data | Python | MariaDB**

**Due: Tuesday, October 20, 2026, at 11:59 PM ET**

## Purpose

In Assignment 1, you explored what OpenEMR does. In Assignment 2, you investigated how one workflow is implemented. In Assignment 3, you tested a small part of that implementation independently.

Assignment 4 asks a different question:

> **How can we determine whether the data used by and stored in a software system is correct, consistent, reproducible, and usable at different scales?**

You will generate **synthetic data only**, validate it before and after loading, deliberately introduce controlled data defects, investigate atomicity and insertion order, and compare the same data-testing pipeline at three standardized Project VITAL data levels.

The datasets created here are reusable Project VITAL test fixtures. Later assignments may use the same levels to investigate efficiency, latency, scalability, and reliability.

## Learning Objectives

By the end of this assignment, your team should be able to:

1. distinguish data testing from functional testing;
2. define testable data-quality properties;
3. generate reproducible synthetic relational data;
4. validate completeness, validity, uniqueness, consistency, and referential integrity;
5. distinguish database acceptance from semantically correct data;
6. verify loaded data with database evidence and selected UI observations;
7. demonstrate that a validator detects known defects;
8. investigate atomicity and insertion-order behavior;
9. compare data-testing behavior across dataset sizes;
10. document evidence, assumptions, uncertainty, and AI-assisted work.

# Standard Project VITAL Data Levels

| Level | Patients | Primary purpose in A4 |
|---|---:|---|
| **Small** | **200** | correctness, debugging, validation |
| **Medium** | **2,000** | comparison at moderate scale |
| **Large** | **20,000** | high-volume integrity and pipeline behavior |

Use seed **42** for submitted datasets. Course validation may use an alternate seed such as **314159**.

Running the generator twice with the same level and seed should produce equivalent dataset contents.

## Data Volume Is Not Workload

In A4 you vary **data volume**, not concurrency/load. A database containing 20,000 patients is not the same experiment as 20,000 simultaneous requests. Later assignments may combine dataset size with workload.

# Safety, Privacy, and Scope

Use **synthetic data only**. Do not use real patient information, real medical records, personally identifying information copied from real people, production OpenEMR systems, or institutional clinical systems.

Perform database experiments only in the isolated Project VITAL/OpenEMR environment.

# A4 Pipeline

```text
Define data properties
        ↓
Generate synthetic data
        ↓
Pre-load validation
        ↓
Load into isolated OpenEMR
        ↓
Post-load database validation
        ↓
Selected UI spot-checks
        ↓
Controlled defect injection
        ↓
Validator detects defect
        ↓
Repair
        ↓
Validation passes again
        ↓
Compare 200 / 2,000 / 20,000 patients
```

# Part A — Data Specification

Complete `assignment-04/data-specification.md`.

Identify:

- entities/tables represented;
- important fields;
- required versus optional fields;
- identifiers;
- relationships among records;
- categorical values;
- date/time relationships;
- domain constraints you intend to validate;
- which properties come from direct evidence and which are assumptions.

For important properties, identify evidence from the OpenEMR schema, source code, observed UI behavior, Assignment 2 evidence, or course specification. **AI-generated statements are not evidence.**

# Part B — Reproducible Synthetic Data Generation

Use the provided generation framework to support:

```text
small   → 200 patients
medium  → 2,000 patients
large   → 20,000 patients
```

The generator must accept a configurable seed.

The levels must not differ only in patient rows. Generate related synthetic records such as encounters, appointments, and vital-sign records according to the provided framework. Relationships must remain internally consistent except during controlled experiments.

Do **not** commit large generated datasets unless explicitly instructed. Your repository should contain the code/configuration needed to reproduce them from `generator + level + seed`.

# Part C — Data-Quality Test Plan

Complete `assignment-04/validation-plan.md`. Define properties **before** evaluating the datasets.

Your plan must include:

- **Completeness:** required identifiers/relationships/records are present.
- **Validity:** values have expected representations/types/categories and evidence-supported constraints.
- **Uniqueness:** values expected to be unique contain no unexpected duplicates.
- **Consistency:** related or derived values do not contradict one another.
- **Referential integrity:** dependent records reference appropriate existing parent records.

Do not assume a field must be unique or required because its name suggests it. Verify the requirement.

For each rule record:

| Property | Why it matters | Evidence for expected behavior | How it will be tested |
|---|---|---|---|

# Part D — Pre-Load Validation

Run the validator against each generated dataset before loading.

Record at least:

- level and seed;
- expected/actual patient count;
- related-record counts;
- rules executed;
- failures;
- overall result.

A successful generator run does **not** prove generated data is correct.

# Part E — Load into OpenEMR

Use the provided controlled loader. Do not manually create hundreds or thousands of records through the UI.

For each level record:

- records attempted;
- records successfully loaded;
- records rejected;
- load duration;
- unexpected warnings/errors.

# Part F — Post-Load Database Validation

After loading, verify the database contains what you intended. Check as appropriate:

- record counts;
- NULL/missing values;
- uniqueness;
- referential integrity;
- expected relationships;
- selected field values.

Do not conclude that data is correct merely because an INSERT succeeded. Distinguish **database acceptance** from **semantic validity**.

# Part G — UI Spot Checks

For each level, inspect a small sample through OpenEMR. Determine whether generated patients can be found, displayed information matches loaded data, related records appear where expected, and whether UI behavior differs from database expectations.

Do not manually inspect thousands of records. Provide a few meaningful examples.

# Part H — Controlled Defect Injection: GREEN → RED → GREEN

Document in `assignment-04/defect-injection.md`.

**GREEN:** validate a known-valid dataset.

**RED:** introduce one controlled defect, such as a duplicate identifier, missing required value, orphan record, invalid category, inconsistent relationship, or other evidence-supported invalid value. The validator should detect it.

**GREEN:** repair/regenerate the data and demonstrate validation passes again.

Record the defect, why it is invalid, evidence for that expectation, outputs before/after corruption and after repair, and what the experiment demonstrates.

> A RED result during this experiment is successful testing evidence.

# Part I — Atomicity Experiment

Document in `assignment-04/atomicity-experiment.md`.

Investigate a multi-record operation with a controlled failure partway through. Answer:

1. What operation was attempted?
2. What records were intended?
3. Where/how was failure introduced?
4. What did you predict?
5. What actually remained in the database?
6. Was the operation atomic?
7. What evidence supports the conclusion?
8. Why could partial completion matter?

# Part J — Insertion Order and Referential Integrity

Document in `assignment-04/insertion-order-experiment.md`.

Using the safe provided framework, attempt a controlled insertion-order violation, such as a dependent record before its expected parent.

Answer:

1. What relationship is being investigated?
2. What order is normally expected?
3. What abnormal order was attempted?
4. Did the database accept/reject it?
5. Did the semantic validator accept/reject the resulting state?
6. What does this reveal about relying only on database constraints?
7. What should testing check beyond SQL success/failure?

# Part K — Three-Level Scale Experiment

Run the supported pipeline for all three levels and complete `assignment-04/scale-analysis.md`.

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

Discuss whether rules behaved consistently, problems appeared only at larger volumes, related records scaled as expected, unexpected failures/resource issues occurred, and which observations deserve later performance investigation.

These times are **baseline observations, not rigorous performance benchmarks**. Do not claim scalability or poor performance from one run. Rigorous performance testing requires additional controls, repetitions, workload definitions, warm-up decisions, latency distributions, and other experimental considerations.

# Part L — Workflow-Specific Data Investigation

Return to your Assignment 2 workflow.

**Appointment Scheduling:** investigate patient references, provider/facility/category relationships, date/time representation, status/category values, and scheduling consistency.

**Vital Signs:** investigate patient/encounter/form relationships, missing measurements, numeric representation, related/derived values, and evidence-supported validation/range behavior.

**Patient Registration:** investigate identifiers, demographics, missing values, duplicates, uniqueness assumptions, and registration consistency.

Do not invent domain rules. Every expectation must be supported by evidence or labeled as a hypothesis.

# Part M — AI Verification Log

If generative AI is used, maintain `assignment-04/ai-verification-log.md`.

For at least **two substantive AI-assisted claims or suggestions**, record:

| AI suggestion/claim | How verified | Evidence | Accepted, modified, or rejected? |
|---|---|---|---|

Claims requiring verification include statements such as "this field is required," "this column is unique," "this relationship has a foreign key," or "this range is invalid."

A strong log may include an AI suggestion that was rejected or corrected after examining the actual system.

# Required Deliverables

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

**Starter infrastructure:** The course repository provides `generate_data.py`, `validate_data.py`, and `load_data.py` under `environment/data-testing/scripts/`. These are starting points, not completed student deliverables. Document any adaptations and implement the additional validation, testing, and analysis required by this assignment.

**Benchmarking:** Develop your own `assignment-04/scripts/benchmark.py` (or an equivalent reproducible benchmark tool) to measure and record the required scale experiments.

**Submission:** Place your team-developed scripts and tests under `assignment-04/` in your team repository. You may reuse the provided starter scripts with attribution, but identify what your team added or modified. Do not commit generated patient datasets, credentials, or database dumps. Use `datasets/README.md` to document how to reproduce datasets.

The provided infrastructure may add supporting files.

# Required Evidence

Include enough evidence to reproduce and evaluate your conclusions:

- commands used;
- dataset level and seed;
- generated record counts;
- validation results;
- relevant database queries/results;
- selected UI evidence;
- GREEN → RED → GREEN evidence;
- atomicity evidence;
- insertion-order evidence;
- three-level scale results;
- uncertainties and limitations.

Prefer concise, meaningful evidence over large screenshot collections.

# Evaluation Rubric

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

Strong work defines properties before testing, distinguishes evidence from assumptions, generates reproducibly, validates relationships rather than only counts, proves validators can detect controlled defects, combines database/application evidence, interprets unexpected results, avoids unsupported medical assumptions, distinguishes data volume from workload, and documents uncertainty.

You are not graded on obtaining a particular runtime or making every experiment pass.

# Repository Workflow and Submission

Work in your assigned private Project VITAL team repository. Start with:

```bash
git pull
```

Commit meaningful units of work. Do not commit secrets, local environment configuration, unintended database dumps, real data, or generated large datasets.

Before submission:

1. ensure required files are present;
2. regenerate standard datasets with seed `42`;
3. verify required experiments;
4. confirm the documented final state is reproducible;
5. confirm no real patient information is present;
6. review the AI verification log;
7. commit and push required work.

Create the submission tag:

```bash
git tag -a assignment-04 -m "Assignment 4 submission"
git push origin assignment-04
```

After pushing your work and the `assignment-04` tag, submit your team repository reference and submission tag through the LMS. Do not upload a separate ZIP unless your instructor specifically requests one.

# Final Perspective

A program can execute successfully while operating on incorrect data.

A database can accept a row while the resulting state is semantically wrong.

A validator can pass a small dataset and still contain assumptions that fail at larger scales.

Assignment 4 therefore asks you to treat **data itself as a testable artifact**.

The goal is not merely to create 20,000 synthetic patients. The goal is to build evidence that the data and its relationships satisfy clearly defined properties—and to understand the limits of that evidence.
