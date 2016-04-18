from inputNN import *
from outputNN import *


expandlength = 20
seqfile = "testInput"
modelfile = "pipelineLessP.pkl"
outfile = "test.txt"
inputFile="testInput"
windowSlideSize=100
rangeSize=1000

#output object with default params
outputObject = outputNN(outfile=outfile, modelfile=modelfile, seqfile=seqfile)

#start input object and read file
inputObject = inputNN(inputFile)

#Start computing
inputObject.input(windowSlideSize = windowSlideSize, rangeSize = rangeSize, outObject = outputObject)