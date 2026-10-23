# Continuous Privacy Testing and Regression Report

**Team:** [ ]
**Contributors:** [ ]
**Date / commit:** [ ]

> Use Project VITAL synthetic data only. Do not commit secrets or patient data. Passing a k threshold does not certify anonymity.


## Part 7 — CI workflow
**Workflow:** `.github/workflows/privacy-tests.yml`

| Stage | Script/command | Expected result | Observed result |
|---|---|---|---|
| Generate deterministic synthetic source | [ ] | [ ] | [ ] |
| Create research export | [ ] | [ ] | [ ] |
| Check prohibited identifiers | [ ] | [ ] | [ ] |
| Validate pseudonymous links | [ ] | [ ] | [ ] |
| Evaluate k >= 3 | [ ] | [ ] | [ ] |
| Check analytical utility | [ ] | [ ] | [ ] |
| Run negative tests | [ ] | Defects rejected | [ ] |

## Part 8 — GREEN → RED → GREEN
| Stage | Commit SHA/link | Change | GitHub Actions run URL | Outcome |
|---|---|---|---|---|
| GREEN: baseline | [ ] | [ ] | [ ] | [ ] |
| RED: deliberate regression | [ ] | [ ] | [ ] | [ ] |
| GREEN: restored | [ ] | [ ] | [ ] | [ ] |

**What meaningful privacy regression did you introduce?** [ ]

**Which automated check detected it, and why?** [ ]

**How did you restore correct behavior?** [ ]

## Required analysis — Nine questions
1. Direct identifier vs. quasi-identifier: [ ]
2. Why pseudonymization is not anonymization: [ ]
3. Effect of initial quasi-identifiers on class sizes: [ ]
4. Changes made to improve selected k: [ ]
5. Utility preserved: [ ]
6. Utility reduced: [ ]
7. Why passing selected k does not prove anonymity: [ ]
8. Privacy regression detected by CI: [ ]
9. Remaining risks beyond automated tests: [ ]

## Final checklist
- [ ] Six report templates completed
- [ ] Transformation and validation code committed
- [ ] Negative privacy tests demonstrate rejection
- [ ] GREEN → RED → GREEN run links supplied
- [ ] Final CI green
- [ ] No secrets or real patient data committed
