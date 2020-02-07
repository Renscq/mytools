#!/usr/bin/env python
# -*- coding: utf-8 -*-
#rensc
import sys, getopt, gc
from collections import OrderedDict

#func: How to use this script
def usage():
    print("")
    print("Usage is as follows:")
    print("")
    print("  eg:\tpython salmonMerge.py -i info.txt -c R -o gene_abund_merge.txt &")
    print("  -i:\tthe list of quant.sf file")
    print("  -c:\t(R/T) the column of quant.sf file(Reads/TPM)")
    print("  -o:\tthe name of output file")
    print("  -h:\tprint this page.")
    print("")
    sys.exit()

def readFile(info,merge,title,s,output):
    file_list = open(info,'r')
    for file in file_list:
        title = title + '\t' + file.strip().split('/')[-1]
        with open(file.strip() + '/quant.sf','r') as sample:
            for line in sample:
                record = line.strip().split()
                ID = record[0]
                if line.startswith('Name'):
                    pass
                elif merge.get(ID):
                    merge[ID] = merge[ID] + '\t' + record[s].strip()
                else:
                    merge[ID] = record[s].strip()
    with open(output,'w') as outf:
        outf.writelines(title + '\n')
        keys = sorted(list(merge.keys()))
        for res in keys:
            outf.writelines(''.join([res,'\t',merge[res],'\n']))

# main program is here
if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "hi:c:o:")
    info = ""
    cate = "T"
    output = "gene_abund_merge.txt"
    if opts:
        for op, value in opts:
            if op == "-i":
                info = value
            elif op == "-c":
                cate = value
            elif op == "-o":
                output = value
            elif op == "-h":
                usage()
                sys.exit()
    else:
        usage()
        sys.exit()
    merge = {}
    title = 'gene'
    if cate == "R":
        s = -1
        readFile(info, merge, title, s, output)
    elif cate == "T":
        s = -2
        readFile(info, merge, title, s, output)
    else:
        usage()
        sys.exit()
    gc.collect()
