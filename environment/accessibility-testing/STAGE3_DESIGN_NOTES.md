# Stage 3 Design Notes

Project VITAL now separates two accessibility-testing contexts.

## Real-world audit target

```text
OpenEMR login / authenticated pages / patient finder
```

Purpose:

- discover existing accessibility issues;
- interpret automated findings;
- perform manual keyboard/focus evaluation;
- reason about WCAG.

These pages may contain known baseline issues.

## Controlled CI target

```text
fixtures/ci-accessible.html
```

Purpose:

- enforce known accessibility expectations;
- prove CI detects regressions;
- provide deterministic GREEN → RED → GREEN evidence.

This separation prevents existing OpenEMR accessibility debt from making the course CI unusable.

The final Assignment 6 should require students to understand both.
