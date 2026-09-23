#!/bin/bash
set -e
source $(dirname $0)/utils.sh

if [[ $# != 2 ]] ; then
    >&2 echo "expected exactly 2 arguments: <item_id> <new_status from in_progress, done>"
    exit 1
fi
item_id=${1}
new_status=${2}

post_route="/items/${item_id}"
items_url=${LOCALHOST}${post_route}
run_and_log "curl -X PATCH -H \"Content-Type: application/json\" -d \"{\\\"status\\\": \\\"${new_status}\\\"}\" \"${items_url}\""
