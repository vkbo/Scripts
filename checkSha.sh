#¬/bin/bash
# Check a shasum directly from command line
# Usage: checkSha.sh <path> <shasum>

echo "$2  $1" | shasum -c
