#!/usr/bin/env python
#rensc
import sys, getopt, gc

#func: How to use this script
def usage():
    print("")
    print("Usage is as follows:")
    print("")
    print("  eg:\tpython normFaReads.py -i degradome.fa -n 1e7 -o degradome-norm.fa ")
    print("  -i:\tSpecify the degradome.fa file")
    print("  -n:\tSpecify the normliaze grade (default 1e7)")
    print("  -o:\tSpecify the output file name (degradome-norm.fa)")
    print("")
    sys.exit()

# load the file of degradome.fa
fa_list = []
def load_fa(fa_input):
    print('Step1: Load the file %s.'%fa_input)
    global fa_list
    with open(fa_input,'r') as fa:
        for line in fa:
            rec = line.strip()
            if rec.startswith('>'):
               fa_list.append(rec.split(' ') + [fa.next().strip()])
        global l
        l = len(fa_list[0])
    print ('Step1: Done\ncontain %s samples.\n'%(l-3))

# norm files
norm_reads = []
def norm_fa(Num):
    print ('Step2: Normal the raw reads.')
    # sum the total reads
    barcodes = []
    for i in range(l-2):
        tmp = 0
        for line in fa_list:
            tmp += int(line[i+1])
        barcodes.append(tmp)
    s = 0
    # normal the sample reads
    for line1 in fa_list:
        mer = 0
        for k in range(l-3):
            norm = int((int(line1[k + 1]) * Num) / barcodes[k])
            fa_list[s].insert(l-1 + k,str(norm))
            mer += norm
        fa_list[s].insert(2*l-4, str(mer))
        s += 1
    print ('Step2: Done.\n')

# output the file
def output(out_fa,fa_list):
    print ('Step3: Results output.')
    with open(out_fa,'w') as out:
        for line in fa_list:
            ids = line[0:-1]
            seq = line[-1]
            out.write(' '.join(ids) + '\n' + seq + '\n')
    print ('Step3: Done.')


# main program is here
if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "hi:n:c:o:")
    fa_input, out_fa, Num= "", "", 1e7
    if opts:
        for op, value in opts:
            if op == "-i":
                fa_input = value
                out_fa = fa_input.split('.')[0] + '-norm.fa'
            elif op == "-n": Num = eval(value)
            elif op == "-o": out_fa = value
            elif op == "-h": usage();sys.exit()
    else:
        usage()
    print ('Your parameters are as follow:')
    print('Input file name: %s' % fa_input)
    print('Correction level: %s' % Num)
    print('Output file name: %s\n' % out_fa)
    load_fa(fa_input)
    norm_fa(Num)
    output(out_fa,fa_list)
    gc.collect()

