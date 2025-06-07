#!/bin/bash

echo "Processing: $1"
OUT="${1%.*}_clean.mkv"
DT=$(stat -c %y "$1")
mkvmerge -o "$OUT" --atracks "en,no" --stracks "en,nb" "$1"
touch -m -t $(date -d "$DT" +%Y%m%d%H%M.%S) "$OUT"
