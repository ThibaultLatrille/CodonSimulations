# GLOBAL IMPORTS
import argparse
import pandas as pd
from ete3 import Tree

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--output', required=True, type=str, dest="output")
    parser.add_argument('-i', '--input', required=True, type=str, dest="input")
    args = parser.parse_args()
    t = Tree(args.input + ".nhx", format=1)

    node_dico = {"NodeName": []}
    for n in t.iter_descendants():
        if n.is_root(): continue
        node_dico["NodeName"].append(n.name)
        for attr in n.features:
            if not (("dN" in attr) or ("population_size" in attr)): continue
            if attr not in node_dico: node_dico[attr] = []
            node_dico[attr].append(getattr(n, attr))
    pd.DataFrame(node_dico).to_csv(args.output, sep="\t", index=False)
