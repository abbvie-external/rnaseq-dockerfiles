args <- commandArgs(trailingOnly = TRUE)
print(args)

dfile<-args[1]  #data file
pfile<-args[2]  #phenotype file
cfile<-args[3]  #contrast file
outdir<-args[4]

library("DESeq2")

d<-read.table(dfile,header=T,sep="\t",check.names=F)
ncol<-ncol(d)
d2<-d[,9:ncol]
rownames(d2)<-d[,1]

contrast<-as.vector(as.matrix(read.table(cfile,header=F, sep="\t")))
phenotypes<-read.table(pfile,header=T, sep=",")
type<-phenotypes['phenotype']

keep<- as.vector(as.matrix(type)) %in% contrast
d2<-d2[,keep]
type<-data.frame(type[keep,])

rownames(type)<-colnames(d2)
colnames(type)<-c("type")
type$type<-factor(type$type)

dds <- DESeqDataSetFromMatrix(countData = d2,
                              colData = type,
                              design = ~ type)

dds <- DESeq(dds)
res <- results(dds, contrast=c("type",contrast[c(2,1)]))

results<-as.data.frame(res)[,c("baseMean","log2FoldChange","pvalue", "padj")]
dd <- assay(rlog(dds))

d2.sum<-apply(d2,2,sum)
d2.cpm<-1000000*t(t(d2)/d2.sum)
#d2.fpkm<- 1000*d2.cpm/d$length
#dd.fpkm<-1000*(2^dd)/d$length

#get meanA, meanB
g1<-type==contrast[1]
g2<-type==contrast[2]

d3<-log2(d2.cpm+0.1)
d3.m<-apply(d3,1,mean)

results$baseMean<-d3.m
results$baseMeanA<-apply(d3[,g1],1,mean)
#results$baseMeanA<-d3[,g1]
results$baseMeanB<-apply(d3[,g2],1,mean)  ##TODO
#results$baseMeanB<-d3[,g2]
results$log2FoldChange<-results$baseMeanB-results$baseMeanA
results$foldChange<-2^results$log2FoldChange
results$cmpr<-paste0(contrast[2],"_vs_",contrast[1])

results$id<-rownames(results)
results2<-results[,c("id","baseMean","baseMeanA", "baseMeanB", "foldChange", "log2FoldChange","pvalue", "padj", "cmpr")]
colnames(results2)<-c("id","baseMean","baseMeanA", "baseMeanB", "foldChange", "log2FoldChange","pval", "padj", "cmpr")

ofile<-paste0(contrast[2],"_vs_",contrast[1],"_txt")
write.table(results2, ofile, sep="\t",row.names=F,col.names=T,quote=F);


 
