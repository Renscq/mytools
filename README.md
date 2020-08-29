# biotools
Hands-on results are for entertainment only.

## randseq.py
Generate some sequences randomly
```shell
$ python randseq.py -n 2
> seq1 
ATACCGTATTGCTGTAGAACTGGCAACTTACCTACTGCCGGCCTCAAAGT
> seq2 
TCAACAAACGTGAGGTATACGTGATGCCGTCACTGCGGGAAGACCAACCG
```

```shell
$ python randseq.py -t R -l 24
> seq1 
AUCCGGGGCCAGGCCACAAUCGUG
> seq2 
AACCCGUUAUGUCUGGUCAGCGGA
> seq3 
CCAUCCGGAUAGCUUUUUUCGGCA
> seq4 
UCCCUCAUAGGAUCGUCAAGGUCC
> seq5 
CGAAAGUCUCCCUAAGACGCCACG
```
## fltReadsLength.py
Filter reads of specific length in sequencing files.
```shell
$ fltReadsLength -f sRNA.fa -m 20 -M 24 -o sRNA_20_24.fa

$ head sRNA_20_24.fa -n 6
>t4500001
gagaactttgaggactgaagt
>t4500017
gagaactttgaggccgaagc
>t4500021
gagaactttgagggccgaagt
```
## getUniqFa.py
Unique sRNA sequences file in fasta format.
```shell
$ getUniqFa -f sRNA.fa -l repeats.fa -u sRNA_uniq.fa

$ head repeats.fa -n 4
>hsa-mir-199a-1 | >hsa-mir-199b | >hsa-mir-199a-2
acaguagucugcacauugguuu
>hsa-mir-9-1 | >hsa-mir-9-2 | >hsa-mir-9-3
auaaagcucgauaaccgaaagu

$ head sRNA_uniq.fa -n 4
>hsa-mir-199a-1
acaguagucugcacauugguuu
>hsa-mir-9-1
auaaagcucgauaaccgaaagu
```

## dos2unix.py

Convert the file format from dos to unix ( `^M` to `\n` )

```shell
$ cat -v input.txt
here is the test file^M

$ dos2unix -i input.txt -o output.txt

$ cat -v output.txt
here is the test file

```

## averageInsertSize.py

Use this scripts to calculate the average insert size of RNA sequencing profilings

```shell
# Two ways to remove abnormal reads for average Insert Size calculation
# specify the minimum and maximum percentage of reads to keep
$ averageInsertSize -b test.bam -c p -m 0.1 -M 0.9
# specify the minimum and maximum reads length to keep
$ averageInsertSize -b test.bam -c l -m 0 -M 1500
```

## getSampReadsCount.py

Use this scripts to calculate the reads count of sRNA-seq. (input txt or fasta format)

```shell
# perform the cutadapt to get the clean reads from sRNA-seq
$ cutadapt -j 0 --match-read-wildcards -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC -e 0.1 -O 6 -m 20 --discard-untrimmed -r test1.drop" -o test1.clean.fq test1.fq
$ cutadapt -j 0 --match-read-wildcards -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC -e 0.1 -O 6 -m 20 --discard-untrimmed -r test2.drop" -o test2.clean.fq test2.fq
$ fq2fa -q test1.fq -a test1.fa
$ fq2fa -q test2.fq -a test2.fa

# make the sample list for every samples
$ cat sample.list
../data/test1.fa
../data/test2.fa

# get the reads count for each samples
$ getSampReadsCount -i sample.list -b 2-barcodes.txt -o 2-samp-reads-count.fa

# columns: samples name + reads
$ cat 2-barcodes.txt
test1	5982378
test2	2245151
total	8227529

# columns: ids + each sample counts + total counts
$ head 2-samp-reads-count.fa
>t1 10 15 25
GATCGATGAGGATTAATAATGTGT
>t2 8 10 18
TAATTCTTCCTACACTGAATCCT
>t3 6 0 6
GGCGAGATTAATGGCTAAAAGAGCTT
>t4 1 10 11
AATATATAAGTGACTTAGACCAAT
>t5 14 1 15
GCTAAGCTTCTATCGACCGCCT

```

