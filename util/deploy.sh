#!/bin/bash

set -e
set -u

DEST=atemoia:www/blizin.ski

if [[ -r "private.cfg.sh" ]]; then
	# To set PREVIEW_DEST and PREVIEW_URL
	source private.cfg.sh
fi

PATH=$PATH:/home/maciej/src/go/bin
export PATH

hugo=hugo
readonly hugo

helpmsg() {
  echo "$0 [ deploy | draft | test ]"
}

function build {
    umask 022
    find static -type f -exec chmod 644 {} \;
    find static -type d -exec chmod 755 {} \;
    echo "Cleaning the destination directory…"
    ${hugo} --cleanDestinationDir "$@"
    find public -type f -exec chmod 644 {} \;
    find public -type d -exec chmod 755 {} \;
}

case "${1:-}" in
  deploy)
    build
    echo "Running rsync…"
    rsync -a --delete public/ "${DEST}"
    echo "Done."
    ;;
  preview)
    build -D --baseURL "${PREVIEW_URL?}"
    echo "Running rsync…"
    rsync -a --delete public/ "${PREVIEW_DEST?}"
    echo "Done."
    ;;
  test)
    ${hugo} -w -D -F server
    ;;
  *)
    helpmsg >&2
    exit 1
    ;;
esac
