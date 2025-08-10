#!/bin/bash
# Delete first argument from all zip files in current folder

for fn in *.zip; do
    echo "Processing: $fn"
    dt=$(stat -c %y "$fn")
    zip --delete "$fn" "$1"
    touch -m -t $(date -d "$dt" +%Y%m%d%H%M.%S) "$fn"
done
