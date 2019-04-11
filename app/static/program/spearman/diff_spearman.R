source('/home/test/04.spearman/labels2colors.R')
args<-commandArgs(trailingOnly=TRUE)
inFile<-args[1]
outFile<-paste(args[2],"diff_spearman.pdf",sep="/")

library("corrplot")
X=read.table(inFile,header=TRUE,row.names=1,sep="\t",check.names=F,quote="")

if (nrow(X) > 15) {
        X=t(X[c(order(rowSums(X)[-nrow(X)], decreasing=T)[1:15]),]) # top 1-15
}else{
X=t(X)
}

M=cor(X, method = "spearman")
head(M)
pdf(file=outFile,11,8.5)

corrplot(as.matrix(M), type = "upper", order = "hclust")
dev.off()
