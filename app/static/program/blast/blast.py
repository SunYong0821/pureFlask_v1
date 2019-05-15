#!usr/bin/python
import sys,os
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from shutil import make_archive

infile=os.path.dirname(sys.argv[1])
outfile= infile + "/out"
dir=sys.argv[1]
parameter=sys.argv[2]
database=sys.argv[3]
evalue =float(sys.argv[4])
fasta_string=open(dir).read()
result_handle=NCBIWWW.qblast(parameter,database,fasta_string)
blast_reads=NCBIXML.parse(result_handle)
with open(outfile+'/blastresultm8.txt','w') as f1, open(outfile+'/blastmatch.txt','w') as  f2:
    f1.write("Query id"+'\t'+"Subject id"+'\t'+"alignment length"+'\t'+"%identity"+'\t'+"mismatches"+'\t'+"gap openings"+'\t'+"q.start"+'\t'+"q.end"+'\t'+"s. start"+'\t'+"s. end"+'\t'+"e-value"+'\t'+"bit    score"+'\n')
    b = 0
    for blast_read in blast_reads:
        for alignment in blast_read.alignments:
            i = 0
            while i < len(alignment.hsps) and evalue > alignment.hsps[i].expect:
                f2.write(blast_read.query.split(";")[0] + '\t')
                f2.write(str(alignment.accession) + '\n')
                f1.write(blast_read.query.split(";")[0]+'\t')
                f1.write(str(alignment.accession)+'\t')
                c = alignment.hsps[i]
                f2.write(str(c.query) + '\n')
                f2.write(str(c.sbjct) + '\n')
                f2.write(str(c.match) + '\n')
                f1.write(str(c.align_length)+'\t')
                identity=(c.identities/c.align_length)*100
                mismatches=c.align_length-c.identities
                f1.write(str(identity)+'\t'+str(mismatches)+'\t'+str(c.gaps)+'\t'+str(c.query_start)+'\t'+str(c.query_end)+'\t'+str(c.sbjct_start)+'\t'+str(c.sbjct_end)+'\t'+str(c.expect)+'\t'+str(c.bits) +'\n')
                i += 1

make_archive(infile + "/out", "zip", infile, "out")