#!/usr/bin/env Rscript

## https://www.bioconductor.org/packages/release/bioc/vignettes/edgeR/inst/doc/edgeRUsersGuide.pdf

library(argparse)
library(edgeR)

parser <- ArgumentParser()
parser$add_argument("-s", "--sampleid", type="character",
    help="sample ID to be stored as column header")
args <- parser$parse_args()

quant <- dirname(list.files(path=getwd(), pattern="abundance.h5", recursive=TRUE, full.names=TRUE))
catch <- catchKallisto(paths=quant, verbose=TRUE)
scaled.counts <- data.frame(catch$counts/catch$annotation$Overdispersion)
names(scaled.counts)[1]<-paste(args$sampleid)
write.table(scaled.counts, "scaledcounts.tsv", quote=FALSE, sep='\t')
