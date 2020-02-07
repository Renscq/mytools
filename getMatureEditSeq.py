#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, gc, re

__author__ = "rensc"
__mail__ = "rensc0718@163.com"

# get arguments and dim the scripts usage
def parse_args():
    parser = argparse.ArgumentParser(description="find all edited sites in seed region",
                                     epilog = 'version 0.2')
    #group = parser.add_argument_group('Arguments')
    parser.add_argument('-i', '--input', required=True, type=str, help="sig mirme individual txt")
    parser.add_argument('-o', '--out', required=True, type=str, help="the name of output file")
    arguments = parser.parse_args()
    return arguments


def in_put(mirme):
    with open(mirme, 'r') as mirmeTxt:
        srna_txt = []
        for line in mirmeTxt:

            if not line.strip():
                pass

            elif '..' not in line and '[' in line:
                tmp = line.strip().split('\t')
                names = tmp[-7:]
                names.insert(0, str(tmp[0]))

            elif '..' not in line and '[' not in line:
                names.append(line.strip())
                srna_txt.append(names)
                names = ''

    return srna_txt


def get_edited(srna):
    mir_5p_pos, mir_3p_pos = [], []
    merged = ['edited\t5p\t3p\traw\t5p\t3p\tmature?\tseq']

    for line2 in srna:

        raw_mature = line2[:-1]
        premirna = line2[-1]
        str1 = re.sub(r'[a-z]', '-', premirna).strip('-').split('-')
        mir_5p, mir_3p = str1[0], str1[-1]
        flag = 'not'
        # does 5p or 3p not exist
        if len(mir_5p) > 5:
            mir_5p_pos = [premirna.index(mir_5p) + 1, premirna.index(mir_5p) + len(mir_5p)]
        if len(mir_3p) > 5:
            mir_3p_pos = [premirna.index(mir_3p) + 1, premirna.index(mir_3p) + len(mir_3p)]

        # does the edited site in 5p region
        if mir_5p_pos[0] <= int(raw_mature[1]) <= mir_5p_pos[1]:

            # does the edited site in seed region
            if mir_5p_pos[0] <= int(raw_mature[1]) <= mir_5p_pos[0] + 7:
                flag = '5p-seed'
            else:
                flag = '5p'

            premirna_list = list(premirna)
            premirna_list[int(raw_mature[1]) - 1] = raw_mature[3]
            premirna_list = ''.join(premirna_list)
            edited_seq = premirna_list[mir_5p_pos[0] - 1: mir_5p_pos[1]]
            merged.append('\t'.join(
                [raw_mature[0], edited_seq, mir_3p, raw_mature[0].split('_')[0], mir_5p, mir_3p, flag, premirna]))

        elif mir_3p_pos[0] <= int(raw_mature[1]) <= mir_3p_pos[1]:
            # does the edited site in seed region
            if mir_3p_pos[0] <= int(raw_mature[1]) <= mir_3p_pos[0] + 7:
                flag = '3p-seed'
            else:
                flag = '3p'

            premirna_list = list(premirna)
            premirna_list[int(raw_mature[1]) - 1] = raw_mature[3]
            premirna_list = ''.join(premirna_list)
            edited_seq = premirna_list[mir_3p_pos[0] - 1: mir_3p_pos[1]]
            merged.append('\t'.join(
                [raw_mature[0], mir_5p, edited_seq, raw_mature[0].split('_')[0], mir_5p, mir_3p, flag, premirna]))
        else:
            merged.append('\t'.join(
                [raw_mature[0], mir_5p, mir_3p, raw_mature[0].split('_')[0], mir_5p, mir_3p, flag, premirna]))
    return merged


def out_put(merged, outname):
    with open(outname, 'w') as out_txt:
        for line3 in merged:
            out_txt.writelines(line3.strip() + '\n')


# main programme
def main():
    args = parse_args()

    srna_out = in_put(args.input)

    merged_out = get_edited(srna_out)

    out_put(merged_out, args.out)

    gc.collect()


if __name__ == '__main__':
    main()
