# Project VITAL — Assignment 3: Unit Testing and Continuous Integration

**Team Assignment | OpenEMR | PHPUnit | GitHub Actions**

## Purpose

In Assignment 1, you investigated **what OpenEMR does**. In Assignment 2, your team investigated **how one OpenEMR workflow works** through user-visible behavior, HTTP requests, source code, components, dependencies, and data.

In Assignment 3, you will ask:

> **What part of this implementation can we test independently and automatically?**

You will identify a small unit related to your Assignment 2 workflow, evaluate whether it is practical to test in isolation, design and implement meaningful unit tests, and configure Continuous Integration (CI) so those tests run automatically when code changes.

The goal is not simply to make PHPUnit display green output. The goal is:

**architecture → testable unit → test design → evidence → automated feedback**

## Start Here

Your private team repository already contains the Assignment 3 workspace and CI configuration.

Before selecting a unit or writing your graded tests:

1. **Pull the latest version of your team repository.**

   ```bash
   git pull

## Connection to Assignment 2

Continue with the workflow your team investigated in Assignment 2. The course teams investigated:

1. **Patient Registration**
3. **Appointment Scheduling**
5. **Recording Vital Signs**

Your Assignment 3 unit must have a defensible relationship to your team's Assignment 2 workflow.

> **Your workflow is not your unit.**

Each workflow crosses multiple parts of OpenEMR. Use your Assignment 2 artifacts to move toward a smaller piece of implementation:

```text
Assignment 2 Workflow
        ↓
Component Diagram
        ↓
Source-Code Investigation
        ↓
Dependency Map
        ↓
Candidate Function / Class / Helper
        ↓
Can it reasonably be isolated?
       / \
     YES  NO
      ↓    ↓
    TEST   Investigate a smaller
           or more suitable unit
```

A target might be a function, class, validator, formatter, parser, calculator, helper, value object, utility, or small service. These are examples of *kinds* of targets, not specific OpenEMR answers.

## Learning Objectives

By the end of this assignment, you should be able to:

1. Use architectural evidence to identify a testable unit in an unfamiliar production codebase.
2. Distinguish a unit from a workflow, subsystem, integration, or end-to-end behavior.
3. Evaluate testability and recognize dependencies that make isolation difficult.
4. Design meaningful normal, boundary, invalid, and risk-based unit tests.
5. Implement deterministic PHPUnit tests.
6. Use data-driven/parameterized testing appropriately.
7. Interpret failures as evidence rather than merely trying to make tests green.
8. Configure GitHub Actions to run tests automatically.
9. Demonstrate that local testing and CI can detect failure.
10. Explain what unit testing cannot establish.

## Part 0 — Validate Your Environment

From the root of your team repository:

```bash
bash environment/unit-testing/setup-unit-tests.sh
mkdir -p assignment-03/tests
cp environment/unit-testing/examples/ProjectVITALSmokeTest.php assignment-03/tests/ProjectVITALSmokeTest.php
bash environment/unit-testing/run-unit-tests.sh
```

A successful environment should end with output similar to:

```text
OK (2 tests, 2 assertions)
```

Exact PHP/PHPUnit patch versions and timing may differ. The smoke test verifies the environment only and **does not count toward the six meaningful unit tests required**.

Your graded tests belong in `assignment-03/tests/`. The helper scripts use a temporary OpenEMR checkout under `.project-vital/openemr-unit/`. Do not edit that cache as the authoritative version of your work and do not commit `.project-vital/`.

## Part A — From Your Assignment 2 Workflow to a Unit

Review your Assignment 2 workflow definition, HTTP trace, C4 component diagram, source-code investigation, focused ERD, dependency map, and architecture-informed testing analysis.

Identify **2–3 possible unit-testing targets** related to your workflow.

| Candidate | Source Location | Responsibility | Inputs / Outputs | Important Dependencies | Initial Testability |
|---|---|---|---|---|---|
| Candidate 1 | ... | ... | ... | ... | High / Medium / Low |
| Candidate 2 | ... | ... | ... | ... | High / Medium / Low |
| Candidate 3, if needed | ... | ... | ... | ... | High / Medium / Low |

Select **one** target and explain:

1. How is it connected to your Assignment 2 workflow?
2. What evidence indicates that it participates in or supports the workflow?
3. Why is it small enough to be considered a unit?
4. What are its observable inputs and outputs?
5. What dependencies might make isolation difficult?
6. Why did you select it instead of the other candidate(s)?

Do not select an unrelated utility merely because it is easy to test.

## What Counts as a Unit?

For this assignment, think of a unit as:

> **the smallest practical piece of behavior that your team can exercise deterministically and meaningfully in isolation.**

A good candidate generally lets you control inputs, observe outputs/effects, repeat the test with the same result, and minimize dependence on the complete application, browser, database, network, session, filesystem, clock, and global state.

A target may initially appear suitable and turn out not to be. That discovery is useful. If substantial dependencies make isolation unreasonable, document what you learned and select a better target. Do **not** silently turn the assignment into an integration or system test.

## Part B — Evaluate Testability

Investigate the dependencies of your selected target.

| Characteristic | Observation / Evidence | Impact on Unit Testing |
|---|---|---|
| Database dependency | | |
| Global state | | |
| Configuration / environment | | |
| Session state | | |
| Date / time | | |
| Filesystem | | |
| Network / external service | | |
| Randomness | | |
| Other application components | | |

Rate overall testability as **High, Medium, or Low** and justify the rating using evidence.

Consider whether inputs are controllable, outputs observable, results repeatable, application initialization is required, a database is required, mocks/stubs become more complex than the behavior, or important dependencies are hidden in global state.

A Low rating may reveal a real testability problem. If the target cannot reasonably be exercised in the Project VITAL isolated environment, return to Part A and choose a more appropriate target.

## Part C — Study Existing OpenEMR Tests

Locate at least two existing OpenEMR isolated/unit tests. For each, identify:

- test file;
- production code being tested;
- framework;
- test structure;
- at least one assertion;
- required setup; and
- one practice your team could reuse.

Do not copy an existing test and present it as your own.

## Part D — Design Tests Before Implementing Them

Design at least **6 meaningful tests**:

- at least **2 normal cases**;
- at least **2 boundary/edge cases**;
- at least **1 invalid/error/exception case**; and
- at least **1 additional risk-based case**.

| Test ID | Behavior / Requirement | Input | Expected Result | Category | Why It Matters |
|---|---|---|---|---|---|
| UT-01 | ... | ... | ... | Normal | ... |

For every expected result, be able to explain where the expectation came from: production-code behavior, documented requirement, verified domain rule, or other defensible evidence.

A test must make a meaningful assertion. Simply executing code is insufficient.

## Part E — Implement the Tests

Implement tests in:

```text
assignment-03/tests/YourSelectedComponentTest.php
```

Use PHPUnit, meaningful names/assertions, deterministic behavior, and practical isolation.

Think in terms of:

```text
ARRANGE → ACT → ASSERT
```

Implement at least **6 passing, meaningful unit tests**. Quality and diversity matter more than raw count.

## Part F — Data-Driven Testing

At least one behavior must use a PHPUnit data-driven/parameterized approach.

Explain why the cases exercise the same behavior, what varies, what remains constant, and why the data-driven approach improves clarity or maintainability.

Select cases because they represent meaningful behavior, boundaries, equivalence classes, or risks.

## Part G — Run Locally

Run all Assignment 3 tests:

```bash
bash environment/unit-testing/run-unit-tests.sh
```

Or one test file:

```bash
bash environment/unit-testing/run-unit-tests.sh YourSelectedComponentTest.php
```

Record the command, tests/assertions reported, result, execution time if shown, and relevant warnings.

## Part H — Prove the Local Runner Detects Failure

Temporarily alter **one expected result in your own test** so it is deliberately wrong. Run the suite and confirm PHPUnit reports failure. Restore the correct expectation and rerun.

Required evidence:

```text
GREEN
  ↓
deliberately incorrect expectation
  ↓
RED
  ↓
inspect the failure
  ↓
restore correct expectation
  ↓
GREEN
```

Do not leave the broken expectation in the final submission. The purpose is to demonstrate that the testing mechanism detects failure.

## Part I — Focused Coverage

Measure focused coverage for the selected unit when supported by the course environment. Do **not** attempt to maximize coverage across all OpenEMR.

Explain what is covered, what remains uncovered, whether that matters for your selected risks, what important behaviors coverage percentages do not reveal, and why 100% coverage would still not prove correctness.

Coverage is evidence about execution, not proof of software quality.

## Part J — Configure Continuous Integration

Create the workflow from the validated Project VITAL template:

```bash
mkdir -p .github/workflows
cp environment/unit-testing/github-actions-unit-tests.template.yml .github/workflows/unit-tests.yml
```

The pipeline checks out the team repository and pinned OpenEMR source, prepares PHP/Composer, copies Assignment 3 tests, and executes PHPUnit.

Inspect the workflow before committing it. Your team should be able to explain its major steps.

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

If a push fails with a message mentioning `workflow` scope and you use GitHub CLI:

```bash
gh auth refresh -h github.com -s workflow
gh auth setup-git
gh auth status
git push
```

Never place tokens in the repository. See `environment/unit-testing/GITHUB_ACTIONS_SETUP.md` for detailed troubleshooting.

## Part L — Verify Green CI

Record the successful Actions run: branch, commit, workflow name, result, and approximate duration. The workflow run itself is primary evidence; screenshots may supplement it.

## Part M — Prove CI Detects Failure

Create:

```bash
git switch -c experiment/ci-failure
```

Temporarily make one expected result deliberately incorrect:

```bash
git add assignment-03/tests
git commit -m "Experiment: verify CI detects failing unit test"
git push -u origin experiment/ci-failure
```

The desired result is **RED**. Inspect which test failed, which workflow step failed, what PHPUnit reported, and whether CI matches the local behavior you expected.

A RED result here is successful evidence that CI detects the deliberately introduced problem.

## Part N — Restore CI to Green

Restore the correct expectation:

```bash
git add assignment-03/tests
git commit -m "Restore passing unit test"
git push
```

Required CI evidence:

```text
GREEN → RED → GREEN
```

Do not merge or tag the deliberately broken state.

## Part O — Analyze a Failure

Analyze at least one meaningful failure encountered during the assignment. This may be a test failure, setup problem, dependency problem, incorrect expectation, CI failure, or another relevant testing problem.

Explain:

1. What failed?
2. What failure message or symptom did you observe?
3. What was your initial hypothesis?
4. What evidence did you inspect?
5. What was the actual cause?
6. What correction did you make?
7. What did you learn?

The objective is **evidence-based diagnosis**, not merely making output green.

## Part P — What Unit Testing Cannot Tell You

Return to your original Assignment 2 workflow.

Identify at least one important question about that workflow that your unit tests cannot answer.

For example, unit testing one component does not necessarily establish that:

- the browser sends the correct request;
- multiple components integrate correctly;
- data is associated with the correct record;
- information persists correctly in the database;
- authorization rules work across the complete workflow; or
- the complete user workflow satisfies its requirements.

For the behavior you identify:

1. Explain why your unit tests cannot establish it.
2. Identify the next appropriate testing level: **integration, system, or acceptance testing**.
3. Explain what additional environment, data, dependencies, or evidence that test would require.

The purpose is to understand the **scope and limits** of unit testing.

## Required Deliverables

1. Assignment 2 workflow identification.
2. Candidate-unit investigation and final target justification.
3. Testability assessment and rating.
4. Analysis of at least two existing OpenEMR isolated/unit tests.
5. Unit-test design table with at least six tests.
6. At least six meaningful passing unit tests.
7. At least one data-driven/parameterized test.
8. Local GREEN → RED → GREEN evidence.
9. Focused coverage analysis when supported.
10. `.github/workflows/unit-tests.yml`.
11. Successful CI evidence.
12. CI GREEN → RED → GREEN evidence.
13. Failure analysis.
14. Unit-testing limits / next-testing-level reflection.
15. AI Verification Log if generative AI was used.

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
│   ├── evidence/
│   │   └── README.md
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
| A2 → unit selection and testability reasoning | 15% |
| Unit-test design | 20% |
| Unit-test implementation | 20% |
| Parameterized testing and focused coverage | 10% |
| Continuous Integration | 20% |
| GREEN → RED → GREEN and failure diagnosis | 10% |
| Testing-level reflection and communication | 5% |
| **Total** | **100%** |

## Use of Generative AI

Generative AI may be used as an investigation and learning aid subject to the course policy—for example, to explain PHP/PHPUnit syntax, propose test cases or boundaries, explain failures, investigate dependencies, discuss testability, or explain CI configuration.

However:

> **AI-generated tests are not evidence that behavior is correct.**

Your team must verify expected results, production-code meaning, testing scope, assertions, dependencies, determinism, and relevance to the Assignment 2 workflow.

Never provide credentials, tokens, real patient information, or other sensitive data.

If AI is used, document at least two meaningful suggestions:

| AI Suggestion / Claim | How We Verified It | Result |
|---|---|---|
| ... | ... | Useful / Modified / Rejected |
| ... | ... | Useful / Modified / Rejected |

At least one entry must demonstrate evaluation rather than automatic acceptance. An AI response, by itself, is **not evidence**.

## Submission

Submit according to the Project VITAL Student Submission Guide.

Required tag:

```text
assignment-03
```

Before tagging, confirm all deliverables are committed, six meaningful tests pass, local and CI runs are green, deliberate failures are restored, `.project-vital/` is not committed, and no credentials or real patient data are included.

```bash
git tag assignment-03
git push origin assignment-03
```

Submit the repository reference and `assignment-03` tag through the LMS.

## Workflow Summary

```text
Assignment 2 workflow
        ↓
Review architecture evidence
        ↓
Identify 2–3 candidate units
        ↓
Select unit + assess testability
        ↓
Study existing OpenEMR tests
        ↓
Design 6+ tests
        ↓
Implement + run locally
        ↓
GREEN → RED → GREEN
        ↓
Focused coverage analysis
        ↓
Configure GitHub Actions
        ↓
CI GREEN → RED → GREEN
        ↓
Analyze a meaningful failure
        ↓
Return to original workflow
        ↓
Explain what unit testing cannot establish
        ↓
Identify the next testing level
        ↓
Tag assignment-03
```

## Final Perspective

Assignment 3 is not primarily about PHPUnit syntax. It is about making a justified testing decision.

You began with a real workflow, investigated its architecture, selected a small piece of behavior, evaluated whether it could be isolated, designed tests from evidence and risk, and automated those tests.

A passing test tells you that a particular observation matched a particular expectation under particular conditions.

It does **not** automatically tell you that the complete workflow is correct.

Understanding that distinction is part of becoming a software tester.
