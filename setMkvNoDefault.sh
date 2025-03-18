#!/bin/bash
# Turn off forced subtitles track

for fn in *.mkv; do
    echo "Processing: $fn"
    dt=$(stat -c %y "$fn")
    mkvpropedit "$fn" -e track:s1 -s flag-forced=0 -s flag-default=0
    touch -m -t $(date -d "$dt" +%Y%m%d%H%M.%S) "$fn"
done
