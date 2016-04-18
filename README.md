# PyCorn

#Introduction
Our pipeline is an open source tool developed for genome-wide prediction of transcription start site from maize genome data. Using a trained neural network, the pipeline takes as input sequence and outputs coordinates of possible TSS locations.

The pipeline is composed of two main stages: Training and Testing. 
In the training phase the parameters of the neural network are set. We supply as default, a trained neural network. If the user wishes, we supply instructions on how to train the network. 
For the testing phase, the user supplies a file that contains genomic data in FASTA format of the Zea Maize. The output file will contain coordinates of possible TSS locations. 

#Installation
First, you need to install scikit-neuralnetwork: 

	pip install scikit-neuralnetwork

To install the pipeline simply clone the repository: 

	git clone https://github.com/adamscarlat/BioinformaticsPipeline.git

Or download it as a zip folder

#Training Phase
Construction of neural network:
The model is pre-trained using genomic coordinates of predominant TSS taken from the article Mejia-Guerra et al., 2015. Default parameters for training are 40,000 positive sequences and 25,000 negative sequences. The neural network is configued with 128 hidden nodes and is able to classify a sequence that contains a TSS. 
The training process is accomplished by driver.py which you can find in folder APP/driver.
First, it takes raw bed file as input and generate a positive dataset with coordinates in bed format. Then use this new bed file as input to get positive dataset in FASTA format from mazie genome. In order to generate negative dataset, 

Finding the best model:




#Run Pipeline
You can find the main script “ ” in  , use “python” to run it.
Command:

	python pipeline inputfileName outputfileName windowslidesize

inputfile: genome sequence in FASTA format
outputfile: position of transcription start sites and its neighbor nucleotides
windowslidesize: the window size when you scan the genome

For example:

	python pipeline myGenome.fa tssLocation 100

#Input File
Accepted input sequnce is in FASTA format, which begins with a single-line description starting with “>”, followed by lines of sequnce data.


#Output File
You can check the format of output files:

	`$ cat ../output.csv`
	
In this directory, you can find the results of PyCorn.

	output.csv
	This file contains the predicted position of transcription start sites.
        Column_No.	Description
            1		Coordinate of transcription start sites in genome
            2		Sequence of transcription start site and its neighbors on both sides
	For example,
		167 	...ACGTG[C]ACGGT...
		653		...TGCCA[G]CGTGT...
		1355	...GATCG[A]TGCCA...
				......


#Performance Evaluation

	| Model	 | non-overlapped : overlapped negative data | Cool  |
	
	| -------|:-----------------------------------------:| -----:|

	| 1      | 100: 0				     | $1600 |

	| 2	 | 70 : 30		                     |   $12 |

	| 3	 | 30 : 70		       |    $1 |
