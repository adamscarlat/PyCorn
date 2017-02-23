# PyCorn
<img align="right" src="https://dl.dropboxusercontent.com/u/92784443/pyCorn_small.jpeg">

## Introduction
Our pipeline is an open source tool developed for genome-wide prediction of transcription start sites (TSS) from maize genome data. Using a trained neural network, the pipeline takes as input a sequence and outputs coordinates of possible TSS locations.

The pipeline is composed of two main stages: Training and Testing.
During the training phase, the parameters of the neural network are set. We supply as a default, a trained neural network. If the user wishes, we supply instructions on how to train the network.
For the testing phase, the user supplies a file that contains genomic data from the Zea Maize genome in [FASTA format](http://zhanglab.ccmb.med.umich.edu/FASTA/). The output file will contain coordinates of possible TSS locations.

## Installation
First, install [scikit-neuralnetwork](https://github.com/aigamedev/scikit-neuralnetwork):
```
pip install scikit-neuralnetwork
```

To install the pipeline, simply clone the repository:
```
git clone https://github.com/adamscarlat/pyCorn.git
```
Or download it as a zip file.

## Training Phase

### Data Preparation
To build the neural-network model, we used 75,681 pre-labeled genomic coordinates of predominant TSS taken from the article *Mejia-Guerra et al., 2015* as our positive data. We used [`pybedtools`](https://pypi.python.org/pypi/pybedtools) to generate the corresponding sequence. For negative data, we pick from the rest of nucleotides that were not labeled as predominant TSS from the corn genome. Next, to denote the pattern sequence around TSS (or non-TSS in the negative data), we choose a *frame* that centers at the target nucleotide and expands 500 nucleotides upstream and 499 nucleotides downstream.

The coordinates, from either the original bed file provided by Mejia-Guerra or our choice of negative data, along with the whole corn genomic sequence are fed into `pybedtools` to generate a sequence in FASTA format. This serves as our main training data.

Sequences that contain more than 10 **'N'** nucleotides (bad reads) are ignored by `PyCorn`.

### Construction of the Neural Network
**Input nodes:** 1000 nodes that represent the sequence of input data

**Hidden layer:** 1 hidden layer with 128 nodes

**Output nodes:** 2 nodes that specifies whether the central nucleotide is TSS or not

### Finding the Best Model
By varying the amount of positive and negative training data, as well as some other parameters, we can find the best neural-network model. You can find more details about those parameters in the [**Performance Evaluation**](#performance-evaluation) section. The best model is serialized and stored as a separate file which can be replaced in the future if a better model is found.

## Running the Pipeline
You can find the main script `pycorn.py` in `App\src\`.

The command obeys the following format:
```sh
$ python pycorn.py -i inputFile -o outputFile -w windowSlideSize
```
`inputFile` denotes genomic sequence in FASTA format  
`outputFile` denotes the position of TSS and its neighboring nucleotides  
`windowslidesize` denotes the window size when scanning the genome  

Example:
```sh
$ python pycorn.py  -i myGenome.fa  -o tssLocation -w 100
```

> **NOTE**: If no parameters are supplied the testInputSmall test data will be used with a window size of 100. This test data simulates a small genomic sequence. Default result will be saved to testResult.txt

The parameter `windowslidesize` defines the resolution of the search. From our testing, smaller window size gives a better resolution up to a certain point. A window size that is too small may result in an increase of false positives while a window size that is too large may result in an increase of false negatives.The recommended window slide size is between 50 - 100. 

## Input File
Accepted input sequence is in FASTA format, which begins with a single-line description starting with “>”, followed by lines of sequence data.

An example for a valid input file (chromosome 1 of the Zea Maize):
```
>1 dna:chromosome chromosome:AGPv3:1:1:301476924:1
GAATTCCAAAGCCAAAGATTGCATCAGTTCTGCTGCTATTTCCTCCTATCATTCTTTCTG
ATGTTGAAAATGATATTAAGCCTAGGATTCGTGAATGGGAGAAGGTATTTTTGTTCATGG
TAGTCATTGGAACCTGCTAGATTGTACACTTGACAATAACATATATTAATATTAGTGACC
CCATTTTTAAATTTCCTAGGCTGGCATTGAACAAGACTATGTTAGTAGGATGTTGTTGAA
...
```

## Output File
You can check the format of output files:
```sh
$ cat ../output
```
	
You can find the results of PyCorn in this directory.
```
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
```

## Performance Evaluation

The performance of the trained model was evaluated by collecting the training error of each epoch. We observed a decrease of 90% in the training error over a span of 40 epochs. The validation rate obtained for the given network was 77%.

To test the result of the pipeline we matched our results against a sequence of 60,000 nucleotides from the Zea Maize genome that does not contain a TSS. We tested four different neural network models, which are displayed below:
```
| Model      |   Sequence Length      | Negative Sequences | Positive Sequences | sensitivity | specificity |  
|:-----------|--------------------------------------------:|:------------------:|-------------|------------:|
| 1          |      400               |     100,000        |  	75,000	        |  0.809      |   0.702     |
| 2          |      400               |     100,000        |    15,000          |  0.046      |   0.994     |
| 3          |      400               |     100,000        |    75,000          |  0.648      |   0.799     |
| 4          |      800               |     100,000        |    75,000          |  0.44       |   0.898     |
| 5          |      400               |     100,000        |    15,000          |  0.181      |   0.967     |
```

`Sequence Length` - length of the training example and testing sequences  
`Negative Sequences` - number of negative sequences in the negative set  
`Positive Sequences` - number of positive sequences in the positive set  
`sensitivity` - true positive rate  
`specificity` - true negative rate  
