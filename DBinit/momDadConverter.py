#! /usr/bin/env python

################################################################################
#Author: Gary Foreman
#Last Modified: 9/29/14
#From AnimalData.csv converts the mom and dad fields from their own numbering
#system to the Cornell numbering system
################################################################################

import numpy as np


FILE_STRING = "AnimalData.csv"

if __name__ == '__main__':
    cornell_number = np.genfromtxt(FILE_STRING, usecols=(0), delimiter=',',
                                   dtype='string', skip_header=1)
    pedigree_number = np.genfromtxt(FILE_STRING, usecols=(7), delimiter=',',
                                    dtype='int', skip_header=1)
    mother = np.genfromtxt(FILE_STRING, usecols=(9), delimiter=',', dtype='int',
                           skip_header=1)
    father = np.genfromtxt(FILE_STRING, usecols=(8), delimiter=',', dtype='int',
                           skip_header=1)
    sex = np.genfromtxt(FILE_STRING, usecols=(10), delimiter=',', dtype='int', 
                        skip_header=1)

    #note: if sex == 1 means male, and if MotherQTL and FatherQTL are properly
    #      labeled, then the mom and dad columns are mislabeled, the labels
    #      should be reversed

    for i in xrange(len(cornell_number)-1):
        for j in xrange(i+1, len(cornell_number)):
            if cornell_number[i] == cornell_number[j]:
                if pedigree_number[i] != pedigree_number[j]:
                    if sex[i] == 2:
                        for k in xrange(len(cornell_number)):
                            if mother[k] == pedigree_number[j]:
                                mother[k] = pedigree_number[i]
                    elif sex[j] == 1:
                        for k in xrange(len(cornell_number)):
                            if father[k] == pedigree_number[j]:
                                father[k] = pedigree_number[i]

                    pedigree_number[j] = pedigree_number[i]

    foxes = dict()

    for i in xrange(len(cornell_number)):
        foxes[pedigree_number[i]] = cornell_number[i]

    foxes[0] = 'NULL'

    with open('momDadConverted.txt', 'w') as outfile:
        outfile.write('cornell_number mother father\n')
        for i in xrange(len(pedigree_number)):
            outfile.write(cornell_number[i] + ' ' +  foxes[mother[i]] + ' ' + 
                          foxes[father[i]] + '\n')
    
    for i in xrange(len(cornell_number)-1):
        for j in xrange(i+1, len(cornell_number)):
            if cornell_number[i] == cornell_number[j]:
                if father[i] != father[j]:
                    print "Father mismatch at", i, j
                    print cornell_number[i], father[i], father[j]
                if mother[i] != mother[j]:
                    print "Mother mismatch at", i, j
                    print cornell_number[i], mother[i], mother[j]

    for i in xrange(len(cornell_number)-1):
        if (pedigree_number[i] == 122 or pedigree_number[i] == 461 or 
            pedigree_number[i] == 7 or pedigree_number[i] == 77):
            print cornell_number[i], pedigree_number[i], mother[i], father[i]

    print

    for i in xrange(len(cornell_number)-1):
        if cornell_number[i] == 'F05F307' or cornell_number[i] == 'F05F325':
            print cornell_number[i], father[i]

