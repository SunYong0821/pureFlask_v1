import sys, os
import pandas as pd
from collections import defaultdict, Counter
from random import shuffle
from shutil import make_archive

inputdir = os.path.dirname(sys.argv[1])
outdir = inputdir + "/out"

re = pd.read_excel(sys.argv[1])
ef = re.dropna(how="all").fillna(0).reset_index(drop=True)

vindex = ef.iloc[:, 5].apply(lambda x : int(x[-2:]) if str(x[-2:]).isdigit() else x[-2:])
libindex = ef.iloc[:, 7].apply(lambda x : int(x.split('-')[-1]) if x.split('-')[-1].isdigit() else x.split('-')[-1])
if ef.iloc[:, 7][vindex != libindex].tolist():
    indexerr = ','.join(ef.iloc[:, 7][vindex != libindex].tolist())
    print(f"index error: {indexerr}", file=sys.stderr)

alldata = ef.iloc[:,4].sum()
targetsize = alldata / int(sys.argv[2])
index = Counter(ef.iloc[:, 6].apply(lambda z : str(z).strip()))
morerepeat = [i[0] for i in index.most_common() if i[1] > int(sys.argv[2])]
if morerepeat:
    sys.exit("more repeat index: "+",".join(morerepeat))

library = {}
line = {}
size = {}
for i in range(ef.shape[0]):
    library[ef.loc[i][7]] = set([ef.loc[i][6]])
    # 1 mismatch
    #library[ef.loc[i][7]] = set([ef.loc[i][6][0:x] + 'N' + ef.loc[i][6][x+1:len(ef.loc[i][6])] for x,v in enumerate(ef.loc[i][6])])
    line[ef.loc[i][7]] = ef.loc[i]
    size[ef.loc[i][7]] = ef.loc[i][4]

intersection = defaultdict(list)
for i,v in library.items():
    for ii,vv in library.items():
        if i != ii and v & vv:
            intersection[i].append(ii)

big = 0
test = 0
randomsuccess = 0
while 1:
    lane = {i : [] for i in range(int(sys.argv[2]))}
    used = {}
    z = list(size.keys())
    shuffle(z)
    circle = 0
    writer = pd.ExcelWriter(outdir+'/out.lane.xlsx')
    duplicate = 0
    for i in range(int(sys.argv[2])):
        tmpsize = 0
        repeatindex = []
        for wk in z:
            if wk in used:
                continue
            if wk in repeatindex:
                continue
            else:
                if wk in intersection:
                    repeatindex.extend(intersection[wk])
                    tmpsize += size[wk]
                    if tmpsize - targetsize > 3:
                        tmpsize -= size[wk]
                        continue
                    elif abs(tmpsize - targetsize) <= 3:
                        lane[i].append(wk)
                        used[wk] = 0
                        break
                    else:
                        lane[i].append(wk)
                        used[wk] = 0
                        continue
                else:
                    tmpsize += size[wk]
                    if tmpsize - targetsize > 3:
                        tmpsize -= size[wk]
                        continue
                    elif abs(tmpsize - targetsize) <= 3:
                        lane[i].append(wk)
                        used[wk] = 0
                        break
                    else:
                        lane[i].append(wk)
                        used[wk] = 0
                        continue
        circle += len(lane[i])
        cl = Counter((line[x].文库类型 for x in lane[i]))
        duplicate += sum(z - 1 for z in cl.values() if z > 1)
        mat = pd.concat((line[x] for x in lane[i]), axis = 1)
        mat.T.to_excel(writer, sheet_name='lane'+str(i + 1), index=False)
    if duplicate > big:
        test += 1
        big = duplicate
        writer.save()

    if circle == ef.shape[0]:
        randomsuccess += 1
        if randomsuccess > 50 or test > 10:
            break

make_archive(inputdir + "/out", "zip", inputdir, "out")