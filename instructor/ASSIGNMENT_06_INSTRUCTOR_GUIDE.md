# Assignment 6 — Instructor Guide
## Accessibility Testing and Continuous Accessibility Validation

## Purpose

Assignment 6 introduces accessibility as a software-quality concern using Project VITAL's local OpenEMR environment.

The assignment intentionally separates:

```text
REAL-WORLD AUDIT TARGET
OpenEMR
    ↓
existing accessibility behavior/issues
    ↓
automated + manual investigation

CONTROLLED CI TARGET
Project VITAL teaching fixture
    ↓
known expected accessibility properties
    ↓
deterministic regression detection
```

This distinction is central to the assignment.

The existing OpenEMR interface contains accessibility findings. Requiring the entire application to produce zero axe violations would make the CI signal dependent on pre-existing application behavior rather than student-introduced regressions.

The controlled fixture provides a stable CI contract while OpenEMR provides a realistic audit environment.

---

# Validated instructor environment

The infrastructure was validated locally using Dockerized Playwright and `@axe-core/playwright`.

The local host did not have Node.js installed. Stage 1 was therefore revised to run Playwright in Docker rather than adding Node/npm as a host prerequisite.

The validated approach uses a pinned Playwright container/package version.

OpenEMR was reachable from the macOS host at:

```text
https://localhost:8443
```

and returned:

```text
HTTP/1.1 302 Found
Location: interface/login/login.php?site=default
```

From the Playwright container, the working host address was:

```text
https://host.docker.internal:8443
```

Do not revert to `hostmachine` on the validated macOS Docker Desktop setup unless there is a specific reason to do so.

---

# Stage 1 — Login baseline

Validated command:

```bash
bash environment/accessibility-testing/run_openemr_login_scan.sh
```

Validated result:

```text
Automated violations: 2
Needs manual review/incomplete: 1
```

Observed automated findings:

```text
[serious] color-contrast
[critical] select-name
```

These numbers are a **validated instructor baseline**, not a required universal result.

OpenEMR versions, themes, browser engines, configuration, and future upstream changes can alter results.

Students should record and interpret what their assigned semester environment actually reports.

---

# Stage 2 — Authenticated baseline

Validated command:

```bash
bash environment/accessibility-testing/run_stage2_authenticated_scan.sh
```

The test authenticated successfully and scanned two targets.

## Authenticated landing page

Validated result:

```text
Automated violations: 7
Needs manual review/incomplete: 2
```

Observed rules:

```text
color-contrast    serious   7 nodes
frame-title       serious   1 node
html-has-lang     serious   1 node
link-name         serious   1 node
listitem          serious   3 nodes
select-name       critical  1 node
target-size       serious   40 nodes
```

## Patient Finder

Validated result:

```text
Automated violations: 3
Needs manual review/incomplete: 2
```

Observed rules:

```text
aria-hidden-focus  serious
color-contrast     serious
html-has-lang      serious
```

The Patient Finder is the preferred primary real-world teaching target because the baseline is smaller and easier for students to investigate.

The authenticated landing page remains useful as a comparison showing that different pages within one application can have substantially different accessibility characteristics.

---

# Stage 2 — Keyboard baseline

Validated command:

```bash
bash environment/accessibility-testing/run_keyboard_baseline.sh
```

The first 20 Tab presses were dominated by the OpenEMR Product Registration interaction.

A repeating sequence included:

```text
INPUT   email
INPUT   allow_telemetry
BUTTON  Submit
BUTTON  Ask again later
BODY
DIV     OpenEMR Product Registration
```

and then returned to the registration controls.

Several elements reported CSS outline values such as:

```text
outline=none/0px
```

## Teaching interpretation

Do not tell students that `outline=none` automatically proves invisible focus.

Visible focus can be implemented using:

- outline;
- border;
- background;
- box shadow;
- pseudo-elements;
- other visual changes.

Students must visually inspect the focused control.

The registration interaction also demonstrates why automated focus-sequence collection is not equivalent to evaluating whether focus order is logical or usable.

---

# Stage 3 — Controlled accessibility CI

The controlled fixture is:

```text
environment/accessibility-testing/fixtures/ci-accessible.html
```

Local validation:

```bash
bash environment/accessibility-testing/run_accessibility_ci_local.sh
```

Validated GREEN state:

```text
2 passed
LOCAL ACCESSIBILITY CI CHECKS PASSED
```

The CI tests cover:

1. zero automated axe violations for the scoped fixture under the configured A/AA tag set;
2. meaningful relative keyboard focus order across the search controls.

---

# Important Stage 3 implementation discovery

The first keyboard test assumed:

```text
Tab 1 → family-name
Tab 2 → date
Tab 3 → Search button
```

That assumption failed in Chromium because a date input can introduce browser-specific/internal focus behavior.

The test was corrected to look for the **relative order of meaningful controls** over several Tab presses rather than asserting an exact browser-specific Tab count.

This is an important testing lesson:

> Automated interaction tests should assert meaningful application behavior rather than unnecessarily encoding browser implementation details.

If this issue reappears, inspect the current `accessibility-ci.spec.js` before changing the fixture.

---

# Validated CI workflow

Workflow:

```text
Project VITAL Accessibility Tests
```

The GitHub Actions workflow was validated successfully on the Assignment 6 feature branch.

The initial workflow produced a GREEN run.

---

# Controlled regression experiment

The instructor validation intentionally removed the accessible naming relationship from the family-name input.

An early attempt did not fail because the resulting markup still did not create the intended detectable condition.

The final unambiguous defect used an unlabeled input, conceptually:

```html
<p>Family name</p>
<input>
```

This preserves visible nearby text while removing the programmatic label relationship.

Local result:

```text
Accessibility violations:
  [critical] label: Form elements must have labels
```

axe reported that the element lacked:

```text
implicit label
explicit label
aria-label
aria-labelledby
title
placeholder
```

The automated WCAG test failed as intended.

The keyboard test also failed because removing the input ID meant it no longer matched the controlled meaningful-focus sequence.

This secondary failure is acceptable for the instructor experiment, but the primary evidence is the axe `label` violation.

---

# Validated GREEN → RED → GREEN

GitHub Actions successfully demonstrated:

```text
GREEN
  ↓
introduce missing accessible label
  ↓
RED
  ↓
restore correct markup
  ↓
GREEN
```

This is the central continuous-testing evidence for Assignment 6.

The experiment should fail because of a meaningful accessibility defect, not because the student:

- breaks HTML syntax;
- deletes a test;
- changes an assertion to false;
- crashes Playwright;
- introduces an unrelated build failure.

---

# Why the fixture is necessary

Do not require:

```text
OpenEMR axe violations == 0
```

as the Assignment 6 CI gate.

The validated real OpenEMR pages already contain existing findings.

A zero-violation gate on the full application would conflate:

```text
existing accessibility debt
```

with:

```text
new accessibility regression
```

The fixture provides a controlled regression boundary.

Students should still audit the real application because accessibility education would be weakened if the assignment consisted only of testing a deliberately clean teaching page.

---

# Manual Patient Finder task

Students should perform a keyboard-only Patient Finder workflow:

```text
reach/open finder
→ reach search control
→ enter search
→ execute
→ navigate results
→ return to search
```

The grading emphasis is on observations and reasoning.

Students should discuss:

- reachability;
- keyboard activation;
- focus visibility;
- focus order;
- unexpected focus movement;
- accessible names/instructions;
- keyboard traps.

A technically completable task does not by itself establish that the workflow is accessible.

---

# Zoom/reflow

Require evaluation at 200% browser zoom.

Students should investigate:

- clipping;
- overlap;
- content loss;
- dialog usability;
- navigation;
- horizontal scrolling;
- readability.

The purpose is to expose a property that an axe scan alone does not fully evaluate.

---

# Expected conceptual distinction

Students should understand three layers.

## 1. Automated accessibility analysis

Example:

```text
axe
```

Good for detecting many machine-testable structural/accessibility rules.

Cannot prove complete accessibility.

## 2. Automated interaction evidence

Example:

```text
Tab focus-sequence test
```

Good for repeatable properties such as whether expected controls can appear in a focus sequence.

Cannot determine whether the sequence feels logical to a human or whether focus is meaningfully visible in every context.

## 3. Manual evaluation

Examples:

```text
keyboard-only task
visible focus
zoom/reflow
understanding control purpose
workflow usability
```

Requires human judgment.

The strongest answer recognizes that the three approaches complement rather than replace each other.

---

# Common problems and troubleshooting

## `node: command not found`

The current infrastructure should not require host Node.js.

Use:

```bash
bash environment/accessibility-testing/run_stage1_validation.sh
```

which runs the testing stack through Docker.

Do not instruct students to install Node merely to solve this error unless the course infrastructure has intentionally changed.

---

## OpenEMR works in browser but Playwright cannot connect

Confirm host access:

```bash
curl -k -I https://localhost:8443
```

A redirect to the OpenEMR login page establishes that OpenEMR is listening.

For Docker Desktop on the validated macOS setup, the Playwright container should use:

```text
host.docker.internal
```

rather than `localhost`.

---

## `"docker run" requires at least 1 argument`

Inspect the shell script for a dangling continuation:

```bash
\
```

especially after editing/removing a `docker run` option.

---

## Authenticated login fails

Check that the expected local OpenEMR credentials are available through the environment configuration.

Do not print credentials for debugging in student-visible logs.

Do not commit `.env`.

---

## Patient Finder path changes

The validated default is:

```text
/interface/main/finder/dynamic_finder.php
```

The Stage 2 infrastructure supports an override through:

```text
ACCESSIBILITY_PATIENT_FINDER_PATH
```

Verify the current OpenEMR semester image before permanently changing the course infrastructure.

---

## Controlled missing-label experiment remains GREEN

First confirm the test is loading:

```text
../fixtures/ci-accessible.html
```

Then inspect the actual fixture.

An input can still receive an accessible name through mechanisms such as:

```text
<label>
aria-label
aria-labelledby
title
```

For an unambiguous instructor validation defect, use nearby visible text that is not programmatically associated with the input.

---

# Grading guidance

Suggested emphasis:

| Area | Suggested weight |
|---|---:|
| Automated OpenEMR analysis and interpretation | 20% |
| Keyboard/focus manual evaluation | 20% |
| Patient Finder workflow analysis | 15% |
| Zoom/reflow evaluation | 10% |
| Continuous accessibility CI | 15% |
| GREEN → RED → GREEN experiment | 10% |
| Accessibility-testing strategy and conclusions | 10% |

Adjust to the course grading model as needed.

Do not award full credit for screenshots without interpretation.

The assignment is intended to assess reasoning about evidence, not the ability to run commands mechanically.

---

# Strong student conclusions

Look for statements such as:

> The automated scan detected a missing accessible name, but the scanner alone did not establish whether the complete workflow was keyboard usable.

or:

> CI detected the intentionally introduced label regression, demonstrating that the automated check can protect this scoped accessibility property. It does not establish accessibility of the entire OpenEMR application.

Weak/incorrect conclusions include:

> axe passed, therefore the page is accessible.

> The CI workflow is green, therefore Project VITAL is WCAG compliant.

> I could complete the task, therefore there are no accessibility problems.

---

# Instructor evidence checklist

Before releasing the assignment for a semester, verify:

- [ ] Dockerized Stage 1 passes.
- [ ] OpenEMR login scan reaches the current local image.
- [ ] Authenticated scan logs in successfully.
- [ ] Patient Finder path remains valid.
- [ ] Keyboard evidence script executes.
- [ ] Controlled fixture is GREEN locally.
- [ ] GitHub accessibility workflow is GREEN.
- [ ] Missing-label experiment produces RED.
- [ ] Restored fixture returns GREEN.
- [ ] No credentials/secrets are committed.
- [ ] Student instructions match the semester branch structure.

---

# Assignment 6 validated state

At initial instructor validation, the infrastructure successfully established:

```text
real OpenEMR automated baseline
        +
authenticated baseline
        +
keyboard evidence
        +
manual-testing framework
        +
controlled accessibility CI
        +
meaningful accessibility regression
        ↓
GREEN → RED → GREEN
```

This is the validated foundation for the student assignment.
