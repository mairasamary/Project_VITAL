#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
IMAGE="mcr.microsoft.com/playwright:v1.62.0-noble"

if ! docker info >/dev/null 2>&1; then
  echo "Docker is not running."
  exit 1
fi

docker run --rm --ipc=host \
  -v "${ROOT}:/work" \
  -w /work/environment/accessibility-testing \
  "${IMAGE}" \
  /bin/bash -lc "npm install >/dev/null && npx playwright test tests/accessibility-ci.spec.js"

echo
echo "LOCAL ACCESSIBILITY CI CHECKS PASSED"
