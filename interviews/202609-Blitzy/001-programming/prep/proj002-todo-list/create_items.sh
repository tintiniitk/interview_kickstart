#!/bin/bash
set -e
# shellcheck disable=SC1091
source "$(dirname "$0")"/utils.sh

if [[ $# -gt 0 ]]; then
    >&2 echo "No argument expected"
    exit 1
fi

post_route='/items'
post_url=${LOCALHOST}${post_route}
todos=("Walk the dog" "Buy groceries on weekend" "Buy shoes on Sunday" "Buy round-trip air-tickets next week")
for todo in "${!todos[@]}"; do
    todo_text="${todos[${todo}]}"
    printf "\n\nAdding todo \"%s\" ...\n\n" "{todo_text}"
    run_and_log "curl -X POST -H \"Content-Type: application/json\" -d \"{\\\"text\\\": \\\"${todo_text}\\\"}\" \"${post_url}\""
done
