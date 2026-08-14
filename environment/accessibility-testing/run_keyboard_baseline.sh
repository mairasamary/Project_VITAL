#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
ENV_FILE="${ROOT}/environment/.env"
IMAGE="mcr.microsoft.com/playwright:v1.62.0-noble"

set -a
# shellcheck disable=SC1090
source "${ENV_FILE}"
set +a

PORT="${OPENEMR_HTTPS_PORT:-8443}"
export OPENEMR_BASE_URL="https://host.docker.internal:${PORT}"

docker run --rm --ipc=host \
  -e OPENEMR_BASE_URL="${OPENEMR_BASE_URL}" \
  -e OPENEMR_ADMIN_USER="${OPENEMR_ADMIN_USER}" \
  -e OPENEMR_ADMIN_PASSWORD="${OPENEMR_ADMIN_PASSWORD}" \
  -v "${ROOT}:/work" \
  -w /work/environment/accessibility-testing \
  "${IMAGE}" \
  /bin/bash -lc "npm install >/dev/null && npx playwright test tests/openemr-keyboard-baseline.spec.js"

echo
echo "Keyboard evidence:"
echo "  ${ROOT}/.project-vital/accessibility-testing/authenticated/keyboard-focus-sequence.json"
