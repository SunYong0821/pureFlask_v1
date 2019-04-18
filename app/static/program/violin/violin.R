args = args <- commandArgs(TRUE)
# Rscript violin.R $in $type $data $preout $out
library(ggplot2)
library(Cairo)

dd <- read.table(args[1],header = TRUE,sep="\t")
#CairoPDF
pdf(file=paste("out/",args[4],".pdf",sep=""),width=14,height=6)

p <- ggplot(dd, aes(x=dd[,as.integer(args[2])], y=dd[,as.integer(args[3])])) +
  geom_violin(aes(fill=factor(dd[,as.integer(args[2])]))) +
  scale_y_continuous(limits=c(0,6)) +
#  labs(title="Log10(Depth) distribution in microHaplotype") +
  theme(axis.text.x=element_text(angle=50,hjust=0.5, vjust=0.5)) +
  theme(legend.position="none" ) +
  theme(plot.title = element_text(hjust = 0.5)) + 
  xlab("") +
  ylab("")
p
print(p)
dev.off()
