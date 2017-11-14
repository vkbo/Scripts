#!/bin/bash

if [ "$1" == "-r" ]; then
    find Sync -name '*sync-conflict*' -exec rm -fv {} \;
else
    find Sync -name '*sync-conflict*'
fi
