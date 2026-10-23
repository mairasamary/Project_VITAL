# Assignments

This directory contains student-facing Project VITAL modules and assignments.

The planned sequence is designed to move from **system understanding** to increasingly broad testing scopes and quality dimensions.

## Planned Modules

1. System Understanding
   - C4 model
   - URL/workflow flow map
   - ERD / ORM relationships
   - module/package dependency graph

2. Unit Testing

3. Integration Testing

4. System Testing

5. Continuous Testing

6. Accessibility Testing
   - WCAG
   - automated and manual checks

7. Data Testing
   - anonymization
   - synthetic-data generation
   - atomicity
   - insertion order
   - reproducibility
   - small / medium / high data volumes

8. Security Testing
   - controlled SQL injection testing
   - availability/load-related testing in isolated environments

9. Acceptance Testing
   - stakeholder use cases
   - acceptance criteria
   - end-to-end validation

Assignments should be designed so instructors may use the entire sequence or adopt individual modules independently.

## Fall 2026 Assignment Releases

| Assignment | Topic | Status |
|---|---|---|
| 1 | [System Exploration](01-system-exploration/README.md) | Released |
| 2 | [System Architecture](02-system-architecture/README.md) | Released |
| 3 | [Unit Testing and CI](03-unit-testing-ci/README.md) | Released |
| 4 | [Data Testing](04-data-testing/README.md) | Released |
| 5 | [Privacy Testing](05-privacy-testing/README.md) | Released |

**Assignment 5 deadline:** November 5, 2026, 11:59 PM ET.

The instructor repository also contains future modules.
Their presence does not mean they have been released to students.

## Fall 2026 Implementation

The planned modules above describe the reusable Project VITAL curriculum.
The actual sequence used in **CSCI3364 — Software Testing, Quality and
Security, Fall 2026** is documented below.

| Assignment | Topic | Status |
|---|---|---|
| 1 | [System Exploration](01-system-exploration/README.md) | Released |
| 2 | [System Architecture](02-system-architecture/README.md) | Released |
| 3 | [Unit Testing and Continuous Integration](03-unit-testing-ci/README.md) | Released |
| 4 | [Data Testing: Quality, Integrity, and Scale](04-data-testing/README.md) | Released |
| 5 | [Privacy Testing](05-privacy-testing/README.md) | Released |

### Assignment 5 — Privacy Testing

**Due:** November 5, 2026, at 11:59 PM Eastern.

Assignment 5 builds on synthetic data testing and addresses:

- direct identifiers and quasi-identifiers;
- pseudonymization and referential integrity;
- re-identification risk and equivalence-class analysis;
- generalization, suppression, and privacy-versus-utility tradeoffs;
- automated negative privacy tests;
- continuous privacy validation using GitHub Actions;
- a controlled GREEN → RED → GREEN privacy regression experiment.

Students complete six guided Markdown report templates in their
private team repositories.

### Instructor and Student Repositories

This instructor/model repository maintains the reusable curriculum,
assignment specifications, and supporting materials.

The official Fall 2026 student course repository is:

https://github.com/CSCI3364-Fall2026/Project_VITAL

Private team repositories contain student implementations and evidence.

**Important:** Future modules present in this instructor repository
are not automatically released to students. The official course
repository determines which assignments are active.
