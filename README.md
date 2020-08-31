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

## correct_cds_region.py

Use this scripts to remove the first 15 codons and last 5 codons of each isoforms CDS region. The output gtf file can be used for ribosome footprints quantification.

```shell
# get the gtf file
$ gffread hsa.gff3 -T -o hsa.gtf

# remove the specific length of CDS
$ correct_cds_region -i hsa.gtf -u 10 -d 5 -o hsa.CDS.correct.gtf

# ribosome footprints (RPFs) quantification
featureCounts -T 6 -p -t CDS -g gene_id -a ~/reference/hsa.CDS.correct.gtf -o test1.cds.txt ../STAR/test1Aligned.sortedByCoord.out.bam
```

## calcTPM.py

Convert the gene counts to RPKM / TPM

```shell
# input file of this script is the output file of featureCounts
# test1.cds.txt 
$ calcTPM -i test1.cds.txt -o test1.cds.tpm

$ head test1.cds.tpm
Gene_id	Chr	Start	End	Strand	Length	reads_count	RPM	RPKM	RPK	TPM
gene1	I	1529	1945	-	417	94	8.212	19.694	225.42	17.533
gene2	I	3431	3821	+	936	249	21.754	23.242	266.026	20.691
gene3	I	9649	12188	+	3273	1042	91.035	27.814	318.362	24.762
gene4	I	15975	16015	+	414	0	0.0	0.0	0.0	0.0
gene5	I	17917	18362	+	1362	122	10.659	7.826	89.574	6.967
gene6	I	36144	36503	+	2583	265	23.152	8.963	102.594	7.98
gene7	I	40965	42587	-	1623	0	0.0	0.0	0.0	0.0
gene8	I	43724	44506	-	783	0	0.0	0.0	0.0	0.0
gene9	I	45584	45913	-	2055	672	58.71	28.569	327.007	25.435

```

