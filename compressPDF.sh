#!/bin/bash

convert -density 200x200 -quality 60 -compress jpeg $1.pdf $1-Compressed.pdf
