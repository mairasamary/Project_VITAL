# Assignment 6 — Accessibility Testing and Continuous Accessibility Validation

## Project VITAL

Modern software quality includes more than functional correctness. An interface may technically work while still creating barriers for users who navigate with a keyboard, use assistive technology, require magnification, or perceive content differently.

In this assignment, you will investigate accessibility in **Project VITAL's local OpenEMR environment** using both automated and manual testing.

You will work in two complementary contexts:

1. **Real OpenEMR interfaces** — discover and interpret accessibility issues in an existing application.
2. **A controlled Project VITAL accessibility fixture** — demonstrate that continuous integration can detect an accessibility regression.

The goal is not to claim that OpenEMR is fully accessible or inaccessible. Your goal is to collect evidence, interpret that evidence carefully, and understand what different accessibility-testing techniques can and cannot establish.

---

## Learning objectives

By the end of this assignment, you should be able to:

- explain why accessibility is part of software quality;
- distinguish automated accessibility testing from manual accessibility evaluation;
- run an automated accessibility scanner against a web interface;
- interpret accessibility findings rather than treating them as simple pass/fail results;
- evaluate a workflow using keyboard-only navigation;
- reason about focus order and focus visibility;
- investigate accessible names and form labels;
- examine zoom/reflow behavior;
- explain why automated tools cannot establish complete accessibility or WCAG conformance;
- integrate a scoped accessibility regression test into continuous integration;
- demonstrate a meaningful **GREEN → RED → GREEN** accessibility-testing cycle.

---

# Part 1 — Prepare the environment

Start from your Project VITAL repository.

Make sure the local OpenEMR environment is running according to the semester setup instructions.

The accessibility infrastructure is located at:

```text
environment/accessibility-testing/
```

Project VITAL uses a containerized Playwright environment, so you do **not** need to install Node.js, npm, Playwright, or a browser directly on your computer.

Docker must be running.

---

# Part 2 — Validate the accessibility toolchain

Run:

```bash
bash environment/accessibility-testing/run_stage1_validation.sh
```

The validation script checks the containerized Playwright/axe testing environment and exercises known-good and deliberately problematic teaching fixtures.

Record whether Stage 1 succeeds.

### Question 1

Why is it useful to validate an accessibility-testing tool against controlled examples before using it to draw conclusions about a real application?

---

# Part 3 — Automated accessibility scan of the OpenEMR login page

With OpenEMR running, execute:

```bash
bash environment/accessibility-testing/run_openemr_login_scan.sh
```

The script scans the real local OpenEMR login page.

A JSON baseline is written under:

```text
.project-vital/accessibility-testing/
```

Record:

```text
Automated violations:
Needs manual review/incomplete:
```

For each automated violation, record:

- rule ID;
- impact;
- short description;
- number of affected nodes.

### Question 2

Choose one automated finding.

Explain:

1. what the rule is checking;
2. what element or type of element triggered it;
3. why the issue could matter to a user;
4. what additional manual investigation, if any, would help you understand its real impact.

Do not simply copy the scanner's description.

---

# Part 4 — Authenticated OpenEMR accessibility baseline

Run:

```bash
bash environment/accessibility-testing/run_stage2_authenticated_scan.sh
```

The scanner authenticates to the **local course OpenEMR environment** using credentials supplied by the local environment configuration. Credentials must not be committed to the repository or included in your report.

The scan examines:

1. the authenticated OpenEMR landing page;
2. the Patient Finder.

For each page, record:

| Page | Automated violations | Incomplete/manual-review items |
|---|---:|---:|
| Authenticated landing page | | |
| Patient Finder | | |

Then select **two findings across these pages** and investigate them.

At least one must be different from the finding you analyzed in Part 3.

For each finding, record:

- rule ID;
- impact;
- affected element;
- your interpretation;
- whether manual investigation changed or added to your understanding.

### Question 3

The two pages may produce different numbers and types of findings even though they belong to the same application.

Give two reasons why accessibility results can differ between pages of the same system.

---

# Part 5 — Keyboard and focus investigation

Automated scanning is only part of accessibility testing.

Run:

```bash
bash environment/accessibility-testing/run_keyboard_baseline.sh
```

This creates evidence about which elements receive focus during a sequence of Tab presses.

The output is stored under:

```text
.project-vital/accessibility-testing/authenticated/
```

The automated sequence is **evidence**, not proof that the focus order is usable.

Now perform a manual keyboard-only evaluation.

## Rule

For this portion, do not use the mouse or trackpad while performing the task.

If OpenEMR displays a registration, telemetry, announcement, or similar dialog, evaluate that interaction first.

Record:

- whether every interactive control can be reached;
- whether focus is visibly identifiable;
- whether the focus order appears logical;
- whether the dialog can be dismissed using the keyboard;
- where focus goes after dismissal;
- whether you encounter a keyboard trap.

### Important

A reported CSS value such as:

```text
outline=none
```

does **not by itself prove** that focus is invisible. A site can create a focus indicator using borders, background changes, shadows, or other visual mechanisms.

You must visually evaluate focus.

### Question 4

Compare the automated focus-sequence evidence with your manual experience.

Identify at least one thing the automated evidence told you and at least one thing it could **not** establish.

---

# Part 6 — Manual Patient Finder task

Use the real OpenEMR Patient Finder.

Using only the keyboard:

1. navigate to or open the Patient Finder;
2. reach a patient-search control;
3. enter a search value;
4. execute the search;
5. navigate into or through the results;
6. return to the search controls.

Record your observations in the following categories.

## Operability

- Were all required controls reachable?
- Did standard keyboard activation work?
- Did you encounter a keyboard trap?

## Focus

- Was focus visible?
- Was focus order consistent with the workflow?
- Did focus move unexpectedly after an action?

## Names and instructions

- Could you determine the purpose of the search controls?
- Were buttons and links understandable?
- Did any control depend mainly on visual appearance or position to communicate its purpose?

### Question 5

Choose one accessibility property you evaluated manually that the axe output did not establish.

Explain why human evaluation was necessary.

---

# Part 7 — Zoom and reflow

Evaluate at least one relevant OpenEMR page at increased browser zoom, including **200%**.

Investigate:

- whether important content remains available;
- whether controls overlap;
- whether text becomes clipped;
- whether dialogs remain usable;
- whether navigation remains understandable;
- whether ordinary reading requires problematic horizontal scrolling.

Record at least one screenshot at increased zoom.

### Question 6

Did increased zoom expose a usability or accessibility concern that was not obvious at the default zoom level?

Explain what you observed.

---

# Part 8 — Continuous accessibility testing

So far, you have been auditing an existing application.

Now you will work with a small interface controlled by Project VITAL:

```text
environment/accessibility-testing/fixtures/ci-accessible.html
```

Run:

```bash
bash environment/accessibility-testing/run_accessibility_ci_local.sh
```

The controlled fixture is expected to pass:

1. automated axe WCAG A/AA checks used by the course infrastructure;
2. a basic keyboard focus-order check.

Record the result.

### Question 7

Why does Project VITAL use a controlled fixture for accessibility CI instead of requiring the entire existing OpenEMR interface to have zero automated violations?

---

# Part 9 — Observe accessibility CI in GitHub Actions

Go to:

```text
GitHub → Actions → Project VITAL Accessibility Tests
```

Confirm that the accessibility workflow runs on your branch.

Capture evidence of a successful run.

Your screenshot should make the workflow status and branch identifiable.

---

# Part 10 — Controlled accessibility regression

Now demonstrate that CI can detect a **real accessibility defect**.

Create an experiment branch according to your course Git workflow.

For example:

```bash
git switch -c experiment/accessibility-ci-failure
```

In:

```text
environment/accessibility-testing/fixtures/ci-accessible.html
```

introduce a controlled accessibility defect involving the accessible labeling of the family-name input.

The visual text **Family name** may remain visible, but remove the programmatic relationship that gives the input its accessible label.

Do not:

- introduce a syntax error;
- delete the whole page;
- deliberately crash Playwright;
- modify the test merely to force an assertion failure.

The goal is an **interface accessibility regression**.

Run:

```bash
bash environment/accessibility-testing/run_accessibility_ci_local.sh
```

The accessibility test should now fail.

Inspect the failure.

### Question 8

What accessibility rule detected your defect?

Explain why a sighted mouse user might still understand the control even though the automated accessibility test rejects it.

Commit and push the experiment so that GitHub Actions records the failing accessibility workflow.

Capture evidence of the **RED** run.

---

# Part 11 — Restore accessibility

Restore the correct accessible label relationship.

Run:

```bash
bash environment/accessibility-testing/run_accessibility_ci_local.sh
```

Confirm that the local checks pass again.

Commit and push the repair.

Confirm that GitHub Actions returns to GREEN.

Your evidence should establish:

```text
GREEN → RED → GREEN
```

### Question 9

Why is this experiment stronger evidence of effective accessibility CI than merely showing one successful workflow run?

---

# Part 12 — Accessibility testing strategy

Write a short accessibility-testing strategy for Project VITAL.

Your strategy must contain three layers:

| Layer | Purpose | Example |
|---|---|---|
| Automated accessibility testing | Detect machine-testable regressions | axe rules |
| Automated interaction testing | Exercise predictable interaction properties | keyboard focus sequence |
| Manual accessibility evaluation | Evaluate behavior requiring human judgment | visible focus, logical workflow, zoom/reflow |

For each layer, identify:

- what it can detect;
- what it cannot reliably establish;
- when it should run;
- what evidence should be retained.

### Question 10

Suppose every automated accessibility test in Project VITAL is GREEN.

Can the team conclude that Project VITAL is accessible or fully WCAG conformant?

Explain your answer using evidence from this assignment.

---

# Required evidence

Your submission must include evidence of:

- Stage 1 toolchain validation;
- OpenEMR login-page automated scan;
- authenticated OpenEMR scan;
- Patient Finder scan;
- keyboard/focus investigation;
- manual Patient Finder task;
- 200% zoom/reflow investigation;
- successful local controlled-fixture test;
- GREEN GitHub accessibility workflow;
- intentionally RED GitHub accessibility workflow caused by an accessibility defect;
- restored GREEN workflow.

Do not include passwords, secrets, authentication tokens, or private environment configuration in screenshots or submitted files.

---

# Submission

Submit a Markdown or PDF report containing:

1. your answers to Questions 1–10;
2. the requested tables and observations;
3. screenshots/evidence;
4. your accessibility-testing strategy;
5. the relevant branch/commit identifiers for the GREEN → RED → GREEN experiment.

Keep screenshots focused on evidence. Do not submit dozens of screenshots when one clearly labeled screenshot establishes the result.

---

# What will be evaluated

Your work will be evaluated on:

- correct execution of the accessibility-testing workflow;
- quality of interpretation rather than merely copying tool output;
- distinction between automated evidence and human judgment;
- quality of keyboard/focus investigation;
- understanding of accessible names and labels;
- ability to reason about zoom/reflow;
- successful continuous accessibility validation;
- meaningful GREEN → RED → GREEN experiment;
- quality of the proposed testing strategy;
- clarity and professionalism of the submitted evidence.

---

# Key principle

Accessibility testing is not:

```text
run scanner → get zero errors → declare accessible
```

A stronger process is:

```text
automated analysis
        +
interaction testing
        +
manual evaluation
        +
continuous regression testing
        ↓
better accessibility evidence
```

Your conclusions must remain proportional to the evidence you actually collected.
