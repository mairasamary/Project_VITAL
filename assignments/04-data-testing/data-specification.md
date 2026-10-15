# Assignment 4 — Data Specification

**Team:** [team]  
**Assignment 2 workflow:** [Patient Registration / Appointment Scheduling / Recording Vital Signs]  
**Dataset level(s):** Small (200), Medium (2,000), Large (20,000)  
**Seed for submitted fixtures:** `42`

## 1. Scope and evidence sources
Explain which entities and workflows are in scope. Cite the specific OpenEMR schema, source files, observed UI behavior, Assignment 2 artifacts, or course fixture documentation you consulted.

| Source / artifact | Location or reference | What it establishes | Limitations |
|---|---|---|---|
| [source] | [path/link] | [observation] | [uncertainty] |

## 2. Entities, fields, and identifiers
Document patients, encounters, appointments, and vital-sign records as applicable. Do not infer constraints from field names alone.

| Entity / table | Field | Type or representation | Required / optional? | Identifier or relationship? | Supporting evidence |
|---|---|---|---|---|---|
| [entity] | [field] | [type] | [status] | [role] | [reference] |

## 3. Relationships and cardinality
Describe expected parent-child links, identifier mappings, and any relationships enforced by application logic rather than database constraints.

| Parent | Child | Linking fields | Expected cardinality | Evidence / uncertainty |
|---|---|---|---|---|
| [parent] | [child] | [fields] | [relationship] | [reference] |

## 4. Proposed data-quality rules
For each rule, mark **Evidence-supported** or **Hypothesis requiring verification**. Distinguish the database's technical constraints from application-level expectations.

| Rule ID | Property (completeness / validity / uniqueness / consistency / referential integrity) | Precise rule | Status | Justification and evidence |
|---|---|---|---|---|
| DQ-01 | [property] | [testable statement] | [supported/hypothesis] | [source] |

## 5. Dataset generation assumptions
Explain how identifiers, dates, categories, related records, and measurements are produced. Synthetic vital CSVs use **pounds** for weight and **inches** for height; verify the expected representations against the course environment documentation.

## 6. Open questions and limitations
- [Unverified assumption and how the team will investigate it]
