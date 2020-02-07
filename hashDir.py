#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, subprocess, signal

if len(sys.argv) != 3:
    print("ERROR hashDir requires a command and a path as input arguments.")
    print("Valid commands are: maintain, check or check+update")
    sys.exit(1)

doMaintain = False
doUpdate = False
doCheck = False
if sys.argv[1] == "maintain":
    doMaintain = True
elif sys.argv[1] == "check":
    doCheck = True
elif sys.argv[1] == "check+update":
    doUpdate = True
    doCheck = True
else:
    print("ERROR Unknown command '%s'" % sys.argv[1])
    sys.exit(1)

if not os.path.isdir(sys.argv[2]):
    print("ERROR Unknown directory '%s'" % sys.argv[2])
    sys.exit(1)

def signalHandler(theSignal, theFrame):
    print("\nExiting ...")
    sys.exit(0)

# Capture ctrl+c
signal.signal(signal.SIGINT, signalHandler)

baseDir = os.path.basename(sys.argv[2].rstrip("/"))
rootDir = os.path.dirname(sys.argv[2].rstrip("/"))
scanDir = os.path.join(rootDir, baseDir)
hashFile = os.path.join(rootDir, baseDir+".md5")
backFile = os.path.join(rootDir, baseDir+".bak")

hashData = {}
if os.path.isfile(hashFile):
    with open(hashFile, mode="r") as inFile:
        for hashLine in inFile:
            if len(hashLine) > 34:
                theHash = hashLine[:32]
                theFile = hashLine[34:].rstrip("\n")
                hashData[theFile] = [theHash, False]

os.chdir(rootDir)

fileList = []
for tRoot, tDirs, tFiles in os.walk(baseDir):
    if len(tFiles) > 0:
        for tFile in tFiles:
            fileList.append(os.path.join(tRoot, tFile))

nFiles = len(fileList)
nCount = 0
failList = []
newList = []

print("")
print("Folder: %s" % scanDir)
print("Files: %d" % nFiles)
if doCheck:
    print("Run Mode: Check")
if doMaintain:
    print("Run Mode: Maintain")
print("")

if doMaintain or doUpdate:
    if os.path.isfile(backFile):
        os.unlink(backFile)
    if os.path.isfile(hashFile):
        os.rename(hashFile, backFile)
    outFile = open(hashFile, mode="w+")

for chkFile in sorted(fileList):
    theStatus = "   None"
    isKnown   = chkFile in hashData
    doHash    = doCheck or (doMaintain and not isKnown)
    doCompare = doCheck and isKnown

    if doCheck or (doMaintain and not isKnown):
        sysP = subprocess.Popen(["md5sum \"%s\"" % chkFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdOut, stdErr = sysP.communicate()
        newHash = stdOut.decode("utf-8")[:32].rstrip("\n")
    else:
        newHash = "X"*32

    if isKnown:
        prevHash = hashData[chkFile][0]
        hashData[chkFile][1] = True
    else:
        prevHash = "Z"*32

    if doMaintain:
        if isKnown:
            theStatus = "   Skipped"
            saveHash  = prevHash
        else:
            theStatus = "   NewFile"
            saveHash  = newHash
            newList.append((chkFile, newHash))

    if doCheck:
        if isKnown:
            if newHash == prevHash:
                theStatus = "   Passed"
                saveHash  = prevHash
            else:
                theStatus = "***Failed"
                if doUpdate:
                    saveHash = newHash
                else:
                    saveHash = prevHash
                failList.append((chkFile, prevHash, newHash))
        else:
            theStatus = "   Skipped"
            saveHash  = prevHash

    nCount += 1
    print("[%6.2f%%] %-10s  %s  %s" % (100*nCount/nFiles, theStatus, saveHash, chkFile))
    if doMaintain or doUpdate:
        outFile.write("%s  %s\n" % (saveHash, chkFile))
        outFile.flush()

print("")

if doMaintain or doUpdate:
    outFile.close()

missList = []
for hFile in hashData:
    if not hashData[hFile][1]:
        missList.append(hFile)

nFail = len(failList)
if nFail > 0:
    print("")
    print("%d Failed Checks (%6.2f%%)" % (nFail, 100*nFail/nFiles))
    print("")
    for chkFile, prevHash, newHash in failList:
        print("%-32s != %-32s  %s" % (newHash, prevHash, chkFile))
    print("")

nNew = len(newList)
if nNew > 0:
    print("")
    print("%d New Files (%6.2f%%)" % (nNew, 100*nNew/nFiles))
    print("")
    for chkFile, newHash in newList:
        print("%-32s  %s" % (newHash, chkFile))
    print("")

nMiss = len(missList)
if nMiss > 0:
    print("")
    print("%d Missing Files (%6.2f%%)" % (nMiss, 100*nMiss/nFiles))
    print("")
    for chkFile in missList:
        print("%s" % chkFile)
    print("")
