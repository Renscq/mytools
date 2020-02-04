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
