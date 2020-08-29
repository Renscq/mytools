#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @time    : 2020/4/1 21:06
# @Project : mytools
# @Script  : calcTpm.py
# @Version : python 3.8.5
# @product : PyCharm
# @Author  : Rensc
# @E-mail  : rensc0718@163.com


import argparse
import gc
import time
from argparse import RawTextHelpFormatter
from itertools import islice


# get arguments and define the scripts usage
def parse_args():
    parser = argparse.ArgumentParser(
        description="This script is used to calculate the TPM from featureCounts output.",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s 1.0"
    )
    parser.add_argument(
        "-i", metavar="input", required=True, type=str, help="input file"
    )
    parser.add_argument(
        "-o", metavar="output", required=True, type=str, help="output file"
    )
    # parser.add_argument(
    #     "-t", metavar="type", required=False, type=str, default='t',
    #     help="RPKM or TPM. (default: %(default)s)"
    # )

    args = parser.parse_args()
    return args


# calculate the tpm from feature Counts output files
def calc_tpm(in_file_count, out_file_tpm):
    gene_list = []
    total_reads = 0
    rpk_sum = 0
    title = ['Gene_id', 'Chr', 'Start', 'End', 'Strand', 'Length', 'reads_count', 'RPM', 'RPKM', 'RPK', 'TPM']

    with open(in_file_count, 'r') as in_file:
        with open(out_file_tpm, 'w') as out_file:
            out_file.writelines('\t'.join(title) + '\n')

            for line in islice(in_file, 2, None):
                rec = line.strip().split('\t')
                gene_list.append(rec)
                total_reads += int(rec[6])

            for line in gene_list:
                rpm = (float(line[6]) * 1000000) / total_reads
                rpkm = (float(line[6]) * 1000000 * 1000) / (total_reads * float(line[5]))
                rpk = (float(line[6]) * 1000) / float(line[5])
                rpk_sum += rpk
                line.append(str(round(rpm, 3)))
                line.append(str(round(rpkm, 3)))
                line.append(str(round(rpk, 3)))

            for line in gene_list:
                tpm = (float(line[-1]) * 1000000) / rpk_sum
                line.append(str(round(tpm, 3)))

            for line in gene_list:
                out_file.writelines('\t'.join(line) + '\n')


# gc collect
def clear():
    gc.collect()
    print("All done.")


# get time
def now_time():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


# main
def main():
    now_time()
    args = parse_args()
    calc_tpm(args.i, args.o)
    clear()
    now_time()


if __name__ == '__main__':
    main()