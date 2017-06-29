#!/bin/bash
#
#  autoParity
# ============
#  Author: Veronica Berglyd Olsen
#
#  Description:
#  This script will create parity files for all files in the current folder using par2, and
#  will set the redundancy higher than the largest file in the folder. Meaning that any single
#  file can be missing and still be recreated. Add edditional redundancey on top of that
#  at the prompt.
#
#  Dependency: par2
#

read -p "Additional Redundancy: " ADD

TOTAL=$(du -bc * | sort -nr | head -n1 | awk -F" " '{print $1}')
LARGEST=$(du -b * | sort -nr | head -n1 | awk -F" " '{print $1}')
RESTORE=$(((100*$LARGEST/$TOTAL)+1+$ADD))

if test $RESTORE -ge 100
then
    $RESTORE = 100
fi

echo "Largest File: $LARGEST bytes"
echo "Total Size:   $TOTAL bytes"
echo "Redundancy:   $RESTORE%"

par2create -r$RESTORE Z.par2 *
