#!/usr/bin/env python3
"""
Run scour on an SVG file, or folder of SVG files.
"""

import os
import sys
import scour.scour

if len(sys.argv) != 2:
    print("Usage: optimise_svg.py path")
    sys.exit(1)

path = sys.argv[1]

files = []
if os.path.isdir(path):
    for item in os.listdir(path):
        svg = os.path.join(path, item)
        if os.path.isfile(svg) and svg.endswith(".svg"):
            files.append(svg)
elif os.path.isfile(path) and path.endswith(".svg"):
    files = [path]
else:
    print("Usage: optimise_svg.py path")
    sys.exit(1)


def scour_svg(infile, outfile):
    options = scour.scour.parse_args()
    options.infilename = infile
    options.outfilename = outfile
    (inobj, outobj) = scour.scour.getInOut(options)
    scour.scour.start(options, inobj, outobj)


for svg in files:
    optsvg = svg+"~"
    try:
        scour_svg(svg, optsvg)
        os.replace(optsvg, svg)
    except Exception as exc:
        print("Failed")
        print(exc)

sys.exit(0)
