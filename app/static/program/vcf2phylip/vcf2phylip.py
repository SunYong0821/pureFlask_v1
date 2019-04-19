import sys,os,subprocess,shutil
from shutil import make_archive

path = os.path.dirname(os.path.abspath(sys.argv[0]))
inputdir = os.path.dirname(os.path.abspath(sys.argv[1]))

outdir = inputdir + "/out"
if os.path.exists(outdir):
	shutil.rmtree(outdir)
os.mkdir(outdir)

os.chdir(inputdir)

script = f"java -jar /opt/software/PGDSpider_2.1.1.3/PGDSpider2-cli.jar -inputfile {sys.argv[1]} -outputfile out/{sys.argv[2]}.phy -spid {path}/VCF_to_PHYLIP.spid"
subprocess.run(script, shell=True)
print(outdir)
print(inputdir)

make_archive("out", "zip", "." , "out")
