# Assignment 4 — Controlled Defect Injection (GREEN → RED → GREEN)

## 1. Rule under test
**Rule ID and description:** [reference your validation plan]  
**Evidence that makes this a defect:** [schema/source/observed behavior/fixture requirement]

## 2. Experimental setup
**Isolated fixture path:** [path]  
**Dataset level and seed:** [level, seed]  
**Validator command(s):** [exact commands]  
**Safety:** Work on a disposable synthetic fixture, not real patient data or the original A1–A3 database.

## 3. GREEN — valid baseline
| Command / evidence | Expected | Observed |
|---|---|---|
| [command or log path] | PASS | [result] |

## 4. RED — introduce one controlled defect
**Single modification made:** [describe before/after without altering unrelated fields]  
**Prediction:** [specific rule and error expected]

| Command / evidence | Expected detection | Observed detection |
|---|---|---|
| [command or log path] | [failure] | [result] |

## 5. GREEN — repair or regenerate
Describe how you restored the original valid fixture and reran validation.

| Command / evidence | Expected | Observed |
|---|---|---|
| [command or log path] | PASS | [result] |

## 6. Interpretation and limitations
What does the failure demonstrate about the validator? What does it **not** establish? Confirm that no deliberate defect remains in submitted data.
