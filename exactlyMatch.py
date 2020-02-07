#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, gc

__version__ = '0.1'
__author__ = 'rensc'

# get the arguments and script usage
def parse_args():
    parser = argparse.ArgumentParser(description='Calculate the frequency of exactly matched small RNA')
    group = parser.add_argument_group('Arguments')
    group.add_argument('-t', '--tissue', required=True, type=str,
                       help='the non-redundant small RNA file')
    group.add_argument('-s', '--srna', required=True, type=str,
                       help='the small rna file in FASTA format')
    group.add_argument('-b', '--barcode', required=True, type=str,
                       help='the barcode of non-redundant small RNA file')
    group.add_argument('-o', '--out', required=False, type=str,default= 'norm_sRNA.fa',
                       help='the name of output file (default: %(default)s)')
    arguments = parser.parse_args()
    return arguments

# dim all global args
cand_list, tissue_dict, rows, samples = [], {}, [],[]

# read candidate seq file
def read_sRNA(cand_fa):
    with open(cand_fa, 'r') as cand:
        for line1 in cand:
            line1 = line1.strip().replace('> ', '')
            line1 = line1.strip().replace('>', '')
            line2 = cand.next()
            rec = line2.strip().lower().replace('u', 't')
            cand_list.append(line1.split(' ')[0] + '\t' + rec)

# read tissue
def read_tissue(tissue):
    with open(tissue, 'r') as frequency:
        for line3 in frequency:
            line4 = frequency.next()
            tissue_dict[line4.strip()] = line3.strip().split(' ')[1:]

# read barcodes file
def read_barcode(barcodes):
    with open(barcodes, 'r') as bar:
        for line5 in bar:
            samples.append(line5.strip().split('\t')[0])
            rows.append(int(line5.strip().split('\t')[1]))

def outPut(out):
    with open(out, 'w') as output:
        l = len(rows)
        sample_norm = [tmp + '_norm(RPTM)' for tmp in samples]
        samples.insert(0,'sRNA\tseq')#, samples.insert(1, 'seq')
        samples.extend(sample_norm)
        freq_norm,sum = [],0
        output.writelines('\t'.join(samples) + '\n')
        for line6 in cand_list:
            seq = line6.split('\t')[1]
            if tissue_dict.get(seq):
                freq = tissue_dict[seq]
                for n in range(l-1):
                    norm = int(round((int(freq[n]) * 10000000 )/ rows[n]))
                    freq_norm.append(str(norm))
                    sum += norm
                freq_norm.append(str(sum))
                freq.insert(0,line6)
                freq.extend(freq_norm)
                output.writelines('\t'.join(freq) + '\n')
                sum = 0
                freq_norm = []
            else:
                output.writelines(''.join([line6 + '\t' + '0\t' * 2 * l + '\n']))

def main(arguments):
    read_sRNA(arguments.srna)
    read_barcode(arguments.barcode)
    read_tissue(arguments.tissue)
    outPut(arguments.out)
    gc.collect()

# main program is here
if __name__ == '__main__':
    args = parse_args()
    main(args)
