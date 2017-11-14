#!/bin/bash

if [ "$1" == "-r" ]; then
    find . -name '*sync-conflict*' -exec rm -fv {} \;
else
    find . -name '*sync-conflict*'
fi
