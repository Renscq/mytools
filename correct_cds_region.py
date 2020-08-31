#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @time    : 2020/8/31 15:00
# @Project : py-scripts
# @Script  : corr_gtf.py
# @Version : python 3.8.5
# @product : PyCharm
# @Author  : Rensc
# @E-mail  : rensc0718@163.com


import argparse
import gc
import time
import sys
from argparse import RawTextHelpFormatter
from collections import OrderedDict


# get arguments and define the scripts usage
def parse_args():
    parser = argparse.ArgumentParser(
        description="This script is used to remove the upstream 15 and downstream 5 codons of CDS from gtf annotation.",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s 2.0"
    )
    parser.add_argument(
        "-i", metavar="input", required=True, type=str, help="input gtf file"
    )
    parser.add_argument(
        "-u", metavar="up", required=True, type=int, default=15,
        help="specify the number of upstream codons to removed (default %(default)s)"
    )
    parser.add_argument(
        "-d", metavar="down", required=True, type=int, default=5,
        help="specify the number of downstream codons to removed (default %(default)s)"
    )
    parser.add_argument(
        "-o", metavar="output", required=True, type=str, help="output file"
    )
    args = parser.parse_args()
    print(args)
    sys.stdout.flush()
    return args


# read the gtf file and remove the up/down stream codons
def read_gtf(in_gtf_file):
    with open(in_gtf_file, 'r') as in_gtf:
        # gene = {}
        mrna = {}
        mrna_flag = OrderedDict()

        cds_num = 0
        for line in in_gtf:
            if line.startswith('#') or line.strip().split('\t')[2] == "exon":
                continue

            rec = line.strip().split('\t')
            cds = rec[2]
            tname = rec[8].split(';')[0].split('"')[1]
            strand = rec[6]

            if mrna.get(tname):
                mrna[tname].append(rec)

                if cds == "CDS":
                    cds_num += 1
                    mrna_flag[tname] = [cds_num, strand]

            else:
                mrna[tname] = [rec]
                cds_num = 1
                mrna_flag[tname] = [cds_num, strand]

    return mrna, mrna_flag


# remove the first $up_num codon and $down_num codon, default 15 / 5
def correct_gtf(mrna, mrna_flag, out_gtf_file, up_num, down_num):
    with open(out_gtf_file, 'w') as out_gtf:
        del_gene = []
        up_nt = up_num * 3
        down_nt = down_num * 3

        for tname, info in mrna_flag.items():
            # condition 1
            if info[0] == 1 and info[1] == '+':
                for line in mrna[tname]:
                    rec = line
                    if int(rec[4]) - int(rec[3]) + 1 > up_nt + down_nt:
                        rec[3] = str(int(rec[3]) + up_nt)
                        rec[4] = str(int(rec[4]) - down_nt)
                        out_gtf.writelines('\t'.join(rec) + '\n')
                    else:
                        del_gene.append(tname)
            # condition 2
            elif info[0] == 1 and info[1] == '-':
                for line in mrna[tname]:
                    rec = line
                    if int(rec[4]) - int(rec[3]) + 1 > up_nt + down_nt:
                        rec[3] = str(int(rec[3]) + down_nt)
                        rec[4] = str(int(rec[4]) - up_nt)
                        out_gtf.writelines('\t'.join(rec) + '\n')
                    else:
                        del_gene.append(tname)
            # condition 3
            elif info[0] > 1 and info[1] == '+':
                flag = 0
                temp_mrna = {tname: []}

                for line in mrna[tname]:
                    rec = line
                    flag += 1

                    if flag >= 1 and flag != info[0]:
                        if up_nt == 0:
                            temp_mrna[tname].append(rec)
                        else:
                            if int(rec[4]) - int(rec[3]) + 1 > up_nt:
                                rec[3] = str(int(rec[3]) + up_nt)
                                up_nt = 0
                                temp_mrna[tname].append(rec)
                            else:
                                up_nt = up_nt - (int(rec[4]) - int(rec[3]) + 1)

                    elif flag == info[0]:
                        if int(rec[4]) - int(rec[3]) + 1 > up_nt + down_nt:
                            rec[3] = str(int(rec[3]) + up_nt)
                            rec[4] = str(int(rec[4]) - down_nt)
                            up_nt, down_nt = up_num * 3, down_num * 3
                            temp_mrna[tname].append(rec)
                        else:
                            down_nt = down_nt - (int(rec[4]) - int(rec[3]) + 1)

                            if len(temp_mrna[tname]) >= 1:
                                for cds_num in range(len(temp_mrna[tname]), -1, -1):
                                    previous_cds = temp_mrna[tname][cds_num - 1]
                                    if int(previous_cds[4]) - int(previous_cds[3]) + 1 > up_nt + down_nt:
                                        previous_cds[4] = str(int(previous_cds[4]) - down_nt)
                                        break
                                    else:
                                        down_nt = down_nt - (int(previous_cds[4]) - int(previous_cds[3]) + 1)
                                        del temp_mrna[tname][cds_num - 1]
                            else:
                                temp_mrna = {tname: []}
                                del_gene.append(tname)
                        flag = 0

                length = len(temp_mrna[tname])
                if length >= 1:
                    for cds in range(length):
                        out_gtf.writelines('\t'.join(temp_mrna[tname][cds]) + '\n')
                else:
                    pass
            # condition 4
            elif info[0] > 1 and info[1] == '-':
                temp_mrna = {tname: []}
                length = len(mrna[tname])
                flag = 0
                rev_mrna = {tname: []}

                for rev_num in reversed(range(length)):
                    rev_mrna[tname].append(mrna[tname][rev_num])

                for line in rev_mrna[tname]:
                    rec = line
                    flag += 1

                    if flag >= 1 and flag != info[0]:
                        if up_nt == 0:
                            temp_mrna[tname].append(rec)
                        else:
                            if int(rec[4]) - int(rec[3]) + 1 > up_nt:
                                rec[4] = str(int(rec[4]) - up_nt)
                                temp_mrna[tname].append(rec)
                                up_nt = 0
                            else:
                                up_nt = up_nt - (int(rec[4]) - int(rec[3]) + 1)

                    elif flag == info[0]:
                        if int(rec[4]) - int(rec[3]) + 1 > up_nt + down_nt:
                            rec[4] = str(int(rec[4]) - up_nt)
                            rec[3] = str(int(rec[3]) + down_nt)
                            up_nt, down_nt = up_num * 3, down_num * 3
                            temp_mrna[tname].append(rec)
                        else:
                            down_nt = down_nt - (int(rec[4]) - int(rec[3]) + 1)
                            if len(temp_mrna[tname]) >= 1:
                                for cds_num in range(len(temp_mrna[tname]), -1, -1):
                                    previous_cds = temp_mrna[tname][cds_num - 1]
                                    if (int(previous_cds[4]) - int(previous_cds[3])) + 1 > up_nt + down_nt:
                                        previous_cds[3] = str(int(previous_cds[3]) + down_nt)
                                        break
                                    else:
                                        down_nt = down_nt - (int(previous_cds[4]) - int(previous_cds[3]) + 1)
                                        del temp_mrna[tname][cds_num - 1]
                            else:
                                temp_mrna = {tname: []}
                                del_gene.append(tname)
                        flag = 0

                length = len(temp_mrna[tname])
                if length >= 1:
                    for cds in range(length - 1, -1, -1):
                        out_gtf.writelines('\t'.join(temp_mrna[tname][cds]) + '\n')
                else:
                    pass

        if len(del_gene) >= 1:
            for gene_name in del_gene:
                print('deleted:' + gene_name)
        else:
            print('None gene been deleted')


# gc collect
def clear():
    gc.collect()
    print("All done.")
    sys.stdout.flush()


# get time
def now_time():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    sys.stdout.flush()


# main
def main():
    now_time()
    args = parse_args()
    mrna, mrna_flag = read_gtf(args.i)
    correct_gtf(mrna, mrna_flag, args.o, args.u, args.d)
    clear()
    now_time()


if __name__ == '__main__':
    main()

