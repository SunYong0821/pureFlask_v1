library("pheatmap")
data<-read.table("./AllSamples.correlation.xls",head=TRUE)
rownames(data)<-data[,1]
colnames(data)<-c("Sample",rownames(data))
len<-length(data)
data<-as.matrix(data[,2:len])
mycolors <- colorRampPalette(c("white","blue"))(1001)
pheatmap(data,show_rownames=TRUE,show_colnames=TRUE,col=mycolors,cluster_rows=FALSE,cluster_cols=FALSE,legend=TRUE,fontsize=15,main="Correlation between Samples(method=pearson)",display_numbers=TRUE,number_format = "%.2f",cellwidth = 80,cellheight = 80,breaks=seq(0.6485424,1,(1-0.6485424)/1000),border_color="black",filename ="out/aa.correlation.pdf")
