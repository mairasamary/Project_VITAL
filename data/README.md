# Data

This directory contains tools and guidance for synthetic test data and anonymization exercises.

## Core Principles

Project VITAL should not require real patient or protected health information.

Data activities should emphasize:

- synthetic data generation;
- reproducibility;
- referential integrity;
- atomicity;
- insertion order;
- transparency;
- anonymization and pseudonymization;
- validation of generated records.

## Suggested Dataset Sizes

- **Small:** approximately 200 users/objects
- **Medium:** approximately 2,000 users/objects
- **High:** approximately 20,000 users/objects

Generators should support deterministic seeds where practical so failures can be reproduced consistently.
