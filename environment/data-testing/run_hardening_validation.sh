#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"

echo "== Validate existing 200-patient batch =="
python3 "${ROOT}/environment/data-testing/validate_openemr_load.py" \
  --batch VITAL-SMALL-42

echo
echo "== Verify duplicate batch is rejected before loading =="
set +e
python3 "${ROOT}/environment/data-testing/load_openemr.py" \
  "${ROOT}/.project-vital/data-testing/small" \
  --batch VITAL-SMALL-42 --yes
rc=$?
set -e

if [ "${rc}" -ne 3 ]; then
  echo "Expected preflight exit code 3; got ${rc}"
  exit 1
fi
echo "Duplicate-batch preflight correctly rejected."

echo
echo "== Verify independent batches can coexist =="
python3 "${ROOT}/environment/data-testing/test_batch_coexistence.py"

echo
echo "HARDENING VALIDATION PASSED"
