#!usr/bin/python
import sys,os
from Bio import SeqIO
from shutil import make_archive

infile=os.path.dirname(sys.argv[1])
outfile= infile + "/out"
dir=sys.argv[1]
min_length=float(sys.argv[2])
max_length=float(sys.argv[3])
fasta_strings=SeqIO.parse(dir,"fasta")
with open(outfile+'/faslengthfilter.txt','w') as f:
    f.write("Id" + '\t' + "length" + '\n')
    for fasta_string in fasta_strings:
        if len(fasta_string.seq) >= min_length and len(fasta_string.seq) <= max_length:
            f.write(str(fasta_string.id) + '\t' + str(len(fasta_string.seq)) + '\n' + str(fasta_string.seq) + '\n')

make_archive(infile+ "/out", "zip",infile,"out")
