#!/usr/bin/Rscript
args <- commandArgs(TRUE);
if (length(args) != 5){
        print("Usage: Rscript fpkm_density.R <input matrix> <out info> <sample1> <sample2> <method>");
        quit();
}
samples_tpm=args[1];
pdf_image=paste(args[2], "pdf", sep=".");
xb=paste("log10(exp+1) of",args[3],sep=" ");
yb=paste("log10(exp+1) of",args[4],sep=" ");
ma=paste("Correlation Plot",args[5],"method",sep=" ")
data <- read.table(samples_tpm, header = T, sep='\t')
library(ggplot2)

p <- qplot(log10( data$A+1 ), log10( data$B+1 ), xlab=xb, ylab=yb, main=ma, size=I(0.5))
p <- p + geom_abline(slope=1, size=0.5, colour="blue", alpha=0.5)
p <- p + theme_bw() + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())
xc <- 4/5 * min(log10(data$A+1)) + 1/5* max(log10(data$A+1))
yc <- 1/6 * min(log10(data$B+1)) + 5/6* max(log10(data$B+1))
c <- cor(log10( data$A+1 ),log10( data$B+1 ),method=args[5])^2
c <- round(c, 4)
p <- p + annotate("text", label = paste("r^2==",c), x = xc, y = yc, size = 5, colour = "blue", parse=TRUE)
p <- p + theme(plot.title=element_text(hjust=0.5))
pdf(pdf_image)
print(p)
dev.off()
