#!/usr/bin/env python3
"""Simple tool to hash and verify files in a directory tree.

This script can be used to regularly check the integrity of a directory
structure. The tools has a set of switches that allow you to choose whether to
list, check, maintain or update the content of a folder, recursively.

The tool will detect changes to file data, deleted files, newly added files,
file renames and duplicate files. It does this by using the standard MD5
hashing algorithms. The decision to use MD5 is primarily for speed since this is
not a security tool. The MD5 algorithm is not safe for other uses.

The tool creates a folder in the current working directory names "Hash". (The
folder can be changed by specifying `--md5dir`.) It also keeps a backup of
previous hash files when it is in writing mode, so it never overwrites the
latest hash file.

The hash file itself is a valid .md5 hash file and can be used with the
standard `md5sum -c <hashfile.md5>` command.

Usage Example:

Scan all files in your Documents folder, and check their hash against previous
values.

```bash
ch ~
python hashDir.py --update Documents
```

Scan all files in your Documents folder, but don't check already known files.

```bash
ch ~
python hashDir.py --maintain Documents
```

Check the integrity of all files in the folder against previous hash file.

```bash
ch ~
python hashDir.py --check Documents
```

"""

import os
import sys
import signal
import argparse
import datetime
import subprocess

__version__ = "2023.03.19"


def signalHandler(signal, frame):
    print("\nExiting ...")
    sys.exit(0)


def getFileSize(fileName):
    """Formats a file size with kB, MB, GB, etc.
    """
    try:
        theVal = float(os.path.getsize(fileName))
    except Exception:
        theVal = 0

    for pF in ["k", "M", "G", "T", "P", "E"]:
        theVal /= 1000.0
        if theVal < 1000.0:
            if theVal < 10.0:
                return f"{theVal:5.3f} {pF}B"
            elif theVal < 100.0:
                return f"{theVal:5.2f} {pF}B"
            else:
                return f"{theVal:5.1f} {pF}B"

    return str(theVal)


def hashDir(args):
    """The core hashing function.
    """
    print("Hashing Folder")
    print("==============")

    # Capture ctrl+c
    signal.signal(signal.SIGINT, signalHandler)

    scanDir = os.path.relpath(args.path)
    baseDir = os.path.basename(os.path.abspath(args.path.rstrip("/")))
    hashDir = os.path.abspath(args.md5dir)
    backDir = os.path.join(hashDir, "backup")
    hashFile = os.path.join(hashDir, baseDir+".md5")

    if not os.path.isdir(hashDir):
        os.mkdir(hashDir)
    if not os.path.isdir(backDir):
        os.mkdir(backDir)

    if args.tee:
        logStream = open(f"{scanDir}.log", mode="w")

        def tPrint(text, end="\n"):
            logStream.write(f"{text}{end}")
            logStream.flush()
            print(text, end=end)

    else:
        def tPrint(text, end=None):
            print(text, end=end)

    tPrint(f"Scan Path: {scanDir}")
    tPrint(f"Hash File: {hashFile}")
    tPrint("")

    hashData = {}
    hashMap = {}
    duplicateFiles = []
    tPrint("Scanning for previous hash file ... ", end="")
    if os.path.isfile(hashFile):
        with open(hashFile, mode="r") as inFile:
            for hashLine in inFile:
                if len(hashLine) > 34:
                    theHash = hashLine[:32]
                    theFile = hashLine[34:].rstrip("\n")
                    hashData[theFile] = [theHash, False]
                    if theHash in hashMap:
                        duplicateFiles.append((theFile, hashMap[theHash]))
                    hashMap[theHash] = theFile
            tPrint(f"found {len(hashData)} records")
    else:
        tPrint("not found")

    fileList = []
    tPrint("Scanning for files ... ", end="")
    for tRoot, _, tFiles in os.walk(scanDir):
        if len(tFiles) > 0:
            for tFile in tFiles:
                fileList.append(os.path.join(tRoot, tFile))
    tPrint(f"found {len(fileList)} files")
    tPrint("")

    nFiles = len(fileList)
    nCount = 0
    newList = []
    failList = []
    renameList = []

    doList = args.update or args.maintain or args.maintain or args.list
    doScan = (args.update or args.maintain or args.maintain) and not args.list
    doWrite = (args.update or args.maintain) and not args.list
    doCompare = args.check or args.update

    tPrint("Run Mode:")
    tPrint(" - Check file existence (list): %s" % ("Yes" if doList else "No"))
    tPrint(" - Add new files (maintain): %s" % ("Yes" if doScan else "No"))
    tPrint(" - Remove deleted files (maintain): %s" % ("Yes" if doScan else "No"))
    tPrint(" - Check existing records (check): %s" % ("Yes" if doCompare else "No"))
    tPrint(" - Write changes (update/maintain): %s" % ("Yes" if doWrite else "No"))
    tPrint("")

    if doWrite:
        if os.path.isfile(hashFile):
            modTime = os.path.getmtime(hashFile)
            timeStamp = datetime.datetime.fromtimestamp(modTime).strftime("%Y%m%d-%H%M%S")
            backFile = os.path.join(backDir, baseDir+"-"+timeStamp+".md5")
            os.rename(hashFile, backFile)
            tPrint(f"Copied: {hashFile} -> {backFile}")
            tPrint("")
        outFile = open(hashFile, mode="w+")

    for chkFile in sorted(fileList):
        theStatus = "   None"
        isGone = not os.path.isfile(chkFile)
        isKnown = chkFile in hashData and not isGone
        doHash = doCompare or (args.maintain and not isKnown)

        isRename = False
        newHash = ""

        if doHash and not isGone:
            cmdFile = chkFile.replace('"', r'\"').replace("$", r"\$")
            sysP = subprocess.Popen(
                [f'md5sum "{cmdFile}"'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            stdOut, _ = sysP.communicate()
            newHash = stdOut.decode("utf-8")[:32].rstrip("\n")
            isRename = newHash in hashMap

        if isKnown:
            hashData[chkFile][1] = True
            oldHash = hashData[chkFile][0]

            theStatus = "   Found"
            saveHash = oldHash

            if doCompare:
                if newHash == oldHash:
                    theStatus = "   Passed"
                    saveHash = oldHash
                else:
                    if doWrite:
                        theStatus = "***Changed"
                        saveHash = newHash
                    else:
                        theStatus = "***Failed"
                        saveHash = oldHash
                    failList.append((chkFile, oldHash, newHash))

        elif isRename:
            oldFile = hashMap[newHash]
            hashData[oldFile][1] = True
            theStatus = "***Renamed"
            saveHash = newHash
            renameList.append((chkFile, oldFile, newHash))

        else:
            if isGone:
                theStatus = "***Gone"
                saveHash = "-"*32
            else:
                theStatus = "   New"
                newList.append((chkFile, newHash))
                saveHash = newHash

        nCount += 1
        progress = 100*nCount/nFiles
        fileSize = getFileSize(chkFile)
        tPrint(f"[{progress:6.2f}%] {theStatus:<10s}  {saveHash}  {fileSize:8s}  {chkFile}")
        if doWrite:
            outFile.write(f"{saveHash}  {chkFile}\n")
            outFile.flush()

    tPrint("")

    if doWrite:
        outFile.close()

    # Generate Reports
    # ================

    def plural(count):
        return "s" if count > 1 else ""

    # Pre-Compute
    missList = []
    for hFile in hashData:
        if not hashData[hFile][1]:
            missList.append((hashData[hFile][0], hFile))

    duplList = []
    for fileOne, fileTwo in duplicateFiles:
        if hashData[fileOne][1] and hashData[fileTwo][1]:
            duplList.append((hashData[fileTwo][0], fileOne, fileTwo))

    # Reports
    nDupl = len(duplList)
    if nDupl > 0:
        tPrint("")
        tPrint(f"{nDupl} Duplicate File{plural(nDupl)} ({100*nDupl/nFiles:.2f}%)")
        tPrint("")
        for fileHash, fileOne, fileTwo in duplList:
            tPrint(f"{fileHash:32s}  {fileOne} == {fileTwo}")
        tPrint("")

    nRename = len(renameList)
    if nRename > 0:
        tPrint("")
        tPrint(f"{nRename} Renamed File{plural(nRename)} ({100*nRename/nFiles:.2f}%)")
        tPrint("")
        for chkFile, oldFile, newHash in renameList:
            tPrint(f"{newHash:32s}  {oldFile} -> {chkFile}")
        tPrint("")

    nFail = len(failList)
    if nFail > 0:
        tPrint("")
        tPrint(f"{nFail} Failed Check{plural(nFail)} ({100*nFail/nFiles:.2f}%)")
        tPrint("")
        for chkFile, prevHash, newHash in failList:
            tPrint(f"{newHash:32s} != {prevHash:32s}  {chkFile}")
        tPrint("")

    nNew = len(newList)
    if nNew > 0:
        tPrint("")
        tPrint(f"{nNew} New File{plural(nNew)} ({100*nNew/nFiles:.2f}%)")
        tPrint("")
        for chkFile, newHash in newList:
            tPrint(f"{newHash:32s}  {chkFile}")
        tPrint("")

    nMiss = len(missList)
    if nMiss > 0:
        tPrint("")
        tPrint(f"{nMiss} Missing File{plural(nMiss)} ({100*nMiss/nFiles:.2f}%)")
        tPrint("")
        for oldHash, chkFile in missList:
            tPrint(f"{oldHash:32s}  {chkFile}")
        tPrint("")

    if args.tee:
        logStream.close()

    return 0


def main():
    """Main entry point and argument parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--list", action="store_true",
        help="Scan folder and list existing record, but don't write"
    )
    parser.add_argument(
        "-m", "--maintain", action="store_true",
        help="Hash new files and remove deleted files"
    )
    parser.add_argument(
        "-c", "--check", action="store_true",
        help="Check the hash of existing files"
    )
    parser.add_argument(
        "-u", "--update", action="store_true",
        help="Update the hash of existing files if they don't pass"
    )
    parser.add_argument(
        "-d", "--md5dir", type=str, default="Hash",
        help="The folder to read/write the hash fails from/to (default = Hash)"
    )
    parser.add_argument(
        "-t", "--tee", action="store_true",
        help="Write a log file of the output"
    )
    parser.add_argument("path", type=str, help="The folder to check")

    return hashDir(parser.parse_args())


if __name__ == "__main__":
    sys.exit(main())
