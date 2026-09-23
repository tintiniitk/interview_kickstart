#!/bin/bash
set -e
source $(dirname $0)/utils.sh

if [[ $# > 0 ]] ; then
    >&2 echo "No argument expected"
    exit 1
fi

post_route='/items'
get_url=${LOCALHOST}${post_route}
run_and_log "curl -X GET -H \"Content-Type: application/json\" \"${get_url}\""
