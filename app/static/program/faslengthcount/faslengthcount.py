#!usr/bin/python
import sys,os
from Bio import SeqIO
from shutil import make_archive

infile=os.path.dirname(sys.argv[1])
outfile= infile + "/out"
dir=sys.argv[1]
fasta_strings=SeqIO.parse(dir,"fasta")

with open(outfile+'/faslength.txt','w') as f1:
    f1.write("Id" + '\t' + "length" + '\n')
    for fasta_string in fasta_strings:
        f1.write(str(fasta_string.id) + '\t' + str(len(fasta_string.seq)) + '\n')

make_archive(infile+ "/out", "zip",infile,"out")
