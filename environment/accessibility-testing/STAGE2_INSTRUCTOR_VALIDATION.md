# Stage 2 Instructor Validation — Authenticated Accessibility Testing

Stage 1 established that the Dockerized Playwright + axe toolchain works and that the real OpenEMR login page can be scanned.

Validated Stage 1 login baseline:

```text
Automated violations: 2
Needs manual review/incomplete: 1

serious  color-contrast
critical select-name
```

Stage 2 adds authenticated baseline collection.

## Before running

OpenEMR must be running and `environment/.env` must contain the local semester credentials used by Docker:

```text
OPENEMR_ADMIN_USER
OPENEMR_ADMIN_PASSWORD
```

These credentials are passed to the Playwright container as environment variables and are never printed by the scripts.

## Run authenticated axe scans

```bash
bash environment/accessibility-testing/run_stage2_authenticated_scan.sh
```

Expected targets:

1. authenticated landing page;
2. patient finder.

Reports:

```text
.project-vital/accessibility-testing/authenticated/
├── authenticated-landing-axe.json
└── patient-finder-axe.json
```

These tests collect a baseline. They do not require zero violations.

Record the console summaries.

## If patient finder path changes

The default target is:

```text
/interface/main/finder/dynamic_finder.php
```

Override it locally without changing course source:

```bash
ACCESSIBILITY_PATIENT_FINDER_PATH="/correct/path" \
  bash environment/accessibility-testing/run_stage2_authenticated_scan.sh
```

If the path changes in a future OpenEMR semester baseline, update the infrastructure only after verifying the new page.

## Keyboard evidence

Run:

```bash
bash environment/accessibility-testing/run_keyboard_baseline.sh
```

This records the first 20 Tab-focus targets on the authenticated landing page.

It is deliberately called **evidence**, not an automated pass/fail accessibility conclusion.

Then perform the human review in:

```text
environment/accessibility-testing/AUTHENTICATED_MANUAL_AUDIT.md
```

## What to record

For each authenticated page:

- automated violation count;
- incomplete/manual-review count;
- rule IDs and impact;
- one automated result investigated manually;
- one keyboard/focus property;
- one property automation could not establish.

## Next stage

After Stage 2 results are known:

1. select the best teaching target(s);
2. decide which axe findings should become CI regressions versus baseline-known issues;
3. build a controlled accessible/broken component for CI;
4. demonstrate accessibility GREEN → RED → GREEN;
5. write the student Assignment 6 only after the CI scope is validated.
