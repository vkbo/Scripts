#!/bin/bash
#
#  Main Backup Script
# ====================
#  Author:  Veronica Berglyd Olsen
#  Date:    29.06.2017
#  URL:     https://github.com/Jadzia626/Scripts
#  License: GPLv3
#  Website: http://vkbo.net
#
#  Usage:   ./7zBackup.sh [Source] [RunDiff]
#  Example: ./7zBackup.sh Sync/Primary true
#
#  [Source]  : What folder to back up. This is appended to ROOT path in settings.
#              The last part of the source path is used as the backup job name.
#  [RunDiff] : To run a differential backup, use DIFF. Otherwise a full backup
#              will run. Also, if there is no full backup found to diff against
#              a full backup is run.
#
#  Intended Usage:
#
#  This script was made to back up my Syncthing main storage, which runs on a Linux
#  server. The synced folders are sorted into Primary, Secondary and Tertiary
#  subfolders with different backup schedules. This is handled by a separate script
#  which is called from crontab every night. The script I use is also added to this
#  gist as sampleScript.sh.
#
#  The archives are encrypted 7zip files with encrypted meta data. However for
#  convenience, the file list is also outputted. This may seem a little odd, but
#  the reason I use encryption is not to protect them on the main storage, but so
#  I can sync the 7z files to off-site storage without the content being accessible.
#

# Settings

ROOT=/data/Storage                    # Root path of folders to back up
BDIR=$ROOT/Backup                     # Where to store backup files
ZPWD=$(cat $ROOT/Settings/Backup.pw)  # File where the password is stored

if [ ! -z $1 ] && [ -d $ROOT/$1 ]; then
    SDIR=$ROOT/$1
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Error: Missing source directory $ROOT/$1"
    exit 1
fi

if [ ! -z $2 ] && [ "$2" == "DIFF" ]; then
    DIFF=true
else
    DIFF=false
fi

TYPE=$(basename $SDIR)
LAST=$BDIR/$TYPE.diff
ODIR=$BDIR/$(date +%Y-%m)
CURR=$(date +%Y-%m-%d)

if [ ! -d $ODIR ]; then
    mkdir $ODIR
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Created folder $ODIR"
fi

if [ $DIFF = true ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Differentual backup of $SDIR has been requested"
    if [ -e $LAST ]; then
        DATE=$(cat $LAST)
        SARC=$BDIR/${DATE:0:7}/${DATE:0:10}.$TYPE.Full
        TARC=$ODIR/$CURR.$TYPE.Diff
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] No information on last full backup found"
        DIFF=false
        TARC=$ODIR/$CURR.$TYPE.Full
    fi
else
    TARC=$ODIR/$CURR.$TYPE.Full
fi

if [ -e $TARC.7z ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Archive already exists $TARC.7z"
    exit 0
fi

if [ $DIFF = true ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting differential backup of $SDIR"
    7z u -bd -p$ZPWD -mhe=on -xr!.stfolder $SARC.7z $SDIR -t7z -u- -up0q3r2x2y2z0w2!$TARC.7z >> $TARC.log 2>&1
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting full backup of $SDIR"
    7z u -bd -p$ZPWD -mhe=on -xr!.stfolder $TARC.7z $SDIR >> $TARC.log 2>&1
    echo $CURR > $LAST
fi

7z l  -p$ZPWD $TARC.7z > $TARC.list
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup completed"
