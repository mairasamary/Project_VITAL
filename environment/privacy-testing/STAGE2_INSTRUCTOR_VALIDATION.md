# Stage 2 Instructor Validation — Privacy Testing

Stage 1 established an important result on the 200-patient seed-42 dataset:

```text
age_band + sex + state + postal_prefix
minimum k = 1
7 patients unique on those quasi-identifiers
```

This is exactly the privacy lesson we wanted: removal of direct identifiers plus stable pseudonyms does not automatically make a dataset anonymous.

## Stage 2 goals

Stage 2 validates:

- controlled k-threshold failure;
- stronger generalization;
- preservation of important analytical utility;
- direct-identifier leakage detection;
- pseudonymous referential-integrity detection.

Run:

```bash
bash environment/privacy-testing/run_stage2_validation.sh
```

The baseline strategy is expected to fail a `k >= 3` threshold if small equivalence classes remain.

The stronger strategy uses:

```text
20-year age bands
state-level geography
sex suppressed
year-level encounter time
```

For this synthetic teaching dataset, we test whether that strategy reaches the selected teaching threshold.

Passing `k >= 3` does **not** certify anonymity, HIPAA de-identification, GDPR anonymization, or compliance with any external privacy regime. It is only one measurable property under the stated quasi-identifier model.

## Utility

The utility report intentionally checks whether some analyses remain possible after transformation, including:

- patient/encounter/vitals counts;
- encounter reason distribution;
- selected vitals aggregates.

Students should later identify analyses that are *lost* because of generalization, such as exact-age or exact-date analysis.

## Next stage

If Stage 2 passes, build:

1. privacy CI;
2. GREEN → RED → GREEN privacy validation;
3. final student Assignment 5;
4. instructor guide.
