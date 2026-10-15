# Assignment 4 — Three-Level Data-Testing Comparison

## 1. Experimental setup
**Dataset seed:** `42`  
**Generator / validator / loader versions or paths:** [paths]  
**Benchmark implementation:** `assignment-04/scripts/benchmark.py` (or equivalent)  
**Hardware / software / Docker conditions:** [description]

Use separate newly initialized A4 database projects and volumes for each load. Do not overwrite an existing populated database.

## 2. Reproducible procedure
List exact generation, validation, loading, and SQL verification commands. State how timing was measured and whether runs were repeated.

## 3. Results
| Metric | Small | Medium | Large |
|---|---:|---:|---:|
| Patient count (target) | 200 | 2,000 | 20,000 |
| Encounter count | | | |
| Appointment count | | | |
| Vital-record count | | | |
| Generation time (seconds) | | | |
| Pre-load validation time (seconds) | | | |
| Load time (seconds) | | | |
| Attempted / committed / rejected | | | |
| Validation errors | | | |
| Post-load count checks | | | |

## 4. Reproducibility check
Generate a fixture twice using the same level and seed. Explain how you compared content equivalence (not merely filenames). Link logs, hashes, or test output.

## 5. Analysis
What changed across levels? Did related record counts scale as expected? Did new integrity failures appear? What resource limits or environmental factors affected results?

## 6. Claims you can and cannot make
**Data volume is not concurrent workload.** Explain why these baseline timings are not rigorous proof of application scalability. Note the need for repetitions, workload controls, warm-up, and other controls for a stronger performance study.

## 7. Evidence and limitations
Link benchmark code, machine-readable results, relevant queries, and representative logs. State uncertainty and unexpected outcomes.
