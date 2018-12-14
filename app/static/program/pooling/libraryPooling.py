import sys, os
from shutil import make_archive
import pandas as pd
pd.set_option('precision', 6)

# python libraryPooling.py <xls> <number lane> <volume, eg 10ul> <basesize, eg 250[,350,450]>

vol = int(sys.argv[3])

basesize = sys.argv[4]
bs = basesize.split(',')
bsint = [int(i) for i in bs]

if len(bs) != int(sys.argv[2]):
    sys.exit("The number of basesize(250[,350,450]) must equal number of lane!")

inputdir = os.path.dirname(sys.argv[1])
outdir = inputdir + "/out"

writer = pd.ExcelWriter(outdir + '/out.pooling.xlsx')
for l in range(int(sys.argv[2])):
    re = pd.read_excel(sys.argv[1], sheet_name = l)
    meansize = bsint[l]
    l += 1
    ef = re.dropna(how="all").fillna(0).reset_index(drop=True)

    #maxsize = ef.iloc[:, 4] == ef.iloc[:, 4].max()
    #meansize = int(ef.iloc[:, 9][maxsize].mean())
    ef['基准片段'] = meansize  # 10
    ef['转换系数'] = 0.0  # 11
    ef['转换浓度'] = 0.0  # 12
    ef['稀释倍数'] = 1  # 13
    ef['稀释浓度'] = 0.0  # 14

    for i in range(ef.shape[0]):
        x = ef.iat[i, 9] - meansize
        if abs(x) <= 25:
            ef.iat[i, 11] = 1
            ef.iat[i, 12] = ef.iat[i, 8]
        elif 25 < abs(x) <= 75:
            ef.iat[i, 11] = 1.05
            if x > 0:
                ef.iat[i, 12] = ef.iat[i, 8] / 1.05
            else:
                ef.iat[i, 12] = ef.iat[i, 8] * 1.05
        elif 75 < abs(x) <= 125:
            ef.iat[i, 11] = 1.1
            if x > 0:
                ef.iat[i, 12] = ef.iat[i, 8] / 1.1
            else:
                ef.iat[i, 12] = ef.iat[i, 8] * 1.1
        elif 125 < abs(x) <= 175:
            ef.iat[i, 11] = 1.15
            if x > 0:
                ef.iat[i, 12] = ef.iat[i, 8] / 1.15
            else:
                ef.iat[i, 12] = ef.iat[i, 8] * 1.15
        elif 175 < abs(x) <= 225:
            ef.iat[i, 11] = 1.3
            if x > 0:
                ef.iat[i, 12] = ef.iat[i, 8] / 1.3
            else:
                ef.iat[i, 12] = ef.iat[i, 8] * 1.3
        elif 225 < abs(x) <= 275:
            ef.iat[i, 11] = 1.4
            if x > 0:
                ef.iat[i, 12] = ef.iat[i, 8] / 1.4
            else:
                ef.iat[i, 12] = ef.iat[i, 8] * 1.4
        elif 275 < abs(x) <= 325:
            ef.iat[i, 11] = 1.55
            if x > 0:
                ef.iat[i, 12] = ef.iat[i, 8] / 1.55
            else:
                ef.iat[i, 12] = ef.iat[i, 8] * 1.55
        elif 325 < abs(x) <= 375:
            ef.iat[i, 11] = 1.7
            if x > 0:
                ef.iat[i, 12] = ef.iat[i, 8] / 1.7
            else:
                ef.iat[i, 12] = ef.iat[i, 8] * 1.7
        elif 375 < abs(x) <= 425:
            ef.iat[i, 11] = 1.9
            if x > 0:
                ef.iat[i, 12] = ef.iat[i, 8] / 1.9
            else:
                ef.iat[i, 12] = ef.iat[i, 8] * 1.9
        else:
            sys.exit('部分样本片段跟基准片段相差太大，请检查修改之后再运行！！！')
        ef.iat[i, 14] = ef.iat[i, 12]

    volume = ef.iloc[:, 4] / ef.iloc[:, 12]
    fold = volume.max() / volume.min()
    line = []
    blank = list(ef.columns)
    blank.extend(['混合体积', '混合量', '混合总体积', '混合总量', '混合浓度', 'PoolingID', 'Pooling总量', 'Pooling体积'])
    blank = pd.DataFrame(blank, index=blank).T
    psum = psumvol = 0
    for i in range(5):
        edf = ef.copy()
        edf['混合体积'] = 1 / volume.min() * volume[volume <= volume.min() * vol]
        edf['混合量'] = edf['混合体积'] * edf['稀释浓度']
        edf['混合总体积'] = edf['混合体积'].sum()
        edf['混合总量'] = edf['混合量'].sum()
        edf['混合浓度'] = edf['混合总量'] / edf['混合总体积']
        edf['PoolingID'] = 'pooling' + str(i + 1)
        edf['Pooling总量'] = edf.dropna().iloc[:, 4].sum()
        psum += edf['Pooling总量'][0]
        edf['Pooling体积'] = edf.dropna().iloc[:, 4].sum() / edf['混合浓度'][0]
        psumvol += edf['Pooling体积'][0]
        line.append(edf.dropna())
        line.append(blank)
        if fold // vol == 0:
            break
        volume = volume[volume > volume.min() * vol]
        fold = volume.max() / volume.min()

    pcon = psum / psumvol
    line.pop(-1)
    qian = pd.concat(line, ignore_index = True)
    hou = pd.DataFrame([pcon] * qian.shape[0], columns = ['Pooling浓度'])
    pd.concat([qian, hou], axis = 1).to_excel(writer, sheet_name = 'lane' + str(l), index=False)

writer.save()

make_archive(inputdir + "/out", "zip", inputdir, "out")