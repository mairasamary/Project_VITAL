# Stage 1 Patch — Containerized Playwright

The first Stage 1 draft assumed that `node` and `npm` were installed on the instructor/student host.

Instructor validation immediately showed:

```text
node: command not found
```

Project VITAL already requires Docker for OpenEMR, so the accessibility test runner is now containerized as well.

This reduces the host prerequisites to:

```text
Docker
Project VITAL repository
```

rather than requiring every student to install and maintain a separate Node.js/Playwright toolchain.

The runner uses the pinned official Playwright image:

```text
mcr.microsoft.com/playwright:v1.62.0-noble
```

and the project's `@playwright/test` dependency is also pinned to `1.62.0`.

Playwright's documentation recommends keeping the Docker image version aligned with the Playwright version used by the tests.

For local OpenEMR scans, the container accesses the host through:

```text
hostmachine
```

mapped with Docker's `host-gateway`, because `localhost` from inside the Playwright container refers to that container rather than the Mac/host.
