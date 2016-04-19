import sys
import re
import math
from outputNN import *

class inputNN:

	#sequence file path
	filePath = ""

	#description of sequence
	descript = ""
	#whole sequence
	seq = ""

	#Constructor
	def __init__(self, filePath):
		self.filePath = filePath
		self.descript, self.seq = self.getSeq(self.filePath)
		pass


	#get nucleotide sequence from file
	def getSeq(self, filePath):
		f=open(filePath, "r")
		s=f.readline()
		if re.match('>',s):
			descript=s
			seq=f.read().replace('\n','')
			return descript, seq
		else:
			print 'Error: There is no description line'
			return

	def input(self, windowSlideSize, rangeSize, outObject):
		initial=rangeSize / 2
		iterationCounter = 1
		while len(self.seq) > rangeSize:
			rowofMatirx=min(100,(len(self.seq) - rangeSize) // windowSlideSize + 1)
			#print rowofMatirx
			#print rowofMatirx
			#while len(seq)>2*rangeSize:
			newInit,matrix,self.seq = self.generateInputMatrix(self.seq, windowSlideSize, rangeSize, rowofMatirx, initial)
			initial = newInit
			#print len(wholeSequence)
			outObject.compute(matrix, windowSlideSize)
			initial=initial + rowofMatirx
			print iterationCounter
			iterationCounter += 1
		outObject.out.write("===================\n")
		outObject.out.write("Total TSS(s) found:" + str(outObject.TSSCount) + "\n")
		return

	def generateInputMatrix(self, wholeSequence,windowSlideSize,rangeSize,rowofMatirx,initial):
		matrix=[]
		seq=[]
		s=''

		for i in range(0,rowofMatirx):
			seq=wholeSequence[(i*windowSlideSize):(rangeSize+i*windowSlideSize)]
			#print seq
			#seq=s.split('')
			#print seq
			#if seq.count('N')>=(0.01*len(seq)):
			#	continue
			seq_num=[]
			try:
				for n in range(len(seq)):
					if seq[n]=='A':
						seq_num.append(1)
					elif seq[n]=='C':
						seq_num.append(2)
					elif seq[n]=='T':
						seq_num.append(3)
					elif seq[n]=='G':
						seq_num.append(4)
					else:
						seq_num.append(0)
			except:
				print "more character than ATCGN, check your seq"

			seq_num.append(initial + int(round(i * 1.0 *windowSlideSize/2)))
			matrix.append(seq_num)
			#print initial
		wholeSequence=wholeSequence[(rowofMatirx*windowSlideSize):]
		newInit = initial + int(round(i * 1.0 *windowSlideSize/2) - windowSlideSize/2)
		return newInit,matrix,wholeSequence
