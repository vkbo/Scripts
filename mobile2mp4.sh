#!/bin/bash
# Convert a video file to mp4, make sure it's an even number of pixels, and compress
# Source: https://stackoverflow.com/questions/18123376/webm-to-mp4-conversion-using-ffmpeg

ffmpeg -i "$1" -qscale 0 -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -r 24 "${1%.*}_scaled.mp4"
