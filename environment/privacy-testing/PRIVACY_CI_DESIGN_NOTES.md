# Privacy CI Design Notes

The continuous privacy workflow deliberately checks only selected, automatable properties.

## Automated properties

- prohibited direct-identifier columns are absent;
- pseudonymous patient/encounter/vitals relationships remain intact;
- the selected quasi-identifier model meets the configured teaching k threshold;
- selected aggregate analytical properties remain available;
- known privacy defects are rejected.

## Properties NOT established by CI

A green workflow does not establish:

- irreversible anonymity;
- resistance to every linkage attack;
- legal compliance;
- HIPAA Safe Harbor;
- HIPAA Expert Determination;
- GDPR anonymization;
- freedom from membership inference;
- freedom from attribute disclosure;
- sufficient protection against an attacker with richer auxiliary data.

This limitation should become part of the student Assignment 5 analysis.

## Secret

The CI secret string used by this teaching workflow is not a real operational secret and is used only with synthetic data.

A real pseudonymization key must not be committed to Git or embedded in public CI configuration.
