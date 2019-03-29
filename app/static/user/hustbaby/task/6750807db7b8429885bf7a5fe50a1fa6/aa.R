library(ggplot2);
options(bitmapType='cairo')
x <- read.table("aa.matrix", head = T, sep = "	")
pdf(file="out/aa.enrichment.pdf",width=10,height=10)
p <- ggplot(x,aes(x=-log10(Qvalue),y=reorder(Pathway,Qvalue)))
p + geom_point(aes(size=Gene_number, colour=RichFactor))+theme(axis.text=element_text(color='black'),panel.background = element_rect(fill='transparent'),panel.grid=element_line(color='grey'),panel.border=element_rect(fill='transparent',color='black'),axis.title=element_text(size=15))+ylab("Pathway")+scale_color_gradient(low="springgreen",high="#E41A1C")
dev.off()
