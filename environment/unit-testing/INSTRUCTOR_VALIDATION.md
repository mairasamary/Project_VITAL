# Instructor Validation — Assignment 3 Unit Test Environment

Perform this check before releasing Assignment 3 each semester.

## 1. Start from the semester baseline

Use a clean clone of the semester branch/release.

## 2. Verify Docker

```bash
docker --version
docker info
```

## 3. Prepare the isolated OpenEMR source

```bash
bash environment/unit-testing/reset-unit-tests.sh
```

If no cache exists, that is fine.

Then:

```bash
bash environment/unit-testing/setup-unit-tests.sh
```

## 4. Install the smoke test

```bash
mkdir -p assignment-03/tests
cp environment/unit-testing/examples/ProjectVITALSmokeTest.php \
   assignment-03/tests/ProjectVITALSmokeTest.php
```

## 5. Run locally

```bash
bash environment/unit-testing/run-unit-tests.sh
```

Expected outcome:

- Docker starts the PHP 8.2 flex image.
- Composer dependencies install on the first run.
- PHPUnit starts with `phpunit-isolated.xml`.
- Both smoke assertions pass.

## 6. Run a second time

```bash
bash environment/unit-testing/run-unit-tests.sh
```

Confirm that dependencies do not need to be rebuilt from scratch.

## 7. Validate a red test

Temporarily edit:

```php
self::assertSame(5, 2 + 2);
```

Run again and confirm PHPUnit fails.

Restore:

```php
self::assertSame(4, 2 + 2);
```

Run again and confirm green.

## 8. Validate GitHub Actions

Copy the template:

```bash
mkdir -p .github/workflows
cp environment/unit-testing/github-actions-unit-tests.template.yml \
   .github/workflows/unit-tests.yml
```

Commit the smoke test and workflow on a temporary validation branch.

Push it and confirm:

1. GitHub Actions starts.
2. OpenEMR `v8_2_0` is checked out.
3. Composer dependencies install.
4. Project VITAL tests run.
5. The workflow is green.
6. JUnit and Clover artifacts are generated.

Then create a temporary failing test on an experiment branch and verify the workflow turns red.

Restore the test and verify green again.

## 9. Remove instructor smoke artifacts if appropriate

The smoke test is a setup validator and does not count toward student Assignment 3 test totals.

Decide whether to:

- provide the smoke test to students as environment validation; or
- remove it before the assignment release.

## 10. Record validation

Record in semester notes:

- Project VITAL semester tag
- OpenEMR ref
- date validated
- operating system used for local validation
- Docker version
- local result
- GitHub Actions result
- any required fixes
