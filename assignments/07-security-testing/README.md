# Assignment 7 — Security Testing and Continuous Security Validation

## Project VITAL

Security is part of software quality, but security testing requires an additional constraint: **authorization**.

In this assignment, you will evaluate selected security properties of the **local Project VITAL/OpenEMR environment** and a **controlled Project VITAL security fixture**. You will collect evidence about security configuration and access-control behavior, create a small threat model, and demonstrate that continuous integration can detect a deliberately introduced security regression.

This assignment is intentionally bounded. You are **not** being asked to "hack OpenEMR." You are being asked to design and execute safe, reproducible security tests in an environment where you have explicit permission.

## Safety and authorization rules

You may test only your local Project VITAL/OpenEMR environment, the controlled fixtures in `environment/security-testing/`, and course repositories/workflows.

You must **not** scan public OpenEMR installations, test Boston College production systems, test third-party sites, brute-force passwords, perform denial-of-service/resource-exhaustion attacks, exploit vulnerabilities to gain access, or use real patient data/PHI.

If you are uncertain whether a test is authorized, do not run it until you have asked the instructor.

## Learning objectives

By the end of this assignment, you should be able to:

- explain why security testing requires explicit authorization and scope;
- create a simple threat model;
- evaluate selected HTTP security configuration evidence;
- test whether an unauthenticated request is prevented from reaching an authenticated resource;
- distinguish a security finding from proof of exploitability;
- design a controlled security regression test;
- integrate a scoped security check into CI;
- demonstrate **GREEN → RED → GREEN** security validation;
- communicate security evidence without overstating it.

# Part 1 — Prepare and validate the environment

Start Project VITAL/OpenEMR and run:

```bash
bash environment/security-testing/run_stage1_validation.sh
```

Stage 1 uses a controlled local fixture. It does not contact OpenEMR or an external system.

### Question 1
Why should a security-testing tool be validated against a controlled fixture before it is used to draw conclusions about a real application?

# Part 2 — Establish scope and create a threat model

Complete `environment/security-testing/THREAT_MODEL_TEMPLATE.md` using the **Patient Finder / patient lookup workflow**. Identify assets, actors, entry points, trust boundaries, at least three threats, one safely testable property, and one important concern outside the authorized scope.

### Question 2
Why is “What are we authorized to test?” part of security test planning rather than merely an administrative question?

# Part 3 — Passive OpenEMR security baseline

Run:

```bash
bash environment/security-testing/run_openemr_baseline.sh
```

The script makes one ordinary request and records response/redirect behavior, selected HTTP security headers, and selected cookie attributes under `.project-vital/security-testing/`.

Record:

| Property | Observed result |
|---|---|
| HTTP status / redirect | |
| Strict-Transport-Security | |
| Content-Security-Policy | |
| X-Content-Type-Options | |
| Referrer-Policy | |
| Frame-related protection | |
| Session cookie Secure | |
| Session cookie HttpOnly | |
| Session cookie SameSite | |

### Question 3
Choose two observed header/cookie properties. For each, explain the concern it relates to, what your observation establishes, and what it does **not** establish. Do not label a missing header as an exploitable vulnerability without additional evidence.

# Part 4 — Authentication-boundary check

Run:

```bash
bash environment/security-testing/run_unauthenticated_check.sh
```

An unauthenticated request to the application entry point should be directed into the authentication workflow rather than directly into authenticated application functionality.

### Question 4
What evidence does the redirect from the application entry point to the login page provide about the authentication boundary? Why does this result not prove that access control is correct throughout OpenEMR?


# Part 5 — Threat-driven test design

Choose two threats from your model and design one bounded test for each:

```text
Threat:
Security property:
Precondition:
Test action:
Expected secure behavior:
Evidence to collect:
Potential false positive / false negative:
Why the test is authorized and safe:
```

At least one must involve authorization/access control. If a test would require destructive behavior, brute force, high request volume, privilege escalation, or testing outside Project VITAL, document it conceptually but do **not** execute it.

### Question 5
Which proposed test gives stronger evidence, and why?

# Part 6 — Controlled security fixture and local CI

Run:

```bash
bash environment/security-testing/run_security_ci_local.sh
```

The controlled fixture should pass checks for a protected path, selected defensive HTTP headers, and session-cookie attributes.

### Question 6
Why is a controlled fixture useful for security CI when the real OpenEMR application may contain existing security debt or behaviors outside your team's control?

# Part 7 — GitHub Actions GREEN

Confirm the workflow **Project VITAL Security Tests** is GREEN on your branch and capture evidence.

# Part 8 — Controlled security regression

Create:

```bash
git switch -c experiment/security-ci-failure
```

In `environment/security-testing/fixtures/security_fixture_server.py`, remove only:

```text
X-Content-Type-Options: nosniff
```

Do not modify the test. Do not introduce a syntax error or crash the fixture. Run the local CI script again. It should fail because the security property regressed.

### Question 7
Why is changing the product/fixture stronger evidence than changing the test merely to force a failure?

Push the experiment and capture the RED GitHub Actions run.

# Part 9 — Restore GREEN

Restore `X-Content-Type-Options: nosniff`, rerun locally, commit/push, and confirm GitHub Actions returns to GREEN.

Your evidence should establish:

```text
GREEN → RED → GREEN
```

### Question 8
What does this experiment establish about this security check? What does it not establish about the overall security of OpenEMR?

# Part 10 — Security testing strategy

Write a short strategy containing at least:

| Layer | Purpose | Example |
|---|---|---|
| Passive configuration checks | Observe defensive configuration | HTTP headers / cookie attributes |
| Authorization checks | Verify protected behavior requires authorization | unauthenticated protected-resource request |
| Controlled regression tests | Detect changes to known security properties | CI security fixture |
| Manual threat analysis | Identify threats automation may not discover | trust boundaries / misuse scenarios |

For each layer state what it can detect, what it cannot establish, when it should run, what evidence should be retained, and whether human review is required.

### Question 9
Which security checks belong on every commit, and which are better suited to manual review or pre-release testing? Justify.

### Question 10
If every automated security check is GREEN, can the team conclude that OpenEMR is secure? Explain.

# Required evidence

Include evidence of Stage 1 validation, completed threat model, passive baseline, unauthenticated access-control check, two threat-driven test designs, successful local controlled-fixture test, GREEN workflow, intentionally RED workflow, restored GREEN workflow, and final testing strategy.

Do not include passwords, secrets, tokens, private environment configuration, or real patient information.

# Submission

Submit a Markdown or PDF report containing answers to Questions 1–10, the completed threat model, tables/observations, focused screenshots/evidence, your testing strategy, and branch/commit identifiers for GREEN → RED → GREEN.

# Key principle

Security testing is not:

```text
run scanner → get zero findings → declare secure
```

A stronger process is:

```text
define scope and authorization
        +
model threats
        +
test selected security properties
        +
retain evidence
        +
continuously check important regressions
        ↓
better security evidence
```

Your conclusions must remain proportional to the evidence you actually collected.
