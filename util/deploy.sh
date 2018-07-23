#!/bin/bash

set -e
set -u

DEST=atemoia:www/blizin.ski

export PATH=$PATH:/home/maciej/src/go/bin
hugo=hugo

helpmsg() {
  echo "$0 [ deploy | test ]"
}

case "${1:-}" in
  deploy)
    umask 022
    find static -type f -exec chmod 644 {} \;
    find static -type d -exec chmod 755 {} \;
    echo "Cleaning the destination directory…"
    ${hugo} --cleanDestinationDir
    find public -type f -exec chmod 644 {} \;
    find public -type d -exec chmod 755 {} \;
    echo "Running rsync…"
    rsync -a --delete public/ "${DEST}"
    echo "Done."
    ;;
  test)
    ${hugo} -w -D -F --baseUrl="${HOSTNAME}" server
    ;;
  *)
    helpmsg >&2
    exit 1
    ;;
esac
