# Project VITAL — Assignment 4 Data-Testing Environment

This environment uses a separate Docker Compose project to protect the original course database.

Project: `vital-a4-student`
Database container: `vital-a4-student-db`
OpenEMR container: `vital-a4-student-app`
HTTP port: 8085; HTTPS port: 8448

**Never reset or delete the original A1–A3 environment.**

## Starting the isolated A4 environment

From the repository root, change to `environment` and run:

```bash
cd environment
export VITAL_DB_CONTAINER=vital-a4-student-db
export VITAL_APP_CONTAINER=vital-a4-student-app
export OPENEMR_HTTP_PORT=8085
export OPENEMR_HTTPS_PORT=8448
docker compose -p vital-a4-student -f docker-compose.yml -f data-testing/docker-compose.a4.yml up -d
```

Wait for OpenEMR to initialize. Check the containers using the same Compose options followed by `ps`.

**Do not run `docker compose down -v` against the original course environment.**

## Generate and validate data

From the repository root, generate a reproducible small dataset:

```bash
python3 environment/data-testing/scripts/generate_data.py --level small --seed 42 --output .project-vital/data/small
python3 environment/data-testing/scripts/validate_data.py --input .project-vital/data/small
```

Repeat with `--level medium` (2,000 patients) and `--level large` (20,000 patients), using separate output directories.

Generated data belongs under `.project-vital/data/`, which is excluded from Git. Do not commit generated datasets or database credentials.

### Vital measurement units

Synthetic vital records use **pounds (lb)** for `weight` and **inches (in)** for `height`, matching the OpenEMR database storage conventions used in this course. The generator converts its source ranges of 45–110 kg and 145–195 cm before writing the CSV files. The loader inserts these values without further unit conversion.

## Database initialization and loading

The SQL identity initialization and Python database loader require a dedicated A4 database. Do not execute either against the original course environment. The tested initialization and loading commands are provided below.

## Tested A4 database workflow

These commands assume the dedicated A4 containers have been started and OpenEMR has finished initializing. Run them from the `environment` directory.

### Initialize the database identity

Only for a newly created, empty A4 database:

```bash
docker exec -i vital-a4-student-db sh -c 'exec mariadb -uroot -p"$MYSQL_ROOT_PASSWORD" openemr' < data-testing/sql/init_a4_identity.sql
```

### Dry-run validation

```bash
docker compose -p vital-a4-student -f docker-compose.yml -f data-testing/docker-compose.a4.yml --profile tools run --rm --no-deps a4-runner sh -c 'pip install --quiet --disable-pip-version-check -r /workspace/environment/data-testing/requirements.txt && python /workspace/environment/data-testing/scripts/load_data.py --input /data/small'
```

### Load the validated dataset

**This command writes synthetic records to the isolated A4 database. Run it only after verifying the project, container, identity marker, and empty baseline.**

```bash
docker compose -p vital-a4-student -f docker-compose.yml -f data-testing/docker-compose.a4.yml --profile tools run --rm --no-deps a4-runner sh -c 'pip install --quiet --disable-pip-version-check -r /workspace/environment/data-testing/requirements.txt && python /workspace/environment/data-testing/scripts/load_data.py --input /data/small --apply --confirm vital-a4'
```

The loader refuses a nonempty baseline. Do not rerun the load against an already populated database.

### Verify loaded counts

```bash
docker exec vital-a4-student-db sh -c 'mariadb -uroot -p"$MYSQL_ROOT_PASSWORD" openemr -e "SELECT COUNT(*) AS patients FROM patient_data; SELECT COUNT(*) AS encounters FROM form_encounter;"'
```

**Never use these commands against the original A1–A3 environment or a database containing real patient data.**

## Medium and large scale experiments

Generate and validate the medium (2,000 patients) and large (20,000 patients) datasets using the commands above, changing the level and output directory.

Each database-loading experiment requires a separate, newly initialized A4 Docker Compose project with its own database volume, container names, and available HTTP/HTTPS ports. Do not load a second dataset into a populated database.

For each new project, repeat the identity initialization, dry run, and confirmed load using the appropriate dataset path (`/data/medium` or `/data/large`). The loader will refuse to write when its protected clinical tables are not empty.

Record generation time, validation results, loading time, database counts, and any observed performance differences. Students must implement their own benchmarking utility as required by the assignment.

Never delete or reset an existing course database to prepare another experiment.
