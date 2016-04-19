# PyCorn
<img align="right" src="https://dl.dropboxusercontent.com/u/92784443/pyCorn_small.jpeg">

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

###Data preparation
To build a neural-network model, we used 75,681 pre-labeld genomic coordinates of predominant TSS taken from the article *Mejia-Guerra et al., 2015* as our positive data, and we use **pybedtools** to generate the corresponding sequence. For negative data, we pick from the rest of neucleotides that were not labeled as predominant TSS from the corn genome. Next, in order to find the pattern around TSS, we choose a "frame" that centers at the target nucleotide and explands 500 nucleotides upstream and 499 nucleotides downstream to represent the sequence around TSS (or non-TSS in the negative data). 

The cooridinates (either from the original bed file provided by Mejia-Guerra or our choice of negative data), along with the whole corn genomic equence are fed to bedtools to generate sequence in FASTA format, which serves as our main training data. 

Sequences that contain more than 10 **'N'** nucleotides (bad reads) are ignored in PyCorn.

###Construction of neural network
**Input nodes:** 1000 nodes that represent the sequence of input data

**Hidden layer:** 1 hidden layer with 128 nodes

**Output nodes:** 2 nodes that specifies whether the central nucleotide is TSS or not

###Training the neural network
The neural network is trained using **scikit-learn neural network**. You can find the training process in [App/driver/scikitNN.py](https://github.com/adamscarlat/PyCorn/blob/master/App/driver/scikitNN.py).

###Finding the best model
Several combinations of the amount of postive/negative data and some other parameters are tested to find the best neural-network model. You may find more details about those parameters in the **Performance Evaluation** section. The best model is serialized and stored as a separate file [App/src/pipelineLessP.pkl](https://github.com/adamscarlat/PyCorn/blob/master/App/src/pipelineLessP.pkl) which can be replaced in the future once a better model is found.

#Run Pipeline
You can find the main script `pycorn.py` in `App\src\` , use “python” to run it.
Command:

	python pycorn.py inputfileName outputfileName windowslidesize

For example:

	python pycorn.py myGenome.fa tssLocation 100

inputfile: genomic sequence in FASTA format
outputfile: position of transcription start sites and its neighbor nucleotides
windowslidesize: the window size when you scan the genome

The parameter `windowslidesize` defines the resolution of the search. From our testing, smaller window size gives a better resolution up to a certain point. A window size that is too small may result in an increase of false positives while a window size that is too large may result in an increase of false negatives.The recommended window slide size is between 50 - 100. 

#Input File
Accepted input sequnce is in FASTA format, which begins with a single-line description starting with “>”, followed by lines of sequnce data.

An example for a valid input file (chromosome 1 of the Zea Maize):

	>1 dna:chromosome chromosome:AGPv3:1:1:301476924:1
	GAATTCCAAAGCCAAAGATTGCATCAGTTCTGCTGCTATTTCCTCCTATCATTCTTTCTG
	ATGTTGAAAATGATATTAAGCCTAGGATTCGTGAATGGGAGAAGGTATTTTTGTTCATGG
	TAGTCATTGGAACCTGCTAGATTGTACACTTGACAATAACATATATTAATATTAGTGACC
	CCATTTTTAAATTTCCTAGGCTGGCATTGAACAAGACTATGTTAGTAGGATGTTGTTGAA
	...



#Output File
You can check the format of output files:

	$ cat ../output
	
In this directory, you can find the results of PyCorn.

	output
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

Performance of the network training was measured by collecting the training error of each epoch. We observed a decrease of 90% in the training error over a span of 40 epochs. The validation rate obtained for the given network was 77%.

In order to test the result of the pipeline we matched our results against a sequence of 60,000 nucleotides from the Zea Maize genome that do not contain a TSS. We tested 4 different neural network models listed as models 1-4.
* ratio (pure/partial) signifies the ratio between negative learning examples that are completley pure (do not overlap into positive 	  areas). partial represent negative sequences that overlap into positive areas for up to 95%.
* max overlap length- the maximum overlap of a negative sequence into a positive area.
* jump- window slide size of the pipeline (see run pipeline).
* ned D- number of negative examples in training phase
* pos D- number of positive examples in training phase
* FP over 60,000 nts- number of false positive TSS 
	
		| Model      |   ratio(pure/partial)  | max overlap length | jump | Neg D | Pos D |  #FP over 60,000 nts  |
		|:-----------|--------------------------------------------:|:------------:|:-----:|----------------------:|
		| 1          |    Only pure negative  |       0            |  100 | 20000 | 50000 |  143                  |
		| 2          |      7:3               |      900           |  100 | 30000 | 50000 |  120                  |
		| 3          |      3:7               |      950           |  100 | 40000 | 50000 |  94                   |
		| 4          |      3:7               |      950           |  100 | 50000 | 10000 |  8                    |
