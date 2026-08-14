# Instructor Validation — Data Testing Stage 1

Before finalizing Assignment 4 infrastructure:

```bash
bash environment/data-testing/run_checks.sh
```

Expected:

- 200 synthetic patients generated;
- related encounters and vitals generated;
- validator reports `VALIDATION PASSED`;
- generator unit tests pass.

Then test controlled corruption:

```bash
cp -R .project-vital/data-testing/validation-small \
      .project-vital/data-testing/validation-broken

python3 environment/data-testing/corrupt_data.py \
  .project-vital/data-testing/validation-broken \
  --defect orphan-vitals

python3 environment/data-testing/validate_data.py \
  .project-vital/data-testing/validation-broken
```

Expected: validation fails.

Generate medium/high:

```bash
python3 environment/data-testing/generate_data.py \
  --size medium --seed 42 \
  --output .project-vital/data-testing/medium

python3 environment/data-testing/validate_data.py \
  .project-vital/data-testing/medium

python3 environment/data-testing/generate_data.py \
  --size high --seed 42 \
  --output .project-vital/data-testing/high

python3 environment/data-testing/validate_data.py \
  .project-vital/data-testing/high
```

Finally start the normal OpenEMR environment and capture the exact schema:

```bash
cd environment
docker compose up -d
cd ..

bash environment/data-testing/inspect_openemr_schema.sh
```

Review:

```text
.project-vital/data-testing/schema/
```

The next infrastructure step is to build the loader against these validated table definitions.
