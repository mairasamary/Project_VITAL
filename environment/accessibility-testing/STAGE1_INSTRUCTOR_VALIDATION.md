# Stage 1 Instructor Validation — Accessibility Testing

## Goal

Validate that the accessibility-testing stack can:

```text
pass known-good fixture
detect known-bad fixture
scan real OpenEMR page
produce machine-readable evidence
support a manual audit
```

## Step 1

Run:

```bash
bash environment/accessibility-testing/run_stage1_validation.sh
```

The fixture suite should pass even though one fixture is intentionally inaccessible. The second test passes because axe successfully detects the intentional defects.

## Step 2

Start OpenEMR:

```bash
cd environment
docker compose up -d
cd ..
```

Confirm:

```bash
docker compose -f environment/docker-compose.yml ps
```

## Step 3

Run:

```bash
bash environment/accessibility-testing/run_openemr_login_scan.sh
```

Record:

```text
Automated violations:
Needs manual review/incomplete:
```

Do not decide the student grading threshold yet.

We first need to see the actual OpenEMR baseline.

## Step 4 — Manual review

Open the local OpenEMR login page in a browser and use:

```text
environment/accessibility-testing/manual-audit-template.md
```

At minimum test:

- keyboard-only navigation;
- visible focus;
- input labels;
- page/heading structure;
- zoom/narrow layout;
- errors/status messages.

## Next stage

After Stage 1:

1. inspect actual login-page violations;
2. decide which authenticated OpenEMR interface(s) make good teaching targets;
3. automate login using semester-local credentials without exposing them in Git;
4. scan selected authenticated pages;
5. identify manual-only findings;
6. design accessibility CI;
7. only then write Assignment 6.

## Course standard note

WCAG 2.2 is the course reference. Automated axe rule tags provide useful coverage, but automated results are not equivalent to full WCAG conformance testing.
