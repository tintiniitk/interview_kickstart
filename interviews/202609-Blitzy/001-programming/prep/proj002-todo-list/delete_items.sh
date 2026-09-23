#!/bin/bash
set -e
source $(dirname $0)/utils.sh

post_route='/items'
items_url=${LOCALHOST}${post_route}
run_and_log "curl -X DELETE \"${items_url}\""
