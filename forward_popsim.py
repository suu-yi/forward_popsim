#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: forward_popsim.py
Date: 2022-03-18
Author: Yi Su

Description:
    This program uses data from a .ped file from PLINK to simulate populations 
        generation by generation, subjecting them to user defined parameters and
        outputs the final generation in a "simulated" .ped file and tracks the 
        origins of the final population.  
    User defined parameters include: number of generations simulated, effective
        population size. 
    Output also includes a sim.log file that shows the population size of each 
        generation and the total runtime.

List of functions:
    even()
    mutate()
    offspring()
    
Procedure:
    1. Take data from PLINK .ped file and creates an initial population in a 
        nested dictionary. Tuples are used as keys to track the population origins.
    2. Use the dictionary initial population to create offspring generation.
    3. Use a dictionary to track the population origins for each generation.
    4. Write final population into a file.
    5. Write the origins for each individual of the final simulated population
        into a txt file.
    6. Create a log file for the population size for each generation and the runtime
         in secs.
          

Usage:
    python forward_popsim.py [-h] [-i] [-o] [-g] [-ne] [-u] [-m] [-M]

"""

import random
import argparse
import numpy
import sys
import warnings
import timeit

warnings.filterwarnings("ignore", category=DeprecationWarning)

start = timeit.default_timer()

parser = argparse.ArgumentParser(description='')
parser.add_argument('-i', '--infile', metavar='', help='required input .ped file')
parser.add_argument('-o', '--output', metavar='', help='output file name, default name: sim_out.ped', default='sim_out.ped')
parser.add_argument('-g', '--generations', metavar='', type=int, help='number of generations to simiulate', default=1)
parser.add_argument('-ne', '--breeding', metavar='',type=float, help='ratio of breeding population, default at 0.8', default=0.8)
parser.add_argument('-u', '--mutation', metavar='', type=float, help='mutation rate of alleles, default at 10^-8', default=0.00000001)
parser.add_argument('-m', '--minoffspring', metavar='',type=int, help='minimum number of offsprings per couple', default=0)
parser.add_argument('-M', '--maxoffspring', metavar='',type=int, help='maximum number of offsprings per couple', default=5)
args = parser.parse_args()

if __name__ == '__main__':
    ped = args.infile
    outfile = args.output
    gens = args.generations
    Ne_p = args.breeding
    u = args.mutation
    min_off = args.minoffspring
    max_off = args.maxoffspring

if len(sys.argv) == 1:
    print("\n >>>>>> PLINK .ped input filename is required, specified with the flag -i ...please try again. \n")
    sys.exit()

############# functions

def even(x):
    '''
    Parameters
    ----------
    x : float
        convert the float into an even integer

    Returns
    -------
    y : integer
    '''
    x = round(x)
    if x%2:
        y = x+1
    else: y = x
    return y

def mutate(a,r):
    mut = numpy.random.uniform(0.0, 1.0, size=None)
    sample = random.sample(a,2)
    if mut <= r:
        x = sample[1]
    else:
        x = sample[0]
    return x

def offspring(k1, k2, d):
    '''
    Parameters
    ----------
    k1 : string
        Dict key for parent 1
    k2 : string
        Dict key for parent 2
    d : dictionary
        dictionary of population
        
        uses key for parents to retrieve alleles and creates new alleles  

    Returns
    -------
    ofs : list
        offspring alleles
    '''
    p1 = d[k1]
    p2 = d[k2]
    ofs = []
    for i in range(0,len(p1),2):
        g = p1[i:i+2]
        g2 = p2[i:i+2]
        if '0' not in g and g2:
            ofs.append(mutate(g, u))
            ofs.append(mutate(g2, u))
        else: 
            ofs.append('0')
            ofs.append('0')
    return ofs


#### logfille
log = open('sim.log', 'w')
########### check diploid

with open(ped) as filecheck:
    for line in filecheck:
        if len(line.split())%2:
            print("Diploids only for now. Please check the input file and make sure the .ped does not contain haploid data!")
            sys.exit()
            

############ initial population P

# population names
pop_set = set()
indic = {}

with open(ped) as infil:
    for line in infil:
        pop_set.add(line.split()[0])

with open(ped) as indv:
    for line in indv:
        x = line.split()
        indic[tuple(x[0:2])] = x[6:len(x)]

print("Population size for each generation: ", file=log)                         
print('P: ', end='', file=log)
print(len(indic), file=log)
                        
########### creates simulations                     

popsize = len(indic)
p_dict = {}
tracked_dict = {}

count = 1

while count <= gens:
    o_dict = {}
    track_dict = {}

######## random mating

    if count > 1:
        if popsize <= 1:
            print('Simulated population has reached extinction. More information in the sim.log file.')
            sys.exit()
        
        pop_list = list(p_dict.keys())
        Ne = even(Ne_p*popsize)
        pop_name = p_dict.keys()
        
        ne_idv = random.sample(pop_name, Ne)
    
        # coupling
        n = 1
        for i in range(0,len(ne_idv),2):
            p1 = ne_idv[i]
            p2 = ne_idv[i+1]
            # offspring
            m = random.randint(min_off, max_off)
            
            for j in range(m):
                o_dict[f'F{count}_{n}'] = offspring(p1, p2, p_dict)
                track_dict[f'F{count}_{n}'] = tracked_dict[p1]+tracked_dict[p2]
                n += 1

    # from initial population P    
    else:
        if popsize <= 1:
            print('Cannot simulate population with only one individual!')
            sys.exit()
        pop_list = list(pop_set)
        
        Ne = even(Ne_p*popsize)
        pop_name = indic.keys()
        
        ne_idv = random.sample(pop_name, Ne)
    
        # coupling
        n = 1
        for i in range(0,len(ne_idv),2):
            p1 = ne_idv[i]
            p2 = ne_idv[i+1]
            # offspring
            m = random.randint(min_off, max_off)
            
            for j in range(m):
                o_dict[f'F{count}_{n}'] = offspring(p1, p2, indic)
                track_dict[f'F{count}_{n}'] = [pop_list.index(p1[0])] + [pop_list.index(p2[0])]
                n += 1

         
    print(f'F{count}: ', end='', file=log)
    
    count += 1
    p_dict = o_dict
    tracked_dict = track_dict
    popsize = len(p_dict)

    print(popsize, file=log)
    
    
############ tracking the origins

with open('origins.txt','w') as origins_out:
    for k,v in tracked_dict.items():
        print(k, end=':\t', file=origins_out)
        for code in set(v):
            print(list(pop_set)[int(code)], end=' ', file=origins_out)
        print('\n', file=origins_out)

            
############## create simulated '.ped' file of the final simulated gen population

with open(outfile, 'w') as out:
    for indiv, geno in p_dict.items():
        print('sim', end=' ', file=out)
        print(str(indiv), end=' ', file=out)
        print('0 0 0 -9', end=' ', file=out)
        for g in geno:
            print(g+' ', end='',file=out)
        print('\n', file=out)

print(f"Files created: {outfile}, origins.txt, sim.log")
stop = timeit.default_timer()


print('Runtime: ', stop - start, 'sec', file=log)
log.close()
