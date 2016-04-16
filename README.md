# PyCorn

Introduction
Our pipeline is an open source tool developed for genome-wide prediction of transcription start site from maize genome data. Using a trained neural network, the pipeline takes as input sequence and outputs coordinates of possible TSS locations.

The pipeline is composed of two main stages: Training and Testing. 
In the training phase the parameters of the neural network are set. We supply as default, a trained neural network. If the user wishes, we supply instructions on how to train the network. 
For the testing phase, the user supplies a file that contains genomic data in FASTA format of the Zea Maize. The output file will contain coordinates of possible TSS locations. 

System Requirements

Installation

To install the pipeline simply clone the repository: 
	git clone https://github.com/adamscarlat/BioinformaticsPipeline.git


Or download it as a zip folder


Preparation


Run Pipeline
Output Files
You can check the format of output files:
	$ cd ../../
In this directory, you can find the results of PyCorn.
	output.csv
	
Publication
Performance Evaluation

