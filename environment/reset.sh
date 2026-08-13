#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "This will delete the Project VITAL OpenEMR database and all persistent local course data."
read -r -p "Type RESET to continue: " answer

if [ "$answer" != "RESET" ]; then
  echo "Reset cancelled."
  exit 0
fi

docker compose down -v
docker compose up -d

echo "Project VITAL environment reset complete."
