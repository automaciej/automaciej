#!/bin/bash

set -e
set -u

DEST=atemoia.blizinski.pl:www/blizin.ski
readonly PRIV_CFG=private_cfg.sh

if [[ -r "${PRIV_CFG}" ]]; then
	# To set PREVIEW_DEST and PREVIEW_URL
	source "${PRIV_CFG}"
fi

PATH=$PATH:/home/maciej/src/go/bin
export PATH

hugo=hugo
readonly hugo

helpmsg() {
  echo "$0 [ deploy | preview | dev ]"
}

function build {
    umask 022
    find static -type f -exec chmod 644 {} \;
    find static -type d -exec chmod 755 {} \;
    echo "Cleaning the destination directory…"
    ${hugo} --cleanDestinationDir "$@"
}

RSYNC=( rsync -a --delete --update )

case "${1:-}" in
  deploy)
    build
    echo "Running rsync…"
    "${RSYNC[@]}" public/ "${DEST}"
    echo "Done."
    ;;
  preview)
    build -D --baseURL "${PREVIEW_URL?}"
    echo "Running rsync…"
    "${RSYNC[@]}" public/ "${PREVIEW_DEST?}"
    echo "Done."
    ;;
  dev)
    ${hugo} -w -D -F \
	    --templateMetrics \
	    --baseURL http://localhost:1313 \
	    server
    ;;
  *)
    helpmsg >&2
    exit 1
    ;;
esac
