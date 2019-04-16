
library(ggseqlogo)
motif_seq <- c("CGATGCTGATCG","CGATGCTGATCG","CAGTCGATCGTA","CGATGCTGATCG","GCTAGCTAGCTA","CGATGCTGATCG","GCTAGTCGATCA")
pdf('./app/static/user/123123/task/52f6d8b3a8f046e7999f11bb318ec842/out/out.pdf', height=4, width=7)
ggseqlogo(motif_seq, method = 'bits', col_scheme='nucleotide')
dev.off()
    