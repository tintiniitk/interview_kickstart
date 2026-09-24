#!/bin/bash
set -e
# shellcheck disable=SC1091
source "$(dirname "$0")"/utils.sh

if [[ $# -gt 1 ]] ; then
    >&2 echo "At the most 1 arguments (both optional) expected: [<status>]"
    exit 1
fi
INPUT_DATA=""
if [[ $# -gt 0 ]] ; then
    status=${1}
    INPUT_DATA+="\\\"status\\\": \\\"${status}\\\""
fi
if test -n "${INPUT_DATA}" ; then
    INPUT_DATA="-H \"Content-Type: application/json\" -d \"{${INPUT_DATA}\"}"
fi

post_route='/items'
items_url=${LOCALHOST}${post_route}
run_and_log "curl -X DELETE ${INPUT_DATA} \"${items_url}\""
