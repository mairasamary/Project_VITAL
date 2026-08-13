# Project VITAL OpenEMR Environment

This directory provides the reference System Under Test (SUT) environment for Project VITAL.

The environment runs:

- **OpenEMR 8.2.0**
- **MariaDB 11.8.8**
- Docker Compose
- persistent Docker volumes for the database, OpenEMR site configuration, and logs

The goal is to give every team the same reproducible baseline while keeping all testing isolated from production systems.

## Prerequisites

Students need:

- Git
- Docker Desktop (macOS/Windows) or Docker Engine + Docker Compose (Linux)
- a modern web browser
- enough free disk space for the Docker images and test data

Students do **not** need to install PHP, Apache, or MariaDB directly.

## First-time setup

From the Project VITAL repository:

```bash
cd environment
cp .env.example .env
docker compose pull
docker compose up -d
```

The first startup can take several minutes because Docker must download images, initialize MariaDB, and allow OpenEMR to complete its setup.

Check status:

```bash
docker compose ps
```

View logs if needed:

```bash
docker compose logs -f openemr
```

## Accessing OpenEMR

Open:

- HTTP: `http://localhost:8080`
- HTTPS: `https://localhost:8443`

The local HTTPS certificate may trigger a browser warning because this is an isolated teaching environment.

Default credentials from `.env.example`:

- Username: `admin`
- Password: `vital-admin`

Instructors may change these values before distributing the environment.

## Stopping the environment

```bash
docker compose stop
```

Restart later with:

```bash
docker compose start
```

## Resetting the environment

To remove the containers **and all persistent course data**:

```bash
docker compose down -v
```

Then start again:

```bash
docker compose up -d
```

**Warning:** `down -v` deletes the OpenEMR database and local course data. This is intentional for a reproducible testing lab, but students should export anything they need before resetting.

## Source-code access

The running Docker image is the System Under Test. For architecture and white-box investigation, students should also inspect the corresponding OpenEMR source code separately.

Recommended approach:

```bash
git clone https://github.com/openemr/openemr.git openemr-source
cd openemr-source
git checkout v8_2_0
```

If the upstream tag naming changes or the exact tag is unavailable, instructors should provide the exact commit/ref used for the course and record it in `VERSION.md`.

Students should **not** make their architecture analysis against the moving `master` branch.

## Database inspection

Students may inspect the database from inside the MariaDB container:

```bash
docker compose exec mysql mariadb -uroot -p
```

Enter the root password from `.env`.

Useful introductory commands include:

```sql
SHOW DATABASES;
USE openemr;
SHOW TABLES;
DESCRIBE patient_data;
```

For the System Understanding assignment, database access should initially be **read-only in practice**: students should inspect schemas and relationships rather than manually alter records.

## Safety

This environment is intended only for local educational testing.

- Do not use real patient information.
- Do not connect the environment to a production healthcare system.
- Do not conduct security/load testing against public OpenEMR demos or third-party systems.
- Security and availability experiments should target only the student's/team's isolated instance.
- Do not commit `.env`, passwords, generated PHI-like datasets, or secrets to GitHub.

## Why the environment is pinned

A testing course requires reproducibility. All teams should test the same software baseline. Upgrading OpenEMR during the semester can change behavior, architecture, database structure, and expected test results.

A later version can intentionally be introduced as a regression-testing exercise.
