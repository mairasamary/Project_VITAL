# Project VITAL — GitHub Actions Setup and Validation Guide

This guide documents the complete process for validating the **Assignment 3 unit-testing and Continuous Integration (CI) environment**, including the GitHub authentication issue that can occur when pushing workflow files.

It is intended for instructors preparing Project VITAL and may also be useful for students if they are responsible for creating their own GitHub Actions workflow.

---

# 1. What This Guide Validates

Assignment 3 requires two different things to work:

```text
LOCAL TESTING
     │
     ▼
OpenEMR isolated PHPUnit tests
     │
     ▼
GREEN / RED results


CONTINUOUS INTEGRATION
     │
     ▼
GitHub Actions
     │
     ▼
Automatic test execution
     │
     ▼
GREEN / RED results
```

Before releasing Assignment 3, validate **both**.

---

# 2. Local Unit-Test Validation

From the root of the Project VITAL repository, first prepare the pinned OpenEMR unit-test checkout:

```bash
bash environment/unit-testing/setup-unit-tests.sh
```

Create the Assignment 3 test directory:

```bash
mkdir -p assignment-03/tests
```

Copy the Project VITAL smoke test:

```bash
cp environment/unit-testing/examples/ProjectVITALSmokeTest.php \
   assignment-03/tests/ProjectVITALSmokeTest.php
```

Run the unit tests:

```bash
bash environment/unit-testing/run-unit-tests.sh
```

A successful result should look similar to:

```text
Running Project VITAL isolated tests...

PHPUnit 11.x

..  2 / 2 (100%)

OK (2 tests, 2 assertions)
```

The exact PHP and PHPUnit patch versions may differ.

The important result is:

```text
OK
```

with no failures or errors.

---

# 3. Validate the Red → Green Cycle Locally

A test environment is not fully validated merely because it can produce a green result.

You must also verify that it detects a failing test.

Temporarily edit:

```text
assignment-03/tests/ProjectVITALSmokeTest.php
```

Change:

```php
self::assertSame(4, 2 + 2);
```

to:

```php
self::assertSame(5, 2 + 2);
```

Run:

```bash
bash environment/unit-testing/run-unit-tests.sh
```

PHPUnit should now report a failure.

Then restore:

```php
self::assertSame(4, 2 + 2);
```

Run again:

```bash
bash environment/unit-testing/run-unit-tests.sh
```

The result should return to:

```text
OK
```

The desired validation sequence is:

```text
GREEN
  ↓
RED
  ↓
GREEN
```

---

# 4. Prepare the GitHub Actions Workflow

Create the workflow directory if necessary:

```bash
mkdir -p .github/workflows
```

Copy the Project VITAL workflow template:

```bash
cp environment/unit-testing/github-actions-unit-tests.template.yml \
   .github/workflows/unit-tests.yml
```

Verify:

```bash
ls .github/workflows
```

You should see:

```text
unit-tests.yml
```

---

# 5. Use a Validation Branch

Do not perform the first CI validation directly on `main`.

Create a temporary branch:

```bash
git switch -c feature/assignment-03-ci-validation
```

Add and commit the workflow:

```bash
git add .github/workflows/unit-tests.yml \
        assignment-03/tests/ProjectVITALSmokeTest.php

git commit -m "Validate Assignment 3 continuous integration"
```

---

# 6. Important GitHub Authentication Requirement

GitHub applies additional security restrictions to files under:

```text
.github/workflows/
```

A Git credential that can normally push source files may still be refused when attempting to create or modify a GitHub Actions workflow.

A typical error looks like:

```text
refusing to allow a Personal Access Token to create or update workflow
`.github/workflows/unit-tests.yml` without `workflow` scope
```

or:

```text
refusing to allow an OAuth App to create or update workflow
`.github/workflows/unit-tests.yml` without `workflow` scope
```

This means:

> Git authentication is working, but the credential does not have permission to modify GitHub Actions workflow files.

This is **not** an error in `unit-tests.yml`.

---

# 7. Recommended Authentication Method — GitHub CLI

Project VITAL recommends the GitHub CLI (`gh`) for this workflow.

Check whether GitHub CLI is installed:

```bash
gh --version
```

If you are not authenticated:

```bash
gh auth login
```

Recommended choices:

```text
GitHub.com
HTTPS
Login with a web browser
```

Then configure Git to use the GitHub CLI credential:

```bash
gh auth setup-git
```

---

# 8. Add the Required `workflow` Scope

Even after `gh auth setup-git`, your OAuth credential may not initially include permission to modify GitHub Actions workflows.

Add the missing scope:

```bash
gh auth refresh -h github.com -s workflow
```

GitHub may open a browser or device-authorization process.

Complete the authorization.

Then check:

```bash
gh auth status
```

Look for a token scope list that includes:

```text
workflow
```

For example:

```text
Token scopes: 'gist', 'read:org', 'repo', 'workflow'
```

The exact set of scopes may vary.

The important requirement is that:

```text
workflow
```

is present.

---

# 9. Retry the Push

Once the GitHub CLI credential includes the `workflow` scope, retry:

```bash
git push -u origin feature/assignment-03-ci-validation
```

You do **not** need to create another commit if the previous push was rejected.

The commit still exists locally.

---

# 10. If Git Still Uses the Wrong Credential

If the error changes between references to a Personal Access Token and an OAuth App, Git may be switching between stored credentials.

First confirm the GitHub CLI authentication:

```bash
gh auth status
```

Then reconfigure Git:

```bash
gh auth setup-git
```

Retry:

```bash
git push -u origin feature/assignment-03-ci-validation
```

If necessary, refresh the scope again:

```bash
gh auth refresh -h github.com -s workflow
```

---

# 11. macOS Credential Cache Troubleshooting

On macOS, Git credentials may also be stored in Keychain.

If Git repeatedly uses an outdated HTTPS credential, remove the cached GitHub credential:

```bash
printf "protocol=https\nhost=github.com\n" | git credential-osxkeychain erase
```

Then configure GitHub CLI again:

```bash
gh auth setup-git
```

and retry the push.

Do this only when Git is clearly using an old cached credential.

---

# 12. Alternative — Personal Access Token

If GitHub CLI is not used, a Personal Access Token may be used instead.

A token used to push workflow files must have permission to modify GitHub Actions workflows.

For a classic Personal Access Token, this generally requires:

```text
repo
workflow
```

For a fine-grained token, ensure the repository is selected and that appropriate **Contents** and **Workflows** write permissions are granted.

Do not store Personal Access Tokens in the repository.

---

# 13. Verify That GitHub Actions Started

After a successful push, open the repository on GitHub.

Navigate to:

```text
Actions
```

Find:

```text
Project VITAL Unit Tests
```

You should see a run for:

```text
feature/assignment-03-ci-validation
```

The expected CI process is:

```text
Push branch
     │
     ▼
GitHub Actions runner
     │
     ├── Checkout team/Project VITAL repository
     │
     ├── Checkout pinned OpenEMR source
     │
     ├── Set up PHP
     │
     ├── Install Composer dependencies
     │
     ├── Copy Project VITAL tests
     │
     ▼
PHPUnit
     │
     ├── PASS → GREEN
     └── FAIL → RED
```

The first run may take longer than local testing because the GitHub runner must prepare the environment.

---

# 14. Validate the CI Red → Green Cycle

After the first GitHub Actions run is green, verify that CI detects a failure.

Create a temporary experiment branch:

```bash
git switch -c experiment/ci-failure
```

Temporarily modify the smoke test:

```php
self::assertSame(5, 2 + 2);
```

Commit:

```bash
git add assignment-03/tests/ProjectVITALSmokeTest.php

git commit -m "Experiment: verify CI detects failing unit test"
```

Push:

```bash
git push -u origin experiment/ci-failure
```

The GitHub Actions workflow should run automatically and become **red**.

This is the expected outcome.

---

# 15. Restore the Passing Test

Restore:

```php
self::assertSame(4, 2 + 2);
```

Commit and push:

```bash
git add assignment-03/tests/ProjectVITALSmokeTest.php

git commit -m "Restore passing smoke test"

git push
```

The next CI run should become **green**.

The final validation is:

```text
LOCAL
GREEN → RED → GREEN

CI
GREEN → RED → GREEN
```

---

# 16. What a Successful Validation Proves

After completing this process, you have established that:

- the pinned OpenEMR source can be obtained;
- the PHP development environment runs;
- Composer dependencies install;
- PHPUnit starts correctly;
- Project VITAL test files are discovered;
- valid tests pass;
- invalid expectations fail;
- CI starts automatically from Git events;
- GitHub Actions executes the tests;
- CI correctly reports failures;
- CI returns to green after the problem is corrected.

This provides the infrastructure needed for Assignment 3.

---

# 17. Instructor Pre-Semester Checklist

Before releasing Assignment 3:

- [ ] `.project-vital/` is listed in `.gitignore`.
- [ ] `setup-unit-tests.sh` completes.
- [ ] Smoke test passes locally.
- [ ] Deliberate local failure is detected.
- [ ] Local test returns to green after restoration.
- [ ] GitHub CLI authentication works.
- [ ] `gh auth status` shows `workflow` scope where required.
- [ ] CI workflow can be pushed.
- [ ] GitHub Actions starts automatically.
- [ ] CI passes with the valid smoke test.
- [ ] CI fails with the deliberate invalid assertion.
- [ ] CI returns to green after restoration.
- [ ] No `.env`, credentials, or tokens are committed.
- [ ] The exact OpenEMR baseline has not changed unexpectedly.

---

# 18. Student-Facing Note

If students are required to create or modify `.github/workflows/*.yml` in their own team repositories, they may encounter the same GitHub authentication restriction.

Instructors should tell students:

> GitHub may require additional authorization before an HTTPS credential can modify GitHub Actions workflow files. If your normal `git push` works for source code but is rejected specifically for `.github/workflows/`, check whether your GitHub credential has workflow permission.

The preferred recovery sequence is:

```bash
gh auth login
gh auth refresh -h github.com -s workflow
gh auth setup-git
gh auth status
git push
```

Students should not create multiple unnecessary tokens or expose authentication tokens in screenshots, reports, GitHub issues, or course submissions.

---

# 19. Common Error Reference

## Error: Personal Access Token lacks `workflow` scope

```text
refusing to allow a Personal Access Token to create or update workflow
without `workflow` scope
```

### Fix

Use a token with workflow permission, or switch to GitHub CLI:

```bash
gh auth login
gh auth refresh -h github.com -s workflow
gh auth setup-git
```

---

## Error: OAuth App lacks `workflow` scope

```text
refusing to allow an OAuth App to create or update workflow
without `workflow` scope
```

### Fix

Refresh the GitHub CLI credential:

```bash
gh auth refresh -h github.com -s workflow
```

Then verify:

```bash
gh auth status
```

and retry:

```bash
git push
```

---

## Error: Git still uses old credentials

### macOS

```bash
printf "protocol=https\nhost=github.com\n" | git credential-osxkeychain erase
gh auth setup-git
```

Then retry.

---

# 20. Guiding Principle

Continuous Integration should not be treated as successful merely because the GitHub Actions page is green.

A valid CI setup must demonstrate:

> **It runs automatically, it detects a failure, it communicates that failure, and it returns to green after the problem is corrected.**
