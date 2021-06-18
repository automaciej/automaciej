#!/bin/bash

readarray -t files < <(find content -name '*.md')

for f in "${files[@]}"; do
	if ! grep -q -E '<!--.*more.*-->' "${f}"; then
		echo "${f}"
	fi
done
