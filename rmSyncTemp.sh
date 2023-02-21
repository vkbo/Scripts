#!/bin/bash
# Clean up Syncthing temp files

if [ "$1" == "-r" ]; then
    find . -name '*.syncthing.*.tmp' -exec rm -fv {} \;
else
    find . -name '*.syncthing.*.tmp'
fi
