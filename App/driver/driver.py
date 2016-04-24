import sys, string, os
sys.path.append('../modules/')
import createPositiveTss as pTss
import createNegativeSet as nTss
import mergetable as mTable
import numpy as np
from pybedtools import BedTool
import CreateNegativeSetX2 as createNSbed


'''
Input: 
	bed_file_pre- file path for raw .bed file (dominant TSS locations), 
	rangeSize- for creating the output file in [range/2;range/2] lines,
	outputFileName- name for the new file
Output:
	The positive dataset coordinates in BED format 

It will create a file only if the file does not already exist
'''
def getPositiveDatasetBED(config):
	if (not os.path.isfile(config['bed_file_post'])):
		try:
			rangeSize=int(config['positive_dataset_range'])
			print "range size: ", rangeSize 
			pTss.getPoints(filePath=config['bed_file_pre'], rangeSize=rangeSize, outputFileName=config['bed_file_post'])
		except ValueError:
			print 'driver.getPositiveDatasetBED; Range supplied in configuration.txt must be an integer'
		except IOError:
			print 'driver.getPositiveDatasetBED; File ', config['bed_file_pre'], ' not found'


def getNegativeDatasetBED(config):
	createNSbed.activate(int(config['positive_dataset_range']))

'''
Input:
	negative_dataset_size- size of the negative dataset
	sequenceLength- equal to the chosen positive dataset sequence size (positive_dataset_range) 
Output:
	The negative dataset sequences in FASTA format

It will create a file only if the file does not already exist
'''
def getNegativeDatasetFASTA(config):
	try:
		coordinates = BedTool(config['negativesBedFile'])
		genome = BedTool(config['maize_genome_filepath'])
		dataset = coordinates.sequence(fi=genome, fo=config['negative_dataset_output'])
	except ValueError:
		print 'getNegativeDatasetFASTA; File ', config['maize_genome_filepath'], ' not found'


'''
Input:
	bed_file_post- bed file containing coordinates of the TSS regions
	positive_dataset_output- file name of the positive dataset file 
	maize_genome_filepath- maize genome filepath
Output:
	The positive dataset sequences in FASTA format

It will create a file only if the file does not already exist
'''
def getPositiveDatasetFASTA(config):
	if (not os.path.isfile(config['positive_dataset_output'])):
		try:
			coordinates = BedTool(config['bed_file_post'])
			genome = BedTool(config['maize_genome_filepath'])
			dataset = coordinates.sequence(fi=genome, fo=config['positive_dataset_output'])
		except ValueError:
			print 'getPositiveDatasetFASTA; File ', config['maize_genome_filepath'], ' not found'

'''
Input:
	negative_dataset_output- The negative dataset sequences in FASTA format
	positive_dataset_output- file name of the positive dataset file 
Output:
	Creates a numpy matrix where letters from the alphabes {A,C,T,G} are transformed
	into integers in the range 1-4. If a sequence has more than nThreshold N's
	it gets discarded.

'''
def createTrainingTable(config):
	table=mTable.mergeTable(positivefile=config['positive_dataset_output'], negativefile=config['negative_dataset_output'])
	nCounter=0
	nThreshold=10
	newTable=[]
	letterToInteger={'A': 1, 'C': 2, 'T': 3, 'G': 4, 'N':7, '1':1, '0':0}
	for data in table:		
		#Count N's in test sequence	
		nCounter=data.count('N')
		#take only if there are less than 10 N's
		if nCounter < nThreshold:
			newTable.append([letterToInteger[letter] for letter in data])
	
	return np.array(newTable)



'''
Create configuration dictionary from
configuration.txt. All configuration 
details will be available in config
'''
def createConfigDictionary(filePath):
	config={}
	f=open(filePath,'r')
	for line in f:
		try:
			lineParts=line.split('=')
			config[lineParts[0]]=lineParts[1].rstrip()
		except IndexError:
			print 'driver; Configuration file is not written properly. usage: [configuration_name=configuration_value]'
	return config 


#if driver.py is used as a program. Else it can be used 
#as a module
if __name__ == "__main__":
	config=createConfigDictionary('configurations.txt')
	getPositiveDatasetBED(config)
	getNegativeDatasetBED(config)
	getPositiveDatasetFASTA(config)
	getNegativeDatasetFASTA(config)
	featureTable=createTrainingTable(config)
	#y=featureTable[:,featureTable.shape[1]-1]
	#A=featureTable[:,0:featureTable.shape[1]-2]
	#print A,y

