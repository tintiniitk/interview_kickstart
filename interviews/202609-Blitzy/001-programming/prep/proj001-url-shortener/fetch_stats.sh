#!/bin/bash
set -e
source $(dirname $0)/utils.sh

if [[ $# -lt 1 ]] ; then
    >2 echo "minimum 1 argument required: <short-route_url>"
    exit 1
fi

short_url=${1}

route_url='/stats/${short_url}'
get_url=${LOCALHOST}${route_url}
run_and_log "curl -X GET \"${get_url}\""
