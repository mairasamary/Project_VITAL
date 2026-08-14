# Assignment 4 --- Instructor Guide

## Data Testing and Continuous Data Validation

### Project VITAL

> **Instructor-only document.**\
> This guide describes the validated infrastructure, expected behavior,
> baseline results, release procedure, troubleshooting, and grading
> considerations for Assignment 4.

------------------------------------------------------------------------

# 1. Purpose of This Guide

Assignment 4 asks students to investigate data quality and data-pipeline
behavior in the Project VITAL OpenEMR environment.

The student assignment deliberately emphasizes reasoning and evidence
rather than successful script execution. The instructor infrastructure
therefore has two purposes:

1.  provide a stable environment in which meaningful data-testing
    experiments can be performed; and
2.  provide known-good reference behavior so instructors can distinguish
    student discoveries from infrastructure problems.

The validated assignment pipeline is:

``` text
OpenEMR schema understanding
          ↓
Deterministic synthetic generation
          ↓
Intermediate validation
          ↓
Controlled invalid data
          ↓
Transactional OpenEMR loading
          ↓
Post-load semantic validation
          ↓
UI verification
          ↓
Scale experiments
          ↓
Continuous data validation
```

------------------------------------------------------------------------

# 2. Important Design Principle

Assignment 4 should **not** become a "run these scripts and take
screenshots" exercise.

Project VITAL provides substantial infrastructure because OpenEMR's data
model and safe database loading are complex. Students should spend their
effort on:

-   identifying properties worth testing;
-   predicting behavior;
-   designing negative tests;
-   distinguishing database constraints from semantic correctness;
-   analyzing rollback behavior;
-   interpreting scale results;
-   deciding what belongs in CI;
-   investigating failures;
-   identifying remaining risk.

Grade the quality of this reasoning more heavily than whether every
command produced `PASSED`.

------------------------------------------------------------------------

# 3. Instructor Infrastructure

The primary infrastructure is located under:

``` text
environment/data-testing/
```

Depending on the semester version, this directory should contain the
validated equivalents of tools for:

-   schema inspection;
-   deterministic data generation;
-   intermediate validation;
-   controlled corruption;
-   OpenEMR loading;
-   database validation;
-   batch reset;
-   rollback testing;
-   insertion-order testing;
-   loader hardening/coexistence testing;
-   benchmarking;
-   local CI validation;
-   GitHub Actions setup/documentation.

The student-facing assignment should be stored under the semester's
Assignment 4 directory, for example:

``` text
assignments/04-data-testing/
```

Do not expose instructor-only notes or expected baseline interpretations
unless intentionally desired.

------------------------------------------------------------------------

# 4. Relevant OpenEMR Data Model

The assignment focuses conceptually on:

``` text
Patient
   ↓
Encounter
   ↓
Vitals
```

The relevant OpenEMR tables include:

``` text
patient_data
form_encounter
form_vitals
forms
```

A critical lesson from instructor validation was that the conceptual
three-entity model is not sufficient to understand how OpenEMR
represents a vitals form.

The `forms` relationship is important for OpenEMR to recognize/register
the form correctly.

Students should discover and explain this relationship rather than
merely state that three CSV files exist.

------------------------------------------------------------------------

# 5. Semester Pre-Release Validation

Before releasing Assignment 4, validate the environment against the
semester's OpenEMR baseline.

Recommended sequence:

``` text
1. OpenEMR environment starts
2. Schema inspection works
3. Generator tests pass
4. Small deterministic generation passes
5. Intermediate validator passes
6. Controlled corruption is rejected
7. Small OpenEMR load passes
8. Database validator passes
9. Rollback test passes
10. Insertion-order experiment passes
11. Loader hardening/coexistence passes
12. Benchmark utility passes at Small
13. Benchmark utility passes at Medium
14. Benchmark utility passes at High
15. Local data-CI checks pass
16. GitHub Actions GREEN → RED → GREEN passes
```

Do not assume a previous semester's OpenEMR image behaves identically
after an upgrade.

------------------------------------------------------------------------

# 6. Schema Inspection

Run the semester's schema-inspection script, for example:

``` bash
bash environment/data-testing/inspect_openemr_schema.sh
```

A validated Project VITAL environment previously produced local schema
captures for:

``` text
patient_data
form_encounter
form_vitals
forms
row-counts
```

These captures belong under the local `.project-vital/` working area and
should not become student-maintained source files unless the course
design explicitly requires that.

Check that the fields used by the generator/loader still exist and
retain compatible types.

If OpenEMR changes its schema, **stop and update the infrastructure
before releasing the assignment**.

------------------------------------------------------------------------

# 7. Deterministic Generator Validation

The generator must produce synthetic data only.

Known validated scales are:

  Scale      Patients
  -------- ----------
  Small           200
  Medium        2,000
  High         20,000

Encounter and vitals counts vary with the seed.

For seed `42`, the validated semester baseline produced:

  Scale      Patients   Encounters   Vitals
  -------- ---------- ------------ --------
  Small           200          287      245
  Medium        2,000        2,924    2,516
  High         20,000       30,157   25,721

A separate Small benchmark using seed `314159` produced:

``` text
Patients:   200
Encounters: 308
Vitals:     263
```

Therefore, do not grade students against a fixed encounter/vitals count
unless they are using the same required seed.

Verify that:

-   same seed + same requested scale produces identical data;
-   a different seed changes generated records;
-   manifests correctly describe generated data;
-   generated records contain no real patient information.

------------------------------------------------------------------------

# 8. Intermediate Validation

The intermediate validator should reject invalid data before any
database operation begins.

A valid dataset should end with:

``` text
VALIDATION PASSED
```

The instructor should verify at least one positive and several negative
cases before release.

Students should understand that intermediate validation protects the
database boundary.

Do not award significant credit merely for showing `VALIDATION PASSED`;
require students to explain which properties were established.

------------------------------------------------------------------------

# 9. Controlled Corruption

The environment includes a mechanism for creating intentionally invalid
datasets.

Before release, confirm that the supported corruption modes still
produce defects the validator detects.

At least one negative case should involve an entity relationship, such
as an orphan record.

The CI infrastructure uses a controlled orphan-vitals defect as one
validation case.

Expected pattern:

``` text
Valid synthetic data
        ↓
Controlled corruption
        ↓
Validator
        ↓
REJECTED
```

The wrapper test should treat this rejection as success.

------------------------------------------------------------------------

# 10. Transactional OpenEMR Loading

The loader should perform validation before loading and use a
transaction for the Project VITAL batch.

A successful load should clearly report:

``` text
LOAD COMMITTED
```

The loader should also report useful information such as:

-   batch identifier;
-   patient count;
-   encounter count;
-   vitals count;
-   allocated patient-ID range;
-   allocated encounter range.

Students should use unique batch names.

------------------------------------------------------------------------

# 11. Important Issue Discovered: ID Collisions

An early version of the loader used fixed identifiers.

At higher scale, this caused an actual collision:

``` text
ERROR 1062 (23000)
Duplicate entry ... for key 'pid'
```

The transaction correctly failed and rolled back, but the fixed-ID
strategy was not safe for repeated or coexisting batches.

The hardened loader therefore allocates identifiers based on currently
available ranges and performs collision/preflight checks.

## Instructor implication

If students encounter duplicate `pid` errors using the validated current
loader, do not dismiss the error as expected assignment behavior.

Check whether:

-   they are using the current loader;
-   stale infrastructure was copied;
-   the database contains unexpected manually inserted records;
-   a semester upgrade changed assumptions.

------------------------------------------------------------------------

# 12. Batch Isolation and Duplicate Batch Protection

The hardened loader should reject reuse of an existing Project VITAL
batch identifier before modifying the database.

Multiple distinct Project VITAL batches should be able to coexist.

This behavior matters because:

-   students may perform multiple experiments;
-   one team's data should not silently overwrite another batch;
-   benchmarking must be repeatable;
-   cleanup must target only the intended batch.

The validated hardening suite demonstrated:

``` text
existing batch validation       ✓
duplicate batch preflight       ✓
multiple batch coexistence      ✓
collision avoidance             ✓
```

------------------------------------------------------------------------

# 13. Post-Load Validation

After loading, validate the batch semantically.

A successful validation should report counts and integrity findings
similar to:

``` text
Patients:             ...
Encounters:           ...
Vitals:               ...
Vitals form links:    ...
Orphan encounters:    0
Broken form links:    0
Unregistered vitals:  0
Patient mismatches:   0

BATCH VALID
```

The validator distinguishes three important outcomes:

``` text
BATCH VALID
BATCH INVALID
BATCH NOT FOUND
```

This distinction is intentional.

`BATCH NOT FOUND` must not be treated as equivalent to a valid empty
batch.

------------------------------------------------------------------------

# 14. Atomicity / Rollback Experiment

The instructor-validated failure experiment produced:

``` text
LOAD FAILED — transaction should have rolled back.
Rows remaining after failed transaction: (0, 0, 0)
ATOMICITY TEST PASSED — rollback left no partial batch.
```

This is one of the central conceptual experiments in the assignment.

Students should explain why the important result is not simply "the load
failed."

The important property is:

> A failed multi-table operation did not leave a partially loaded
> logical batch.

If rows remain after a controlled failed transaction, treat that as an
infrastructure defect requiring investigation.

------------------------------------------------------------------------

# 15. Insertion-Order Experiment

The validated insertion-order experiment produced an important result:

``` text
Database orphan count during transaction: 1
Transaction rolled back.
INSERTION-ORDER EXPERIMENT PASSED.
Finding: the database accepted the orphan row; semantic validation detected it.
```

This is pedagogically valuable.

Students may initially predict that the database itself will reject
every semantically invalid relationship.

The experiment demonstrates that:

``` text
database accepted
```

does not necessarily imply:

``` text
application data is semantically correct
```

Do not "correct" this behavior merely to make the database reject the
test. The distinction is part of the assignment's learning objective.

------------------------------------------------------------------------

# 16. OpenEMR UI Verification

Require students to inspect at least one loaded synthetic batch through
OpenEMR.

The goal is to establish another layer of evidence:

``` text
CSV representation
        ↓
database representation
        ↓
application/UI representation
```

A record existing in a database table does not automatically prove that
OpenEMR recognizes or displays it correctly.

Students should use representative screenshots, not dozens of repetitive
images.

------------------------------------------------------------------------

# 17. Benchmark Utility

The benchmark utility measures separate pipeline stages.

Typical command:

``` bash
python3 environment/data-testing/benchmark.py \
  --size small \
  --seed 42
```

Supported validation progression:

``` text
small
  ↓
medium
  ↓
high
```

An all-scale option may also be available after individual scales have
been validated.

By default, benchmark batches should be reset after successful
validation.

Results are stored locally under:

``` text
.project-vital/data-testing/benchmark-results/
```

including CSV and Markdown reports.

These local experiment artifacts should normally remain uncommitted.

------------------------------------------------------------------------

# 18. Validated Instructor Benchmark Baseline

On the instructor validation machine, the benchmark utility produced:

  --------------------------------------------------------------------------------
  Scale      Patients   Encounters     Vitals   Generation    DB Load           DB
                                                                        Validation
  -------- ---------- ------------ ---------- ------------ ---------- ------------
  Small           200          308        263     0.0807 s   3.4593 s     2.0783 s

  Medium        2,000        2,924      2,516     0.1543 s   5.6285 s     2.3816 s

  High         20,000       30,157     25,721     0.9939 s  30.2294 s     2.3899 s
  --------------------------------------------------------------------------------

The Small row above used seed `314159`; Medium and High used seed `42`,
so the table is an infrastructure timing reference rather than a
same-seed scientific comparison.

An independently timed High post-load validation was also observed
around:

``` text
2.278–2.620 seconds
```

## Interpretation

The clearest observed pattern was:

-   generation remained inexpensive;
-   database loading became substantially more expensive as scale
    increased;
-   post-load validation remained comparatively stable in these
    experiments.

Do **not** present these numbers to students as required targets.

Hardware, Docker resources, database state, operating system, caching,
and background activity affect timing.

Grade the student's interpretation of their own evidence.

------------------------------------------------------------------------

# 19. Benchmarking Is Not Performance Testing

Assignment 4 contains a scale experiment, but it is not intended to
replace a later performance-testing assignment.

Students should not conclude:

> "OpenEMR can process 20,000 patients in 30 seconds."

The measured operation is the Project VITAL synthetic-data loading
pipeline under a specific local configuration.

Appropriate conclusions are narrower, such as:

> "In our environment, database loading increased much more noticeably
> than post-load validation as the Project VITAL dataset grew."

Maintain this distinction when grading.

------------------------------------------------------------------------

# 20. Continuous Data Validation

The Assignment 4 CI workflow is intentionally lightweight.

Expected conceptual pipeline:

``` text
Push / Pull Request
        ↓
Generator unit tests
        ↓
Generate small deterministic sample
        ↓
Validate sample
        ↓
Verify same-seed reproducibility
        ↓
Create controlled invalid data
        ↓
Confirm validator rejects it
        ↓
GREEN / RED
```

The validated workflow used a 25-patient deterministic CI sample.

Large OpenEMR database loads are deliberately excluded from normal CI.

------------------------------------------------------------------------

# 21. Why High-Volume OpenEMR Loading Is Not in CI

Students should reason about this boundary.

The 200 / 2,000 / 20,000 experiments:

-   require database infrastructure;
-   take longer;
-   are milestone tests;
-   are useful for scale analysis;
-   do not need to execute on every commit.

The lightweight CI tests:

-   provide fast feedback;
-   detect generator/validator regressions;
-   test deterministic behavior;
-   can run frequently;
-   avoid unnecessary Docker/database cost.

A strong student answer should discuss both **test value** and **test
frequency**.

------------------------------------------------------------------------

# 22. GitHub Actions Workflow

The validated workflow appears in GitHub Actions as:

``` text
Project VITAL Data Tests
```

Before release, confirm a feature-branch push produces a successful run.

The workflow should include equivalents of:

``` text
Check out repository
Set up Python
Run generator unit tests
Generate deterministic CI dataset
Validate deterministic CI dataset
Verify reproducibility
Prove validator rejects bad data
```

------------------------------------------------------------------------

# 23. GREEN → RED → GREEN Instructor Validation

The actual instructor validation successfully demonstrated:

``` text
Add Assignment 4 continuous data testing
    GREEN

Experiment: verify data CI detects failure
    RED

Restore passing data generator test
    GREEN
```

This proves that the workflow is not merely configured to appear green.

Students should perform a comparable controlled experiment.

A good controlled defect changes a testable property.

A poor controlled defect merely creates invalid YAML or broken Python
syntax.

------------------------------------------------------------------------

# 24. GitHub Workflow Authorization

GitHub may reject attempts to create or modify `.github/workflows/*.yml`
when the current authentication token lacks workflow authorization.

A previously validated CLI solution was:

``` bash
gh auth refresh -h github.com -s workflow
gh auth setup-git
gh auth status
```

Then retry:

``` bash
git push
```

The detailed Assignment 3 workflow setup documentation may also be
reused:

``` text
environment/unit-testing/GITHUB_ACTIONS_SETUP.md
```

Keep this troubleshooting information available to students, but avoid
turning token configuration into an assessed learning objective.

------------------------------------------------------------------------

# 25. macOS Metadata

During instructor development, `.DS_Store` was accidentally committed.

Ensure the repository ignores macOS metadata, typically with:

``` gitignore
.DS_Store
**/.DS_Store
```

Also ensure local generated Project VITAL artifacts remain ignored:

``` gitignore
.project-vital/
```

Do not use a nonexistent `gitignore` shell command.

Edit `.gitignore` directly and commit the change.

------------------------------------------------------------------------

# 26. Expected Student Misconceptions

Watch for the following.

### "The database accepted it, so it is valid."

Incorrect. The insertion-order experiment specifically demonstrates why
semantic validation may still be necessary.

### "CI is green, so the database loader works."

Incorrect. The data CI deliberately does not exercise the full OpenEMR
loading pipeline.

### "The high dataset loaded, so OpenEMR performance is good."

Unsupported. Assignment 4 does not perform formal application
performance testing.

### "A failed negative test means our assignment failed."

Not necessarily. If invalid data is rejected as predicted, the negative
test succeeded.

### "Same seed means the same number of patients only."

Incomplete. Deterministic generation should reproduce the generated
dataset, not merely its size.

### "BATCH NOT FOUND means there were zero errors."

Incorrect. It means the requested test batch does not exist.

------------------------------------------------------------------------

# 27. Grading Guidance

Student rubric:

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

## Emphasize reasoning

A team should not lose major credit merely because it discovers a
genuine unexpected behavior, provided it:

-   documents the behavior accurately;
-   investigates it;
-   distinguishes infrastructure problems from system behavior;
-   explains the testing implications.

Conversely, a report containing only screenshots of green output should
not receive full credit.

------------------------------------------------------------------------

# 28. Evidence Expectations

Good evidence includes:

-   concise command excerpts;
-   one useful schema/relationship diagram;
-   negative-test outputs;
-   rollback evidence;
-   representative OpenEMR UI evidence;
-   benchmark table;
-   CI run evidence;
-   relevant commit IDs.

Discourage:

-   full terminal dumps with no explanation;
-   hundreds of generated CSV rows;
-   repetitive screenshots;
-   committed benchmark datasets;
-   screenshots containing irrelevant personal information.

------------------------------------------------------------------------

# 29. Remaining-Risk Discussion

Students must identify at least three risks not fully tested by
Assignment 4.

Reasonable directions may include:

-   concurrent database loads;
-   very large-scale datasets beyond the assignment limit;
-   malformed Unicode or unusual character sets;
-   date/time boundary conditions;
-   duplicate clinical events;
-   domain-specific medical plausibility;
-   migration between OpenEMR versions;
-   recovery from Docker/database interruption;
-   UI behavior under large datasets;
-   authorization/access-control interactions;
-   long-term database growth.

Do not require these exact answers. Evaluate whether the proposed risk
and future test are technically coherent.

------------------------------------------------------------------------

# 30. Cleanup Between Teams or Experiments

Use the Project VITAL batch reset mechanism rather than manually
deleting arbitrary OpenEMR rows.

The reset operation should target only the intended Project VITAL batch.

Before beginning a new semester, remove stale Project VITAL experimental
data as appropriate while preserving any intentional OpenEMR baseline
data.

Never encourage students to run broad destructive SQL against the
OpenEMR database.

------------------------------------------------------------------------

# 31. Branch Hygiene

Instructor validation may use branches such as:

``` text
feature/assignment-04-data-ci-validation
experiment/data-ci-failure
```

The deliberately broken experiment branch should not be merged into the
stable semester branch.

After validation:

1.  retain the correct CI workflow;
2.  retain relevant instructor documentation;
3.  merge only validated infrastructure;
4.  delete experimental branches when no longer useful.

------------------------------------------------------------------------

# 32. Pre-Release Checklist

Before publishing Assignment 4 to students:

-   [ ] OpenEMR starts successfully.
-   [ ] Relevant schema has been rechecked.
-   [ ] Generator unit tests pass.
-   [ ] Same-seed reproducibility works.
-   [ ] Intermediate validation passes valid data.
-   [ ] Controlled invalid data is rejected.
-   [ ] Valid Small load commits.
-   [ ] Post-load validation reports `BATCH VALID`.
-   [ ] OpenEMR UI recognizes representative synthetic data.
-   [ ] Failed transactional load leaves no partial batch.
-   [ ] Insertion-order experiment still demonstrates intended behavior.
-   [ ] Duplicate batch preflight works.
-   [ ] Multiple Project VITAL batches can coexist.
-   [ ] Small benchmark passes.
-   [ ] Medium benchmark passes.
-   [ ] High benchmark passes.
-   [ ] Benchmark reset behavior works.
-   [ ] Local CI validation passes.
-   [ ] GitHub Actions produces GREEN.
-   [ ] Controlled CI defect produces RED.
-   [ ] Restoration produces GREEN.
-   [ ] `.project-vital/` is ignored.
-   [ ] `.DS_Store` is ignored.
-   [ ] Student Assignment 4 instructions match the current
    infrastructure.
-   [ ] No real patient data exists in assignment materials.

------------------------------------------------------------------------

# 33. Recommended Semester Release Sequence

Use the following order when preparing a new semester:

``` text
Update semester branch
        ↓
Start OpenEMR
        ↓
Revalidate schema
        ↓
Run Assignment 4 infrastructure checks
        ↓
Run benchmark Small → Medium → High
        ↓
Validate GitHub Actions
        ↓
Review student instructions
        ↓
Remove instructor experiment artifacts
        ↓
Merge validated semester infrastructure
        ↓
Release Assignment 4
```

If the OpenEMR image changes, rerun the complete validation sequence
rather than assuming compatibility.

------------------------------------------------------------------------

# 34. Known-Good Assignment 4 State

At the completion of instructor development, the following had been
demonstrated successfully:

``` text
Synthetic generation                    ✓
Intermediate validation                 ✓
Controlled invalid-data detection       ✓
OpenEMR schema inspection               ✓
Transactional loading                   ✓
Rollback / atomicity                    ✓
Insertion-order experiment              ✓
OpenEMR semantic validation             ✓
OpenEMR UI recognition                  ✓
Safe identifier allocation              ✓
Duplicate-batch rejection               ✓
Multiple-batch coexistence              ✓
200-patient scale                       ✓
2,000-patient scale                     ✓
20,000-patient scale                    ✓
Benchmark automation                    ✓
Benchmark cleanup                       ✓
Local CI equivalent                     ✓
GitHub Actions GREEN                    ✓
Controlled GitHub Actions RED           ✓
Restored GitHub Actions GREEN           ✓
```

This is the reference state against which future semester setup should
be validated.

------------------------------------------------------------------------

# 35. Final Instructor Perspective

The most valuable finding from Assignment 4 development was not that
OpenEMR could accept 20,000 synthetic patients.

It was that different layers establish different kinds of evidence:

``` text
Generator tests
      ↓
Can we create controlled, reproducible test data?

Intermediate validation
      ↓
Is the data structurally and semantically acceptable before loading?

Transactions
      ↓
Does failure preserve database atomicity?

Database validation
      ↓
Did the loaded relationships remain coherent?

OpenEMR UI
      ↓
Does the application recognize the loaded representation?

Scale experiments
      ↓
How does behavior change as data volume increases?

Continuous Integration
      ↓
Can important regressions be detected automatically and quickly?
```

Students should leave Assignment 4 understanding that **data correctness
is not established by one test, one database constraint, one successful
load, or one green CI check**.

It is established through multiple layers of evidence.
