#!/usr/bin/env python
# -*- coding: utf-8 -*-
#rensc
import sys, getopt, gc, pysam
import numpy as np

#func: How to use this script
def usage():
    print(
"""\
Usage:

python aveInsertSize.py -b/s <bam/sam file> -c <p/l> [-m] [-M]

Options:
    -b/-s:  <bam/sam>    input file in BAM / SAM format
       -c:    <p/l>      cut outliers by percentage or length
        p:   [-m/-M]     min/max percentage exculding, range is [0:1]
        l:   [-m/-M]     min/max length exculding, range is [0:inf]
       -h:   --help      print this page.

PS: default range of percent is [0.1:0.8], 
    default range of length is [0:1500]
    
eg: python aveInsertSize.py -b test.bam -c p -m 0.1 -M 0.9
eg: python aveInsertSize.py -s test.sam -c l -m 0 -M 1500
""")
    sys.exit()

def testLenM(m,M):
    if m and M:
        pass
    elif m and not M:
        M = 1500
    elif M and not m:
        m = 0
    elif not m and not M:
        m = 0
        M = 1500
    return m,M

def testPerM(m,M):
    if m and M:
        pass
    elif m and not M:
        M = 0.8
    elif M and not m:
        m = 0.1
    elif not m and not M:
        m = 0.1
        M = 0.8
    return m,M

def bamInsertPer(bam,m,M):
    samfile = pysam.AlignmentFile(bam, "rb")
    inSize = []
    (m, M) = testPerM(m, M)
    for read in samfile:
        if int(read.isize) > 0:
            inSize.append(int(read.isize))
        else: pass
    inSize = sorted(inSize)
    length = len(inSize)
    used = inSize[int(length * m):int(length * M)]
    length = len(used)
    ave = np.mean(used)
    mid = np.median(used)
    var = np.var(used)
    std = np.std(used, ddof=1)
    print("sample=" + bam + '\t' + "line=" + str(length) + '\t'
          + "average=" + str(int(ave)) + '\t' + "median=" + str(int(mid)) + '\t'
          + "variance=" + str(int(var)) + '\t' + "stdev=" + str(int(std)))
    # print("sample=%s\tlength=%d\taverage=%d\tmid=%d\tvar=%d\tstdev=%d"%(bam,length,int(ave),int(mid),int(var),int(std)))

def bamInsertLen(bam, m, M):
    samfile = pysam.AlignmentFile(bam, "rb")
    inSize = []
    (m, M) = testLenM(m, M)
    for read in samfile:
        if int(read.isize) > m  and int(read.isize) < M:
            inSize.append(int(read.isize))
        else: pass
    length = len(inSize)
    ave = np.mean(inSize)
    mid = np.median(inSize)
    var = np.var(inSize)
    std = np.std(inSize, ddof=1)
    print("sample=" + bam + '\t' + "line=" + str(length) + '\t'
          + "average=" + str(int(ave)) + '\t' + "median=" + str(int(mid)) + '\t'
          + "variance=" + str(int(var)) + '\t' + "stdev=" + str(int(std)))
    # print("sample=%s\tlength=%d\taverage=%d\tmid=%d\tvar=%d\tstdev=%d" % (bam, length, int(ave), int(mid), int(var), int(std)))

def samInsertPer(sam, m, M):
    with open(sam,'r') as samfile:
        inSize = []
        (m, M) = testPerM(m, M)
        for read in samfile:
            rec = read.strip().split('\t')[8]
            if int(rec) > 0:
                inSize.append(int(rec))
            else: pass
        inSize = sorted(inSize)
        length = len(inSize)
        used = inSize[int(length * m):int(length * M)]
        length = len(used)
        ave = np.mean(used)
        mid = np.median(used)
        var = np.var(used)
        std = np.std(used, ddof=1)
        print("sample=" + sam + '\t' + "line=" + str(length) + '\t'
              + "average=" + str(int(ave)) + '\t' + "median=" + str(int(mid)) + '\t'
              + "variance=" + str(int(var)) + '\t' + "stdev=" + str(int(std)))

def samInsertLen(sam, m, M):
    with open(sam,'r') as samfile:
        inSize = []
        (m, M) = testLenM(m, M)
        for read in samfile:
            rec = read.strip().split('\t')[8]
            if int(rec) > m  and int(rec) < M:
                inSize.append(int(rec))
            else: pass
        length = len(inSize)
        ave = np.mean(inSize)
        mid = np.median(inSize)
        var = np.var(inSize)
        std = np.std(inSize, ddof=1)
        print("sample=" + sam + '\t' + "line=" + str(length) + '\t'
              + "average=" + str(int(ave)) + '\t' + "median=" + str(int(mid)) + '\t'
              + "variance=" + str(int(var)) + '\t' + "stdev=" + str(int(std)))

def main():
    sam, bam, small, large, cate = '', '', '', '', 'p'
    opts, args = getopt.getopt(sys.argv[1:], "hb:s:c:m:M:t:")
    if opts:
        for op, value in opts:
            if op == "-b":
                bam = value
            elif op == "-s":
                sam = value
            elif op == "-c":
                cate = value
            elif op == "-m":
                small = eval(value)
            elif op == "-M":
                large = eval(value)
            elif op == "-h" or op == "--help":
                usage()
                sys.exit()
    else:
        usage()
        sys.exit()

    if cate == 'p':
        if bam:
            bamInsertPer(bam, small, large)
        else:
            samInsertPer(sam, small, large)
    elif cate == 'l':
        if bam:
            bamInsertLen(bam, small, large)
        else:
            samInsertLen(sam, small, large)
    gc.collect()

# main program is here
if __name__ == '__main__':
    main()
