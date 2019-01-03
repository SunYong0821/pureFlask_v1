args <- commandArgs(TRUE)
library(pheatmap)
data = read.table(args[10], header = TRUE, sep = "\t", check.name = FALSE)
rownames(data) = data[,1]
data = data[,2:length(data[1,])]
data = as.matrix(data)
pdf(file = paste("out/", args[9], sep=""), width = as.integer(args[7]), height = as.integer(args[8]))
pheatmap(data, scale = args[1], cluster_rows = as.logical(args[2]), cluster_cols = as.logical(args[3]), show_rownames = as.logical(args[4]), show_colnames = as.logical(args[5]), display_numbers = as.logical(args[6]))
dev.off()