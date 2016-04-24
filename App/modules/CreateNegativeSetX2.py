
import random

#k = 400

def createNegativeCoords(start, end, k):
	total = end - start
	counter = start
	negatives=[]

	while (counter < end): 
		negatives.append([counter, counter+ k ])
		#counter += 1000
		counter += random.randrange(0, k )
	
	return negatives



def addToFile(negativeCoords, chromosome, strand, name, score, f):
	for coords in negativeCoords:
		f.write(chromosome + '\t' + str(coords[0]) + '\t' + str(coords[1]) + '\t' + name + '\t' + score + '\t' + strand + '\n')


def createPartialNegatives(partialNegCount, end, k):	
	negativeSet = []
	for i in xrange(partialNegCount):
		randomEnd = random.randrange(0, k - 50)
		randEndPoint = end + randomEnd

		diff = k - randomEnd
		startPoint = end - diff

		negativeSet.append([startPoint, randEndPoint])

	return negativeSet

def activate(k):
	negativeSets = [
		[999878, 1662537, '1', '+', 'B73_R:TC_21', '3.67753587126814'],
		[7561931, 8024960, '1', '+', 'B73_R:TC_69', '3.29762333698702'],
		[10091565, 10220179, '6', '+', 'B73_R:TC_89', '3.67753587126814'],
		[149814654, 150053147, '9', '-', 'Mo17_S:TC_51204', '4.51502457813909'],
		[180961592, 181250343, '5', '-', 'Mo17_S:TC_27755', '6.44319695606259'],
		[114716561, 115538207, '10', '+', 'B73_R:TC_4902', '13.6531627201252' ],
		[3854633, 4076331, '10', '-', 'B73_R:TC_5211','27.4748475185206'],
		[2808728, 3076639, '2', '+', 'B73_R:TC_6646', '124.926644857516'],
		[7406593, 8196773, '3', '+', 'B73_R:TC_10212', '1.81801034554155'],
		[189609245, 190620884, '4', '+', 'B73_R:TC_14454', '17.95337723795'],
		[98680301, 100722816, '5', '+', 'B73_R:TC_17162', '10.2906299790867'],
		[23830, 351135, '5', '-', 'B73_R:TC_17798', '1.11104935362105'],
		[130298, 270203, '6', '-', 'B73_R:TC_24386', '1.11104935362105'],
		[99876587, 100266743, '7', '+', 'B73_R:TC_30813', '4.06070527807694'],
		[98712701, 100108871, '8', '+', 'B73_R:TC_33263', '2.5488861362763'],
		[554265, 1094154, '3', '+', 'B73_S:TC_12275', '2.92127944985388'],
		[39289685, 40286785, '9', '+', 'B73_R:TC_35027', '2.92127944985388'],
		[299835844, 300071906, '1', '-', 'B73_S:TC_4916', '10.5280199576822'],
		[554265, 1094154, '3', '+', 'B73_S:TC_12275', '1.1094430214305'],
	]

	negativeFile = open('negatives.bed','w')

	for negativeSet in negativeSets:
		negativeCoords = createNegativeCoords(negativeSet[0], negativeSet[1], k)
		numNegarives = len(negativeCoords)
		partialNegCount = (70 * numNegarives) / 100
		partialNegCoords = createPartialNegatives(partialNegCount, negativeSet[1], k)
		negativeCoords += partialNegCoords

		addToFile(negativeCoords = negativeCoords, chromosome = negativeSet[2], strand = negativeSet[3], name = negativeSet[4],
		 score = negativeSet[5], f = negativeFile)

	#x = createNegativeCoords(999878, 1662537, 1, '+', 5)

	#print x