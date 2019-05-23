#!usr/bin/python
import sys,os
from Bio import SeqIO
from shutil import make_archive

infile=os.path.dirname(sys.argv[1])
outfile= infile + "/out"
dir=sys.argv[1]
fasta_strings=SeqIO.parse(dir,"fasta")
fasta_type=sys.argv[2]

with open(outfile+'/faslength.txt','w') as f1:
    if fasta_type == 'nr':
        f1.write("Id" + '\t' + "length" + '\n')
        for fasta_string in fasta_strings:
            f1.write(str(fasta_string.id) + '\t' + str(len(fasta_string.seq)) + '\n')
    elif fasta_type =='nt':
        for fasta_string in fasta_strings:
            f1.write( "Id" + '\t' + "length" + '\t' + "A" + '\t' + "T" + '\t' + "G" + '\t' + "C" + '\t' + "GC content" + '\n')
            GC_content = (fasta_string.seq.count('GC') / len(fasta_string.seq)) * 100
            f1.write(str(fasta_string.id) + '\t' + str(len(fasta_string.seq)) + '\t' + str(
                fasta_string.seq.count('A')) + '\t' + str(fasta_string.seq.count('T')) + '\t' + str(
                fasta_string.seq.count('G')) + '\t' + str(fasta_string.seq.count('C')) + '\t' + str(
                round(GC_content, 2)) + "%" + '\n')


make_archive(infile+ "/out", "zip",infile,"out")
