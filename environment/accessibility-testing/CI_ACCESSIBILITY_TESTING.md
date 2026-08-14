# Project VITAL — Continuous Accessibility Validation

Assignment 6 uses a **controlled teaching fixture** for CI rather than requiring the entire existing OpenEMR interface to have zero accessibility violations.

This is intentional.

The real OpenEMR baseline already contains known accessibility issues. Students should discover and analyze those issues, but pre-existing issues should not make every CI run fail before students introduce changes.

The CI fixture represents a small, scoped interface whose expected behavior is under Project VITAL's control.

## CI checks

The workflow verifies:

```text
semantic labels / names
WCAG A/AA automated axe checks
basic keyboard focus order
```

The fixture is not a substitute for manual OpenEMR evaluation.

## Local validation

Run:

```bash
bash environment/accessibility-testing/run_accessibility_ci_local.sh
```

Expected:

```text
LOCAL ACCESSIBILITY CI CHECKS PASSED
```

## Install GitHub Actions

```bash
mkdir -p .github/workflows

cp environment/accessibility-testing/github-actions-accessibility-tests.template.yml \
   .github/workflows/accessibility-tests.yml
```

Create a validation branch:

```bash
git switch -c feature/assignment-06-accessibility-ci-validation
```

Then:

```bash
git add .github/workflows/accessibility-tests.yml \
        environment/accessibility-testing/

git commit -m "Add Assignment 6 continuous accessibility validation"

git push -u origin feature/assignment-06-accessibility-ci-validation
```

Open:

```text
GitHub → Actions → Project VITAL Accessibility Tests
```

The first run should be green.

---

# Controlled GREEN → RED → GREEN experiment

Create:

```bash
git switch -c experiment/accessibility-ci-failure
```

Introduce one meaningful accessibility regression in:

```text
environment/accessibility-testing/fixtures/ci-accessible.html
```

Recommended instructor validation defect:

Change:

```html
<label for="family-name">Family name</label>
<input id="family-name" ...>
```

to an unlabeled input, for example by removing the `label` association.

That should cause the axe `label` rule to fail.

Commit/push and confirm:

```text
Project VITAL Accessibility Tests → RED
```

Then restore the accessible markup and push again.

Required:

```text
GREEN → RED → GREEN
```

Do not use a syntax error as the controlled regression.
