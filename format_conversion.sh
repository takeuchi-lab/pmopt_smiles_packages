#!/bin/bash

if [ $# -lt 4 ]; then
    echo "Usage: $0 INPUT_FILE OBJECTIVE SMILES_COLUMN OUTPUT_FILE"
    exit
fi

# your  csv filename
filename=$1

# Value you want to predict
objective=$2

# Name of the column in which smiles is stored
smiles=$3

# Output filename
Output_name=$4

tmp_graph_file=${filename%.*}.withoutHyd.graph

rm -f $tmp_graph_file
python sources/to_graph_atomic_simple.py ${filename} 0 ${smiles} ${objective}
if [ -f ${tmp_graph_file} ]; then
    python sources/graph_to_csv.py ${tmp_graph_file} ${Output_name}
    rm ${tmp_graph_file}
else
    echo \"to_graph_atomic_simple.py\" failed. Proper outputs are not made.
fi
