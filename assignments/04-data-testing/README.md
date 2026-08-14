# Project VITAL

## Assignment 4 — Data Testing: Synthetic Data, Integrity, Scale, and Privacy

**Team Assignment | OpenEMR | Python | MariaDB**

---

## Purpose

Software testing depends on data.

A test suite may be well designed and still provide poor evidence if the data used to exercise the system is unrealistic, inconsistent, irreproducible, incomplete, or unsafe.

In this assignment, your team will design and evaluate a **synthetic test-data pipeline** for OpenEMR.

You will move beyond manually creating a few records through the user interface and investigate questions such as:

> How do we create enough realistic data to test the system systematically?

> How do we preserve relationships between records?

> How do we know that the data generator itself is correct?

> How do we reproduce a failing dataset?

> How should privacy and anonymization influence test-data design?

The assignment emphasizes an important idea:

> **Test data is part of the testing system and must itself be tested.**

---

# Learning Objectives

By the end of this assignment, you should be able to:

1. **Design synthetic test data** that reflects realistic entities, relationships, constraints, and edge cases.
2. **Generate data reproducibly** using scripts, configuration, and deterministic random seeds.
3. **Validate data integrity**, including required fields, uniqueness, referential integrity, ranges, and domain constraints.
4. **Reason about insertion order and atomicity** when loading related data into a relational system.
5. **Evaluate system behavior at multiple data scales** using small, medium, and high-volume datasets.
6. **Distinguish anonymization, pseudonymization, and synthetic data** and explain when each is appropriate for testing.

---

# Team and Time Expectations

Work with your Project VITAL team unless your instructor specifies otherwise.

Plan for approximately **4–6 hours of team work outside class**, in addition to guided in-class activities.

All team members should contribute meaningfully to some combination of:

- data-model analysis;
- generator design;
- implementation;
- validation;
- scale testing;
- privacy/anonymization analysis;
- interpretation of results.

---

# Important Data Rule

Project VITAL uses **synthetic data only**.

Do not use:

- real patient data;
- your own medical information;
- information about classmates, friends, or family members;
- real names combined with real contact or medical information;
- exported healthcare records from external systems.

The goal is to create data that is **useful for testing without representing real people**.

---

# Part A — Define the Data Model You Need

Return to your Assignment 2 ERD and architecture work.

Select the portion of the OpenEMR data model needed to support a meaningful testing dataset.

At minimum, your dataset should include a central entity such as a **patient** and at least **two related entity types**.

Depending on your approved scope, examples may include:

```text
Patient
   │
   ├── Appointment
   │
   └── Encounter
          │
          ├── Vitals
          └── Problem / Diagnosis
```

Your exact entities should reflect the OpenEMR version used by Project VITAL.

Document:

- entities/tables involved;
- primary keys;
- foreign keys;
- required fields;
- important uniqueness constraints;
- meaningful domain constraints;
- insertion dependencies.

---

# Part B — Create a Data Dependency / Insertion-Order Plan

Before writing a generator, determine the order in which related records can safely be created.

For example:

```text
Provider
   │
   └──────┐
          ▼
Patient → Appointment

Patient
   │
   ▼
Encounter
   │
   ▼
Vitals
```

If a record requires a foreign key to another record, the referenced record generally needs to exist first.

Create an **Insertion-Order Plan** that identifies:

| Step | Entity | Depends On | Why |
|---|---|---|---|
| 1 | Patient | — | Central record must exist first |
| 2 | Encounter | Patient | Requires patient identifier |
| 3 | Vitals | Encounter | Must belong to an encounter |

Your actual plan must be based on the data model you investigate.

---

# Part C — Design the Synthetic Data Generator

Implement a script or small tool that generates synthetic test data.

**Python is recommended** unless your instructor approves another language.

The generator should support three dataset sizes:

| Level | Minimum Scale |
|---|---:|
| **Small** | 200 primary objects/users/patients |
| **Medium** | 2,000 primary objects/users/patients |
| **High** | 20,000 primary objects/users/patients |

The exact number of dependent records may vary according to your data model.

For example, 200 patients may generate substantially more than 200 total database rows because each patient may have appointments, encounters, or other related data.

---

# Part D — Reproducibility

Your generator must support a deterministic **random seed**.

Conceptually:

```bash
python generate_data.py --size small --seed 42
```

Running the generator again with the same:

```text
size + configuration + seed
```

should produce the same logical dataset.

Demonstrate:

```text
Run 1
seed = 42
    │
    ▼
Dataset A

Run 2
seed = 42
    │
    ▼
Dataset A
```

Then demonstrate that a different seed produces a different dataset:

```text
seed = 99
    │
    ▼
Dataset B
```

Explain why reproducibility is important when diagnosing test failures.

---

# Part E — Transparency

Your generator must make its behavior understandable.

Avoid a tool that simply produces thousands of records without explaining how they were constructed.

Document:

- entities generated;
- approximate number of each entity;
- value distributions;
- assumptions;
- allowed ranges;
- relationships;
- seed;
- generation order;
- any intentionally generated edge cases.

The generator should produce a concise summary such as:

```text
Generation Summary

Seed: 42
Patients: 200
Appointments: 318
Encounters: 267
Vitals records: 251

Edge cases generated:
- 4 patients near age boundary
- 3 names containing punctuation
- 5 appointments at schedule boundaries
```

The exact output format is your choice.

---

# Part F — Data Validation

Do not assume that because your generator ran successfully, its output is correct.

Create automated validation checks for the generated data.

At minimum, test the following categories where relevant:

## 1. Completeness

Required fields contain values.

Examples:

```text
Patient identifier is present
Required date is present
Required relationship is present
```

## 2. Uniqueness

Values that should be unique do not contain unintended duplicates.

## 3. Referential Integrity

Every foreign-key-like relationship references a valid parent record.

For example:

```text
Every encounter references an existing patient.
```

## 4. Domain / Range Validation

Values fall within your intended rules.

Examples might include:

```text
valid date ranges
allowed categorical values
nonnegative measurements
configured identifier formats
```

## 5. Relationship Validation

Generated records have plausible relationships.

For example:

```text
Encounter belongs to the intended patient
Vitals belong to the intended encounter
Appointment refers to an existing patient/provider
```

## 6. Volume Validation

The generated dataset contains the expected number of primary records.

---

# Part G — Intentionally Break the Data

A validation system should detect bad data.

Create at least **three controlled data defects**.

Examples:

- remove a required field;
- create a duplicate value where uniqueness is expected;
- reference a nonexistent parent record;
- create an invalid date relationship;
- insert a value outside an intended range.

Run your validators and demonstrate that they detect the problems.

Then restore valid data.

The required evidence is:

```text
VALID DATA
     ↓
validation passes
     ↓
introduce controlled defect
     ↓
validation fails
     ↓
repair data
     ↓
validation passes
```

Do not leave intentionally corrupted data in your final dataset.

---

# Part H — Atomicity

Consider what should happen if data loading fails partway through an operation.

For example:

```text
Create patient         ✓
Create encounter       ✓
Create vitals          ✗

What should remain?
```

Investigate how your data-loading approach handles partial failure.

Design at least one experiment in which a multi-record load fails intentionally.

Document:

1. Which records were supposed to be created.
2. Where the failure occurred.
3. What records remained after failure.
4. Whether the behavior is acceptable.
5. Whether a transaction or rollback strategy would improve the process.

The goal is to understand:

> **A data-generation script that stops halfway through may leave the test environment in a state that invalidates later test results.**

---

# Part I — Insertion Order

Perform one controlled experiment using an incorrect insertion order.

For example, attempt to create a dependent record before the required parent record.

Record:

- operation attempted;
- observed behavior;
- error or constraint response;
- effect on the database;
- what this reveals about the data model.

Then document the correct insertion order.

---

# Part J — Load the Small Dataset

Generate and load the **Small** dataset.

Target:

```text
200 primary objects
```

Record:

- seed;
- number of records generated;
- generation time;
- load time;
- validation result;
- any errors;
- approximate total number of related records.

After loading, use the OpenEMR user interface to manually inspect a small sample.

Verify that generated data can be found and interpreted through the application, not only in the database.

---

# Part K — Load the Medium Dataset

Generate and load:

```text
2,000 primary objects
```

Record the same measurements:

- generation time;
- load time;
- validation time;
- observed problems;
- application behavior.

Compare the experience with the Small dataset.

---

# Part L — Load the High Dataset

Generate and load:

```text
20,000 primary objects
```

Record:

- generation time;
- load time;
- validation time;
- errors;
- application behavior;
- resource or performance observations.

This is **not yet a formal performance-testing assignment**.

Your goal is to observe whether increased data volume reveals:

- assumptions;
- failures;
- impractical generation strategies;
- validation bottlenecks;
- UI/search issues;
- data-management problems.

Do not perform denial-of-service or uncontrolled stress testing.

---

# Part M — Compare the Three Levels

Create a comparison table.

| Metric | Small | Medium | High |
|---|---:|---:|---:|
| Primary records | 200 | 2,000 | 20,000 |
| Generation time | | | |
| Load time | | | |
| Validation time | | | |
| Errors | | | |
| Key observation | | | |

Then answer:

1. Did generation/load time scale approximately as expected?
2. What became harder as the dataset grew?
3. Did any assumptions work at 200 records but fail at 20,000?
4. What would you change before generating 200,000 records?
5. Which observations belong to data testing versus future performance testing?

---

# Part N — Privacy, Anonymization, and Pseudonymization

Even though Project VITAL uses synthetic data, you must understand how real datasets would need to be handled.

Briefly explain the distinction among:

### Synthetic data

Records are generated and do not represent actual individuals.

### Pseudonymized data

Direct identifiers are replaced, but the data may still be linkable to an individual using additional information.

### Anonymized data

Data is transformed so that individuals cannot reasonably be identified, subject to the applicable definition/policy.

---

# Part O — Design an Anonymization Plan

Assume you were given an **authorized healthcare-like dataset** for testing.

Do **not** actually obtain or use such a dataset.

Create a conceptual anonymization plan for fields such as:

| Field | Proposed Treatment | Reason |
|---|---|---|
| Name | Replace | Direct identifier |
| Email | Replace/remove | Direct identifier |
| Phone | Replace/remove | Direct identifier |
| Address | Generalize/remove | Location identifier |
| DOB | Generalize or transform | Re-identification risk |
| Record ID | Pseudonymize | Preserve relationships without original identifier |
| Encounter dates | Shift consistently | Preserve relative timing while reducing identifiability |
| Diagnosis | Evaluate/retain as appropriate | Needed for testing but may contribute to re-identification |

Your plan should preserve enough structure to support useful testing while reducing privacy risk.

---

# Part P — Test the Generator Itself

Your synthetic data generator is software.

Create automated tests for it.

At minimum, test:

- deterministic output from a fixed seed;
- correct requested record count;
- valid relationships;
- configured ranges;
- invalid configuration handling;
- one important edge case.

This is a continuation of Assignment 3:

> **The test-data tool also requires tests.**

---

# Part Q — Continuous Data Validation

Extend your CI approach so that a **small data-generation/validation check** can run automatically.

Do **not** generate the 20,000-record dataset on every push unless your instructor explicitly requires it.

A sensible CI strategy is:

```text
EVERY PUSH / PULL REQUEST
        │
        ▼
Generate small deterministic sample
        │
        ▼
Run data validators
        │
        ├── PASS → GREEN
        └── FAIL → RED
```

The medium/high datasets may be run manually or at selected milestones.

Document which data tests belong in continuous testing and which are too expensive for every commit.

---

# Required Deliverables

Submit one team package containing:

1. **Focused Data Model**
   - entities;
   - primary/foreign keys;
   - required fields;
   - important constraints.

2. **Insertion-Order Plan**

3. **Synthetic Data Generator**
   - source code;
   - configuration;
   - seed support.

4. **Generator Documentation**
   - assumptions;
   - distributions;
   - edge cases;
   - transparency summary.

5. **Automated Data Validators**

6. **Controlled Bad-Data Experiments**
   - at least three intentionally introduced defects;
   - validator evidence.

7. **Atomicity Experiment**

8. **Incorrect Insertion-Order Experiment**

9. **Small Dataset Results**
   - 200 primary records.

10. **Medium Dataset Results**
    - 2,000 primary records.

11. **High Dataset Results**
    - 20,000 primary records.

12. **Scale Comparison Table and Analysis**

13. **Privacy / Data Handling Analysis**
    - synthetic vs. pseudonymized vs. anonymized;
    - conceptual anonymization plan.

14. **Tests for the Data Generator**

15. **Continuous Data Validation**
    - CI configuration or extension;
    - evidence of passing validation;
    - explanation of what runs continuously versus manually.

16. **AI Verification Log**
    - required if generative AI was used.

---

# Recommended Repository Structure

```text
VITAL-Team-XX/
│
├── assignment-04/
│   ├── README.md
│   ├── data-model.md
│   ├── insertion-order.md
│   ├── scale-results.md
│   ├── privacy-analysis.md
│   ├── atomicity.md
│   ├── ai-verification-log.md
│   │
│   ├── generator/
│   │   ├── generate_data.py
│   │   └── ...
│   │
│   ├── validators/
│   │   └── ...
│   │
│   ├── tests/
│   │   └── ...
│   │
│   └── evidence/
│
└── .github/
    └── workflows/
        └── ...
```

Do not commit large generated datasets unless the instructor explicitly requires them.

Prefer committing:

```text
generator + seed + configuration
```

rather than:

```text
20,000 generated records
```

when the data can be reproduced.

---

# Evaluation

| Criterion | Weight | Evidence of Strong Work |
|---|---:|---|
| **Data model and insertion-order analysis** | 15% | Accurate focused model, dependencies, constraints, and creation order |
| **Synthetic data generator design** | 20% | Reproducible, transparent, configurable, appropriate synthetic data |
| **Data validation and controlled defects** | 20% | Strong automated validators that detect intentionally corrupted data |
| **Atomicity and insertion-order experiments** | 10% | Evidence-based analysis of partial failure, ordering, and data consistency |
| **Small / Medium / High scale testing** | 15% | Correct generation, measurement, comparison, and thoughtful interpretation |
| **Privacy and anonymization analysis** | 10% | Clear distinction among data approaches and appropriate conceptual handling plan |
| **Generator tests + continuous validation** | 10% | Generator is itself tested and appropriate small validation runs automatically |
| **Total** | **100%** | |

---

# Use of Generative AI

Generative AI may be used as an investigation and development aid subject to the course AI policy.

Possible uses include:

- proposing synthetic-data schemas;
- suggesting edge cases;
- helping implement generation scripts;
- suggesting validation rules;
- explaining database constraints;
- helping diagnose generator failures.

However:

> **AI-generated synthetic data is not automatically valid, realistic, safe, or useful for testing.**

Your team must verify:

- field constraints;
- relationships;
- uniqueness;
- required values;
- distributions;
- reproducibility;
- privacy assumptions;
- generated edge cases.

Never provide real patient data or protected information to an AI system.

---

# AI Verification Log

If AI is used, document at least **two meaningful AI suggestions**.

| AI Suggestion | How We Verified It | Result |
|---|---|---|
| Suggested insertion order | Compared with schema/foreign keys and tested loading | Confirmed / Modified / Rejected |
| Suggested data rule | Compared with application/data behavior | Confirmed / Modified / Rejected |

At least one entry should demonstrate meaningful verification or correction.

---

# Submission

Submit according to the **Project VITAL Student Submission Guide**.

Required tag:

```text
assignment-04
```

Before creating the tag, confirm:

- required source files and reports are committed;
- generated data is reproducible from documented configuration/seed;
- no real patient data is present;
- no credentials or `.env` files are committed;
- deliberately corrupted datasets are not the final active dataset;
- CI/data validation is green;
- large generated artifacts are excluded unless specifically required.

Create and push:

```bash
git tag assignment-04
git push origin assignment-04
```

Submit the repository reference and `assignment-04` tag through the LMS.

---

# Assignment 4 Workflow Summary

```text
Understand data model
        ↓
Define insertion order
        ↓
Design synthetic generator
        ↓
Make generation reproducible
        ↓
Validate generated data
        ↓
Break data intentionally
        ↓
VALID → INVALID → VALID
        ↓
Investigate atomicity/order
        ↓
Generate 200
        ↓
Generate 2,000
        ↓
Generate 20,000
        ↓
Compare scale behavior
        ↓
Analyze privacy/anonymization
        ↓
Test the generator
        ↓
Add continuous data validation
        ↓
Tag assignment-04
```

---

# Looking Ahead

Project VITAL has now progressed through:

```text
SYSTEM EXPLORATION
        ↓
SYSTEM ARCHITECTURE
        ↓
UNIT TESTING + CI
        ↓
DATA TESTING
```

You have tested individual code behavior and now the data that drives the system.

Later assignments will expand into broader quality dimensions such as:

```text
INTEGRATION / SYSTEM TESTING
ACCESSIBILITY
SECURITY
ACCEPTANCE
```

The same principle remains:

> **Testing is not only about whether code executes. It is about whether the complete system — including its data — behaves in a trustworthy, reproducible, and explainable way.**
