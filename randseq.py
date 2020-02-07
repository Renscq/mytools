#!/usr/bin/env python

__author__ = "rensc"
__mail__ = "rensc0718@163.com"

import random, sys, getopt

#func: How to use this script
def usage():
    print("Usage is as follows:")
    print("  eg:\tpython seq.py -t D -l 100 -n 20 > outseq.fa")
    print("  -t:\t(D/R) type of DNA/RNA sequence")
    print("  -n:\tnumber of sequence")
    print("  -l:\tspecify the length of sequence")
    sys.exit()

# func: out DNA/RNA sequence random
def outseq(types, number, length):
    for i in range(0, number):
        if types == 'D':
            DNA = "ATGC"
            seq = ""
            for s in range(0, length):
                index = random.randint(0, 3)
                seq = seq + DNA[index]
            print '> seq' + str(i + 1), '\n', seq
        elif types == 'R':
            RNA = "AUGC"
            seq = ""
            for s in range(0, length):
                index = random.randint(0, 3)
                seq = seq + RNA[index]
            print '> seq' + str(i + 1), '\n', seq
        else:
            usage()
            sys.exit()

#def outformat(seq,file_format):

# main program is here
if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "h:t:n:l:")
    types="D"
    number="5"
    length = "50"
    if opts:
        for op, value in opts:
            if op == "-t":
                types = value
            elif op == "-n":
                number = value
            elif op == "-l":
                length = value
            elif op == "-h":
                usage()
                sys.exit()
    else:
        usage()
# output DNA/RNA sequences
    outseq(types, eval(number), eval(length))
