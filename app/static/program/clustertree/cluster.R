args <- commandArgs(TRUE);
if (length(args) != 4){
        print("Usage: Rscript cluster.R <input matrix> <out pdf> <method> <width>");
        quit();
}
library(cluster)

exp_data=read.table(args[1], header=T, sep='\t')
hc_samples <- hclust(dist(t(exp_data)),method=args[3])
hc_samples <- as.dendrogram(hc_samples)
pdf(args[2], width=args[4])
plot(hc_samples,xlab='',ylab='')
