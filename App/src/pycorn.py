from inputNN import *
from outputNN import *
import sys


# expandlength = 20

# outfile = "test.txt"
# inputFile="inputTest"
# windowSlideSize=100


def argError():
	print "Welcome to PyCorn!"
	print "------------------"
	print "Summary: "
	print "PyCorn is a python pipeline based on scikit-learn neural network library. The ultimate goal of PyCorn is " 
	print "to locate potential Transcription Start Site (TSS) according to our pre-trained neural network model."
	print ""

	print "Usage: "
	print "$ python pycorn.py <input file> <output file> <window slide size> "
	print ""

	print "Arguments: "
	print "		input file -  The path of fasta file containing genomic sequence to be identified "
	print "		output file - The path of output text file that will be responsible to store the TSS scanning result."
	print "		window slide size - Default is 400. PyCorn will use pre-trained model to predict TSS by looking into"
	print "                         nucleotides In order words, if you want to scan every nucleotide on the sequence,"
	print "                         please set it to 1. (But it will become very slow)"
	print ""
	print "Note: The suggested Python version is Python 2."

if len(sys.argv) != 4:
	argError()
	sys.exit()

try:
	inputFile=sys.argv[1]
	outfile=sys.argv[2]
	windowSlideSize = int(sys.argv[3])
except:
	argError()

modelfile = "pipelineAS.pkl"
seqfile=inputFile
rangeSize=400

#output object with default params
outputObject = outputNN(outfile=outfile, modelfile=modelfile, seqfile=seqfile)

#start input object and read file
inputObject = inputNN(inputFile)

#Start computing
inputObject.input(windowSlideSize = windowSlideSize, rangeSize = rangeSize, outObject = outputObject)
