#!/bin/bash
#
# Render two git commits as Hugo sites and diff the generated output.
#
# Usage: util/diff_commits.sh <commit1> <commit2> <diff_output_file>

set -e
set -u

helpmsg() {
	echo "Usage: $0 <commit1> <commit2> <diff_output_file>"
}

if [[ $# -ne 3 ]]; then
	helpmsg >&2
	exit 1
fi

readonly COMMIT1="$1"
readonly COMMIT2="$2"
readonly OUTFILE="$3"

readonly REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "${REPO_ROOT}"

# mktemp under $HOME, not /tmp: snap-confined hugo can't read outside
# the home directory, and its home-interface grant excludes dotfiles,
# so the directory name must not start with a dot either.
readonly WORKDIR="$(mktemp -d "${HOME}/diff_commits_tmp.XXXXXX")"
readonly WT1="${WORKDIR}/wt1"
readonly WT2="${WORKDIR}/wt2"
readonly BUILD1="${WORKDIR}/build1"
readonly BUILD2="${WORKDIR}/build2"

cleanup() {
	git worktree remove --force "${WT1}" 2>/dev/null || true
	git worktree remove --force "${WT2}" 2>/dev/null || true
	rm -rf "${WORKDIR}"
}
trap cleanup EXIT

echo "Checking out ${COMMIT1} into ${WT1}…"
git worktree add --detach --quiet "${WT1}" "${COMMIT1}"

echo "Checking out ${COMMIT2} into ${WT2}…"
git worktree add --detach --quiet "${WT2}" "${COMMIT2}"

echo "Building ${COMMIT1}…"
( cd "${WT1}" && hugo --cleanDestinationDir -D -d "${BUILD1}" )

echo "Building ${COMMIT2}…"
( cd "${WT2}" && hugo --cleanDestinationDir -D -d "${BUILD2}" )

echo "Diffing output…"
{
	echo "# diff ${COMMIT1} -> ${COMMIT2}"
	echo
	diff -rq "${BUILD1}" "${BUILD2}" || true
	echo
	diff -ru "${BUILD1}" "${BUILD2}" || true
} > "${OUTFILE}"

echo "Diff written to ${OUTFILE}."
