import os,sys,subprocess,shutil
from shutil import make_archive


inputdir = os.path.dirname(os.path.abspath(sys.argv[1]))
inputname = os.path.basename(sys.argv[1])
prodir = os.path.dirname(os.path.abspath(sys.argv[0]))

outdir = inputdir + "/out"

if os.path.exists(outdir):
        shutil.rmtree(outdir)
os.mkdir(outdir)

os.chdir(inputdir)

script = f"Rscript {prodir}/flower.R {inputname} {sys.argv[2]}"
subprocess.run(script,shell=True)

make_archive("out", "zip", ".", "out")
