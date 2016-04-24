"""
@:function Merge postive & negative data set, and add a binary label column (1 = is-TSS, 0 = non-TSS)
@:author Tay2510
@:param postive file, negative file
"""
from random import shuffle

"""
A function that generates a data matrix from +/- dataset for ML
@:param postiveFile in string path
@:param negativeFile in string path

"""

def mergeTable(positivefile, negativefile):

    tempdata = list()
    plength = 0
    nlength = 0

    # Read postive data file
    p = open(positivefile, 'r')
    pline = p.readline().rstrip()

    counter = 0
    positiveCap = 75000
    while pline and counter < positiveCap:
        if pline[0] != '>':
            pline += '1'
            tempdata.append(list(pline))
            plength += 1
        pline = p.readline().rstrip()
        counter += 1

    print counter
    p.close()

    # Read negative data file
    # The binary label uses '1' as "is-Tss" and '0' as "non-TSS"
    n = open(negativefile, 'r')
    nline = n.readline().rstrip()

    counter = 0
    negativeCap = 100000
    while nline and counter < negativeCap:
        try:
            if nline[0] != '>':
                nline += '0'
                tempdata.append(list(nline))
                nlength += 1
            nline = n.readline().rstrip()
            counter += 1
        except:
            print nline, nlength
    
    print counter
    n.close()

    # return a shuffled data
    shuffle(tempdata)
    return tempdata
