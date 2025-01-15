import csv
import argparse

# Periodic Table and Bonding Table
NUMBER2ELEMENT = [None, "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]
NUMBER2BOND = {2: '-', 3: ':', 4: '=', 6: '#'}

def parse_graph_format(graph):
    vertices = []
    edges = []

    lines = graph.split('\n')
    for line in lines:
        splited_line = line.split()
        if splited_line[0] == 'v':
            vertices_line = splited_line[0] + ' ' + splited_line[1] + ' ' + NUMBER2ELEMENT[(int(splited_line[2])%1000)]
            vertices.append(vertices_line)
        elif splited_line[0] == 'e':
            edges_line = splited_line[0] + ' ' + splited_line[1] + ' ' + splited_line[2] + ' ' + NUMBER2BOND[int(splited_line[3])]
            edges.append(edges_line)

    return vertices, edges

def graph_to_csv(graph):
    output = []
    sections = graph.split('\n\n')
 
    for section in sections:
        if section.strip():
            lines = section.split('\n')
            header = lines[0].split()
            logp = header[3]
            
            # Get vertex and edge information
            vertices, edges = parse_graph_format(section)
            
            # Combine vertex and edge information with a single space
            graph_str = ' '.join(vertices + edges)
            
            # Add to output results list
            output.append((logp, graph_str))
    
    return output

def write_csv(data, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(["objective", "graph"])
        for logp, graph in data:
            writer.writerow([logp, graph])

# Read .graph data from external file
def read_graph_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Main function to convert .graph to .csv
def convert_graph_to_csv(input_file, output_file):
    graph_data = read_graph_file(input_file)
    csv_data = graph_to_csv(graph_data)
    write_csv(csv_data, output_file)

def main():
    parser = argparse.ArgumentParser(description="Convert .graph file to .csv format containing multiple molecular structures.")
    parser.add_argument("input_file", help="Path to the input .graph file")
    parser.add_argument("output_file", help="Path to the output .csv file")

    args = parser.parse_args()
    
    convert_graph_to_csv(args.input_file, args.output_file)

if __name__ == '__main__':
    main()

