#!/usr/bin/env bash
set -e
# shellcheck disable=SC1091
source "$(dirname "$0")"/utils.sh

delete_jobs_route='/jobs'
get_url=${LOCALHOST}${delete_jobs_route}
run_and_log "curl -X DELETE ${INPUT_DATA} \"${get_url}\" | jq"
