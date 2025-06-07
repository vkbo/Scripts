#!/bin/bash

for fn in *.mkv; do
    echo "Processing: $fn"
    out="${1%.*}_clean.mkv"
    dt=$(stat -c %y "$fn")
    mkvmerge -o "$out" --atracks "en,no" --stracks "en,nb" "$fn"
    touch -m -t $(date -d "$dt" +%Y%m%d%H%M.%S) "$out"
done
