#!/bin/bash
# Convert a webm video file to a gif animation
# Source: https://askubuntu.com/a/1350795

ffmpeg -y -i "$1" -vf palettegen _tmp_palette.png
ffmpeg -y -i "$1" -i _tmp_palette.png -filter_complex paletteuse -r 10  "${1%.webm}.gif"
rm _tmp_palette.png
