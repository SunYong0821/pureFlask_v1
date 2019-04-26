import os,sys
from shutil import make_archive

infile=os.path.dirname(sys.argv[1])
outfile= infile + "/out"
length=int(sys.argv[2])
fas = { }
with open(sys.argv[1],'r') as f:
    for line in f:
        if line[0] == '>':
            key = line.strip()
            fas[key] = f.readline().strip()

with open(outfile+'/outresult.fas','w') as f2:
    for key in fas:
        start = 0
        end = start + length
        f2.write(str(key)+'\n')
        while True:
            if end < len(fas[key]):
                f2.write(str(fas[key][start:end]) + '\n')
                start = end
                end += length
            elif end >= len(fas[key]):
                f2.write(str(fas[key][start:]) + '\n')
                break

make_archive(infile+ "/out", "zip",infile,"out")