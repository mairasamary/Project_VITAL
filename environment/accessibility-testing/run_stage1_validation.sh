#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
DIR="${ROOT}/environment/accessibility-testing"

echo "== 1. Verify Node/npm =="
node --version
npm --version

echo
echo "== 2. Install pinned accessibility-test dependencies =="
cd "${DIR}"
npm install

echo
echo "== 3. Install Chromium for Playwright =="
npx playwright install chromium

echo
echo "== 4. Validate accessible and deliberately broken fixtures =="
npx playwright test tests/fixture-accessibility.spec.js

echo
echo "STAGE 1 ACCESSIBILITY TOOLCHAIN VALIDATION PASSED"
echo
echo "Next, with OpenEMR running, execute:"
echo "  bash environment/accessibility-testing/run_openemr_login_scan.sh"
