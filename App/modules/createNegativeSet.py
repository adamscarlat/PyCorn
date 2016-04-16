import random


'''
This module creates the randomized negative dataset
'''

def createNegativeSet(setSize, sequenceLength, outputFileName):
	f=open(outputFileName,'w')
	cho=['A','G','C','T']
	for i in range(0,setSize):
	    sequence = ''.join([random.choice(cho) for n in range(0,sequenceLength)])
	    f.write(sequence+'\n')

	f.close()