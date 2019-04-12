import sys, os, re, subprocess
from shutil import make_archive

inputdir = os.path.dirname(sys.argv[1])
outdir = inputdir + "/out"

method = sys.argv[2]
color = sys.argv[3]
col = int(sys.argv[4])
h = int(sys.argv[5])
w = int(sys.argv[6])

with open(sys.argv[1]) as f:
    rec = re.compile(r'[\t,]')
    c = []
    for line in f:
        ele = rec.split(line.strip())
        c.append(ele[col - 1])

    motif_seq = ','.join([f'"{i}"' for i in c])

with open(inputdir + "/plot.r", 'w') as rf:
    ro = f"""
library(ggseqlogo)
motif_seq <- c({motif_seq})
pdf('{outdir}/out.pdf', height={h}, width={w})
ggseqlogo(motif_seq, method = '{method}', col_scheme='{color}')
dev.off()
    """
    rf.write(ro)

script = f"Rscript {inputdir}/plot.r"
subprocess.run(script, shell=True)

make_archive(inputdir + "/out", "zip", inputdir, "out")
