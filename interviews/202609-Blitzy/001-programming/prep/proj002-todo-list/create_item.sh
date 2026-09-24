#!/bin/bash
set -e
# shellcheck disable=SC1091
source "$(dirname "$0")"/utils.sh

if [[ $# != 1 ]]; then
    >&2 echo "expected exactly 1 argument: <task text e.g. \"walk the dog\">"
    exit 1
fi
todo_text="${1}"

post_route='/items'
post_url=${LOCALHOST}${post_route}
printf "\n\nAdding todo \"%s\" ...\n\n" "${todo_text}"
run_and_log "curl -X POST -H \"Content-Type: application/json\" -d \"{\\\"text\\\": \\\"${todo_text}\\\"}\" \"${post_url}\""
