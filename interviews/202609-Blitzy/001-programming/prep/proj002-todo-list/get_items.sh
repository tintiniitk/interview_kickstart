#!/bin/bash
set -e
source $(dirname $0)/utils.sh

if [[ $# > 2 ]] ; then
    >&2 echo "At the most 2 arguments (both optional) expected: [<limit>=0 [<status>=null]]"
    exit 1
fi
INPUT_DATA=""
if [[ $# > 0 ]] ; then
    limit=${1}
    INPUT_DATA+="\\\"limit\\\": ${limit}"
    if [[ $# > 1 ]] ; then
        status=${2}
        INPUT_DATA+=", \\\"status\\\": \\\"${status}\\\""
    fi
fi
if test -n "${INPUT_DATA}" ; then
    INPUT_DATA="-H \"Content-Type: application/json\" -d \"{${INPUT_DATA}\"}"
fi

post_route='/items'
get_url=${LOCALHOST}${post_route}
run_and_log "curl -X GET ${INPUT_DATA} \"${get_url}\""
