#!/bin/bash
set -e
source $(dirname $0)/utils.sh

post_route='/shorten'
post_url=${LOCALHOST}${post_route}
orig_urls=("www.google.com" "www.yahoo.com" "www.microsoft.com" "www.amazon.com")
for orig_url_index in "${!orig_urls[@]}" ; do
    orig_url="${orig_urls[${orig_url_index}]}"
    printf "\n\nAdding orig_url_index \"${orig_url}\" ...\n\n"
    run_and_log "curl -X POST -H \"Content-Type: application/json\" -d \"{\\\"url\\\": \\\"https://${orig_url}\\\", \\\"ttl_seconds\\\": 180}\" \"${post_url}\""
done