import argparse
import csv
import json
import os, re
from collections import Counter

hg19Coords=(29719561,32883508)
def parseBim(bimFile):
	pos=set()
	if os.path.exists(bimFile):
		with open(bimFile) as bim:
			reader=csv.reader(bim, delimiter="\t")
			for n, row in enumerate(reader):
				chr_, bp_ = row[0], int(row[3])
				if n % 100000 == 0:
					print('PROCESSED {} LINES FROM {} '.format(n, os.path.basename(bimFile)))
				if chr_ == '6':
					if bp_ >= hg19Coords[0] and bp_ < hg19Coords[1]:
						pos.add(bp_)
				else:
					continue 
					#raise ValueError('EXPECTING CHR 6 AS INPUT BIM')
	else:
		raise FileNotFoundError('CHECK FILE LOC {}'.format(bimFile))
	if len(pos) > 100:
		return pos
	else:
		raise ValueError('NOT ENOUGH SNPS IN MHC REGION HAVE YOU VERIFIED IF POS RANGE {} TO {}'.format(hg19Coords))

## Tests
# bimFile = "/media/adiamb/HDD1/PMRA_Stanford_122_132/Stanford_PMRA_Plates_122_130_132_Qced_Shapeit.bim"
# bimFile = "/media/adiamb/HDD1/earlyPlatesAffy5_6/data/PLATES_AFFY6_25_26_27_Qced.bim"
# bimPos=parseBim(bimFile)

def interSect(bimFile, ETH):
	bimPos=parseBim(bimFile)
	if bimPos:
		jsonParams = {'EUR':'data/European_POS_DUMP.json', 
		'EAS':'data/Asian_POS_DUMP.json',
		'AFR':'data/African_POS_DUMP.json',
		'LAT':'data/Hispanic_POS_DUMP.json',
		'ADMIX':'data/MultiEthnic_POS_DUMP.json'}
		if ETH in jsonParams:
			Dump = jsonParams.get(ETH)
			if os.path.exists(Dump):
				with open(Dump) as jsonFile:
					ethModels=json.load(jsonFile)
			else:
				FileNotFoundError('CHECK IF JSON FILES ARE IN data/ FOLDER')
		## evaluate the two lists
		modelCounter = Counter()
		for mod, posList in ethModels.items():
			for pos in posList:
				if int(pos) in bimPos:
					modelCounter[mod] += 1
		#modelCounter.most_common()
		outF = os.path.basename(bimFile)
		outFile= outF.replace('.bim', '.checkOverlap')
		with open('outs/'+outFile, 'w') as outPut:
			writer=csv.writer(outPut, delimiter=' ')
			header = ['ARRAY', 'nSNPS', 'TOTALSNPS', 'PERCENT']
			writer.writerow(header)
			for k, v, in ethModels.items():
				nSnps=modelCounter.get(k)
				totalSnps = len(v)
				perMatched = nSnps/totalSnps
				print('{} MATCHED {} SNPS OUT {} >> {:0.2f}% '.format(k, nSnps, totalSnps, perMatched*100))
				row = [k, nSnps, totalSnps, '{:0.2f}'.format(perMatched*100)]
				writer.writerow(row)
		print('DONE MATCHING {} AND CHECKS {} OUTPUT {}'.format(bimFile, ETH, outFile))

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-bim',required=True, help='A Plink .bim file')
	parser.add_argument('-eth', required=True, help='Ethnicity', choices=['EUR', 'EAS', 'AFR', 'LAT', 'ADMIX'])
	args = parser.parse_args()
	bimFile = args.bim
	ETH = args.eth
	interSect(bimFile, ETH)

if __name__ == '__main__':main()


