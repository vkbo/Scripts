#!/bin/bash
#
# Sample cron script for 7zBackup.sh
#

cd /data/Scripts
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running daily backup script"

BDIR=/data/Storage/Backup

#
#  Primary Sync Backup
# =====================
#  Full: Every week
#  Diff: Every day
#

find $BDIR -name "Primary.diff" -type f -mtime +8 -delete
if [ $(date +%u) = 6 ]; then
    ./7zBackup.sh Sync/Primary FULL
else
    ./7zBackup.sh Sync/Primary DIFF
fi
