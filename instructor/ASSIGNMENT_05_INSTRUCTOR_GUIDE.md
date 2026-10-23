# Assignment 05 --- Instructor Guide

## Privacy Testing: Pseudonymization, Re-identification Risk, and Continuous Privacy Validation

## Purpose

Assignment 05 extends Project VITAL from data testing into privacy
testing.

The assignment is designed to make students confront three distinctions:

1.  **data correctness is not privacy;**
2.  **pseudonymization is not anonymization;**
3.  **a privacy metric is a testable property, not a universal guarantee
    of safety.**

The supplied infrastructure has been validated end-to-end using
synthetic data.

------------------------------------------------------------------------

# Validated Reference Configuration

The instructor validation used Project VITAL's deterministic synthetic
generator.

### Stage 1 source

``` text
size: small
seed: 42

patients:   200
encounters: 287
vitals:     245
```

The initial pseudonymized export removed direct identifiers and used
HMAC pseudonyms while retaining a relatively detailed quasi-identifier
model.

Observed result:

``` text
Quasi-identifiers: age_band, sex, state, postal_prefix
Minimum equivalence k: 1
Patients unique on these fields: 7
```

This is an important teaching result: removal of direct identifiers and
replacement of IDs did not eliminate uniqueness.

------------------------------------------------------------------------

# Stage 2 --- Stronger Generalization

The validated stronger strategy used:

``` text
age band width:       20 years
geography:            state
sex:                  suppressed
time granularity:     year
```

Observed result:

``` text
Patients:                  200
Encounters:                287
Vitals:                    245
Orphan encounters:         0
Unknown-subject vitals:    0
Unknown-encounter vitals:  0
Quasi-identifiers:         age_band, geography
Minimum k:                 9
Patients with k<3:         0

PRIVACY VALIDATION PASSED
```

This supports a useful comparison:

``` text
more detailed QIs  → minimum k = 1
stronger generalization → minimum k = 9
```

Do not present `k=3` or `k=9` as proof of anonymity.

------------------------------------------------------------------------

# Validated Utility Results

For the stronger Stage 2 transformation, the reference implementation
reported:

``` text
patient_count_preserved:         YES
encounter_count_preserved:       YES
vitals_count_preserved:          YES
reason_distribution_preserved:   YES
vitals_numeric_values_preserved: YES
```

Available transformed patient analytical fields included:

``` text
subject_id
age_band
geography
```

Encounter data retained pseudonymous linkage, generalized time, and
encounter reason.

Vitals retained pseudonymous subject/encounter relationships,
generalized time, and selected numeric measurements.

Students should recognize that suppression/generalization reduces detail
even when counts and selected numerical values remain useful.

------------------------------------------------------------------------

# Negative-Test Validation

Two controlled defects have been validated.

## Direct identifier leakage

A test defect reintroduced:

``` text
email
```

Expected result:

``` text
PRIVACY VALIDATION FAILED
 - patients.csv: prohibited columns: email
```

This is an expected negative-test success.

## Broken pseudonymous relationship

A test defect caused one encounter to refer to an unknown subject.

Expected result:

``` text
Orphan encounters: 1

PRIVACY VALIDATION FAILED
 - orphan encounters: 1
```

Again, the validator's failure is the desired test outcome.

------------------------------------------------------------------------

# Local Continuous Privacy Validation

Validated command:

``` bash
bash environment/privacy-testing/run_privacy_ci_checks_local.sh
```

Reference deterministic CI dataset:

``` text
patients:   200
encounters: 287
vitals:     245
seed:       42
```

Expected valid-export result:

``` text
Minimum k: 9
Patients with k<3: 0

PRIVACY VALIDATION PASSED
```

The script then intentionally exercises the two negative tests.

Expected final line:

``` text
LOCAL PRIVACY CI CHECKS PASSED
```

It is normal for `PRIVACY VALIDATION FAILED` to appear inside this run
when evaluating deliberately corrupted datasets.

------------------------------------------------------------------------

# Important CI Design Experiment: Dataset Size Matters

An earlier CI draft used:

``` text
100 patients
seed: 515151
20-year age bands
state geography
sex suppressed
k >= 3
```

It produced:

``` text
Minimum k: 2
Patients with k<3: 2

PRIVACY VALIDATION FAILED
```

The correct response was **not** to weaken the requirement merely to
obtain a green workflow.

The CI was changed to use the already validated 200-patient/seed-42
configuration.

This is a valuable discussion point: equivalence-class results depend on
the released population and the selected quasi-identifiers. A
transformation does not possess a fixed `k` independent of its data.

------------------------------------------------------------------------

# GitHub Actions

Validated workflow:

``` text
.github/workflows/privacy-tests.yml
```

Workflow name:

``` text
Project VITAL Privacy Tests
```

The workflow runs deterministic synthetic generation, transformation,
privacy validation, utility checks, and controlled negative tests.

No real patient information is required or appropriate.

------------------------------------------------------------------------

# Validated GREEN → RED → GREEN Experiment

The instructor validation changed the normal privacy threshold from:

``` text
--min-k 3
```

to:

``` text
--min-k 10
```

The deterministic export had:

``` text
Minimum k: 9
```

Therefore:

``` text
required k >= 3   → GREEN
required k >= 10  → RED
restore k >= 3    → GREEN
```

The validated GitHub history showed:

``` text
GREEN  Add Assignment 5 privacy CI workflow
RED    Change min-k value from 3 to 10 in privacy...
GREEN  Change min-k value from 10 to 3 in privacy...
```

This experiment is pedagogically preferable to introducing a syntax
error because it demonstrates enforcement of an actual privacy-policy
expectation.

------------------------------------------------------------------------

# Suggested Student Workflow

Students should progress conceptually through:

``` text
Identify sensitive fields
        ↓
Pseudonymize identifiers
        ↓
Validate relationships
        ↓
Measure quasi-identifier risk
        ↓
Generalize/suppress
        ↓
Re-measure risk
        ↓
Evaluate utility
        ↓
Create negative tests
        ↓
Automate in CI
        ↓
Demonstrate GREEN → RED → GREEN
```

Students should not be told that the goal is merely to reproduce the
instructor's exact `k=9` result unless reproducibility of the supplied
reference implementation is itself being assessed.

The conceptual goal is to justify the transformation and test its
consequences.

------------------------------------------------------------------------

# Expected Conceptual Conclusions

## Pseudonymization versus anonymization

A good answer should recognize that pseudonymization replaces or
transforms identifiers while allowing records to remain linkable. The
resulting dataset may still permit singling out or linkage through
quasi-identifiers.

Students should not describe HMAC pseudonyms as making the data
anonymous.

## Quasi-identifiers

Students should recognize that fields that are not identifying in
isolation may become identifying when combined.

## k-style equivalence analysis

Students should understand that `k` describes the size of groups sharing
the selected quasi-identifier combination.

They should also recognize that the result depends on:

-   which quasi-identifiers are selected;
-   the population represented;
-   generalization/suppression decisions;
-   auxiliary information available to an attacker.

## Utility

Students should identify actual information lost by
generalization/suppression rather than saying only that "utility
decreases."

## CI

Students should explain that continuous privacy tests protect specified
invariants against regression. They do not prove the absence of every
privacy vulnerability.

------------------------------------------------------------------------

# Claims Students Should Avoid

Watch for overstatements such as:

``` text
"The data are anonymous because names were removed."

"HMAC makes re-identification impossible."

"k=3 means the dataset is HIPAA compliant."

"Passing CI proves the dataset is safe."

"Nobody can identify a patient because minimum k is 9."
```

These should be corrected in feedback.

------------------------------------------------------------------------

# Suggested Grading Framework

A 100-point version can use:

  Area                                                 Points
  ------------------------------------------------- ---------
  Privacy-sensitive attribute analysis                     10
  Pseudonymization/transformation implementation           15
  Referential-integrity validation                         10
  Quasi-identifier and equivalence-class analysis          15
  Stronger generalization/suppression strategy             10
  Privacy-versus-utility analysis                          10
  Negative privacy tests                                   10
  Continuous privacy workflow                              10
  GREEN → RED → GREEN evidence                              5
  Interpretation, limitations, and clarity                  5
  **Total**                                           **100**

Adjust weighting to match the course.

------------------------------------------------------------------------

# Common Failure Modes

### CI fails immediately at the k check

Inspect the deterministic source configuration and quasi-identifiers. Do
not automatically lower the threshold to make the build green.

### Direct identifier test passes unexpectedly

Confirm that the validator checks prohibited columns, not merely
non-empty values.

### Broken relationship is accepted

Confirm that validation checks membership of transformed
foreign/reference keys rather than only checking row counts.

### Pseudonyms change unexpectedly

Check that the same input and key/configuration are being used. Students
should understand why random replacement IDs are different from
deterministic pseudonyms.

### Student commits a real key

Treat this as a security/privacy process error. The assignment should
use only a teaching key with synthetic data. Real secrets should be
removed from Git history as appropriate to the course environment.

### Student's result differs from the instructor's k value

First check seed, dataset size, quasi-identifiers, and transformation
configuration. Different legitimate configurations can produce different
equivalence-class distributions.

------------------------------------------------------------------------

# Privacy Limitations Beyond the Assignment

The automated tests do not establish:

-   irreversible anonymity;
-   resistance to arbitrary external linkage;
-   resistance to all attribute-disclosure attacks;
-   resistance to membership inference;
-   HIPAA Safe Harbor;
-   HIPAA Expert Determination;
-   GDPR anonymization;
-   legal authorization to release data;
-   safety against an adversary with richer auxiliary information.

These limitations are part of the learning objective, not shortcomings
to hide.

------------------------------------------------------------------------

# Repository Organization

Recommended final organization:

``` text
assignments/
└── 05-privacy-testing/
    └── README.md

environment/
└── privacy-testing/
    ├── privacy transformation tools
    ├── privacy validators
    ├── utility analysis
    ├── controlled corruption tools
    ├── local CI validation
    └── supporting documentation

.github/
└── workflows/
    └── privacy-tests.yml

instructor/
└── ASSIGNMENT_05_INSTRUCTOR_GUIDE.md
```

Keep instructor-only expected results and troubleshooting guidance
outside the student assignment folder.

------------------------------------------------------------------------

# Completion Checklist

Before releasing Assignment 05, confirm:

-   Stage 1 demonstrates residual quasi-identifier risk;
-   Stage 2 stronger generalization passes the selected reference
    threshold;
-   direct-identifier leakage is rejected;
-   broken pseudonymous relationships are rejected;
-   utility checks pass;
-   local privacy CI finishes successfully;
-   GitHub displays `Project VITAL Privacy Tests`;
-   the normal workflow is green;
-   a meaningful privacy-policy regression produces red;
-   restoration produces green;
-   no intentionally broken experiment remains in the release state;
-   no real patient data or real secrets are present.

At that point, Assignment 05 is ready for student use.
