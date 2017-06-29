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

#
#  Secondary Sync Backup
# =======================
#  Full: Every month
#  Diff: Every third day
#

find $BDIR -name "Secondary.diff" -type f -mtime +32 -delete
if [ $(date +%d) = 1 ]; then
    ./7zBackup.sh Sync/Secondary FULL
fi
if ! (($(date +%d) % 3)); then
    ./7zBackup.sh Sync/Secondary DIFF
fi

#
#  Tertiary Sync Backup
# ======================
#  Full: Every month
#  Diff: Every week
#

find $BDIR -name "Tertiary.diff" -type f -mtime +32 -delete
if [ $(date +%d) = 1 ]; then
    ./7zBackup.sh Sync/Tertiary FULL
fi
if [ $(date +%u) = 6 ]; then
    ./7zBackup.sh Sync/Tertiary DIFF
fi

#
#  Sync Versions Backup
# ======================
#  Full: Every month
#  Diff: Every week
#

find $BDIR -name "Versions.diff" -type f -mtime +32 -delete
if [ $(date +%d) = 1 ]; then
    ./7zBackup.sh Versions FULL
fi
if [ $(date +%u) = 6 ]; then
    ./7zBackup.sh Versions DIFF
fi
