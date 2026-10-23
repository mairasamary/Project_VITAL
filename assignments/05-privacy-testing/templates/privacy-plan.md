# Privacy Plan and Field Classification

**Team:** [ ]
**Contributors:** [ ]
**Date / commit:** [ ]

> Use Project VITAL synthetic data only. Do not commit secrets or patient data. Passing a k threshold does not certify anonymity.


## Part 1 — Classify source attributes
Inspect synthetic `patients.csv`, `encounters.csv`, and `vitals.csv`. Add rows.

| Table | Field | Type: direct / quasi / analytical / relational | Why? | Export action |
|---|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] | [ ] |

**Why is deleting direct identifiers insufficient?** [ ]

**Which patient, encounter, and vitals relationships must remain intact?** [ ]

## Part 2 — Transformation plan
| Requirement | Implementation plan | Validation method |
|---|---|---|
| Remove prohibited direct identifiers | [ ] | [ ] |
| Stable subject pseudonyms | [ ] | [ ] |
| Preserve encounter-to-subject links | [ ] | [ ] |
| Preserve vitals-to-subject/encounter links | [ ] | [ ] |
| Generalize geography and dates | [ ] | [ ] |
| Deterministic output | [ ] | [ ] |
| Keep pseudonymization secret out of Git | [ ] | [ ] |

**Pseudonymization vs. anonymization:** [ ]

**Risks and assumptions:** [ ]

**Evidence (files/commits/commands):** [ ]
