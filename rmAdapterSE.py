#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, gc, re

__author__ = "rensc"
__mail__ = "rensc0718@163.com"

# get arguments and dim the scripts usage
def parse_args():
    parser = argparse.ArgumentParser(description="Remove the 3'-adapter from sRNA profile",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Common adapters are as follows:
    1. TGGAATTCTCGGGTGCCAAGGAACTCCAG
    2. AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC
    3. ATCTCGTATGCCGTCTTCTGCTTGT
    4. ACGGGCTAATATTTATCGGTGGAGCATC''')
    
    group = parser.add_argument_group('Arguments')
    group.add_argument('-t', '--txt', action='store', type=str, help="sRNA reads in txt format")
    group.add_argument('-a', '--adapter', required=True, type=str, help = "the 3'-adapter of your sRNA profile")
    group.add_argument('-l', '--length', required=False, type=int, default=18, help = "the minimum valid length of sRNA (default: %(default)snt)")
    group.add_argument('-n','--number',required=False,type=int,default=6, help = "the minimum aligned length of adapter (default: %(default)snt)")
    group.add_argument('-o', '--out', required=True, type=str, help="the name of output file")
    arguments = parser.parse_args()
    return arguments

# Define global variables
times, srna_reads, adap_list = 0, [], []


def readTxt(sRNA):

    with open(sRNA,'r') as srna:
        for line in srna:
        
            srna_reads.append(line.strip())


def readAdapter(adapter, num):

    adapter = adapter.upper().replace('U', 'T')

    for i in range(len(adapter) - (num - 1)):
    
        adap_list.append(adapter[i:i + num])


def rmAdapter(outfile, adap_list, srna_reads,length):

    with open(outfile, 'w') as out:
        for seq in srna_reads:

            for index in adap_list:
            
                tmp = re.compile(index)

                if re.search(tmp, seq):
                    reads = re.sub(index, ' ', seq).split(' ')[0]
                    flag = len(reads)

                    if flag >= length:
                        out.writelines(''.join([str(len(reads)), '\tval\t', reads]) + '\n')
                        break
                        
                    else:
                        out.writelines(''.join([str(len(reads)), '\tinv\t', reads]) + '\n')
                        break

            else:
                out.writelines(''.join([str(len(seq)), '\tinv\t', seq]) + '\n')


# main programme
def main():
    args = parse_args()

    readTxt(args.txt)

    readAdapter(args.adapter,args.number)

    rmAdapter(args.out, adap_list, srna_reads, args.length)

    gc.collect()


if __name__ == '__main__':
    main()
