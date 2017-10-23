#!/bin/bash

set -x
set -e
set -u

SOURCE_DIR=jogger/output
APPROVED_DIR=content/post
REJECTED_DIR=jogger/rejected

mkdir -p "${REJECTED_DIR}"

declare -a FILES=()

while read LINE; do
  FILES[${#FILES[@]}]="${LINE}"
done < <(find "${SOURCE_DIR}" -name '*.md' -print)

echo "${#FILES[@]} files to process…"

function migrate_file_to_hugo {
  local APPROVED_DIR=$1
  shift
  local F=$1
  shift
  local bn=$(basename "${F}")
  vim "${F}"
  mv "${F}" "${APPROVED_DIR}"
  git add "${APPROVED_DIR}/${bn}"
}

for LINE in "${FILES[@]}"; do
  clear
  echo "${LINE}"
  head -n 40 "${LINE}"
  read -p "${LINE}: Approve? [y/n]" ANS
  case "${ANS}" in
    y)
      migrate_file_to_hugo "${APPROVED_DIR}" "${LINE}"
      ;;
    n)
      mv "${LINE}" "${REJECTED_DIR}"
      ;;
    *)
      echo >&2 "eh?"
      ;;
  esac
  echo "Sleeping for 1s… Press CTRL+C to stop."
  sleep 1
done
