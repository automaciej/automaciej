#!/bin/bash

set -u
set -e

DEST=quinoa:maciej.blizinski.pl

helpmsg() {
  echo "$0 [ deploy | test ]"
}

case "${1:-}" in
  deploy)
    hugo --cleanDestinationDir
    rsync -p -r --delete public/ "${DEST}"
    ;;
  test)
    hugo -w -D -F --baseUrl="${HOSTNAME}" server
    ;;
  *)
    helpmsg >&2
    exit 1
    ;;
esac
