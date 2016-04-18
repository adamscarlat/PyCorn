import pickle, os

class outputNN:
	#file paths
	outfile = ""
	seqfile = ""
	modelfile = ""

	#neural network object
	nn = None
	TSSCount = 0
	firstIndex = 0
	expandlength = 20 

	#output file object
	out = None

	#Constructor
	def __init__(self, outfile = "test.txt", modelfile = "pipeline.pkl", seqfile = "testInput"):
		self.outfile = outfile
		self.modelfile = modelfile
		self.seqfile = seqfile

		#load nn from pickle file
		self.nn = pickle.load(open(self.modelfile, 'rb'))

		#check if file exists. If yes overwrite it
		if (os.path.isfile(self.outfile)):
			try:
				os.remove(outfile)
			except:
				print "cannot overwrite file"

		self.out = open(outfile, "a+")


		'''
	expandIndex(index) - take a central index and expand it into a index list

	Input: index as the center (predominate TSS in our case)

	Return: a python list that represents the list of index

	'''
	def expendIndex(self, index):
	    indexList = []
	    head = index - self.expandlength
	    tail = index + self.expandlength
	    # if TSS is
	    if (head < self.firstIndex):
	        head = self.firstIndex

	    for i in range(head, tail, 1):
	        indexList.append(i)

	    indexList.append(tail)
	    return indexList

	'''
	getSequence(index []) -

	Input: index as the coordinate of genomic sequence.

	Output: a python list contains chars.

	'''
	def getSequence(self, index):
	    i = self.firstIndex
	    indexlist = self.expendIndex(index)
	    padding = "..."
	    charlist = [padding]
	    with open(self.seqfile) as f:
	        # linear search to locate the specific index
	        while True:
	            # Python: read char by char
	            c = f.read(1)
	            if c == '\n' : continue
	            if not c:
	                # End of file
	                break
	            if i in indexlist:
	                if i == index:
	                    charlist.append('[' + c + ']')
	                else:
	                    charlist.append(c)
	            i += 1
	    charlist.append(padding)
	    return "".join(charlist)


	'''
	compute(xTest [[]]) - function for computing

	Input: xRaw as numerically translated sequences

	Output: print the following to the file
	    167  ...ATCG[C]CTTA...
	     23  ...ATCA[T]GCCT...
	'''
	def compute(self, xRaw, windowSlideSize):
	    # extract index
	    indexarray = []
	    for i in range(len(xRaw)):
	        indexarray.append(xRaw[i].pop())

	    # prediction based on the model
	    yTest = self.nn.predict(xRaw)
	    
	    # check predicted result

	    lastIndex = indexarray[0]
	    for i in range(len(yTest)):
	        if yTest[i] == 1:
	            index = indexarray[i]
	            if (index - lastIndex) <= windowSlideSize:
	            	lastIndex = index
	            	continue

	            self.out.write('{:10d} {:110s}'.format(index, self.getSequence(index)) + "\n")
	            self.TSSCount += 1
	            lastIndex = index





