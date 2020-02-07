#!/usr/bin/env python
#rensc
import sys, getopt, gc

#func: How to use this script
def usage():
    print("")
    print("Usage is as follows:")
    print("")
    print("  eg:\tpython dos2unix.py -i input.txt -o output.txt ")
    print("  -i:\tSpecify the input file name")
    print("  -o:\tSpecify the output file name")
    print("")
    sys.exit()

def dos2unix(input_file,output_file):
    content = ''
    outsize = 0
    with open(input_file, 'rb') as infile:
        content = infile.read()
    with open(output_file, 'wb') as output:
        for line in content.splitlines():
            outsize += len(line) + 1
            line = line.strip()
            output.writelines(line.__add__('\n'))
    print("Already replaced  %s lines from file { %s }." % (len(content) - outsize, input_file) )


# main program is here
if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
    input_file = ""
    output_file = ""
    if opts:
        for op, value in opts:
            if op == "-i":
                input_file = value
            elif op == "-o":
                output_file = value
            elif op == "-h":
                usage()
                sys.exit()
    else:
        usage()

    dos2unix(input_file, output_file)
    gc.collect()
