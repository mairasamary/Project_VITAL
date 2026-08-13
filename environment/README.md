# Environment

This directory will contain the reproducible course environment.

## Goals

The environment should:

- use a pinned OpenEMR version;
- run in Docker or another isolated containerized environment;
- provide a consistent baseline for all teams;
- avoid real patient data;
- support fast reset/rebuild;
- allow controlled security and performance experiments;
- document all required versions and dependencies.

## Planned Contents

- Docker Compose configuration
- `.env.example`
- version-pinning documentation
- reset scripts
- synthetic-data loading instructions
- instructor setup notes

OpenEMR itself should generally be retrieved from its upstream source/image rather than copied into this repository.
