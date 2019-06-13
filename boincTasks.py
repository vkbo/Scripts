#!/usr/bin/env python3

import subprocess

def formatTime(tS):
    tM, tS = divmod(tS, 60)
    tH, tM = divmod(tM, 60)
    return "%02d:%02d:%02d" % (tH, tM, tS)

# Linux Terminal Colours
# No idea if these work on windows
# If not, replace them with empty strings
RED       = "\033[0;31m"
GREEN     = "\033[0;32m"
YELLOW    = "\033[0;33m"
BLUE      = "\033[0;34m"
PURPLE    = "\033[0;35m"
CYAN      = "\033[0;36m"
GREY      = "\033[0;37m"
NORMAL    = "\033[0;38m"
BOLD      = "\033[0;1m"
UNDERLINE = "\033[0;4m"
END       = "\033[0;0m"

# Get BOINC Status
theProc = subprocess.Popen(["boinccmd", "--get_tasks"], stdout=subprocess.PIPE)
(stdOut, stdErr) = theProc.communicate()

# Parse Data
bTasks = {}
tNum   = "None"
for stdLine in str(stdOut).split("\\n"):
    stdLine = stdLine.strip()
    if len(stdLine) < 12: continue
    if stdLine[-11:] == "-----------":
        tSplit = stdLine.split(")")
        if not len(tSplit) == 2: continue
        tNum = tSplit[0]
        bTasks[tNum] = {
            "Name"      : "None",
            "State"     : "None",
            "Elapsed"   : 0.0,
            "Remaining" : 0.0,
            "Progress"  : 0.0,
        }
    else:
        tSplit = stdLine.split(":")
        if not len(tSplit) == 2: continue
        if not tNum in bTasks.keys(): continue
        if tSplit[0] == "name":
            bTasks[tNum]["Name"] = tSplit[1].strip()
        elif tSplit[0] == "active_task_state":
            bTasks[tNum]["State"] = tSplit[1].strip()
        elif tSplit[0] == "current CPU time":
            bTasks[tNum]["Elapsed"] = float(tSplit[1].strip())
        elif tSplit[0] == "estimated CPU time remaining":
            bTasks[tNum]["Remaining"] = float(tSplit[1].strip())
        elif tSplit[0] == "fraction done":
            bTasks[tNum]["Progress"] = float(tSplit[1].strip())*100

bSortTasks = {}
for tNum in bTasks.keys():
    bSortTasks[bTasks[tNum]["Name"]] = bTasks[tNum]

#~ print(bSortTasks)

print(BOLD+" BOINC Status"+END)

listOrder = ["EXECUTING","SUSPENDED","UNINITIALIZED"]
prevState = None
for tState in listOrder:
    for tName in sorted(bSortTasks.keys()):
        if not bSortTasks[tName]["State"] == tState: continue
        if not prevState == bSortTasks[tName]["State"]:
            print()
            print((BOLD+" {:90.90}  Elapsed   Remain    Progress"+END).format(bSortTasks[tName]["State"]))
            prevState = bSortTasks[tName]["State"]
        if bSortTasks[tName]["Progress"] < 40:
            colProg = RED
        elif bSortTasks[tName]["Progress"] < 80:
            colProg = YELLOW
        else:
            colProg = GREEN
        print((" {:90.90}  "+colProg+"{:8}  {:8}  {:7.3f}%"+END).format(
            bSortTasks[tName]["Name"],
            formatTime(bSortTasks[tName]["Elapsed"]),
            formatTime(bSortTasks[tName]["Remaining"]),
            bSortTasks[tName]["Progress"],
        ))

