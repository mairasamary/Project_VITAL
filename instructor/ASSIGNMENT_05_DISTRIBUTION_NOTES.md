# Assignment 5 — Distribution and Instructor Notes

**Due:** Thursday, November 5, 2026, 11:59 p.m. Eastern Time.

This package adapts the existing Project VITAL Assignment 05 privacy-testing materials and instructor-validated privacy-testing infrastructure. The rubric follows the 100-point distribution in the existing instructor guide.

## Before distributing
1. Merge the package into the **instructor** repository at the repository root, preserving paths.
2. Confirm `environment/data-testing/generate_data.py` already exists (from Assignment 4). It is not duplicated in this package.
3. Run `bash environment/privacy-testing/run_privacy_ci_checks_local.sh` from the repo root and inspect results. Scripts regenerate `.project-vital/privacy-testing/`.
4. Verify `.github/workflows/privacy-tests.yml` runs on a feature branch and on `main` with the actual repository's GitHub Actions settings.
5. Copy only the intended student-facing assignment, starter templates, and infrastructure into team repositories. Keep `instructor/` private to the instructor.
6. Confirm the course/LMS deadline and whether a Git tag is required; no tag is mandated here.

## Teaching notes
- Baseline small equivalence classes are a teaching result, not necessarily an error.
- Reference instructor runs (200 patients, seed 42) observed baseline min-k 1 and stronger min-k 9; these are reference observations, not guaranteed values for modified data.
- Do not award full privacy credit for pseudonymization alone or claim k>=3 is proof of anonymity.
- Assess student interpretation and verification, not writing polish or assumed AI use.
- The supplied privacy workflow includes a teaching-only example secret; never reuse it with real data.

## Status
Package assembled from existing materials. Live GitHub Actions and full environment tests must be checked after integration into the semester repository.
