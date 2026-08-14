# Project VITAL — Continuous Data Validation

Assignment 4 uses Continuous Integration to validate the **data-generation pipeline**, not to load thousands of records into OpenEMR on every commit.

The CI scope is intentionally lightweight:

```text
Push / Pull Request
        ↓
Generator unit tests
        ↓
Generate deterministic sample
        ↓
Validate sample
        ↓
Verify reproducibility
        ↓
Introduce controlled bad data
        ↓
Confirm validator rejects it
        ↓
GREEN / RED
```

## Why CI Does Not Load OpenEMR

The full Assignment 4 pipeline includes:

- Docker;
- OpenEMR;
- MariaDB;
- transactional loading;
- 200 / 2,000 / 20,000 scale experiments.

Those are important milestone tests, but they are unnecessarily expensive for every commit.

The CI workflow therefore focuses on properties that should remain continuously true:

- generator code runs;
- deterministic seeds are reproducible;
- requested record counts are correct;
- generated relationships validate;
- invalid data is rejected.

This distinction is part of the learning objective:

> **Continuous testing should run frequently enough to be useful, so not every test belongs in every CI run.**

---

# Install the Workflow

From the team repository root:

```bash
mkdir -p .github/workflows

cp environment/data-testing/github-actions-data-tests.template.yml \
   .github/workflows/data-tests.yml
```

Commit and push the workflow on a branch:

```bash
git switch -c feature/data-tests-ci

git add .github/workflows/data-tests.yml
git commit -m "Add Assignment 4 continuous data validation"
git push -u origin feature/data-tests-ci
```

Then open GitHub:

```text
Actions
→ Project VITAL Data Tests
```

The workflow should start automatically.

---

# Expected Green Run

A successful run proves:

```text
Generator tests              ✓
25-patient deterministic set ✓
CSV validation               ✓
Same-seed reproducibility    ✓
Corrupted-data rejection     ✓
```

The workflow does **not** prove that OpenEMR database loading works. That evidence comes from the separate Assignment 4 milestone testing.

---

# Controlled Red CI Experiment

Students should prove that data CI can detect a real data-validation failure.

A safe experiment is to temporarily weaken or break one generator/validator behavior on an `experiment/**` branch.

For example, temporarily change a generator field so it produces an invalid value, or temporarily change a test expectation.

Create:

```bash
git switch -c experiment/data-ci-failure
```

Make one controlled change, commit, and push:

```bash
git add .
git commit -m "Experiment: verify data CI detects invalid output"
git push -u origin experiment/data-ci-failure
```

The expected workflow result is:

```text
RED
```

Inspect the failing step.

Then restore the correct behavior:

```bash
git add .
git commit -m "Restore valid data behavior"
git push
```

The workflow should return to:

```text
GREEN
```

---

# Required CI Evidence

Assignment 4 should record:

- one successful data-CI run;
- one controlled failed run;
- one successful run after restoration;
- which step failed;
- why the failure occurred;
- why the high-volume database benchmarks are not run on every push.

Required pattern:

```text
GREEN → RED → GREEN
```

---

# GitHub Workflow Permission

If GitHub rejects the push because `.github/workflows/data-tests.yml` requires additional authorization, use the same workflow-permission process documented for Assignment 3:

```bash
gh auth refresh -h github.com -s workflow
gh auth setup-git
gh auth status
git push
```

See:

```text
environment/unit-testing/GITHUB_ACTIONS_SETUP.md
```

for detailed troubleshooting.
