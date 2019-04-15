import sys, os, subprocess
from shutil import make_archive

inputdir = os.path.dirname(sys.argv[1])
name = os.path.basename(sys.argv[1])
outdir = inputdir + "/out"

method = sys.argv[2]
density = sys.argv[3]

script = f"convert -density {density} {sys.argv[1]} {outdir}/{name}.{method}"
subprocess.run(script, shell=True)

make_archive(inputdir + "/out", "zip", inputdir, "out")
