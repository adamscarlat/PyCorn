from inputNN import *
from outputNN import *
import sys


# expandlength = 20

# outfile = "test.txt"
# inputFile="inputTest"
# windowSlideSize=100


if len(sys.argv) != 4:
	print "Please provide correct parameters"
	sys.exit()

try:
	inputFile=sys.argv[1]
	outfile=sys.argv[2]
	windowSlideSize = int(sys.argv[3])
except:
	print "Please provide correct parameters"

modelfile = "pipelineJZ.pkl"
seqfile=inputFile
rangeSize=400

#output object with default params
outputObject = outputNN(outfile=outfile, modelfile=modelfile, seqfile=seqfile)

#start input object and read file
inputObject = inputNN(inputFile)

#Start computing
inputObject.input(windowSlideSize = windowSlideSize, rangeSize = rangeSize, outObject = outputObject)
