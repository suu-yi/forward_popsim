## BINP29 Forward-time Population Simulator

Forward time population simulator is a  script that produces new simulated population generation by generation and track their origins using SNPs from PLINK .ped data of diploid human populations.

#### Methodology

Uses real PLINK pedigree file sample to simulate population over n number of generations and tracks the population origins of the simulated individuals.

Based on a simple model where population evolves generation by generation without overlap. User defined parameters include the proportion of the effective/breeding population, mutation rate, max and min number of offspring per couple. Random sampling is used for mating and each offspring inherits one random allele from each parent. Offspring population (F*n*) replaced the entire parent population (P) as the next parent generation.

### Getting started
##### Sample files
Sample files are provide:  

Input test file: test_gen.ped  
Output test files: testout.ped sim.log origins.txt

#### Prerequisites
To run the python program in command line, the following are required:
- conda
- python 3.8.8
- numpy 1.22.3

#### Installing
Conda needs to be installed in order to install python and numpy for the script to run.

Create a new conda environment and activate the new environment:
```
conda create -n popsim -c conda-forge python=3.8.8 numpy=1.22.3 -y
conda activate popsim
```
### Usage
It is recommended to make a new directory to store the files and use as the working directory to run the script.
To view the descriptions for the parameters, use the -h flag:
```
python forward_popsim.py -h

usage: forward_popsim.py [-h] [-i] [-o] [-g] [-ne] [-u] [-m] [-M]

optional arguments:
  -h, --help            show this help message and exit
  -i , --infile         required input .ped file
  -o , --output         output file name, default name: sim_out.ped
  -g , --generations    number of generations to simiulate
  -ne , --breeding      ratio of breeding population, default at 0.8
  -u , --mutation       mutation rate of alleles, default at 10^-8
  -m , --minoffspring   minimum number of offsprings per couple
  -M , --maxoffspring   maximum number of offsprings per couple
```

To run the script, using the test file :

(example input: 500 individuals, 100 SNPs (diploid), simulate 5 generations)
```
python forward_popsim.py -i test_gen.ped -g 5 -o testout.ped

```

### Output
Three output files are created for each run:
- simulated population file
- population origins of simulated individuals
- log file containing population size for each generation

Remember to always rename the track and log files if multiple runs will be made in the same directory or to prevent accidentally replacing a file.

### Bugs
Deprecation Warning raised if python 3.9 is used but for version 3.8.8, it should be warning free.
```
DeprecationWarning: Sampling from a set deprecated
since Python 3.9 and will be removed in a subsequent version.
  ne_idv = random.sample(pop_name, Ne)
```
Program will stop with large dataset or running a large number of generations.Current known limit: 500 individuals, 20 generations, 100 SNPs PLINK pedigree file.
