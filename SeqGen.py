# Generates sequences based on args
# python SeqGen.py <output filename> <seqnum> <seqlength>

import random, sys

def genSequence(fileName, seqNum, seqLength):
	symbols = ['A', 'C', 'G', 'T']

	f = open(fileName, "w")

	f.truncate(0)

	for i in range(seqNum):
		for j in range(seqLength):
			f.write(random.choice(symbols))

		f.write("\n\n")

	f.close()

genSequence(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))

