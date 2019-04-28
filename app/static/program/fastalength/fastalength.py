import os,sys
from shutil import make_archive
from Bio import SeqIO

infile=os.path.dirname(sys.argv[1])
outfile= infile + "/out"
length=int(sys.argv[2])


with open(outfile+'/outresult.fas','w+') as f2:
    for seq_record in SeqIO.parse(sys.argv[1], "fasta"):
        fasta = seq_record
        start = 0
        end = start + length
        f2.write(str(fasta.description)+'\n')
        if length !=0:
            while True:
                if end < len(fasta.seq):
                    f2.write(str(fasta.seq[start:end]) + '\n')
                    start = end
                    end += length
                elif end >= len(fasta.seq):
                    f2.write(str(fasta.seq[start:]) + '\n')
                    break
        else:
            f2.write(str(fasta.seq[start:]) + '\n')

make_archive(infile+ "/out", "zip",infile,"out")