# Project VITAL — Continuous Privacy Validation

Assignment 5 extends Project VITAL's continuous-testing model to privacy properties.

The CI workflow is intentionally lightweight and deterministic:

```text
Push / Pull Request
        ↓
Generate synthetic source
        ↓
Create privacy-preserving export
        ↓
Check direct identifiers are absent
        ↓
Check pseudonymous relationships
        ↓
Check selected k threshold
        ↓
Check selected analytical utility
        ↓
Inject controlled privacy defects
        ↓
Confirm privacy validator rejects them
        ↓
GREEN / RED
```

## CI Scope

The validated teaching workflow uses:

```text
100 synthetic patients
seed = 515151
20-year age bands
state-level geography
sex suppressed
year-level time
selected threshold: k >= 3
```

These values are course testing parameters. Passing this workflow does **not** establish that a dataset is anonymous, legally de-identified, HIPAA-compliant, GDPR-anonymous, or safe for unrestricted release.

The CI check establishes only that the repository's stated privacy transformation and selected automated privacy rules still behave as expected.

---

# Local Validation

Before installing the workflow, run:

```bash
bash environment/privacy-testing/run_privacy_ci_checks_local.sh
```

Expected final line:

```text
LOCAL PRIVACY CI CHECKS PASSED
```

Note that the controlled leakage and broken-relationship datasets should each produce `PRIVACY VALIDATION FAILED`. Those failures are expected and are treated as successful negative tests by the wrapper script.

---

# Install GitHub Actions

From the repository root:

```bash
mkdir -p .github/workflows

cp environment/privacy-testing/github-actions-privacy-tests.template.yml \
   .github/workflows/privacy-tests.yml
```

Use a validation branch:

```bash
git switch -c feature/assignment-05-privacy-ci-validation
```

Then:

```bash
git add .github/workflows/privacy-tests.yml \
        environment/privacy-testing/

git commit -m "Add Assignment 5 continuous privacy validation"

git push -u origin feature/assignment-05-privacy-ci-validation
```

Open:

```text
GitHub → Actions → Project VITAL Privacy Tests
```

The first run should be green.

---

# Controlled GREEN → RED → GREEN Experiment

A green workflow alone does not demonstrate that privacy regression detection is useful.

Create:

```bash
git switch -c experiment/privacy-ci-failure
```

Introduce one controlled, reversible privacy defect.

A good instructor validation option is to temporarily weaken the transformation so that a prohibited direct identifier appears in the export.

Alternatively, deliberately change one privacy-validation expectation.

Do not break Python syntax merely to make CI red.

Commit and push:

```bash
git add .
git commit -m "Experiment: verify privacy CI detects regression"
git push -u origin experiment/privacy-ci-failure
```

Expected:

```text
Project VITAL Privacy Tests → RED
```

Inspect which step failed and why.

Restore the correct behavior:

```bash
git add .
git commit -m "Restore passing privacy validation"
git push
```

Expected:

```text
Project VITAL Privacy Tests → GREEN
```

Required evidence:

```text
GREEN → RED → GREEN
```

---

# Why the CI Uses Synthetic Data

Project VITAL privacy CI must never depend on real patient information.

Synthetic input makes the workflow:

- reproducible;
- safe for repository execution;
- suitable for automated testing;
- shareable with other instructors.

The assignment is about privacy-testing methods, not processing actual protected health information.
