# Instructor Validation — Assignment 6 Accessibility CI

## Why a controlled fixture?

Stage 1 and Stage 2 established that the real OpenEMR interface has existing accessibility findings.

Validated examples included:

### Login

```text
color-contrast
select-name
```

### Authenticated landing page

```text
color-contrast
frame-title
html-has-lang
link-name
listitem
select-name
target-size
```

### Patient finder

```text
aria-hidden-focus
color-contrast
html-has-lang
```

Therefore, a CI rule requiring the full OpenEMR UI to have zero violations would produce a permanently red build unrelated to student regressions.

The controlled fixture gives the course a stable regression target while OpenEMR remains the real-world audit target.

## Step 1 — local

```bash
bash environment/accessibility-testing/run_accessibility_ci_local.sh
```

Expected:

```text
2 passed
LOCAL ACCESSIBILITY CI CHECKS PASSED
```

The tests establish:

1. zero automated axe violations on the controlled fixture;
2. expected keyboard focus order across the three primary controls.

## Step 2 — GitHub green

Install:

```text
.github/workflows/accessibility-tests.yml
```

Push from:

```text
feature/assignment-06-accessibility-ci-validation
```

Confirm:

```text
Project VITAL Accessibility Tests → GREEN
```

## Step 3 — meaningful red

On an experiment branch, remove the programmatic label from `family-name`.

Push.

Expected:

```text
Project VITAL Accessibility Tests → RED
```

The failing output should identify an accessibility rule such as:

```text
label
```

This is preferred to merely changing a test assertion because it demonstrates a real accessibility regression in the interface.

## Step 4 — restore

Restore the label association.

Push.

Expected:

```text
GREEN
```

Required evidence:

```text
GREEN → RED → GREEN
```

## Manual testing remains mandatory

Even after CI is green, Assignment 6 must require manual evaluation of the real OpenEMR interface.

Automated CI does not establish:

- logical usability of full workflows;
- quality of visible focus;
- complete keyboard operability;
- screen reader comprehension;
- meaningful reading order;
- accessibility of every dynamic state;
- full WCAG conformance.
