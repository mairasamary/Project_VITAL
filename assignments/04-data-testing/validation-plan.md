# Assignment 4 — Data-Quality Validation Plan

**Complete this plan before reviewing validation outcomes.**

## 1. Validation scope
Which dataset files, OpenEMR entities, and Assignment 2 workflow expectations will be tested? What is explicitly outside scope?

## 2. Rule-to-test matrix
Cover completeness, validity, uniqueness, consistency, and referential integrity. For each rule, explain the source of the expectation and whether it is enforced by the database, application, or your validator.

| Test ID | Property | Data-quality rule | Supporting evidence | Method / query / script | Expected result | Severity |
|---|---|---|---|---|---|---|
| V-01 | [property] | [rule] | [source] | [procedure] | [observable outcome] | [severity] |

## 3. Pre-load validation: small, medium, large
Record the level, seed, patient count, related-record counts, rules executed, errors, and status. Include commands and output file paths. **Starter validator PASS does not establish completeness of your test plan.**

| Level | Seed | Expected patients | Actual patients | Encounters | Appointments | Vitals | Rules / failures | Result | Evidence |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| Small | 42 | 200 | | | | | | | |
| Medium | 42 | 2,000 | | | | | | | |
| Large | 42 | 20,000 | | | | | | | |

## 4. Team-developed validation
Describe tests beyond the provided `environment/data-testing/scripts/validate_data.py`. Identify the exact script/test path, how to run it, and a representative assertion.

## 5. Post-load database checks
For each level, record attempted, committed, rejected, and observed database records. Link SQL queries and saved results; compare actual state with the fixture and specification.

| Level | Check / SQL evidence | Expected | Observed | Interpretation |
|---|---|---|---|---|
| [level] | [query/path] | [expected] | [actual] | [meaning] |

## 6. UI spot checks
Choose a small, purposeful sample for each level. Explain why each record was selected; compare UI, database, and fixture observations. State why a sample cannot prove the full dataset is correct.

## 7. Gaps and limitations
What properties do the supplied and team-written validators **not** check? Which rules are still hypotheses?
