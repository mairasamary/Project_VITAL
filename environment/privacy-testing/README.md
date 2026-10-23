# Project VITAL Privacy-Testing Infrastructure — Stage 1

This is the first instructor-validation stage for Assignment 5.

It deliberately begins with **pseudonymization**, not a claim of anonymization.

The source is the synthetic dataset already produced by Project VITAL's data-testing generator. Its patient records contain fields such as first/last name, date of birth, email, phone, city, state, and postal code. The Stage 1 export:

- removes direct identifiers;
- replaces internal keys with stable HMAC-based pseudonyms;
- preserves patient → encounter → vitals relationships;
- generalizes date of birth to a 10-year age band;
- generalizes postal code;
- reduces exact timestamps to month;
- measures equivalence classes across selected quasi-identifiers.

## Run

From the repository root:

```bash
bash environment/privacy-testing/run_stage1_validation.sh
```

Expected final line:

```text
STAGE 1 PRIVACY VALIDATION PASSED
```

Before that, inspect the reported `Minimum k` and number of patients unique on the selected quasi-identifiers.

A low k is **not** an infrastructure failure at this stage. It is evidence that removing direct identifiers is not enough to establish anonymity.

## Important terminology

The generated export is intentionally called **pseudonymized**.

Stable pseudonyms preserve longitudinal linkage, which is useful for research, but they also mean this exercise must not represent the output as automatically or irreversibly anonymous.

`validate_privacy_export.py --min-k N` is a teaching privacy check over a selected quasi-identifier model. Passing a chosen k threshold is not, by itself, proof that a dataset is anonymous or legally de-identified.

## Next validation stage

After Stage 1 works, build Stage 2 around:

1. controlled direct-identifier leakage;
2. broken pseudonymous relationships;
3. stronger quasi-identifier generalization/suppression;
4. k-threshold experiments;
5. explicit utility measurements.

Only after those experiments are stable should we write the final student Assignment 5.
