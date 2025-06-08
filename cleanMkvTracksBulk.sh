#!/bin/bash

for fn in *.mkv; do
    echo "Processing: $fn"
    if [ -n "$1" ]; then
        out="$1/$fn"
    else
        out="${fn%.*}_clean.mkv"
    fi
    dt=$(stat -c %y "$fn")
    mkvmerge -o "$out" --atracks "en,nb,no,da,sv" --stracks "en,nb,no" "$fn"
    touch -m -t $(date -d "$dt" +%Y%m%d%H%M.%S) "$out"
done
