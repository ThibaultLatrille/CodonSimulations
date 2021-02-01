# GLOBAL IMPORTS
import argparse
import pandas as pd
from ete3 import Tree

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--output', required=True, type=str, dest="output")
    parser.add_argument('-i', '--input', required=True, type=str, dest="input")
    args = parser.parse_args()

    ali_file = open(args.input + ".ali", 'r')
    ali_file.readline()

    outfile = open(args.output, "w")
    outfile.write("\n".join([">{0}\n{1}".format(*line.strip().split(" ")) for line in ali_file.readlines()]))
    outfile.close()
