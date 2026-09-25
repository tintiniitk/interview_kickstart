#!/bin/bash
set -e
# shellcheck disable=SC1091
source "$(dirname "$0")"/utils.sh

if [[ $# != 2 ]]; then
	>&2 echo "expected exactly 2 argument: <job description e.g. \"job no. 1\"> <duration in seconds>"
	exit 1
fi
job_description="${1}"
job_duration_seconds="${2}"

post_route='/jobs'
post_url=${LOCALHOST}${post_route}
printf "\n\nAdding job \"%s\" with duration_seconds \"%s\" ...\n\n" "${job_description}" "${job_duration_seconds}"
run_and_log "curl -X POST -H \"Content-Type: application/json\" -d \"{\\\"description\\\": \\\"${job_description}\\\", \\\"duration_seconds\\\": ${job_duration_seconds}}\" \"${post_url}\""
