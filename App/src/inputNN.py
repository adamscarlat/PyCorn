import re

class inputNN:

	#sequence file path
	filePath = ""

	#description of sequence
	descript = ""
	#whole sequence
	seq = ""

	#total nucleotides
	nucTotal = 0

	#Constructor
	def __init__(self, filePath):
		self.filePath = filePath
		self.descript, self.seq = self.getSeq(self.filePath)
		self.nucTotal = len(self.seq)
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
			if (iterationCounter % 10 == 0):
				print "precentage completed: ", 100 - (float(len(self.seq) ) / float(self.nucTotal)) * 100 , "%"

			rowofMatirx=min(1000, (len(self.seq) - rangeSize) // windowSlideSize + 1)
			newInit,matrix,self.seq = self.generateInputMatrix(self.seq, windowSlideSize, rangeSize, rowofMatirx, initial)
			initial = newInit
			outObject.compute(matrix, windowSlideSize)
			initial=initial + rowofMatirx
			iterationCounter += 1
		print 'precentage completed: 100%. See results in output file'
		outObject.out.write("===================\n")
		outObject.out.write("Total TSS(s) found:" + str(outObject.TSSCount) + "\n")
		return

	def generateInputMatrix(self, wholeSequence,windowSlideSize,rangeSize,rowofMatirx,initial):
		matrix=[]
		seq=[]

		for i in range(0,rowofMatirx):
			seq=wholeSequence[(i*windowSlideSize):(rangeSize+i*windowSlideSize)]
			nCounter = 0
			nFlag = False
			seq_num=[]
			try:
				for n in range(len(seq)):
					if nCounter > 0.01*len(seq):
						nFlag = True
						break
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
					if seq[n] == 'N':
						nCounter+=1
			except:
				print "more character than ATCGN, check your seq"

			if nFlag == False:
				seq_num.append(initial + int(round(i * 1.0 *windowSlideSize/2)))
				matrix.append(seq_num)
		wholeSequence=wholeSequence[(rowofMatirx*windowSlideSize):]
		newInit = initial + int(round(i * 1.0 *windowSlideSize/2) - windowSlideSize/2)
		return newInit,matrix,wholeSequence
