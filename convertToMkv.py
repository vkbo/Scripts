#!/usr/bin/env python3
"""Convert a folder of video files into mkv files."""

import subprocess
import sys

from pathlib import Path

if len(args := sys.argv) > 1:
    scan = Path(sys.argv[1])
else:
    scan = Path.cwd()

if scan.is_dir():
    for item in scan.iterdir():
        if item.is_file() and item.suffix in (".mkv", ".mp4", ".avi", ".mpg"):
            print("Processing:", item)
            if item.suffix == ".mkv":
                out = item.with_stem(f"{item.stem}_copy")
            else:
                out = item.with_suffix(".mkv")
            try:
                subprocess.call(["mkvmerge", "-o", str(out), str(item)])
            except Exception as exc:
                print(f"Error {item.relative_to(scan)}: {exc!s}")
