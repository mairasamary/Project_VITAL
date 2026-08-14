# Project VITAL — Assignment 3: Unit Testing and Continuous Integration

**Team Assignment | OpenEMR | PHPUnit | GitHub Actions**

## Purpose

In Assignment 1, you learned what OpenEMR does. In Assignment 2, you investigated how a selected workflow is implemented. In Assignment 3, you will test at the smallest practical scope: an individual function, class, or small component, and configure Continuous Integration (CI) so tests run automatically when code changes.

## Learning Objectives

By the end of this assignment, you should be able to:

1. Select and justify an appropriate unit-testing scope in an unfamiliar production codebase.
2. Design and implement meaningful unit tests covering expected, boundary, invalid, and risk-based behavior.
3. Evaluate software testability and the impact of dependencies and global state.
4. Use PHPUnit evidence to execute, diagnose, and improve unit tests.
5. Configure GitHub Actions so tests execute automatically and failures are visible.
6. Explain the limits of unit testing and identify behaviors requiring broader test levels.

## Part 0 — Validate Your Environment

From the root of your team repository:

```bash
bash environment/unit-testing/setup-unit-tests.sh
mkdir -p assignment-03/tests
cp environment/unit-testing/examples/ProjectVITALSmokeTest.php \
   assignment-03/tests/ProjectVITALSmokeTest.php
bash environment/unit-testing/run-unit-tests.sh
```

A successful environment should end with output similar to:

```text
OK (2 tests, 2 assertions)
```

Exact PHP/PHPUnit patch versions and timing may differ. The smoke test verifies the environment only and **does not count toward the six meaningful unit tests required for this assignment**.

Your graded tests belong in `assignment-03/tests/`. The helper scripts use a temporary OpenEMR checkout under `.project-vital/openemr-unit/`. Do not edit that cache as the authoritative version of your work and do not commit `.project-vital/`.

## Part A — Select an Appropriate Unit

Return to your Assignment 2 architecture investigation and identify one small component related to the workflow you investigated. A complete patient/appointment/encounter workflow is too large.

Suitable targets may include a function, class, validator, formatter, parser, calculator, helper, value object, utility, or small service.

Document the Assignment 2 workflow, source file path, class/function, responsibility, inputs, outputs, dependencies, and why this is an appropriate **unit** rather than an integration/system-test target.

## Part B — Evaluate Testability

Inspect whether the target depends on databases, global state, environment variables, files, network/services, time/date, sessions, randomness, or other difficult-to-isolate resources.

Create a table:

| Characteristic | Observation | Impact on Unit Testing |
|---|---|---|
| Database dependency | ... | ... |
| Global/config state | ... | ... |
| Time/files/services | ... | ... |

Rate testability as **High, Medium, or Low** and justify the rating. If the target cannot reasonably be tested in the isolated environment, reconsider the target rather than silently turning this into an integration test.

## Part C — Study Existing OpenEMR Tests

Locate at least two existing OpenEMR isolated/unit tests. For each, identify the test file, production code, framework, structure, an assertion, required setup, and one practice you could reuse. Do not copy an existing test and present it as your own.

## Part D — Design Tests Before Implementing Them

Design at least **6 meaningful tests**, including at least 2 normal cases, 2 boundary/edge cases, 1 invalid/error/exception case, and 1 additional risk-based case.

| Test ID | Behavior / Requirement | Input | Expected Result | Category | Why It Matters |
|---|---|---|---|---|---|
| UT-01 | ... | ... | ... | Normal | ... |

A test must make a meaningful assertion; simply executing code is insufficient.

## Part E — Implement the Tests

Implement tests in:

```text
assignment-03/tests/YourSelectedComponentTest.php
```

Use PHPUnit and meaningful names/assertions. Tests should be deterministic and isolate the target as much as practical.

Think in terms of:

```text
ARRANGE → ACT → ASSERT
```

Implement at least **6 passing, meaningful unit tests**. Quality and diversity matter more than raw count.

## Part F — Data-Driven Testing

At least one behavior should use a PHPUnit data-driven/parameterized approach. Explain why the cases belong together, what varies, what remains constant, and why the approach improves the suite.

## Part G — Run Locally

Run all Assignment 3 tests:

```bash
bash environment/unit-testing/run-unit-tests.sh
```

Or one test file:

```bash
bash environment/unit-testing/run-unit-tests.sh YourSelectedComponentTest.php
```

Record the command, tests/assertions reported, result, and execution time if shown.

## Part H — Prove the Local Runner Detects Failure

Temporarily alter one expected result in **your own test** so it is deliberately wrong. Run the suite and confirm PHPUnit reports failure. Restore the correct expectation and rerun.

Required evidence:

```text
GREEN → deliberate incorrect expectation → RED → restore → GREEN
```

Do not leave the broken expectation in the final submission.

## Part I — Coverage

Measure focused coverage for the selected unit when supported by the course environment. Do not try to maximize coverage across all OpenEMR.

Explain what is covered, what remains uncovered, whether that matters, and why 100% coverage would not prove correctness.

## Part J — Configure Continuous Integration

Create the workflow from the validated Project VITAL template:

```bash
mkdir -p .github/workflows
cp environment/unit-testing/github-actions-unit-tests.template.yml \
   .github/workflows/unit-tests.yml
```

The pipeline checks out the team repository and pinned OpenEMR source, prepares PHP/Composer, copies Assignment 3 tests, and executes PHPUnit.

## Part K — Push the Workflow

Create a feature branch:

```bash
git switch -c feature/unit-tests
git status
git add assignment-03 .github/workflows/unit-tests.yml
git commit -m "Add Assignment 3 unit tests and CI"
git push -u origin feature/unit-tests
```

Open GitHub **Actions** and locate **Project VITAL Unit Tests**. Confirm that the workflow runs automatically.

### If GitHub rejects the workflow push

GitHub applies additional authorization to `.github/workflows/`. If a push fails with a message mentioning `workflow` scope and you use GitHub CLI:

```bash
gh auth refresh -h github.com -s workflow
gh auth setup-git
gh auth status
git push
```

Confirm the appropriate workflow authorization is present. Never place tokens in the repository. See `environment/unit-testing/GITHUB_ACTIONS_SETUP.md` for detailed troubleshooting.

## Part L — Verify Green CI

Record the successful Actions run: branch, commit, workflow name, result, and approximate duration. The workflow run itself is primary evidence; screenshots may supplement it.

## Part M — Prove CI Detects Failure

Create:

```bash
git switch -c experiment/ci-failure
```

Temporarily make one of your expected results deliberately incorrect, then:

```bash
git add assignment-03/tests
git commit -m "Experiment: verify CI detects failing unit test"
git push -u origin experiment/ci-failure
```

The desired result is **RED**. Inspect which test and workflow step failed and what PHPUnit reported.

## Part N — Restore CI to Green

Restore the correct expectation:

```bash
git add assignment-03/tests
git commit -m "Restore passing unit test"
git push
```

The required CI evidence is:

```text
GREEN → RED → GREEN
```

## Part O — Analyze a Failure

Analyze one meaningful failure encountered during the assignment. Explain what failed, the failure message, your initial hypothesis, evidence inspected, actual cause, correction, and what you learned. The objective is evidence-based diagnosis, not merely making output green.

## Part P — Identify Unit-Test Limits

Identify one important behavior related to your component that these unit tests cannot adequately verify. Explain whether integration, system, or acceptance testing is the appropriate next level and why.

## Required Deliverables

1. Unit-test target and scope justification.
2. Testability assessment and rating.
3. Analysis of at least two existing OpenEMR tests.
4. Unit-test design table with at least six tests.
5. At least six meaningful passing unit tests.
6. At least one data-driven/parameterized test.
7. Local GREEN → RED → GREEN evidence.
8. Focused coverage analysis when supported.
9. `.github/workflows/unit-tests.yml`.
10. CI GREEN → RED → GREEN evidence.
11. Failure analysis.
12. Testing-level reflection.
13. AI Verification Log if generative AI was used.

## Recommended Repository Structure

```text
VITAL-Team-XX/
├── assignment-03/
│   ├── README.md
│   ├── test-target.md
│   ├── testability.md
│   ├── existing-tests.md
│   ├── test-design.md
│   ├── coverage.md
│   ├── failure-analysis.md
│   ├── testing-levels.md
│   ├── ai-verification-log.md
│   └── tests/
│       ├── ProjectVITALSmokeTest.php
│       └── YourSelectedComponentTest.php
└── .github/
    └── workflows/
        └── unit-tests.yml
```

The smoke test may remain as environment evidence but does not count toward the six required tests.

## Evaluation

| Criterion | Weight |
|---|---:|
| Unit selection and testability analysis | 15% |
| Unit test design | 20% |
| Unit test implementation | 20% |
| Parameterized testing and coverage analysis | 10% |
| Continuous Integration | 20% |
| Red → Green experiment and failure diagnosis | 10% |
| Testing-level reflection and communication | 5% |
| **Total** | **100%** |

## Use of Generative AI

Generative AI may be used as an investigation/learning aid subject to the course policy—for example, to explain PHP/PHPUnit syntax, propose test cases or boundaries, explain failures, or discuss CI/testability.

However, **AI-generated tests are not evidence that behavior is correct**. Your team must verify expected results, production-code meaning, scope, assertions, determinism, and relevance. Never provide credentials, tokens, real patient information, or other sensitive data.

If AI is used, document at least two meaningful suggestions:

| AI Suggestion | How We Verified It | Result |
|---|---|---|
| ... | ... | Useful / Modified / Rejected |

At least one entry must demonstrate evaluation rather than automatic acceptance.

## Submission

Submit according to the Project VITAL Student Submission Guide.

Required tag:

```text
assignment-03
```

Before tagging, confirm all deliverables are committed, six meaningful tests pass, local and CI runs are green, deliberate failures are restored, `.project-vital/` is not committed, and no credentials/real patient data are included.

```bash
git tag assignment-03
git push origin assignment-03
```

Submit the repository reference and `assignment-03` tag through the LMS.

## Workflow Summary

```text
Validate environment
      ↓
Select unit + assess testability
      ↓
Study existing tests
      ↓
Design 6+ tests
      ↓
Implement + run locally
      ↓
GREEN → RED → GREEN
      ↓
Configure GitHub Actions
      ↓
CI GREEN → RED → GREEN
      ↓
Analyze coverage/failure
      ↓
Explain limits of unit testing
      ↓
Tag assignment-03
```
