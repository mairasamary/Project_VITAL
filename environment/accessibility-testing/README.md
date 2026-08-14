# Project VITAL — Accessibility Testing Infrastructure (Stage 1)

Stage 1 validates the testing toolchain before we design the student assignment.

Project VITAL uses **WCAG 2.2** as the course accessibility reference. W3C organizes WCAG under four principles — perceivable, operable, understandable, and robust — with testable success criteria at A, AA, and AAA levels.

The automated layer uses Playwright plus `@axe-core/playwright`.

## Important limitation

Automated accessibility testing is intentionally **not treated as proof that a page is accessible**.

The course will combine:

```text
Automated scanning
        +
Keyboard/manual review
        +
Human interpretation
```

## Stage 1 contents

```text
environment/accessibility-testing/
├── package.json
├── playwright.config.js
├── tests/
│   ├── fixture-accessibility.spec.js
│   └── openemr-login.spec.js
├── fixtures/
│   ├── accessible.html
│   └── broken.html
├── manual-audit-template.md
├── run_stage1_validation.sh
└── run_openemr_login_scan.sh
```

## First validation

From the repository root:

```bash
bash environment/accessibility-testing/run_stage1_validation.sh
```

This:

1. checks Node/npm;
2. installs pinned test dependencies;
3. installs Playwright Chromium;
4. verifies that the accessible teaching fixture passes;
5. verifies that the deliberately inaccessible fixture is detected.

Expected final line:

```text
STAGE 1 ACCESSIBILITY TOOLCHAIN VALIDATION PASSED
```

## OpenEMR baseline

Start the normal Project VITAL OpenEMR environment, then run:

```bash
bash environment/accessibility-testing/run_openemr_login_scan.sh
```

The OpenEMR login-page test deliberately **does not fail just because violations exist**. Its purpose is to establish a baseline.

The scan writes:

```text
.project-vital/accessibility-testing/openemr-login-axe.json
```

Send the console summary to the instructor/course maintainer.

## Why begin with the login page?

It is accessible without automating authenticated OpenEMR workflows. Once the scanner works reliably against the real local OpenEMR instance, Stage 2 will add authenticated navigation to selected interfaces and manual keyboard/focus testing.

## Dependency baseline

The initial validated package pins Playwright and the axe Playwright integration so semester behavior is reproducible. Revalidate these dependencies before upgrading them.
