library("DESeq2")
countdata <- read.table("./DESeq2.matrix",skip=1)
len <- length(countdata)
rownames(countdata) <- countdata[,1]
countdata <- countdata[,2:len]
type <- c("Control","Control","Control","Treat","Treat","Treat")
coldata <- data.frame(type)
rownames(coldata) <- c("Case1","Case2","Case3","Control1","Control2","Control3")
colnames(countdata) <- c("Case1","Case2","Case3","Control1","Control2","Control3")

dds <- DESeqDataSetFromMatrix(countData=countdata, colData=coldata, design = ~ type)
dds <- DESeq(dds,quiet=TRUE)
sizefactor <- sizeFactors(dds)
result <- results(dds, cooksCutoff=FALSE, independentFiltering=FALSE, pAdjustMethod="BH")

write.table(result, file="./DESeq2.deseq2", quote=FALSE, sep="\t")
write.table(sizefactor, file="./DESeq2.sizefactor", quote=FALSE, sep="\t")
