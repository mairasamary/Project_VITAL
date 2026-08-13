# Project VITAL

## Assignment 3 — Unit Testing and Continuous Integration

**Week 3 | Team Assignment | OpenEMR + GitHub Actions**

---

## Purpose

In Assignment 1, you learned **what OpenEMR does**.

In Assignment 2, you investigated **how a selected OpenEMR workflow is implemented**.

In this assignment, you will begin testing the system at the smallest practical level:

> **Can we verify the behavior of an individual function, class, or small component in isolation?**

You will select a small, testable OpenEMR component related to your previous architecture investigation, design and implement unit tests for it, and then configure **Continuous Integration (CI)** so those tests run automatically when your team changes the repository.

This assignment introduces an important testing principle:

> A unit test should tell you something specific about one small piece of behavior.

It also introduces an equally important software-engineering principle:

> Tests are more useful when they run automatically and repeatedly, not only when someone remembers to run them.

---

# Learning Objectives

By the end of this assignment, you should be able to:

- Identify an appropriate unit of software to test.
- Distinguish unit testing from integration and system testing.
- Read enough unfamiliar PHP code to understand a small component's behavior.
- Design unit tests covering normal, boundary, and exceptional/invalid behavior.
- Use assertions to express expected software behavior.
- Organize unit tests so failures are understandable and reproducible.
- Evaluate the testability of an existing software component.
- Run tests automatically through a CI pipeline.
- Configure CI to fail when tests fail.
- Use CI results as evidence about software quality.
- Explain the limitations of a unit-test suite.

---

# Team and Time Expectations

Work with your Project VITAL team unless your instructor specifies otherwise.

Plan for approximately **3–5 hours of team work outside class**, in addition to guided in-class activities.

Every team member should participate in:

- understanding the selected component;
- test design;
- implementation;
- review of failures;
- CI configuration or validation.

---

# Important Scope Rule

You are **not** expected to unit test an entire OpenEMR workflow.

A workflow such as:

```text
Create Patient
      ↓
Schedule Appointment
      ↓
Create Encounter
      ↓
Record Vitals
```

is far too large for a unit test.

For this assignment, identify a much smaller target such as:

```text
Function
Class
Validator
Formatter
Parser
Calculator
Helper
Small service
Value object
Utility
```

The selected target should have behavior that can be tested with limited external dependencies.

---

# Part A — Understand Unit-Test Scope

Before writing code, return to your Assignment 2 architecture artifacts.

Identify one small component related to the workflow you investigated.

For example:

```text
Selected Workflow
      │
      ▼
Relevant OpenEMR component
      │
      ▼
Small function/class/helper
      │
      ▼
UNIT TEST TARGET
```

Document:

- Workflow from Assignment 2
- Selected component
- File path
- Class/function name
- Responsibility
- Inputs
- Outputs
- Important dependencies

Then answer:

> **Why is this an appropriate unit-test target?**

---

# Part B — Evaluate Testability

Before implementing tests, inspect the selected code.

Identify anything that makes the component easier or harder to test.

Consider:

- Does it depend on a database?
- Does it depend on global state?
- Does it read environment variables?
- Does it access the filesystem?
- Does it call another service?
- Does it use the current time/date?
- Does it make network requests?
- Does it depend on session state?
- Does it create random values?
- Does it have clearly defined inputs and outputs?
- Can dependencies be replaced, mocked, or avoided?

Create a short **Testability Assessment**.

Use a format similar to:

| Characteristic | Observation | Impact on Unit Testing |
|---|---|---|
| Database dependency | None | Component can be tested without database setup |
| Current time | Uses system time directly | Makes deterministic tests harder |
| Global variable | Reads global configuration | Makes isolation more difficult |

Then assign your target an overall testability rating:

- **High**
- **Medium**
- **Low**

Explain your rating.

---

# Part C — Study Existing OpenEMR Tests

Before creating new tests, locate at least **two existing OpenEMR unit/isolated tests**.

For each example, identify:

- Test file
- Production code being tested
- Test framework
- How the test is structured
- At least one assertion
- What setup is required
- One practice you could reuse in your own tests

Your goal is not to copy an existing test.

Your goal is to understand how testing is already performed in the codebase.

---

# Part D — Design the Tests Before Implementing Them

Create a **Unit Test Design Table** before writing your test code.

Design at least **6 meaningful unit tests**.

Your set must include:

1. At least **2 normal/expected cases**
2. At least **2 boundary or edge cases**
3. At least **1 invalid/error/exception case**
4. At least **1 additional case motivated by your own risk analysis**

Use this format:

| Test ID | Behavior / Requirement | Input | Expected Result | Category | Why This Test Matters |
|---|---|---|---|---|---|
| UT-01 | ... | ... | ... | Normal | ... |
| UT-02 | ... | ... | ... | Boundary | ... |

Avoid tests that only execute code without checking meaningful behavior.

A good unit test should have a clear reason to fail if the behavior changes incorrectly.

---

# Part E — Implement the Unit Tests

Implement your designed tests using the test framework used by the selected OpenEMR component/course environment.

For PHP/OpenEMR code, this will normally involve **PHPUnit**.

Your implementation should:

- use meaningful test names;
- contain clear assertions;
- avoid unnecessary duplication;
- produce deterministic results;
- isolate the selected unit as much as practical;
- clearly distinguish setup, action, and verification.

A conceptual structure is:

```text
Arrange
   ↓
prepare inputs / test state

Act
   ↓
call the unit

Assert
   ↓
verify expected behavior
```

You may organize this explicitly in comments if helpful, but comments are not required when the test code is already clear.

---

## Minimum Requirement

Your team must implement at least:

> **6 passing unit tests**

However, the quality and diversity of the tests matter more than the raw count.

Twenty nearly identical tests are not necessarily stronger than six carefully selected tests.

---

# Part F — Data-Driven / Parameterized Testing

At least one behavior should be tested using a **data-driven or parameterized approach** if supported by the test framework.

For example, instead of:

```text
test input A
test input B
test input C
```

you may define several inputs and expected results and apply the same test logic to all of them.

Document:

- Why the cases belong together
- What varies
- What remains constant
- Why a data-driven approach improves the test suite

If your selected target is genuinely unsuitable for parameterized testing, discuss this with your instructor before replacing this requirement.

---

# Part G — Run the Tests Locally

Before configuring CI, run the test suite in the instructor-provided Project VITAL/OpenEMR development test environment.

Record:

- Command used
- Number of tests
- Number of assertions, if reported
- Pass/fail result
- Execution time, if reported

Example evidence:

```text
Tests: 6
Failures: 0
Errors: 0
```

Do not proceed to CI while your test suite is failing for unexplained reasons.

---

# Part H — Test Coverage

Measure coverage for your **selected unit or small component**, if supported by the course test environment.

Do **not** attempt to maximize coverage across the entire OpenEMR codebase.

Report the relevant coverage result and answer:

1. What lines/branches/behaviors are covered?
2. What remains uncovered?
3. Is the uncovered code important?
4. Would 100% coverage necessarily mean the component is correctly tested?

Coverage is evidence about what executed.

Coverage is **not** proof that the tests are good.

---

# Part I — Configure Continuous Integration

Create a GitHub Actions workflow in your team repository.

Recommended location:

```text
.github/
└── workflows/
    └── unit-tests.yml
```

The workflow should automatically run the unit tests when:

- code is pushed to the relevant branch; and
- a pull request targets the team's main branch.

Conceptually:

```text
Push / Pull Request
        │
        ▼
GitHub Actions
        │
        ▼
Prepare test environment
        │
        ▼
Run unit tests
        │
        ├── PASS → workflow succeeds
        │
        └── FAIL → workflow fails
```

Your exact configuration will depend on the Project VITAL test environment provided by your instructor.

---

# Part J — Required CI Behavior

Your CI pipeline must demonstrate all of the following:

- [ ] It starts automatically from a Git event.
- [ ] It obtains the correct Project VITAL/OpenEMR test baseline.
- [ ] It installs/prepares required dependencies.
- [ ] It runs your unit tests.
- [ ] Passing tests produce a successful workflow.
- [ ] Failing tests produce a failed workflow.
- [ ] The workflow output allows a developer to identify which test failed.

Do not configure the workflow to ignore test failures.

For example, avoid patterns whose purpose is to make a failing test command appear successful.

A red CI result is useful information.

---

# Part K — Prove That CI Detects a Failure

A green CI pipeline does not prove that CI is actually checking the tests.

You must demonstrate that the pipeline can detect a failure.

Use a temporary branch such as:

```text
experiment/ci-failure
```

On that branch only, deliberately make one test fail.

For example, temporarily change an expected value.

Push the branch and record the resulting failed CI run.

Then restore the correct test and verify that CI returns to green.

Do **not** leave the deliberately broken test on your final submission branch.

Document:

```text
Correct test
    ↓
CI GREEN
    ↓
Temporary deliberate failure
    ↓
CI RED
    ↓
Restore correct behavior
    ↓
CI GREEN
```

This is a controlled CI experiment, not an attempt to introduce a defect into the OpenEMR application.

---

# Part L — Interpret a Failure

Choose one failure your team encountered while developing the tests.

This may be:

- a genuine defect;
- an incorrect expected value;
- a setup problem;
- a dependency problem;
- a misunderstanding of the component;
- a flaky/non-deterministic test;
- the deliberate CI failure.

Document:

1. What failed?
2. What did the failure message say?
3. What did your team initially think was wrong?
4. What evidence did you inspect?
5. What was the actual cause?
6. What did you change?
7. What did you learn from the failure?

The goal is to practice **diagnosing** failed tests rather than merely making the output green.

---

# Part M — Unit Testing vs. Other Test Levels

For your selected unit, identify one behavior that **cannot be adequately tested by the unit tests you wrote**.

Explain which broader testing level would be more appropriate:

- integration testing;
- system testing;
- acceptance testing;

and why.

For example:

```text
UNIT TEST

Can the formatter correctly transform a value?
                │
                ▼
             YES


Can the complete clinical form save the value
and display it correctly after reload?
                │
                ▼
              NO
                │
                ▼
       Integration/System Test
```

This distinction is an important part of the assignment.

---

# Required Deliverables

Submit one team package containing:

1. **Unit Test Target**
   - Workflow
   - Component/file
   - Responsibility
   - Inputs/outputs
   - Dependencies
   - Explanation of why the target is appropriate

2. **Testability Assessment**
   - Testability table
   - High/Medium/Low rating
   - Explanation

3. **Existing Test Analysis**
   - At least 2 existing OpenEMR test examples

4. **Unit Test Design Table**
   - At least 6 planned tests
   - Required normal/boundary/invalid/risk categories

5. **Implemented Unit Tests**
   - Source files
   - At least 6 passing tests

6. **Parameterized/Data-Driven Test**
   - Code and short explanation

7. **Local Test Evidence**
   - Command and result

8. **Coverage Analysis**
   - Focused coverage evidence and interpretation, when supported

9. **GitHub Actions CI Workflow**
   - `.github/workflows/unit-tests.yml` or instructor-approved equivalent

10. **CI Evidence**
    - Successful CI run
    - Failed CI run from controlled experiment
    - Successful run after restoration

11. **Failure Analysis**
    - Short diagnosis of one meaningful test/CI failure

12. **Testing-Level Reflection**
    - One important behavior not adequately covered by unit tests
    - Recommended broader testing level

13. **AI Verification Log**
    - Required if generative AI was used

---

# Recommended Repository Structure

Your team repository may contain:

```text
VITAL-Team-XX/
│
├── assignment-03/
│   ├── README.md
│   ├── test-design.md
│   ├── testability.md
│   ├── existing-tests.md
│   ├── coverage.md
│   ├── failure-analysis.md
│   ├── testing-levels.md
│   ├── ai-verification-log.md
│   │
│   └── tests/
│       └── ...
│
└── .github/
    └── workflows/
        └── unit-tests.yml
```

Follow instructor-provided test-environment instructions for any files that must be placed in a specific OpenEMR-compatible location.

---

# Evaluation

This assignment evaluates both **test design** and **continuous testing practice**.

A large number of tests does not automatically earn a high grade.

| Criterion | Weight | Evidence of Strong Work |
|---|---:|---|
| **Unit selection and testability analysis** | 15% | Team selects an appropriately scoped unit and thoughtfully identifies factors affecting isolation and testability. |
| **Unit test design** | 20% | Tests cover meaningful normal, boundary, invalid, and risk-based behaviors with clear expected outcomes. |
| **Unit test implementation** | 20% | Tests are readable, deterministic, correctly asserted, and appropriately isolated. |
| **Parameterized testing + coverage analysis** | 10% | Team uses data-driven testing meaningfully and interprets focused coverage rather than treating coverage as a score to maximize. |
| **Continuous Integration pipeline** | 20% | CI runs automatically, reliably executes tests, correctly reports success/failure, and is understandable from workflow output. |
| **CI failure experiment + diagnosis** | 10% | Team proves CI catches a failing test and demonstrates evidence-based diagnosis of a failure. |
| **Testing-level reflection and communication** | 5% | Team correctly identifies limitations of unit tests and communicates work clearly. |
| **Total** | **100%** | |

---

# Use of Generative AI

Generative AI may be used as a learning and investigation aid, subject to the course AI policy.

Potentially appropriate uses include:

- explaining unfamiliar PHP/PHPUnit syntax;
- suggesting possible test cases;
- explaining an assertion failure;
- helping interpret CI configuration;
- proposing boundary cases;
- explaining mocking or dependency concepts.

However:

> **AI-generated tests are not automatically good tests.**

Your team is responsible for determining:

- whether the expected result is correct;
- whether the test is actually testing the intended unit;
- whether the assertions are meaningful;
- whether the test is deterministic;
- whether the test duplicates another test;
- whether the test would catch a relevant defect.

Do not provide credentials, tokens, real patient information, or other sensitive data to an AI system.

---

# AI Verification Log

If your team uses generative AI, document at least **2 meaningful AI suggestions**.

For each:

| AI Suggestion | How We Verified It | Result |
|---|---|---|
| AI proposed boundary case X | Read implementation and ran test | Useful / Modified / Rejected |
| AI suggested CI command Y | Compared with course/OpenEMR configuration and ran workflow | Confirmed / Incorrect / Modified |

At least one entry should explain how your team **evaluated** the suggestion rather than simply accepting it.

---

# Submission

Submit according to the **Project VITAL Student Submission Guide**.

The required Git submission tag is:

```text
assignment-03
```

Before creating the tag, confirm:

- all required files are committed;
- unit tests pass;
- the final CI run is green;
- the intentionally failing test has been removed/restored;
- no credentials or `.env` files are committed;
- no real patient data is included.

Then create and push the tag:

```bash
git tag assignment-03
git push origin assignment-03
```

Submit the team repository reference and `assignment-03` tag through the LMS as instructed.

---

# Looking Ahead

You have now moved through:

```text
Assignment 1
What does the system do?
        ↓
Assignment 2
How does the system work?
        ↓
Assignment 3
Does a small unit behave correctly,
and can we test it continuously?
```

The next step expands the testing scope:

```text
UNIT
  │
  ▼
INTEGRATION
  │
  ▼
SYSTEM
  │
  ▼
ACCEPTANCE
```

As the scope grows, you will test not only individual components, but also the interactions and workflows that connect them.
