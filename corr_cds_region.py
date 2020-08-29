#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @time    : 2020/8/11 17:43
# @Project : mytools
# @Version : python 3.8.5
# @product : PyCharm
# @Author  : Rensc
# @E-mail  : rensc0718@163.com


import argparse
import gc
import time
from argparse import RawTextHelpFormatter
from collections import OrderedDict


# get arguments and define the scripts usage
def parse_args():
    parser = argparse.ArgumentParser(
        description="This script is used to remove the upstream 15 and downstream 5 codons of CDS from gtf annotation.",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s 1.0"
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

            # if rec[2] == 'gene':
            #     gname = rec[8].split(';')[0].split('"')[1]
            #     gene[gname] = rec
            #     continue

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
        up_nt = up_num * 3
        down_nt = down_num * 3
        for tname, info in mrna_flag.items():

            if info[0] == 1 and info[1] == '+':
                # gname = mrna[tname][0][8].split(';')[0].split('"')[1]
                # out_gtf.writelines('\t'.join(gene[gname]) + '\n')
                for line in mrna[tname]:
                    rec = line
                    rec[3] = str(int(rec[3]) + up_nt)
                    rec[4] = str(int(rec[4]) - down_nt)
                    out_gtf.writelines('\t'.join(rec) + '\n')

            elif info[0] == 1 and info[1] == '-':
                # gname = mrna[tname][0][8].split(';')[0].split('"')[1]
                # out_gtf.writelines('\t'.join(gene[gname]) + '\n')

                for line in mrna[tname]:
                    rec = line
                    rec[3] = str(int(rec[3]) + down_nt)
                    rec[4] = str(int(rec[4]) - up_nt)
                    out_gtf.writelines('\t'.join(rec) + '\n')

            elif info[0] > 1 and info[1] == '+':
                # gname = mrna[tname][0][8].split(';')[0].split('"')[1]
                # out_gtf.writelines('\t'.join(gene[gname]) + '\n')
                flag = 0

                temp_mrna = {tname: []}

                for line in mrna[tname]:
                    rec = line
                    flag += 1

                    if flag == 1:
                        if int(rec[4]) - int(rec[3]) > up_nt:
                            rec[3] = str(int(rec[3]) + up_nt)
                            temp_mrna[tname].append(rec)
                            # out_gtf.writelines('\t'.join(rec) + '\n')
                            skip_cds_sart = 0
                        else:
                            skip_cds_sart = up_nt - (int(rec[4]) - int(rec[3]) + 1)

                    elif flag == info[0]:
                        if int(rec[4]) - int(rec[3]) > down_nt:
                            rec[3] = str(int(rec[3]) + skip_cds_sart)
                            rec[4] = str(int(rec[4]) - down_nt)
                            temp_mrna[tname].append(rec)
                        else:
                            skip_cds_stop = down_nt - (int(rec[4]) - int(rec[3]) + 1)
                            if len(temp_mrna[tname]) >= 1:
                                now_length = len(temp_mrna[tname])
                                # print temp_mrna[tname][now_length - 1]
                                temp_mrna[tname][now_length - 1][4] = str(
                                    int(temp_mrna[tname][now_length - 1][4]) - skip_cds_stop)
                            else:
                                temp_mrna = {tname: []}
                                # out_gtf.writelines('\t'.join(rec) + '\n')

                    elif flag > 1 and flag != info[0]:
                        if skip_cds_sart == 0:
                            temp_mrna[tname].append(rec)
                            # out_gtf.writelines('\t'.join(rec) + '\n')
                        else:
                            temp_loci = rec[3]
                            rec[3] = str(int(rec[3]) + skip_cds_sart)
                            if int(rec[4]) - int(rec[3]) > 0:
                                skip_cds_sart = 0
                                temp_mrna[tname].append(rec)
                                # out_gtf.writelines('\t'.join(rec) + '\n')
                            else:
                                skip_cds_sart = int(rec[3]) - int(rec[4])

                length = len(temp_mrna[tname])

                if length >= 1:
                    for rev_num in range(length - 1, -1, -1):
                        out_gtf.writelines('\t'.join(temp_mrna[tname][rev_num]) + '\n')
                else:
                    pass

            elif info[0] > 1 and info[1] == '-':
                # gname = mrna[tname][0][8].split(';')[0].split('"')[1]
                # out_gtf.writelines('\t'.join(gene[gname]) + '\n')

                # print mrna[tname]
                temp_mrna = {tname: []}
                length = len(mrna[tname])
                flag = 0
                rev_mrna = {tname: []}

                for rev_num in reversed(range(length)):
                    rev_mrna[tname].append(mrna[tname][rev_num])

                for line in rev_mrna[tname]:
                    rec = line
                    flag += 1

                    if flag == 1:
                        if int(rec[4]) - int(rec[3]) > up_nt:
                            rec[4] = str(int(rec[4]) - up_nt)
                            temp_mrna[tname].append(rec)
                            # out_gtf.writelines('\t'.join(rec) + '\n')
                            skip_cds_sart = 0

                        else:
                            skip_cds_sart = up_nt - (int(rec[4]) - int(rec[3]) + 1)

                    elif flag == info[0]:
                        if int(rec[4]) - int(rec[3]) > down_nt:
                            rec[4] = str(int(rec[4]) - skip_cds_sart)
                            rec[3] = str(int(rec[3]) + down_nt)
                            temp_mrna[tname].append(rec)
                        else:
                            skip_cds_stop = down_nt - (int(rec[4]) - int(rec[3]) + 1)
                            if len(temp_mrna[tname]) >= 1:
                                now_length = len(temp_mrna[tname])
                                # print temp_mrna[tname][now_length - 1]
                                temp_mrna[tname][now_length - 1][3] = str(
                                    int(temp_mrna[tname][now_length - 1][3]) + skip_cds_stop)
                            else:
                                temp_mrna = {tname: []}

                            # out_gtf.writelines('\t'.join(rec) + '\n')
                        flag = 0

                    elif flag > 1 and flag != info[0]:
                        if skip_cds_sart == 0:
                            temp_mrna[tname].append(rec)
                            # out_gtf.writelines('\t'.join(rec) + '\n')
                        else:
                            temp_loci = rec[3]

                            if int(rec[4]) - int(rec[3]) > skip_cds_sart:
                                rec[4] = str(int(rec[4]) - skip_cds_sart)
                                temp_mrna[tname].append(rec)
                                skip_cds_sart = 0
                                # out_gtf.writelines('\t'.join(rec) + '\n')
                            else:
                                skip_cds_sart = int(rec[3]) - int(rec[4])

                length = len(temp_mrna[tname])

                if length >= 1:
                    for rev_num in range(length - 1, -1, -1):
                        out_gtf.writelines('\t'.join(temp_mrna[tname][rev_num]) + '\n')
                else:
                    pass


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
    mrna, mrna_flag = read_gtf(args.i)
    correct_gtf(mrna, mrna_flag, args.o, args.u, args.d)
    clear()
    now_time()

if __name__ == '__main__':
    main()
