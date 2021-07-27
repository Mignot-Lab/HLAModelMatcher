require(HIBAG);require(data.table);require(tidyverse)
setwd('/media/adiamb/HDD1/getHLAModels/')
modelsDf = fread('scripts/modelsLocalPath.txt', header = F)
modelVec=gsub('^\\./', '', modelsDf$V1)

parseSnps=function(model){
  if(file.exists(model)){
    hModel = get(load(model))
    out=lapply(hModel, function(hla){
      locusTable = data.table(locus = hla$hla.locus, snps=hla$snp.id, pos=hla$snp.position, alleles = hla$snp.allele)
    }) %>% rbindlist()
    out$model = model
    message(paste0('LOADED MODEL ', model, ' FOUND ', dim(out)[1]))
    return(out)
  }
}

modelDataTables=lapply(modelVec, parseSnps)

modelDF=rbindlist(modelDataTables)
modelDF$ETH=str_split(modelDF$model, pattern = "/", simplify = T)[,1]
modelDF$MODEL=str_split(modelDF$model, pattern = "/", simplify = T)[,2]

fwrite(modelDF, file='data/SNPS_IN_MODELS_JULY27_2021.txt', sep = " ")
## eth specific models
eths = unique(modelDF$ETH)
lapply(eths, function(pop){
  temp = modelDF[ETH == pop]
  fName = paste0('data/', pop, 'SNPS_IN_MODELS_JULY27_2021.txt')
  fwrite(temp, file = fName, sep=" ")
})
