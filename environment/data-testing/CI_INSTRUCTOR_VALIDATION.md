# Instructor Validation — Assignment 4 Data CI

Validate locally first, then validate the GitHub Actions workflow.

## 1. Local equivalent

Run:

```bash
bash environment/data-testing/run_ci_checks_local.sh
```

Expected final output:

```text
LOCAL DATA CI CHECKS PASSED
```

The controlled corruption step should visibly produce a validation failure, but the wrapper script should interpret that failure as the expected outcome and continue.

---

## 2. Install GitHub Actions template

```bash
mkdir -p .github/workflows

cp environment/data-testing/github-actions-data-tests.template.yml \
   .github/workflows/data-tests.yml
```

Use a feature branch:

```bash
git switch -c feature/assignment-04-data-ci-validation
```

Commit:

```bash
git add .github/workflows/data-tests.yml
git commit -m "Validate Assignment 4 continuous data testing"
```

Push:

```bash
git push -u origin feature/assignment-04-data-ci-validation
```

If GitHub refuses workflow-file changes, follow the documented `workflow` authorization procedure.

---

## 3. Verify green CI

In GitHub:

```text
Actions
→ Project VITAL Data Tests
```

Confirm that the branch run is green.

Expected steps:

```text
Check out repository
Set up Python
Generator unit tests
Generate deterministic CI dataset
Validate deterministic CI dataset
Verify reproducibility
Prove validator rejects bad data
```

---

## 4. Verify red CI

Create:

```bash
git switch -c experiment/data-ci-failure
```

Temporarily break one expected generator/validation behavior.

A simple instructor validation option is to edit `test_generator.py` and make one correct assertion deliberately incorrect.

Commit and push:

```bash
git add environment/data-testing/test_generator.py
git commit -m "Experiment: verify data CI detects failure"
git push -u origin experiment/data-ci-failure
```

Expected:

```text
Project VITAL Data Tests → RED
```

---

## 5. Restore

Restore the test:

```bash
git add environment/data-testing/test_generator.py
git commit -m "Restore passing data generator test"
git push
```

Expected:

```text
Project VITAL Data Tests → GREEN
```

Required validation:

```text
GREEN → RED → GREEN
```

---

## 6. Cleanup

Do not merge the intentionally broken commit into `main`.

After validation, retain only the valid workflow and documentation.

The experiment branch may be deleted after evidence has been recorded.
