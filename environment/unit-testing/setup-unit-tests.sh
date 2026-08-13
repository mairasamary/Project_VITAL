#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
CACHE="${ROOT}/.project-vital"
SRC="${CACHE}/openemr-unit"
OPENEMR_REF="v8_2_0"
OPENEMR_REPO="https://github.com/openemr/openemr.git"

mkdir -p "${CACHE}"

if [ -d "${SRC}/.git" ]; then
    echo "OpenEMR unit-test checkout already exists:"
    echo "  ${SRC}"
    echo
    current_ref="$(git -C "${SRC}" describe --tags --exact-match 2>/dev/null || true)"
    if [ "${current_ref}" = "${OPENEMR_REF}" ]; then
        echo "Pinned OpenEMR ref ${OPENEMR_REF} is already checked out."
        exit 0
    fi
    echo "Existing checkout is not at ${OPENEMR_REF}."
    echo "Run environment/unit-testing/reset-unit-tests.sh if you want to recreate it."
    exit 1
fi

echo "Cloning OpenEMR ${OPENEMR_REF}..."
git clone --depth 1 --branch "${OPENEMR_REF}" "${OPENEMR_REPO}" "${SRC}"

mkdir -p "${SRC}/tests/Tests/Isolated/ProjectVITAL"

echo
echo "OpenEMR unit-test source prepared:"
echo "  ${SRC}"
echo
echo "Next:"
echo "  mkdir -p assignment-03/tests"
echo "  cp environment/unit-testing/examples/ProjectVITALSmokeTest.php assignment-03/tests/"
echo "  bash environment/unit-testing/run-unit-tests.sh"
