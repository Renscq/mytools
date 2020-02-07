#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, gc, re

__author__ = "rensc"
__mail__ = "rensc0718@163.com"


# get arguments and dim the scripts usage
def parse_args():
    parser = argparse.ArgumentParser(description="get unique fasta sequence",
                                     epilog = 'version 0.1')
    #group = parser.add_argument_group('Arguments')
    parser.add_argument('-f', '--fa', required=True, type=str, help="sRNA seq in fasta format")
    parser.add_argument('-l', '--log', required=False, type=str, help="the repeats seq file")
    parser.add_argument('-u', '--uniq', required=True, type=str, help="the unique sRNA")
    arguments = parser.parse_args()
    return arguments


# dim global parameters
srna_uniq_dict = {}
srna_repeat_dict = {}
srna_inputs = {}


def get_keys(my_dict, value):
    return [k for k, v in my_dict.items() if v == value]


def read_input(input_fa):

    with open(input_fa, 'r') as inputs:

        for line in inputs:
            srna_id = line.strip()
            # seq = inputs.next()
            seq = inputs.__next__()
            srna_inputs[srna_id] = seq

            if seq not in srna_uniq_dict.values():
                srna_uniq_dict[srna_id] = seq

            else:
                srna_repeat_dict[srna_id] = seq


def get_repeats(uniq_srna, repeats_srna):

    repeats_srna_uniq = []

    for srna, seq in uniq_srna.items():
        repeats_names = get_keys(repeats_srna, seq)

        if len(repeats_names) == 1:
            pass

        elif len(repeats_names) > 1:
            repeats_names.insert(0, srna)
            repeats_srna_uniq.append(repeats_names)
            repeats_srna_uniq.append(seq)

    return repeats_srna_uniq


def output_repeats(repeats_log, repeats_srna_out):

    with open(repeats_log, 'w') as out:

        for line in repeats_srna_out:
            if line[0].startswith('>'):
                out.writelines(' | '.join(line) + '\n')
            else:
                out.writelines(line)

def output_uniq(out_name,uniq_srna):

    with open(out_name,'w') as out:

        for srna, seq in uniq_srna.items():
            out.writelines(srna + '\n' + seq)


def main():

    args = parse_args()

    read_input(args.fa)

    if args.log and args.uniq:
        repeats_srna_out = get_repeats(srna_uniq_dict, srna_repeat_dict)
        output_repeats(args.log, repeats_srna_out)
        output_uniq(args.uniq, srna_uniq_dict)

    elif args.uniq:
        output_uniq(args.uniq, srna_uniq_dict)

    gc.collect()


# run here
if __name__ == '__main__':
    main()

