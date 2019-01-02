args <- commandArgs(TRUE);
if (length(args) != 3){
        print("Usage: Rscript cluster.R <input matrix> <out pdf> <method>");
        quit();
}
library(cluster)

exp_data=read.table(args[1], header=T, sep='\t')
hc_samples <- hclust(dist(t(exp_data)),method=args[3])
hc_samples <- as.dendrogram(hc_samples)
pdf(args[2])
plot(hc_samples,xlab='',ylab='')
