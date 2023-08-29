#!/bin/bash
# Convert an ebook to .epub
# The command is mainly because the ebook-converter tool is
# exceptionally silly with tab completion

ebook-convert "$1" .epub
