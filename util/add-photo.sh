#!/bin/bash

# Adds a photo to blog.
# 
# Usage:
#   add-photo /path/to/IMG0001.JPG bike-trip-01

set -u
set -x
set -e

readonly INPUT_FILE=$1
shift

readonly TITLE=$1
shift

declare -r YEAR="$(date +%Y)"
readonly IMG_DIR=static/images
declare -r SIZE_BIG="1280x1280"
declare -r SIZE_SMALL="440x440"

function conv_img {
  local _FROM=$1
  local _SIZE=$2
  local _TO=$3
convert \
    -size "$_SIZE" \
    "$_FROM" \
    -resize $_SIZE \
    +profile '*' \
    -quality 95 \
    "$_TO"
git add "${_TO}"
}
conv_img "${INPUT_FILE}" "${SIZE_SMALL}" "${IMG_DIR}/${YEAR}/${TITLE}-small.jpg"
conv_img "${INPUT_FILE}" "${SIZE_BIG}" "${IMG_DIR}/${YEAR}/${TITLE}.jpg"
echo "image = \"/images/${YEAR}/${TITLE}.jpg\""
echo "{{< figure src=\"/images/${YEAR}/${TITLE}-small.jpg\" >}}"
