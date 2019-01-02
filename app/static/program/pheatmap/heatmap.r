args <- commandArgs(TRUE)
library(pheatmap)
data = read.table("format.txt", header = TRUE, sep = "\t", check.name = FALSE)
rownames(data) = data[,1]
data = data[,2:length(data[1,])]
data = as.matrix(data)
pdf(file = ARGV[9], width = ARGV[7], height = ARGV[8], scale = ARGV[1], cluster_rows = ARGV[2], cluster_cols = ARGV[3], show_rownames = ARGV[4] show_colnames=ARGV[5] display_numbers=ARGV[6])
pheatmap(data)
dev.off()