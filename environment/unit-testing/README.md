# Project VITAL — Unit Testing Environment

This environment supports **Assignment 3: Unit Testing and Continuous Integration**.

It is separate from the normal OpenEMR application environment used for system exploration.

## Why a Separate Environment?

Assignments 1 and 2 use the running OpenEMR application:

```text
Browser
   ↓
OpenEMR application container
   ↓
MariaDB
```

Assignment 3 focuses on **isolated/unit tests**. OpenEMR's own test configuration distinguishes isolated tests from tests that require database/application initialization.

For Project VITAL, Assignment 3 begins with **isolated tests** so students can focus on unit-test design before introducing database and service dependencies.

The reference baseline is:

```text
OpenEMR source: v8_2_0
PHP:            8.2
PHPUnit:        OpenEMR Composer dependency (PHPUnit 11.x)
Test config:    phpunit-isolated.xml
Docker image:   openemr/openemr:flex-3.22-php-8.2
```

The OpenEMR source is downloaded into a local cache and is **not committed to the team repository**.

---

# Directory Model

A team repository using this environment should look approximately like:

```text
VITAL-Team-XX/
│
├── assignment-03/
│   └── tests/
│       ├── ProjectVITALSmokeTest.php
│       └── YourSelectedComponentTest.php
│
├── .github/
│   └── workflows/
│       └── unit-tests.yml
│
└── ...
```

Project VITAL's helper scripts maintain a local working copy of OpenEMR under:

```text
.project-vital/
└── openemr-unit/
```

This directory should be ignored by Git.

---

# Prerequisites

You need:

- Git
- Docker
- Docker Compose / Docker Desktop
- a working Project VITAL repository

Verify:

```bash
git --version
docker --version
docker info
```

If `docker info` cannot connect to the Docker daemon, start Docker Desktop or Docker Engine before continuing.

---

# Step 1 — Prepare the OpenEMR Unit-Test Source

From the root of your team repository:

```bash
bash environment/unit-testing/setup-unit-tests.sh
```

The script:

1. creates `.project-vital/`;
2. clones OpenEMR;
3. checks out the pinned `v8_2_0` release;
4. prepares the location where Project VITAL tests are injected.

The first run requires Internet access.

---

# Step 2 — Add Assignment 3 Tests

Store Project VITAL Assignment 3 tests under:

```text
assignment-03/tests/
```

The helper script copies these files into the isolated-test area of the temporary OpenEMR checkout before PHPUnit runs.

Do not edit the cached OpenEMR checkout as the authoritative version of your work.

Your graded test files belong in your team repository.

---

# Step 3 — Run Tests Locally

From the root of the team repository:

```bash
bash environment/unit-testing/run-unit-tests.sh
```

The script:

1. verifies the pinned OpenEMR checkout;
2. copies your Assignment 3 tests into the OpenEMR isolated test tree;
3. starts a one-shot PHP 8.2 OpenEMR development container;
4. installs OpenEMR Composer dependencies when necessary;
5. runs only your Project VITAL isolated tests.

A successful result should finish with PHPUnit reporting no failures or errors.

---

# Step 4 — Run the Smoke Test First

Before writing your own component tests, use the provided smoke test.

Copy:

```text
environment/unit-testing/examples/ProjectVITALSmokeTest.php
```

to:

```text
assignment-03/tests/ProjectVITALSmokeTest.php
```

Then run:

```bash
bash environment/unit-testing/run-unit-tests.sh
```

The smoke test verifies that:

- PHPUnit starts;
- OpenEMR Composer autoloading works;
- an OpenEMR class can be resolved;
- the Project VITAL test overlay is being executed.

After this succeeds, keep or remove the smoke test according to instructor instructions. It does **not** count toward the six meaningful unit tests required for Assignment 3.

---

# Step 5 — Run a Single Test File

You can optionally pass a test filename:

```bash
bash environment/unit-testing/run-unit-tests.sh YourSelectedComponentTest.php
```

This is useful while developing one test class.

---

# What the Script Does

Conceptually:

```text
Team Repository
 assignment-03/tests/
        │
        │ copied temporarily
        ▼
.project-vital/openemr-unit/
 tests/Tests/Isolated/ProjectVITAL/
        │
        ▼
OpenEMR PHP 8.2 Flex Container
        │
        ▼
Composer dependencies
        │
        ▼
vendor/bin/phpunit
  -c phpunit-isolated.xml
        │
        ├── PASS
        └── FAIL
```

---

# Do Not Commit the OpenEMR Cache

The following must remain local:

```text
.project-vital/
```

Add this to the team repository `.gitignore`:

```gitignore
.project-vital/
```

The setup script will also warn you if this entry is missing.

---

# Why We Use OpenEMR's Isolated Test Configuration

OpenEMR's `phpunit-isolated.xml` is explicitly intended for tests that do not require:

- secondary services;
- a database/data layer;
- substantial application initialization.

That makes it a strong starting point for a course assignment about **unit testing**.

Later Project VITAL assignments can introduce tests with broader dependencies.

---

# Common Problems

## Docker is not running

If you see a Docker daemon/socket error:

```bash
docker info
```

Start Docker Desktop/Engine and try again.

## OpenEMR source directory already exists but is wrong

Run:

```bash
bash environment/unit-testing/reset-unit-tests.sh
bash environment/unit-testing/setup-unit-tests.sh
```

This deletes only the **cached unit-test checkout**, not your team test files.

## Composer install takes a long time

The first run may take several minutes.

Dependencies are stored in the cached OpenEMR checkout, so later runs should normally be faster.

## PHPUnit reports that no tests were found

Verify:

```bash
ls assignment-03/tests
```

Test files should generally follow PHPUnit naming conventions such as:

```text
SomethingTest.php
```

## A test accidentally requires the database

That may mean the selected target is not appropriate for this isolated/unit assignment.

Return to your Testability Assessment and reconsider whether:

- the dependency can be mocked/replaced; or
- another unit should be selected.

Do not silently turn Assignment 3 into a full integration test.

---

# Instructor Validation

Before each semester, the instructor should:

```bash
bash environment/unit-testing/reset-unit-tests.sh
bash environment/unit-testing/setup-unit-tests.sh
mkdir -p assignment-03/tests
cp environment/unit-testing/examples/ProjectVITALSmokeTest.php assignment-03/tests/
bash environment/unit-testing/run-unit-tests.sh
```

Confirm that the smoke test passes on the exact Project VITAL semester release.

Then validate the GitHub Actions template separately.

