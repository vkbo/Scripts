#!/bin/bash
# Convert an ebook to .mobi
# The command is mainly because the ebook-converter tool is
# exceptionally silly with tab completion

ebook-convert "$1" .mobi
