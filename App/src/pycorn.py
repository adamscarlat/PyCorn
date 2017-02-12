from inputNN import *
from outputNN import *
import argparse

#globals
modelfile = "pipelineH.pkl"	# last updated by Jingzhi on May 5 2016
defaultInput = 'testInputSmall'
defaultOutput = 'testResult.txt'
rangeSize=400


def getHelpText():
	helpFile = open('HelpMessage.txt', 'r')
	for line in helpFile:
		print line


def getInputArgs():
	parser = argparse.ArgumentParser(description=getHelpText())
	parser.add_argument('-i','--inputFile', help='Input genomic sequence', required=False, default=defaultInput)
	parser.add_argument('-o','--outputFile', help='Output file', required=False, default=defaultOutput)
	parser.add_argument('-w','--windowSize', help='Window Size', required=False, default=100)
	args = vars(parser.parse_args())
	return args


args = getInputArgs()

seqfile=args['inputFile']


#output object with default params
outputObject = outputNN(outfile=args['outputFile'], modelfile=modelfile, seqfile=args['inputFile'])

#start input object and read file
inputObject = inputNN(args['inputFile'])

windowSize = int(args['windowSize'])

#Start computing
inputObject.input(windowSlideSize = windowSize, rangeSize = rangeSize, outObject = outputObject)


