args <- commandArgs(TRUE)
library(pheatmap)
data = read.table(args[10], header = TRUE, sep = "\t", check.name = FALSE)
rownames(data) = data[,1]
data = data[,2:length(data[1,])]
data = as.matrix(data)
pdf(file = paste("out/", args[9], sep=""), width = args[7], height = args[8])
pheatmap(data, scale = \"args[1]\", cluster_rows = args[2], cluster_cols = args[3], show_rownames = args[4], show_colnames=args[5], display_numbers=args[6])
dev.off()