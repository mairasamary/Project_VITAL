# Assignment 07 report templates
Create the following files under assignment-07. Replace every placeholder with your own evidence.
## SUBMISSION.md
Team / workflow / members and individual contributions; OpenEMR version and local setup; synthetic data setup; role configuration; tool versions; exact install and execution commands; evidence index (path, test ID, outcome); known limitations; CI run links; final tag.
## threat-model.md
Diagram with labeled assets, actors, trust boundaries and flows. Table: threat ID | STRIDE category | asset | actor | boundary | threat | control | test ID. Include scope and exclusions.
## security-test-plan.md
Test ID | threat ID | category | role | preconditions | steps | expected outcome | evidence required. Preserve initial plan and document later changes.
## manual-security-report.md
Role matrix: operation | expected permissions by role | observed permissions by role | evidence. For each test: ID, actual result, pass/fail/inconclusive, evidence, cleanup. Include positive controls.
## automated-security-report.md
ZAP version, passive-only scope, browser and workflow states, scan observations, three manual verifications, limitations. Redact all cookies, credentials, tokens and synthetic identifiers where unnecessary.
## security-findings.md
Finding ID | threat ID | classification | severity and rationale | preconditions | reproduction | expected | actual | evidence | impact | recommendation | regression ID.
## automation.md
Test ID | finding/control | fixture or live | assertions | command | outcome | evidence. Include dependency versions, environment variable names (not values), cleanup and limitations.
## ci-report.md
Stage | commit SHA | run URL | expected | actual | failed assertion. Explain restored fixture and why fixture success is not OpenEMR assurance.
## ai-evaluation.md
Initial plan reference; five suggestions with relevance, correctness, safety, decision and rationale; accepted test ID; validation and corrections. No secrets in prompts.
## reflection.md
Highest-impact concern; evidence limits; security vs privacy; AI limitations; permanent regression priorities.
