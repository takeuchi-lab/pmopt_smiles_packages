#!/bin/bash

if [ $# -lt 3 ]; then
    echo "Usage: $0 INPUT_FILE NUM_SPLITS OUTPUT_FILE"
    exit
fi

# your csv filename
filename=$1

# Number of divisions to cross-validate
n_splits=$2

# Output file path
output=$3

python sources/make_cvdata.py ${filename} ${n_splits} ${output}