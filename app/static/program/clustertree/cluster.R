args <- commandArgs(TRUE);
if (length(args) != 5){
        print("Usage: Rscript cluster.R <input matrix> <out pdf> <method> <width> <height>");
        quit();
}
library(cluster)

exp_data=read.table(args[1], header=T, sep='\t')
hc_samples <- hclust(dist(t(exp_data)),method=args[3])
hc_samples <- as.dendrogram(hc_samples)
pdf(args[2], width=as.integer(args[4]), height=as.integer(args[5]))
plot(hc_samples,xlab='',ylab='')
