# Project VITAL

**Verification, Integration, Testing, Accessibility & Lifecycle**

Project VITAL is an open educational software-testing kit built around a real-world open-source software system. The initial implementation uses **OpenEMR** as the System Under Test (SUT), while the course structure is designed so instructors can adapt the materials to other open-source systems.

## Purpose

Project VITAL helps students learn how to understand, test, evaluate, and continuously verify a substantial software system that they did not build themselves. The emphasis is on testing strategy, evidence, reproducibility, and software quality rather than on learning OpenEMR or PHP as ends in themselves.

## Core Learning Areas

The project is designed to support:

- System understanding: architecture, URL/workflow maps, data models, and dependencies
- Unit, integration, system, and acceptance testing
- Continuous testing and CI
- Accessibility testing and WCAG
- Data testing, synthetic-data generation, anonymization, integrity, and reproducibility
- Security testing in isolated environments
- Test design based on stakeholder requirements and use cases

## Course Model

The complete project is intended to span approximately **10–12 weeks**, with modules that can also be adopted independently.

Students work primarily in **teams of 3–4**, combining guided in-class activities with out-of-class testing, implementation, analysis, and documentation. Instructors may add individual reflections, quizzes, oral check-ins, or code reviews to assess individual understanding.

## System Under Test

The reference implementation uses a **pinned stable OpenEMR release** deployed in an isolated Docker-based environment.

OpenEMR is not vendored into this repository. Environment configuration will retrieve the designated version so that students and instructors work from a reproducible baseline.

Only synthetic or appropriately anonymized data should be used. Project VITAL is not intended for testing against production healthcare systems or real patient data.

## Repository Structure

- `assignments/` — student-facing testing modules and assignments
- `instructor/` — instructor guidance, adoption notes, and teaching resources
- `rubrics/` — assessment criteria
- `docs/` — architecture and project documentation
- `environment/` — reproducible OpenEMR/Docker course environment
- `tests/` — reference testing infrastructure and examples
- `data/` — synthetic-data generation and anonymization tooling
- `.github/` — GitHub templates and continuous-testing workflows

## Privacy and Data Handling

Project VITAL follows a **data-minimization approach**.

- No real patient or protected health information (PHI) is required.
- Testing activities should use synthetic or appropriately anonymized data.
- Grades and other education records should remain in institution-approved systems, not in public repositories.
- Student work should not be incorporated into the public project without appropriate permission.
- Instructors should follow their institution's FERPA, privacy, data-retention, and approved-technology policies.

## Licensing

Project VITAL uses a dual-license approach:

- Educational materials and documentation are licensed under **CC BY-SA 4.0**.
- Original software, scripts, test infrastructure, and configuration are licensed under **GPL-3.0-or-later**.

See `LICENSE.md` for details.

OpenEMR remains subject to its own license and is not redistributed as part of this repository.

## Status

Project VITAL is under active development. The initial repository structure and reference OpenEMR testing environment are being developed first, followed by the individual testing modules.
