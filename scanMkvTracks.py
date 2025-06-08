"""Scan a folder hierarchy for MKV files with more than 10 tracks."""

import json
import subprocess
import sys

from pathlib import Path

scan = Path(sys.argv[1])

def countTracks(file: Path) -> int:
    """Get file info from input video file."""
    try:
        p = subprocess.Popen(f'mkvmerge -J "{file!s}"', stdout=subprocess.PIPE, shell=True)
        out, _ = p.communicate()
        data = json.loads(out.decode("utf-8"))
        return len(data.get("tracks", []))
    except Exception as exc:
        print(f"Error {item.relative_to(scan)}: {exc!s}")
        return -1

report = []
if scan.is_dir():
    for item in scan.glob("**/*.mkv"):
        if item.is_file() and (n := countTracks(item)):
            state = "***OVER" if n >= 10 else "   OK  "
            print(f"{state} [{n:>2}] {item.relative_to(scan)}", flush=True)
            if n >= 10:
                report.append(f"[{n:>2}] {item.relative_to(scan)}")

print("")
print("Result")
print("="*120)
print("\n".join(report))
print("")
