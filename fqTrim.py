#!/usr/bin/env python
# author : rensc

import sys, getopt, os, gc
from os.path import basename

# func: How to use this script
def usage():
    print("")
    print("Usage is as follows:")
    print("")
    print("  eg:\tpython fqfilter.py -i test.fq -l 30 -o output.fq")
    print("  -l:\tSpecified sequence length (default 20nt)")
    print("  -o:\toutput file name (default trimmed.fq)")
    print("")
    sys.exit()

# main program is here
if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "hi:l:o:")
    fq_file = ""
    length = "20"
    fq_trim = ""
    if opts:
        for op, value in opts:
            if op == "-i":
                fq_file = value
            elif op == "-l":
                length = eval(value)
            elif op == "-o":
                fq_trim = value
            elif op == "-h":
                usage()
                sys.exit()
    else:
        usage()
    # output trimmed sequences
    FQdata = open(fq_file, 'r')
    if fq_trim:
        FQtrim = open(fq_trim, 'w')
    else:
        base = os.path.splitext(fq_file)[0]
        FQtrim = open(base + "-" + str(length) + "bp.fq", 'w')

    counts = 0
    fq_ID = fq_seq = fq_name = fq_score = ""
    for line in FQdata:
        if counts % 4 == 0:
            fq_ID = line.strip("\n")
        elif counts % 4 == 1:
            fq_seq = line
        elif counts % 4 == 2:
            fq_name = line
        elif counts % 4 == 3:
            fq_score = line
            if len(fq_seq) >= length:
                FQtrim.write(fq_ID + " length=" + str(length) + "\n" +\
                             fq_seq[0:length] + "\n" + \
                             fq_name + \
                             fq_score[0:length] + "\n")
        counts = counts + 1

    FQtrim.close()
    FQdata.close()
    gc.collect()
