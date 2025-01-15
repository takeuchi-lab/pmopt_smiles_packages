from pysmiles import read_smiles
import pandas as pd
import sys
import csv
import os
import re
from collections import defaultdict

EXTRACTED_NODE_INFO = 'element'
EXTRACTED_EDGE_INFO = 'order'

def dict_order(ls, init=0):
    dc = {}
    for i, e in enumerate(ls):
        dc[e] = i+init
    return dc

NUMBER2ELEMENT = [None, "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]
ELEMENT2NUMBER = dict_order(NUMBER2ELEMENT)

def iloc_num_name(df, row_num, col_name):
    return df.loc[df.index[row_num], col_name]

def main(in_fname, hydrogen, colname_smiles, *app_info_columns):
    #smstr = "C[C@@H]1CC\C(=C(/C)C)C(=O)C1"
    hydrogen = int(hydrogen)

    if len(app_info_columns) == 0:
        raise RuntimeError(f'At least one "app_info_columns" name required')
    
    if in_fname[-5:] == '.xlsx':
        data = pd.read_excel(in_fname, header=0, index_col=None)
    else:
        data = pd.read_csv(in_fname, header=0, index_col=None)
    
    columns_not_found = []
    if colname_smiles not in data.columns:
        columns_not_found.append(colname_smiles)
    for colname in app_info_columns:
        if colname not in data.columns:
            columns_not_found.append(colname)
    
    if len(columns_not_found) > 0:
        raise RuntimeError(f'Specified columns ({", ".join(columns_not_found)}) not included in the file "{in_fname}"')

    #node_info2id = {}
    node_frequency = defaultdict(int)
    edge_frequency = defaultdict(int)
    
    fname_base = (os.path.splitext(in_fname))[0]
    if hydrogen:
        fname_base += '.withHyd'
    else:
        fname_base += '.withoutHyd'
    out_graph = f'{fname_base}.graph'

    outf_g = open(out_graph, "w")
    # csvwrite = csv.writer(outf_s, lineterminator="\n")
    # csvwrite.writerow(["CompoundID", "SMILES", "#Nodes", "#Edges"])

    graphs = [None] * len(data)

    # Write graphs
    for i in range(len(data)):
        smstr = iloc_num_name(data, i, colname_smiles)

        smstr_split = smstr.split(".")
        if len(smstr_split) > 1:
            smstr = max(smstr_split, key=lambda s: len(s))
        
        graphs[i] = read_smiles(smstr, explicit_hydrogen=hydrogen)

        # Print the graph with the format of gSpan
        # Example: https://github.com/betterenvi/gSpan/blob/master/graphdata/graph.data

        outf_g.write('t #')
        for ap in app_info_columns:
            outf_g.write(' ')
            outf_g.write(re.sub(r"\s|#", "_", str(ap)))
            outf_g.write(' ')
            outf_g.write(re.sub(r"\s|#", "_", str(iloc_num_name(data, i, ap))))
        outf_g.write(f" SMILES {smstr}\n")

        nodes = graphs[i].nodes(data=True)
        for node in nodes:
            node_label = ELEMENT2NUMBER[node[1][EXTRACTED_NODE_INFO]]
            if "hcount" in node[1]:
                node_label += node[1]["hcount"] * 1000
            outf_g.write("v %d %d\n" % (node[0], node_label))
            node_frequency[node_label] += 1
        
        edges = graphs[i].edges(data=True)
        for edge in edges:
            edge_info = edge[2][EXTRACTED_EDGE_INFO]
            outf_g.write("e %d %d %d\n" % (edge[0], edge[1], edge_info*2))
            edge_frequency[edge_info] += 1

        outf_g.write("\n")

    outf_g.close()

if __name__ == '__main__':
    if len(sys.argv) < 5:
        sys.stderr.write("Usage: to_graph [SMILES_TABLE_FILE] [INCLUDE_HYDROGEN] [SMILES_COLUMN] [TITLE_COLUMN_1] ([TITLE_COLUMN_2] ...)\n")
        sys.exit(-1)
    
    main(*sys.argv[1:])
