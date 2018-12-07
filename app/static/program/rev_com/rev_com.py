import sys, os, subprocess

def rev(seq):
    return seq[::-1]

def com(seq):
    comdict = {'A':'T', 'C':'G', 'T':'A', 'G':'C'}
    return ''.join(comdict[i] for i in seq)

outdir = os.path.dirname(sys.argv[1])

if sys.argv[2] == "1":
    with open(sys.argv[1]) as inputfile, open(outdir + '/out.txt', 'w') as out:
        for i in inputfile:
            if i.startswith('>'):
                out.write(i)
                continue
            i = i.strip()
            out.write(rev(i) + '\n')
elif sys.argv[2] == "2":
    with open(sys.argv[1]) as inputfile, open(outdir + '/out.txt', 'w') as out:
        for i in inputfile:
            if i.startswith('>'):
                out.write(i)
                continue
            i = i.strip()
            out.write(com(i) + '\n')
elif sys.argv[2] == "3":
    with open(sys.argv[1]) as inputfile, open(outdir + '/out.txt', 'w') as out:
        for i in inputfile:
            if i.startswith('>'):
                out.write(i)
                continue
            i = i.strip()
            out.write(com(rev(i)) + '\n')                
else:
    print("参数设置出错！", file=sys.stderr)

subprocess.run("gzip -c " + outdir + '/out.txt ' + outdir + '/out.txt.gz', shell=True)