#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, gc
import pandas as pd
__author__ = 'Rensc'

# get arguments and dim the scripts usage
def parse_args():
    parser = argparse.ArgumentParser(description="format the MIRME file",
                                     epilog='version 0.1')
    parser.add_argument('-i', '--input', required=True, type=str,
                        help="results of MIRME")
    parser.add_argument('-l', '--list', required=True, type=str,
                        help="list of samples")
    parser.add_argument('-o', '--out', required=True, type=str,
                        help="the name of output file (csv format)")
    infile = parser.add_mutually_exclusive_group(required=True)
    infile.add_argument('-p', '--per',action='store_true',
                        help='pick out percentage (mutually exclusive with -d)')
    infile.add_argument('-d', '--dlt',action='store_true',
                        help='delete redundant column')
    arguments = parser.parse_args()
    return arguments


# dim global arguments
args = parse_args()
base_title = ["Edit_site", "miRNA", "ME_Position_in_PremiR", "WT_Nucl","ME_Nucl",
          "miR_Chr", "miR_Strand", "PremiR_Start", "PremiR_End", "ME_Genome_Position",
          "5'_Mature_Start", "5'_Mature_End", "3'_Mature_Start", "3'_Mature_End"]

each_title = ["ME_Reads_Num", "Norm_ME_Num(TPTM)", "Total_Reads_Num", "Norm_Total_Num(TPTM)",
            "ME_Percent", "P_value", "Corrected_P_value"]
samp_list = []


# delete repeats column
def delete_repeats():
    with open(args.list,'r') as samples:
        for line in samples:
            samp_list.append(line.strip())

    length = len(samp_list)
    data_index = []
    edit_index = [0, 1, 2, 3, 4, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    df = pd.read_csv(args.input, header=None, sep = "\t")

    for i in range(length):
        data_index.extend(list(range(5 + 22 * i, 12 + 22 * i)) + [21 + 22 * i])

    data_df = df.iloc[:, data_index]
    edit_df = df.iloc[:, edit_index]
    combined = pd.concat([edit_df, data_df], axis=1)

    for ids in range(length):
        base_title.extend(each_title)
        base_title.append(samp_list[ids])

    combined.columns = base_title
    combined.to_csv(args.out, index=False, header=True)


# get percentage
def pick_percentage():
    with open(args.list,'r') as samples:

        for line in samples:
            samp_list.append(line.strip())

    length = len(samp_list)
    per_index = []
    base_index = [0, 1, 2, 3, 4, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    df = pd.read_csv(args.input, header=None, sep = "\t")

    for i in range(length):
        per_index.append(9 + 22 * i)

    per_df = df.iloc[:, per_index]
    base_df = df.iloc[:, base_index]
    combined = pd.concat([base_df, per_df], axis=1)
    base_title.extend(samp_list)
    combined.columns = base_title
    combined.to_csv(args.out, index=False, header=True)


# format the reads to fasta
def main():
    if args.dlt:
        delete_repeats()
    elif args.per:
        pick_percentage()
    gc.collect()


# main programme is here
if __name__ == '__main__':
    main()
