#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
DIR="${ROOT}/environment/accessibility-testing"
IMAGE="mcr.microsoft.com/playwright:v1.62.0-noble"

if ! docker info >/dev/null 2>&1; then
  echo "Docker is not running."
  exit 1
fi

echo "== 1. Pull pinned Playwright image =="
docker pull "${IMAGE}"

echo
echo "== 2. Install project dependencies inside container =="
docker run --rm --ipc=host \
  -v "${ROOT}:/work" \
  -w /work/environment/accessibility-testing \
  "${IMAGE}" \
  /bin/bash -lc "npm install"

echo
echo "== 3. Validate accessible and deliberately broken fixtures =="
docker run --rm --ipc=host \
  -v "${ROOT}:/work" \
  -w /work/environment/accessibility-testing \
  "${IMAGE}" \
  /bin/bash -lc "npx playwright test tests/fixture-accessibility.spec.js"

echo
echo "STAGE 1 ACCESSIBILITY TOOLCHAIN VALIDATION PASSED"
echo
echo "Next, with OpenEMR running, execute:"
echo "  bash environment/accessibility-testing/run_openemr_login_scan.sh"
