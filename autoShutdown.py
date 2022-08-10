#!/usr/bin/env python
"""
Monitor the network connection, and shut down the host if the network
has been down for a certain amount of time. This is a simple way to shut
down in case of power loss when the machine itself is on a simple UPS.
"""

import os
import sys
import time
import logging
import subprocess

TIME_LIMIT = 75


logging.basicConfig(
    format="[{asctime:}] {levelname:8} {message:}", style="{", level=logging.INFO
)
logger = logging.getLogger()


def sysCall(callArgs, cwd=None):
    """Wrapper function for system calls.
    """
    sysP = subprocess.Popen(
        callArgs, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True, cwd=cwd
    )
    stdOut, stdErr = sysP.communicate()
    return stdOut.decode("utf-8"), stdErr.decode("utf-8"), sysP.returncode


def main():
    """Check when the interface was last seen, and if it was too long
    ago, run the shutdown command.
    """
    if len(sys.argv) != 3:
        logger.error("Script requires two arguments: interface workdir")
        return 1

    interface = sys.argv[1]
    workdir = sys.argv[2]

    statusFile = os.path.join(workdir, f"{interface}.txt")
    stdOut, _, exCode = sysCall([f"ip link show {interface}"])

    nowTime = time.time()
    lastSeen = nowTime
    if os.path.isfile(statusFile):
        with open(statusFile, mode="r") as inFile:
            try:
                lastSeen = float(inFile.read())
            except Exception:
                return 1

    if exCode != 0:
        logger.error("Call to ip command returned error code %d", exCode)
        return 1

    since = nowTime - lastSeen
    if "NO-CARRIER" in stdOut:
        logger.warning("Interface %s is DOWN. Last seen %.1f seconds ago.", interface, since)
        if nowTime - lastSeen > TIME_LIMIT:
            logger.info("Running SHUTDOWN.")
            _, stdErr, exCode = sysCall(["/sbin/shutdown -h now"])
            if exCode != 0:
                logger.error(stdErr.strip())
            return 0
    else:
        with open(statusFile, mode="w") as outFile:
            outFile.write(f"{nowTime:.3f}")
        logger.info("Interface %s is UP. Last seen %.1f seconds ago.", interface, since)

    return 0


if __name__ == "__main__":
    sys.exit(main())
