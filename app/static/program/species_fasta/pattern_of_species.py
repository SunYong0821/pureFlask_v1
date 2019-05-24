#!/usr/bin/python

import sys,os
from Bio import SeqIO
from shutil import make_archive

infile=os.path.dirname(sys.argv[1])
outfile= infile + "/out"
dir=sys.argv[1]
pattern_species=sys.argv[2]
head=sys.argv[3]

db = {
       "Arabidopsis_thaliana":"./app/patterspieces/Arabidopsis_thaliana_TAIR10.1_genomic.fna",
        "Caenorhabditis_elegans":"./app/patterspieces/Caenorhabditis_elegans.WBcel235.dna.toplevel.fa",
       "Danio_rerio":"./app/patterspieces/Danio_rerio.GRCz11.fa",
       "Drosophila_melanogaster":"./app/patterspieces/Drosophila_melanogaster.fa",
        "Mus_musculus":"./app/patterspieces/Mus_musculus.fa",
         "Oryza_sativa":"./app/patterspieces/Oryza_sativa_Build_genomic.fna",
        "Rattus_norvegicus":"./app/patterspieces/Rattus_norvegicus.fa",
         "Saccharomyces_cerevisiae":"./app/patterspieces/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa"
   }
reference_sequence=db[pattern_species]

with open(outfile+ '/outresult.fas','w') as f1,open(dir,'r') as p:
    pattern_fasta = SeqIO.parse(reference_sequence, "fasta")
    if sys.argv[3] == "True":
        p.readline()
    for line in p:
        line = line.split()
        name = '-'.join(line)
        chromosome_type = line[0]
        min_length = int(line[1])
        max_length = int(line[2])
        for fasta_string in pattern_fasta:
            if fasta_string.description == chromosome_type:
                f1.write('>' + name + '\n' + str(fasta_string.seq[min_length - 1:max_length]) + '\n')


make_archive(infile+ "/out", "zip",infile,"out")