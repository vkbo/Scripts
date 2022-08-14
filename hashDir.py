#!/usr/bin/env python3
"""Simple tool to hash and verify files in a tree.
"""

import os
import sys
import signal
import argparse
import datetime
import subprocess


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

    print(f"Scan Path: {scanDir}")
    print(f"Hash File: {hashFile}")
    print("")

    hashData = {}
    print("Scanning for previous hash file ... ", end="")
    if os.path.isfile(hashFile):
        with open(hashFile, mode="r") as inFile:
            for hashLine in inFile:
                if len(hashLine) > 34:
                    theHash = hashLine[:32]
                    theFile = hashLine[34:].rstrip("\n")
                    hashData[theFile] = [theHash, False]
            print(f"found {len(hashData)} records")
    else:
        print("not found")

    fileList = []
    print("Scanning for files ... ", end="")
    for tRoot, _, tFiles in os.walk(scanDir):
        if len(tFiles) > 0:
            for tFile in tFiles:
                fileList.append(os.path.join(tRoot, tFile))
    print(f"found {len(fileList)} files")
    print("")

    nFiles = len(fileList)
    nCount = 0
    failList = []
    newList = []

    doList = args.update or args.maintain or args.maintain or args.list
    doScan = (args.update or args.maintain or args.maintain) and not args.list
    doWrite = (args.update or args.maintain) and not args.list
    doCompare = args.check or args.update

    print("Run Mode:")
    print(" - Check file existence (list): %s" % ("Yes" if doList else "No"))
    print(" - Add new files (maintain): %s" % ("Yes" if doScan else "No"))
    print(" - Remove deleted files (maintain): %s" % ("Yes" if doScan else "No"))
    print(" - Check existing records (check): %s" % ("Yes" if doCompare else "No"))
    print(" - Update existing records (update): %s" % ("Yes" if doWrite else "No"))
    print("")

    if doWrite:
        if os.path.isfile(hashFile):
            modTime = os.path.getmtime(hashFile)
            timeStamp = datetime.datetime.fromtimestamp(modTime).strftime("%Y%m%d-%H%M%S")
            backFile = os.path.join(backDir, baseDir+"-"+timeStamp+".md5")
            os.rename(hashFile, backFile)
            print(f"Copied: {hashFile} -> {backFile}")
            print("")
        outFile = open(hashFile, mode="w+")

    for chkFile in sorted(fileList):
        theStatus = "   None"
        isGone = not os.path.isfile(chkFile)
        isKnown = chkFile in hashData and not isGone
        doHash = doCompare or (args.maintain and not isKnown)

        if doHash and not isGone:
            sysP = subprocess.Popen(
                ["md5sum \"%s\"" % chkFile],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            stdOut, _ = sysP.communicate()
            newHash = stdOut.decode("utf-8")[:32].rstrip("\n")

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
                        theStatus = "***Fail+Up"
                        saveHash = newHash
                    else:
                        theStatus = "***Failed"
                        saveHash = oldHash
                    failList.append((chkFile, oldHash, newHash))

        else:
            if isGone:
                theStatus = "   Missing"
                saveHash = " "*32
            else:
                theStatus = "   NewFile"
                newList.append((chkFile, newHash))
                saveHash = newHash

        nCount += 1
        progress = 100*nCount/nFiles
        fileSize = getFileSize(chkFile)
        print(f"[{progress:6.2f}%] {theStatus:<10s}  {saveHash}  {fileSize:8s}  {chkFile}")
        if doWrite:
            outFile.write(f"{saveHash}  {chkFile}\n")
            outFile.flush()

    print("")

    if doWrite:
        outFile.close()

    # Generate Reports
    # ================

    missList = []
    for hFile in hashData:
        if not hashData[hFile][1]:
            missList.append(hFile)

    nFail = len(failList)
    if nFail > 0:
        print("")
        print(f"{nFail} Failed Checks ({100*nFail/nFiles:6.2f}%)")
        print("")
        for chkFile, prevHash, newHash in failList:
            print(f"{newHash:32s} != {prevHash:32s}  {chkFile}")
        print("")

    nNew = len(newList)
    if nNew > 0:
        print("")
        print(f"{nNew} New Files ({100*nNew/nFiles:6.2f}%)")
        print("")
        for chkFile, newHash in newList:
            print(f"{newHash:32s}  {chkFile}")
        print("")

    nMiss = len(missList)
    if nMiss > 0:
        print("")
        print(f"{nMiss} Missing Files ({100*nMiss/nFiles:6.2f}%)")
        print("")
        for chkFile in missList:
            print(chkFile)
        print("")

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
        help="The folder to read/write the hash failes from/to (default = Hash)"
    )
    parser.add_argument("path", type=str, help="The folder to check")

    return hashDir(parser.parse_args())


if __name__ == "__main__":
    sys.exit(main())
