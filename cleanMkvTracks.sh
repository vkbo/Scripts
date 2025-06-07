#!/bin/bash

echo "Processing: $1"
out="${1%.*}_clean.mkv"
dt=$(stat -c %y "$1")
mkvmerge -o "$out" --atracks "en,no" --stracks "en,nb" "$1"
touch -m -t $(date -d "$dt" +%Y%m%d%H%M.%S) "$out"
