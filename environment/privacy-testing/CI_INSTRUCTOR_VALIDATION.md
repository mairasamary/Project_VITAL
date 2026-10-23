# Instructor Validation — Assignment 5 Privacy CI

## 1. Validate locally

Run:

```bash
bash environment/privacy-testing/run_privacy_ci_checks_local.sh
```

Expected:

```text
LOCAL PRIVACY CI CHECKS PASSED
```

Confirm that the wrapper also demonstrates:

```text
valid privacy export          → PASS
direct-identifier leakage     → REJECTED
broken pseudonymous relation  → REJECTED
```

## 2. Install the workflow

```bash
mkdir -p .github/workflows

cp environment/privacy-testing/github-actions-privacy-tests.template.yml \
   .github/workflows/privacy-tests.yml
```

Create:

```bash
git switch -c feature/assignment-05-privacy-ci-validation
```

Commit/push and confirm:

```text
Project VITAL Privacy Tests → GREEN
```

## 3. Controlled failure

Create:

```bash
git switch -c experiment/privacy-ci-failure
```

Introduce one privacy regression.

Recommended experiment: temporarily modify the privacy transformation so that a prohibited identifier is retained in the research export.

Commit/push and confirm:

```text
Project VITAL Privacy Tests → RED
```

The failure should be caused by privacy validation, not invalid syntax or missing files.

## 4. Restore

Restore the correct transformation and push.

Confirm:

```text
Project VITAL Privacy Tests → GREEN
```

## 5. Cleanup

Retain:

- valid privacy infrastructure;
- valid GitHub Actions workflow;
- privacy-testing documentation.

Do not merge the intentionally broken state into `main`.

Once this sequence passes, Assignment 5 privacy infrastructure is ready for consolidation into the student assignment and instructor guide.
