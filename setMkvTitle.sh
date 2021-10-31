#!/bin/bash

# Set meta data title to same as filename and preserve modified time
for fn in *.mkv; do
    echo "Processing: $fn"
    dt=$(stat -c %y "$fn")
    mkvpropedit "$fn" -e info -s title="${fn%.mkv}"
    touch -m -t $(date -d "$dt" +%Y%m%d%H%M.%S) "$fn"
done
