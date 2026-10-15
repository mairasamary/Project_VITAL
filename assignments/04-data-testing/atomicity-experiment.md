# Assignment 4 — Atomicity Experiment

## 1. Question and prediction
Describe a multi-record operation in the **isolated A4 database**. What does it mean for this operation to be atomic? Predict what should remain after a failure midway through.

## 2. Safety and initial state
**Docker Compose project / database:** [dedicated A4 project]  
**Baseline record counts and query evidence:** [paths]  
**Confirmation that this is not the A1–A3 database:** [evidence]

## 3. Operation and controlled failure
| Step | Intended database change | Failure point? | Expected state |
|---|---|---|---|
| 1 | [change] | No | [prediction] |
| 2 | [change] | [Yes/No] | [prediction] |

Provide reproducible commands or a script path. Explain the transaction boundaries and whether autocommit or explicit transactions are involved. Do not assume the loader automatically makes every multi-record operation atomic.

## 4. Actual results
| Evidence / SQL query | Before | After failure | Expected if atomic? |
|---|---|---|---|
| [query/path] | [state] | [state] | [yes/no] |

## 5. Interpretation
Did the **observed operation** behave atomically? What does the evidence establish? Could partial completion create an inconsistent patient/encounter/appointment/vital record set? Distinguish observations from assumptions.

## 6. Cleanup and limitations
Document safe rollback or cleanup within the isolated experiment and any unresolved questions.
