#!/bin/bash

if [ ! -z "$1" ]; then
    SDIR=$1
else
    echo "Missing input folder"
    exit 1
fi

if [ ! -z "$2" ]; then
    ARCH=$2
else
    ARCH=${SDIR%/}.tar.gz
fi

tar -czvf "$ARCH" "$SDIR"
touch -r "$SDIR" "$ARCH"
