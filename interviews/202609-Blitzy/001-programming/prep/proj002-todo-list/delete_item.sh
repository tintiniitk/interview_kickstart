#!/bin/bash
set -e
# shellcheck disable=SC1091
source "$(dirname "$0")"/utils.sh

if [[ $# != 1 ]]; then
    >&2 echo "expected exactly 1 argument: <item_id>"
    exit 1
fi
item_id=${1}

post_route="/items/${item_id}"
items_url=${LOCALHOST}${post_route}
run_and_log "curl -X DELETE \"${items_url}\""
