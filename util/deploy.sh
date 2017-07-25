#!/bin/bash

set -e
set -u

DEST=atemoia:www/blizin.ski

helpmsg() {
  echo "$0 [ deploy | test ]"
}

case "${1:-}" in
  deploy)
    umask 022
    find static -type f -exec chmod 644 {} \;
    find static -type d -exec chmod 755 {} \;
    hugo --cleanDestinationDir
    find public -type f -exec chmod 644 {} \;
    find public -type d -exec chmod 755 {} \;
    rsync -a --delete public/ "${DEST}"
    ;;
  test)
    hugo -w -D -F --baseUrl="${HOSTNAME}" server
    ;;
  *)
    helpmsg >&2
    exit 1
    ;;
esac
