#!/bin/bash
# A wrapper script to create a 7z archive from a folder.
# Usage: 7zArch.sh <path> <archive>

if [ ! -z "$1" ]; then
    SDIR=$1
else
    echo "Missing input folder"
    exit 1
fi

if [ ! -z "$2" ]; then
    ARCH=$2
else
    ARCH=${SDIR%/}.7z
fi

7z a -r -p -bb0 -mhe=on "$ARCH" "$SDIR"
touch -r "$SDIR" "$ARCH"
