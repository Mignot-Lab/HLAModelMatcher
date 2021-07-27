from collections import defaultdict
import csv
import glob
import json
import os


def jsonDump(dict, jsonFile):
	with open(jsonFile, 'w') as F:
		json.dump(dict, F)


def main():
	snpFiles = glob.glob('data/*.txt')
	#remove last item > since its concatenated file
	snpFiles.pop()
	for file in snpFiles:
		posDic=defaultdict(list)
		eth = ''
		with open(file) as snpIn:
			reader = csv.reader(snpIn, delimiter=' ')
			next(reader)
			for row in reader:
				pos, model, eth = row[2], row[6], row[5]
				if pos not in posDic[model]:
					posDic[model].append(pos)
		outJson = os.path.join('data/', '{}_POS_DUMP.json'.format(eth))
		if not os.path.exists(outJson):
			jsonDump(dict=posDic, jsonFile=outJson)
			print('WROTE {} JSON FILE FOR ETH {} '.format(outJson, eth))
		else:
			print('SKIPPING {} FILE EXISTS {}'.format(outJson, eth))


if __name__ == "__main__":
	main()

# jsonFile = 'data/test.json'
# dict = posDic
# jsonDump(dict=posDic, jsonFile=jsonFile)