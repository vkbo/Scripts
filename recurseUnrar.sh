#!/bin/bash
# Recursively extract rar files in a folder

find $1 -name '*.rar' -execdir unrar e {} \;
