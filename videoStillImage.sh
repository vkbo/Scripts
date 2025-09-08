#!/bin/bash

ffmpeg -ss $2 -i "$1" -frames:v 1 "$3"
