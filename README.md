# biotools
Hands-on results are for entertainment only.

## usage of randseq.py
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
## usage of fltReadsLength.py
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
## usage of getUniqFa.py
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
