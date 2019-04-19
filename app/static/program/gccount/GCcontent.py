import matplotlib
import os
import shutil
import sys

matplotlib.use('AGG')
import matplotlib.pyplot as plt
from Bio import SeqIO
from Bio.SeqUtils import GC
from shutil import make_archive

by= int(sys.argv[2])
inputdir = os.path.dirname(os.path.abspath(sys.argv[1]))
name = os.path.basename(os.path.abspath(sys.argv[1]))

os.chdir(inputdir)

outdir = inputdir + "/out/"

if os.path.exists(outdir):
	shutil.rmtree(outdir)
os.mkdir(outdir)

for seq_record in SeqIO.parse(name,"fasta"):
	i=0
	gc = GC(seq_record.seq)
	seqlen = len(seq_record)
	if seqlen < by:
		print("seq length is litter than bin")
		os._exit(0)
	box = []
	gc_list = []
	while by+i < seqlen + 1:
		my_seq = seq_record.seq[i:by-1+i]
		my_gc = GC(my_seq)
		box.append(i+1)
		gc_list.append(my_gc)
		i = i + 1
	plt.figure(figsize=(8,4))
	plt.plot(box,gc_list,"-",linewidth=2)
	plt.xlabel("site")
	plt.ylabel("GC content")
	plt.title("GC content distribution")
	plt.savefig(outdir + seq_record.id + ".pdf")
	f = open(outdir + sys.argv[3] + ".txt",'a') 
	f.write("seq id: %s \tlen: %d \tGC: %f \n" % (seq_record.id,len(seq_record),gc))
	f.close()

make_archive("out", "zip", "." , "out")
