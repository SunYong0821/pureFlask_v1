args <- commandArgs(TRUE);
if (length(args) != 7){
        print("Usage: Rscript edgeRdiff.R <input matrix> <edgeR.DE_results> <Group1 name> <Group1 num> <Group2 name> <Group2 num> <dispersion>");
        quit();
}
library(edgeR)

data = read.table(args[1], header=T, row.names=1, com='')
total_num<- as.numeric(args[4])+as.numeric(args[6])

col_ordering = c(1:total_num)
rnaseqMatrix = data[,col_ordering]
rnaseqMatrix = round(rnaseqMatrix)
conditions = factor(c(rep(args[3], args[4]), rep(args[5], args[6])))
disp=as.numeric(args[7])
exp_study = DGEList(counts=rnaseqMatrix, group=conditions)
exp_study = calcNormFactors(exp_study)
et = exactTest(exp_study, dispersion=disp)
tTags = topTags(et,n=NULL)
write.table(tTags, file=args[2], sep='	', quote=F, row.names=T)
