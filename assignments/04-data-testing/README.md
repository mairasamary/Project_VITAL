# Assignment 4 --- Data Testing and Continuous Data Validation

## Project VITAL

### Overview

Modern software systems depend not only on correct code, but also on
correct data. A system can execute without crashing and still behave
incorrectly because its data is incomplete, inconsistent, duplicated,
incorrectly related, or loaded in an unsafe way.

In this assignment, your team will test the data pipeline used with the
Project VITAL OpenEMR environment. You will work with **synthetic
patient data only** and investigate data quality at several stages:

``` text
Synthetic Data Generation
          ↓
Intermediate Data Validation
          ↓
Controlled Defect Injection
          ↓
Transactional Database Loading
          ↓
OpenEMR Database Validation
          ↓
Scale Testing
          ↓
Continuous Data Validation (CI)
```

This assignment is not simply about loading records into a database.
Your goal is to determine whether the data pipeline behaves correctly,
whether invalid data is detected, whether failures leave the database in
a safe state, and how the pipeline behaves as the amount of data
increases.

------------------------------------------------------------------------

## Learning Objectives

By completing this assignment, you should be able to:

1.  distinguish code testing from data testing;
2.  identify important data-quality properties;
3.  reason about relationships between data entities;
4.  design positive and negative data tests;
5.  use deterministic synthetic data for reproducible testing;
6.  test database loading and transactional behavior;
7.  distinguish database constraints from application-level or semantic
    validation;
8.  evaluate data behavior at increasing scales;
9.  interpret timing measurements rather than merely report them;
10. incorporate lightweight data validation into Continuous Integration;
11. use CI failures as evidence about software behavior; and
12. communicate test results, limitations, and remaining risks.

------------------------------------------------------------------------

# 1. Rules and Safety

## 1.1 Synthetic Data Only

You must use **only synthetic data** generated for Project VITAL.

Do **not** use:

-   real patient information;
-   personal health information;
-   data copied from an actual medical record;
-   personally identifiable information belonging to a real person.

The provided generator creates artificial records specifically for this
assignment.

## 1.2 Work Only in the Local Project VITAL Environment

All database-loading experiments must use the local Docker-based OpenEMR
environment supplied for Project VITAL.

Do not run these experiments against any production, institutional,
clinical, or externally hosted OpenEMR database.

## 1.3 Preserve Evidence

Testing is about evidence. Keep useful records of:

-   commands executed;
-   validation output;
-   CI runs;
-   controlled failures;
-   timing results;
-   screenshots where appropriate;
-   observations made in OpenEMR.

Do not submit thousands of generated records to Git.

------------------------------------------------------------------------

# 2. Infrastructure Provided to You

Project VITAL provides infrastructure for generating, validating,
loading, resetting, and benchmarking synthetic data.

The exact files available in your semester repository may include tools
such as:

``` text
environment/data-testing/
```

with scripts for:

-   synthetic-data generation;
-   intermediate validation;
-   controlled corruption;
-   OpenEMR loading;
-   post-load validation;
-   resetting Project VITAL batches;
-   benchmarking;
-   local CI checks.

You are expected to **understand what these tools are testing and
interpret their results**.

A successful assignment is not demonstrated by simply running every
provided command and reporting that it passed.

------------------------------------------------------------------------

# 3. Your Responsibilities

Your team is responsible for:

-   understanding the relevant OpenEMR data model;
-   identifying important data-quality properties;
-   executing and extending the provided tests;
-   designing meaningful negative tests;
-   predicting expected behavior before experiments;
-   investigating unexpected behavior;
-   collecting evidence;
-   interpreting scale results;
-   demonstrating continuous data validation;
-   explaining limitations and remaining risks.

When a test fails unexpectedly, investigate it. An unexpected failure
can be valuable testing evidence.

------------------------------------------------------------------------

# 4. Part A --- Understand the Data Model

Before loading data, investigate the OpenEMR structures involved in this
assignment.

The Project VITAL dataset focuses on three conceptual entities:

-   patients;
-   encounters;
-   vitals.

However, the database representation may require additional
relationships for OpenEMR to recognize records correctly.

Use the schema-inspection material supplied with the environment and
examine the relevant structures.

At minimum, investigate the roles of:

``` text
patient_data
form_encounter
form_vitals
forms
```

## Questions to Answer

In your report, explain:

1.  How is a patient identified?
2.  How is an encounter connected to a patient?
3.  How are vitals connected to an encounter?
4.  What role does the `forms` table play?
5.  Which relationships appear to be enforced directly by the database?
6.  Which relationships may require semantic/application-level
    validation?
7.  What could go wrong if records are inserted in an incorrect order?

Include a small relationship diagram. It does not need to represent the
entire OpenEMR schema---only the portion relevant to this assignment.

------------------------------------------------------------------------

# 5. Part B --- Deterministic Synthetic Data

Generate a small synthetic dataset using the Project VITAL generator.

Use the commands documented in:

``` text
environment/data-testing/
```

Use a fixed seed so your experiment is reproducible.

## Inspect the Output

Examine:

``` text
patients.csv
encounters.csv
vitals.csv
manifest.json
```

Do not merely open the files. Determine what properties should hold.

Examples include:

-   expected record counts;
-   unique patient identifiers;
-   valid dates;
-   required values;
-   encounters referencing existing patients;
-   vitals referencing valid encounters;
-   plausible field ranges;
-   deterministic output for a fixed seed.

## Reproducibility Experiment

Generate the same dataset twice using the same seed.

Then generate another dataset using a different seed.

Explain:

-   what remained identical;
-   what changed;
-   why deterministic generation is useful in testing.

------------------------------------------------------------------------

# 6. Part C --- Intermediate Data Validation

Before data reaches OpenEMR, validate the generated dataset.

Run the provided intermediate validator.

A valid dataset should report:

``` text
VALIDATION PASSED
```

## Your Task

Identify the categories of defects that the validator checks.

Create a table in your report similar to:

  Property                 Why It Matters   How It Is Tested   Expected Failure
  ------------------------ ---------------- ------------------ ------------------
  Patient ID uniqueness    ...              ...                ...
  Encounter relationship   ...              ...                ...
  Vitals relationship      ...              ...                ...

Do not limit your discussion to the examples above.

------------------------------------------------------------------------

# 7. Part D --- Negative Data Testing

Testing only valid input is insufficient.

Use the supplied corruption mechanism where appropriate and design
controlled defects that should make a dataset invalid.

Test **at least three distinct defect categories**.

At least one must involve a relationship between entities.

Possible categories include:

-   duplicate identifiers;
-   missing required data;
-   invalid values;
-   orphan encounters;
-   orphan vitals;
-   inconsistent relationships;
-   invalid ranges.

The exact tests should be based on the behavior of the provided Project
VITAL environment.

## For Each Negative Test

Document:

1.  the property being tested;
2.  your prediction;
3.  the defect introduced;
4.  the validator result;
5.  whether the result matched your prediction;
6.  what risk the test represents.

A negative test is successful when invalid data is **correctly
rejected**.

------------------------------------------------------------------------

# 8. Part E --- Database Loading and Transaction Testing

After intermediate data passes validation, test loading it into the
local OpenEMR database.

Use a unique Project VITAL batch name for your experiment.

Follow the loader documentation supplied in:

``` text
environment/data-testing/
```

The loader should validate the intermediate dataset before modifying the
database.

## 8.1 Successful Transaction

Load a valid dataset.

Record:

-   batch name;
-   number of patients;
-   number of encounters;
-   number of vitals;
-   assigned identifier ranges;
-   whether the transaction committed.

Then run the post-load validator.

A successful batch should report:

``` text
BATCH VALID
```

## 8.2 Atomicity / Rollback Experiment

Test what happens when a load fails during a transaction.

Your goal is to determine whether the database is left with a **partial
batch**.

Record:

-   what failure was introduced;
-   what you predicted;
-   whether the transaction rolled back;
-   how many records from the failed batch remained afterward.

Explain why partial loading would be dangerous.

## 8.3 Insertion-Order / Relationship Experiment

Investigate what happens when a dependent record is inserted before the
record it logically depends on.

Do not assume that the database will reject the operation.

Compare:

> **database acceptance**

with:

> **semantic correctness**

Explain what your experiment reveals about relying exclusively on
database constraints.

## 8.4 Duplicate Batch / Collision Protection

Investigate how the loader protects existing Project VITAL data.

Explain:

-   why batch identifiers must be unique;
-   why identifier collisions matter;
-   what should happen if a previously used batch name is reused;
-   why multiple valid Project VITAL batches should be able to coexist.

------------------------------------------------------------------------

# 9. Part F --- Verify the Data in OpenEMR

Database queries alone are not enough.

For at least one successfully loaded dataset, interact with OpenEMR
through the application UI.

Locate synthetic records and verify that representative data appears
where expected.

Check examples from more than one entity type where possible.

Record:

-   what you searched for;
-   what you found;
-   whether the UI representation agreed with the generated data;
-   any behavior that surprised you.

Include limited screenshots as evidence. Do not fill the report with
repetitive screenshots.

------------------------------------------------------------------------

# 10. Part G --- Scale Testing

You will now investigate the same pipeline at increasing data scales.

The standard Project VITAL scales are:

  Scale      Approximate Patients
  -------- ----------------------
  Small                       200
  Medium                    2,000
  High                     20,000

The exact encounter and vitals counts depend on the seed and generator.

Use the benchmark utility documented in:

``` text
environment/data-testing/BENCHMARKING.md
```

Validate the scales in this order:

``` text
Small → Medium → High
```

Do not begin with the high-volume experiment.

## Measurements

For each scale, collect:

-   patient count;
-   encounter count;
-   vitals count;
-   generation time;
-   intermediate-validation time;
-   database-load time;
-   post-load database-validation time.

The benchmark produces local CSV and Markdown results. These generated
benchmark artifacts should normally remain outside Git.

## Important

This is a **scale experiment**, not a formal performance benchmark.

Timing depends on:

-   your computer;
-   Docker resources;
-   storage;
-   operating system;
-   existing database state;
-   caching;
-   background activity.

You are not graded on achieving a particular number of seconds.

You are graded on the quality of your analysis.

## Analysis Question

Answer:

> Which stage scaled most noticeably as the dataset increased:
> generation, intermediate validation, database loading, or post-load
> validation? What evidence supports your conclusion?

Also discuss whether all pipeline stages scaled in the same way.

------------------------------------------------------------------------

# 11. Part H --- Continuous Data Validation

Some data tests should execute automatically whenever software changes.

However, not every test belongs in Continuous Integration.

Project VITAL's CI deliberately uses a **small deterministic dataset**
rather than loading 20,000 patients into OpenEMR on every push.

Read:

``` text
environment/data-testing/CI_DATA_TESTING.md
```

Install/use the data-testing workflow according to the repository
instructions.

The workflow should test lightweight properties such as:

-   generator tests;
-   deterministic generation;
-   intermediate validation;
-   reproducibility;
-   rejection of controlled invalid data.

## Explain the CI Boundary

In your report, answer:

> Why do we run lightweight data tests on every push but keep the
> OpenEMR database loads and large-scale experiments outside the normal
> CI workflow?

Your answer should discuss feedback speed, cost, test purpose, and
frequency.

------------------------------------------------------------------------

# 12. Part I --- GREEN → RED → GREEN

You must demonstrate that CI is capable of detecting a real failure.

A green workflow alone does not prove that the tests are useful.

Use a separate experiment branch and create **one controlled, reversible
defect**.

The required sequence is:

``` text
Correct system
     ↓
GREEN
     ↓
Controlled defect
     ↓
RED
     ↓
Restore correct behavior
     ↓
GREEN
```

## Required Evidence

Record:

-   the original successful CI run;
-   the controlled change;
-   the failed CI run;
-   the step that detected the failure;
-   the relevant failure message;
-   the restoration commit;
-   the final successful run.

Do not introduce meaningless syntax errors merely to make CI red. The
failure should demonstrate that a test or validator detects incorrect
behavior.

Do not merge the intentionally broken state into the semester's stable
branch.

------------------------------------------------------------------------

# 13. Part J --- Engineering Analysis

Conclude your report by answering the following.

### Data Quality

Which data-quality properties were most important in this system, and
why?

### Constraints vs. Validation

What did you learn about the difference between database constraints and
semantic/application-level validation?

### Transactions

What risk is addressed by transactional loading?

### Negative Testing

Which negative test provided the most useful information?

### Scale

What changed as the dataset grew? What did not change as much as you
expected?

### Continuous Testing

Which tests belong in CI? Which should remain milestone/manual tests?

### Remaining Risk

Identify at least **three important data risks that this assignment does
not fully test**.

For each risk, propose a future test.

------------------------------------------------------------------------

# 14. Deliverables

Submit the assignment using the Project VITAL submission process
documented for the course.

Your repository must contain a clearly organized Assignment 4
submission.

## Required Deliverables

### A. Data Testing Report

A Markdown report containing:

-   data-model analysis;
-   relationship diagram;
-   intermediate-validation analysis;
-   negative-test design and results;
-   transaction/rollback findings;
-   insertion-order findings;
-   OpenEMR UI verification;
-   scale results;
-   benchmark interpretation;
-   CI analysis;
-   GREEN → RED → GREEN evidence;
-   remaining risks and proposed future tests.

### B. Test/Code Changes

Include any tests or code your team was responsible for adding or
modifying.

Do not submit generated high-volume datasets unless explicitly
instructed.

### C. Evidence

Include concise evidence such as:

-   selected command output;
-   benchmark table;
-   GitHub Actions run references/screenshots;
-   selected OpenEMR screenshots;
-   commit identifiers where useful.

### D. Team Contribution Statement

Briefly state what each team member contributed.

------------------------------------------------------------------------

# 15. Suggested Report Organization

You may use the following structure:

``` text
1. Data Model
2. Data-Quality Properties
3. Deterministic Generation
4. Intermediate Validation
5. Negative Tests
6. Database Loading
7. Transaction / Rollback Experiment
8. Insertion-Order Experiment
9. OpenEMR Verification
10. Scale Experiment
11. Continuous Data Validation
12. GREEN → RED → GREEN Experiment
13. Remaining Risks
14. Team Contributions
```

------------------------------------------------------------------------

# 16. Evaluation

The assignment is evaluated primarily on **testing reasoning, evidence,
and analysis**, not on whether every command prints `PASSED`.

  -----------------------------------------------------------------------
  Category                                                         Weight
  ------------------------------ ----------------------------------------
  Data-model understanding and                                        15%
  identification of data risks   

  Intermediate validation and                                         15%
  data-quality reasoning         

  Negative-test design and                                            15%
  analysis                       

  Database, transaction,                                              20%
  relationship, and OpenEMR      
  testing                        

  Scale experiment and                                                15%
  interpretation                 

  Continuous data validation and                                      15%
  GREEN → RED → GREEN evidence   

  Report quality, evidence,                                            5%
  reproducibility, and team      
  contribution statement         

  **Total**                                                      **100%**
  -----------------------------------------------------------------------

## What Strong Work Looks Like

Strong submissions:

-   make predictions before experiments;
-   explain why each test matters;
-   distinguish expected failures from infrastructure errors;
-   investigate surprising results;
-   connect failures to realistic system risks;
-   use evidence selectively;
-   interpret timing rather than merely listing numbers;
-   distinguish database integrity from semantic correctness;
-   explain why different tests run at different frequencies;
-   identify meaningful limitations.

## What Is Not Sufficient

The following by themselves do not demonstrate completion:

``` text
"We ran the script and it passed."

"The CI check was green."

"20,000 patients loaded successfully."

"The validator found no errors."
```

Each result must be interpreted in terms of the property being tested
and the evidence it provides.

------------------------------------------------------------------------

# 17. Submission Checklist

Before submitting, confirm that your team has:

-   [ ] used synthetic data only;
-   [ ] explained the relevant OpenEMR data relationships;
-   [ ] demonstrated deterministic generation;
-   [ ] analyzed intermediate validation;
-   [ ] executed at least three meaningful negative tests;
-   [ ] tested a successful database load;
-   [ ] investigated transaction rollback;
-   [ ] investigated insertion-order/relationship behavior;
-   [ ] verified representative data through OpenEMR;
-   [ ] tested Small, Medium, and High scales;
-   [ ] analyzed scale behavior;
-   [ ] demonstrated data CI;
-   [ ] demonstrated GREEN → RED → GREEN;
-   [ ] identified at least three remaining risks;
-   [ ] included a team contribution statement;
-   [ ] excluded generated high-volume data from Git;
-   [ ] committed and pushed the final submission according to the
    course submission guide.

------------------------------------------------------------------------

## Final Perspective

A data pipeline is trustworthy only when we have evidence about both
what it **accepts** and what it **rejects**.

In this assignment, passing tests are only part of that evidence.
Controlled failures, rollback behavior, relationship validation, scale
behavior, and CI failures all help answer the more important engineering
question:

> **What evidence do we have that this system will preserve correct data
> and detect incorrect data when conditions change?**
