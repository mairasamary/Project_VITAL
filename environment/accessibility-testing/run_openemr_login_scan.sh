#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
ENV_FILE="${ROOT}/environment/.env"
IMAGE="mcr.microsoft.com/playwright:v1.62.0-noble"

if [ ! -f "${ENV_FILE}" ]; then
  echo "Missing environment/.env"
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker is not running."
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "${ENV_FILE}"
set +a

PORT="${OPENEMR_HTTPS_PORT:-9301}"

# From the Playwright container, hostmachine maps to the host running Docker.
export OPENEMR_BASE_URL="https://hostmachine:${PORT}"

echo "Scanning OpenEMR login page at:"
echo "  ${OPENEMR_BASE_URL}"
echo

docker run --rm --ipc=host \
  --add-host=hostmachine:host-gateway \
  -e OPENEMR_BASE_URL="${OPENEMR_BASE_URL}" \
  -v "${ROOT}:/work" \
  -w /work/environment/accessibility-testing \
  "${IMAGE}" \
  /bin/bash -lc "npm install >/dev/null && npx playwright test tests/openemr-login.spec.js"

echo
echo "Baseline JSON:"
echo "  ${ROOT}/.project-vital/accessibility-testing/openemr-login-axe.json"
