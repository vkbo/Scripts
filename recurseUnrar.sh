#!/bin/bash

find $1 -name '*.rar' -execdir unrar e {} \;
