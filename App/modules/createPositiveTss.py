import sys
import string
import math

'''
This module creates the coordinates of the positive data set.
'''

def getPoints(filePath, rangeSize, outputFileName):
    k=rangeSize/2
    f=open (filePath, "r")
    points=[]
    while True:
        s=f.readline()
        try:
            if len(s)>0:
                s=s.strip()
                #print s
                point=s.split('\t')
                #print point
                point[1]=int(point[1])
                point[2]=int(point[2])
                point[1]=point[1]-k
                point[2]=point[2]+k
                point[1]=str(point[1])
                point[2]=str(point[2])
                points.append(point)
                #print point
            else:
                break
        except:
            break
    f.close()
    out(points,outputFileName)

def out(points,outputFileName):
    out=file(outputFileName,'a+')
    for i in points:
        s="\t".join(i)
        out.write(s)
        out.write("\n")
 

if __name__ == "__main__":
    filePath=sys.argv[1]


# def main():
#     file1=sys.argv[1]
#     points=getPoints(file1)
#     out(points)
    
# main()