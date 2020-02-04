#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, gc

__version__ = "0.2"
__author__ = "rensc"

# get arguments and dim the scripts usage
def parse_args():
    parser = argparse.ArgumentParser(description="filter the specific length of reads")
    
    infile = parser.add_mutually_exclusive_group(required=True)
    infile.add_argument('-f','--fa',action='store',help = 'sequence in fasta format')
    infile.add_argument('-q', '--fq',action='store',help = 'sequence in fastq format')
    infile.add_argument('-t', '--txt',action='store',help = 'sequence in txt format')
    
    group = parser.add_argument_group('Arguments')
    group.add_argument('-m', '--min', required=False, type=int, default=18, help = "the minimum length of sRNA to keep (default: %(default)snt)")
    group.add_argument('-M','--max',required=False,type=int,default=28, help = "the maximum length of sRNA to keep (default: %(default)snt)")
    group.add_argument('-o', '--out', required=True, type=str, help="the name of output file (same as the input format)")
    
    arguments = parser.parse_args()
    return arguments

def filterTxt(srna,min,max,outfile):
    
    with open(srna,'r') as reads:
        with open(outfile,'w') as out:
            
            for line in reads:
                rec = line.strip()
                if min <= len(rec) <= max:
                    out.writelines(''.join([rec, '\n']))
                else:
                    pass

def filterFa(srna,min,max,outfile):
    
    with open(srna,'r') as reads:
        with open(outfile,'w') as out:
            
            ids,rec = '',''
            for line in reads:
                if line.startswith('>'):
                    if min <= len(rec) <= max:
                        out.writelines(''.join([ids, '\n', rec, '\n']))
                        rec = ''
                    else:
                        rec = ''
                    ids = line.strip()
                else:
                    rec = rec + line.strip()

def filterFq(srna,min,max,outfile):
    
    with open(srna,'r') as reads:
        with open(outfile,'w') as out:
            
            for line1 in reads:
                #line2 = reads.__next__() # grammar in python3
                line2 = reads.next()
                #line3 = reads.__next__()
                line3 = reads.next()
                #line4 = reads.__next__()
                line4 = reads.next()
                rec = line2.strip()
                if min <= len(rec) <= max:
                    out.writelines(''.join([line1, line2, line3, line4]))
                else:
                    pass

def main():
    
    args = parse_args()
    
    if args.fa:
        filterFa(args.fa, args.min, args.max, args.out)
    elif args.fq:
        filterFq(args.fq, args.min, args.max, args.out)
    elif args.txt:
        filterTxt(args.txt, args.min, args.max, args.out)
        
    gc.collect()

if __name__ == '__main__':
    main()
