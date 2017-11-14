#!/bin/bash

if [ "$1" == "-r" ]; then
    find . -name '*.syncthing.*.tmp' -exec rm -fv {} \;
else
    find . -name '*.syncthing.*.tmp'
fi
