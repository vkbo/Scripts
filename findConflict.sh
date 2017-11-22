#!/bin/bash

if [ "$2" == "-r" ]; then
    find "$1" -name '*sync-conflict*' -exec rm -fv {} \;
else
    find "$1" -name '*sync-conflict*'
fi
