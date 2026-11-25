# Assignment 07 — Security Testing and Security Regression
**Due: Tuesday, December 8, 2026, 11:59 PM ET. Total: 100 points. Team assignment.**

Use only your isolated local OpenEMR instance, synthetic records and approved test accounts. No external scanning, brute force, destructive testing, denial of service, or unrestricted active scanning. Never commit credentials, tokens or patient information.

## Workflows
Team 01: appointment scheduling. Team 02: recording vitals. Team 03: patient registration.

## Requirements and rubric
1. **Threat model (15):** Four assets, three actors, three trust boundaries, six threats and corresponding controls. Address all STRIDE categories, marking irrelevant categories with justification. Include a data-flow diagram.
2. **Test plan (10):** Design 12 tests before execution: two authentication, four authorization, two session, two input validation, two configuration. Include IDs, threat links, preconditions, steps, expected outcomes and evidence.
3. **Manual testing (20):** Execute all 12 against local OpenEMR. Configure three approved roles and document expected versus observed permissions. Include positive and negative checks; distinguish hidden UI from enforced authorization. Use only synthetic records; restore any authorized changes.
4. **Automated analysis (10):** Use ZAP passive scanning of normal local workflow traffic. Record version, scope, states and sanitized results. Manually investigate three observations (including passing checks if needed). Explain local HTTP limitations and scanner blind spots. Do not use active scan or spider.
5. **Findings (10):** Report three evidence-based defects, concerns or verified controls, with ID, threat, classification, severity rationale, reproduction, expected/actual, evidence, impact, recommendation and regression link. Do not invent defects.
6. **Regression tests (15):** Four new executable tests, at least three against actual local OpenEMR. Include positive authorization, negative authorization and authentication/session assertions; fourth is a relevant security property. Link at least one to a finding. Record commands, versions and results. Correctly failing tests receive credit; do not weaken assertions. Fixture starter tests do not count.
7. **CI (10):** Add security-tests.yml. Extend the controlled fixture test suite with one meaningful assertion. Demonstrate GREEN → RED → GREEN by temporarily removing the fixture's nosniff header, without modifying the test, then restoring it. Record commit SHAs, run URLs and failed assertion. Never weaken OpenEMR itself.
8. **AI evaluation and reflection (10):** Independently draft plan, then evaluate five AI suggestions for correctness, relevance and safety. Implement one accepted suggestion within the four tests. Explain validation, corrections, limitations, security versus privacy and future regression priorities.

## Starter infrastructure
The existing environment/security-testing scripts provide a controlled Python HTTP fixture, baseline header observations and an unauthenticated entry-point check. Run `bash environment/security-testing/run_stage1_validation.sh` from the project root. These are preliminary checks, not proof of OpenEMR security and not substitutes for your four tests. Copy the relevant fixture and tests into your team submission or document their exact paths. The fixture uses loopback only.

## Submission
Under assignment-07/ include README.md, SUBMISSION.md, threat-model.md, security-test-plan.md, manual-security-report.md, automated-security-report.md, security-findings.md, automation.md, ci-report.md, ai-evaluation.md, reflection.md, diagrams, tests and sanitized evidence. Include dependency lockfiles for third-party dependencies. SUBMISSION.md must index evidence, setup, versions, commands, test outcomes and individual contributions. Add the CI workflow under .github/workflows/. Restore fixture, verify GREEN, then create and push annotated tag assignment-07.

## References
- https://www.zaproxy.org/docs/
- https://owasp.org/www-project-web-security-testing-guide/
- https://playwright.dev/docs/test-intro

A clean scan or passing suite does not prove security. Conclusions must be proportional to evidence.
