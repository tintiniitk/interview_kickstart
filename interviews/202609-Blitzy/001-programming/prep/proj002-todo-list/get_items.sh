#!/bin/bash
set -e
source $(dirname $0)/utils.sh

post_route='/items'
get_url=${LOCALHOST}${post_route}
run_and_log "curl -X GET \"${get_url}\""
