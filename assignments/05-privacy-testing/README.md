# Assignment 05 --- Privacy Testing: Pseudonymization, Re-identification Risk, and Continuous Privacy Validation

## Project VITAL

In this assignment, you will extend Project VITAL from data-quality
testing into **privacy testing**.

A system can produce structurally correct data and still expose
sensitive information. Removing a patient's name is not, by itself,
enough to make a dataset anonymous. Combinations of attributes such as
age, geography, sex, and dates may make records distinctive enough to
support re-identification.

You will build and evaluate a privacy-preserving research export using
**synthetic Project VITAL data only**.

> **Important:** This is a teaching exercise. Passing the automated
> checks in this assignment does not certify a dataset as anonymous,
> legally de-identified, HIPAA-compliant, GDPR-anonymous, or safe for
> unrestricted release.

------------------------------------------------------------------------

## Learning Objectives

By the end of this assignment, you should be able to:

-   distinguish direct identifiers from quasi-identifiers;
-   explain the difference between pseudonymization and anonymization;
-   create stable pseudonymous identifiers while preserving
    relationships across tables;
-   generalize or suppress quasi-identifiers;
-   measure equivalence-class sizes and reason about a selected k
    threshold;
-   evaluate the tradeoff between privacy protection and analytical
    utility;
-   write automated tests for privacy properties;
-   use continuous integration to detect privacy regressions.

------------------------------------------------------------------------

## Scenario

Project VITAL contains synthetic patient, encounter, and vital-sign
data. A research team would like an analytical export that preserves
useful clinical structure without exposing the original identifiers.

Your job is not merely to delete obvious identifiers. You must design a
transformation, test its privacy properties, preserve required
relationships, measure residual re-identification risk, and automate the
resulting privacy expectations.

------------------------------------------------------------------------

## Safety Constraint

Use **only the synthetic data generator supplied with Project VITAL**.

Do not use real patient data, protected health information,
institutional data, or data copied from an operational OpenEMR
installation.

Do not commit real secrets or pseudonymization keys to Git.

------------------------------------------------------------------------

# Part 1 --- Identify Privacy-Sensitive Attributes

Inspect the synthetic patient, encounter, and vitals data.

Classify relevant attributes into categories such as:

-   direct identifiers;
-   quasi-identifiers;
-   analytical attributes;
-   relational identifiers.

In your submission, explain:

1.  which fields you consider direct identifiers and why;
2.  which fields could act as quasi-identifiers;
3.  why removing direct identifiers does not necessarily make the
    remaining data anonymous;
4.  which relationships must remain intact for the research dataset to
    remain useful.

------------------------------------------------------------------------

# Part 2 --- Build a Pseudonymized Research Export

Create a privacy transformation that produces research versions of:

``` text
patients.csv
encounters.csv
vitals.csv
```

Your transformation must:

-   remove prohibited direct identifiers;
-   replace original patient identifiers with stable pseudonymous
    subject identifiers;
-   replace other identifiers as needed while preserving table
    relationships;
-   avoid exposing the secret/key used to construct pseudonyms;
-   transform dates/geographic fields according to your privacy
    strategy;
-   produce deterministic results when the same source data,
    configuration, and teaching secret are used.

A cryptographic keyed construction such as HMAC is appropriate for
stable teaching pseudonyms.

### Referential integrity

After transformation:

-   every encounter subject must refer to an exported subject;
-   every vitals subject must refer to an exported subject;
-   every vitals encounter must refer to an exported encounter.

A privacy transformation that destroys these relationships may reduce
disclosure risk, but it also destroys important analytical utility.

------------------------------------------------------------------------

# Part 3 --- Measure Re-identification Risk

Choose and document a set of quasi-identifiers in the transformed
patient dataset.

Examples may include generalized versions of:

``` text
age
geography
sex
```

For each unique combination of your selected quasi-identifiers,
calculate the number of patient records sharing that combination.

The size of such a group is its **equivalence-class size**.

Report at minimum:

-   number of patients;
-   number of equivalence classes;
-   minimum equivalence-class size;
-   number of patients belonging to classes below your selected
    threshold;
-   number of records/classes that are unique, if any.

For this assignment, use **k \>= 3 as a teaching validation threshold**
unless your instructor specifies otherwise.

### Important interpretation

Do **not** claim that `k >= 3` proves anonymity.

Your analysis must explain what the measurement does and does not tell
us about re-identification risk.

------------------------------------------------------------------------

# Part 4 --- Improve Privacy Through Generalization or Suppression

If your initial privacy strategy leaves small equivalence classes,
modify the transformation.

Possible techniques include:

-   wider age bands;
-   coarser geographic information;
-   less precise dates/times;
-   suppression of selected quasi-identifiers.

Compare at least two privacy configurations.

For each configuration, record:

-   quasi-identifiers used;
-   minimum k;
-   number of patients below the selected k threshold;
-   information that was generalized or suppressed;
-   analytical information that remains available.

Explain why the stronger privacy configuration changes the equivalence
classes.

------------------------------------------------------------------------

# Part 5 --- Evaluate Privacy Versus Utility

Privacy transformations can make data safer but less useful.

Evaluate whether your stronger transformation preserves selected
analytical properties.

At minimum consider:

-   patient count;
-   encounter count;
-   vitals count;
-   encounter-reason distribution;
-   selected numeric vital-sign values or aggregates;
-   relationships among patients, encounters, and vitals.

Discuss at least one example where increased privacy reduces analytical
detail.

Your goal is not to maximize privacy at any cost. Your goal is to
demonstrate that privacy requirements and analytical utility can be
**tested explicitly**.

------------------------------------------------------------------------

# Part 6 --- Negative Privacy Tests

Automated privacy testing should prove that invalid datasets are
rejected.

Create controlled test cases for at least the following:

### A. Direct-identifier leakage

Introduce a prohibited direct identifier into a test export.

Your validator must reject the dataset.

### B. Broken pseudonymous relationship

Modify a pseudonymous relationship so that an encounter refers to an
unknown subject.

Your validator must reject the dataset.

Do not merely break Python syntax or delete arbitrary required files.
The negative tests should represent meaningful privacy/data-integrity
defects.

------------------------------------------------------------------------

# Part 7 --- Continuous Privacy Testing

Add a GitHub Actions workflow for privacy validation.

The workflow should perform a deterministic sequence similar to:

``` text
Generate synthetic source
        ↓
Create privacy-preserving export
        ↓
Validate prohibited identifiers
        ↓
Validate pseudonymous relationships
        ↓
Evaluate selected k threshold
        ↓
Check selected analytical utility
        ↓
Run controlled negative privacy tests
        ↓
PASS / FAIL
```

Keep the CI dataset small enough for fast execution.

The workflow must use synthetic data and must not depend on a real
operational database.

------------------------------------------------------------------------

# Part 8 --- Demonstrate That CI Can Detect a Privacy Regression

A green workflow shows that the current implementation passes. It does
not demonstrate that the workflow detects meaningful privacy failures.

Perform a controlled **GREEN → RED → GREEN** experiment.

1.  Start from a passing privacy workflow.
2.  Introduce one meaningful, reversible privacy-policy regression.
3.  Commit/push the experiment and confirm that the privacy workflow
    becomes red.
4.  Explain why the workflow rejected the change.
5.  Restore the correct behavior.
6.  Commit/push again and confirm that the privacy workflow returns to
    green.

Examples include deliberately changing a validated privacy threshold or
introducing a controlled privacy defect.

Do not merge an intentionally broken state into the final project.

------------------------------------------------------------------------

# Required Analysis

Your final write-up must answer the following questions.

1.  What is the difference between a direct identifier and a
    quasi-identifier?
2.  Why is pseudonymization not equivalent to anonymization?
3.  How did your initial quasi-identifier configuration affect
    equivalence-class sizes?
4.  What changes did you make to improve the selected k result?
5.  What analytical utility was preserved?
6.  What utility was reduced?
7.  Why does passing the selected k threshold not prove that
    re-identification is impossible?
8.  What privacy regression did your CI experiment detect?
9.  What privacy risks remain outside the scope of your automated tests?

------------------------------------------------------------------------

# Deliverables

Submit the Project VITAL repository containing:

``` text
assignment-05/
    [your Assignment 05 work/evidence]

environment/privacy-testing/
    [privacy transformation and validation infrastructure]

.github/workflows/
    privacy-tests.yml
```

Also include a concise report or README containing:

-   your privacy-sensitive field classification;
-   privacy strategies compared;
-   equivalence-class/k results;
-   privacy-versus-utility analysis;
-   negative-test evidence;
-   GREEN → RED → GREEN CI evidence;
-   answers to the required analysis questions.

Screenshots may support your evidence, but automated test output and
committed code are the primary artifacts.

------------------------------------------------------------------------

# Success Criteria

A strong submission demonstrates that:

-   direct identifiers are removed from the research export;
-   pseudonyms are stable for the intended experiment;
-   pseudonymous relationships remain valid;
-   quasi-identifier risk is measured rather than assumed;
-   a stronger transformation improves the selected privacy metric;
-   useful analytical properties are intentionally evaluated;
-   privacy defects are automatically rejected;
-   CI detects a meaningful privacy regression;
-   conclusions do not overstate what k-anonymity-style testing or
    pseudonymization guarantees.

------------------------------------------------------------------------

# Final Reminder

Privacy is not achieved simply by deleting names.

A privacy-preserving data pipeline must consider what an attacker could
infer from the information that remains, what information researchers
still need, and whether the system can continuously detect accidental
regressions in those protections.
