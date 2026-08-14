#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
DATA="${ROOT}/.project-vital/data-testing/stage2-five"
BATCH="STAGE2-FIVE"

echo "== 1. Generate deterministic source data =="
python3 "${ROOT}/environment/data-testing/generate_data.py" \
  --size small --patients 5 --seed 42 --output "${DATA}"

echo "== 2. Validate intermediate data =="
python3 "${ROOT}/environment/data-testing/validate_data.py" "${DATA}"

echo "== 3. Remove prior validation batch if present =="
python3 "${ROOT}/environment/data-testing/reset_loaded_data.py" \
  --batch "${BATCH}" --yes || true

echo "== 4. Load 5 patients transactionally =="
python3 "${ROOT}/environment/data-testing/load_openemr.py" \
  "${DATA}" --batch "${BATCH}" --yes

echo "== 5. Validate database relationships =="
python3 "${ROOT}/environment/data-testing/validate_openemr_load.py" \
  --batch "${BATCH}"

echo
echo "STAGE 2 FIVE-PATIENT LOAD PASSED."
echo "Inspect these records in OpenEMR before resetting."
echo "When ready:"
echo "python3 environment/data-testing/reset_loaded_data.py --batch ${BATCH}"
