#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SRC="${ROOT}/.project-vital/openemr-unit"

if [ ! -d "${SRC}" ]; then
    echo "No cached OpenEMR unit-test checkout exists."
    exit 0
fi

echo "This removes ONLY the cached OpenEMR unit-test checkout:"
echo "  ${SRC}"
echo
echo "Your assignment-03/tests files will not be removed."
read -r -p "Type RESET to continue: " answer

if [ "${answer}" != "RESET" ]; then
    echo "Reset cancelled."
    exit 0
fi

rm -rf "${SRC}"
echo "Cached OpenEMR unit-test checkout removed."
