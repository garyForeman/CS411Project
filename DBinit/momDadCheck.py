#! /usr/bin/env python

################################################################################
#Author: Gary Foreman
#Last Modified: October 5, 2014
#Prints output of momDadConverter.py next to the FatherQTL and MotherQTL fields
#from AnimalData.csv to check consistency.
################################################################################

from __future__ import print_function

import numpy as np
import re


ANIMAL_DATA = "AnimalData.csv"
MOM_DAD_DATA = "momDadConverted.txt"

if __name__ == '__main__':
    cornell_number_animal = np.genfromtxt(ANIMAL_DATA, usecols=(0),
                                          delimiter=',', dtype='string', 
                                          skip_header=1)
    fatherQTL = np.genfromtxt(ANIMAL_DATA, usecols=(2), delimiter=',',
                              dtype='string', skip_header=1)
    motherQTL = np.genfromtxt(ANIMAL_DATA, usecols=(3), delimiter=',',
                              dtype='string', skip_header=1)
    cornell_number_mom_dad = np.genfromtxt(MOM_DAD_DATA, usecols=(0),
                                           dtype='string', skip_header=1)
    mother_cornell = np.genfromtxt(MOM_DAD_DATA, usecols=(1), dtype='string',
                                   skip_header=1)
    father_cornell = np.genfromtxt(MOM_DAD_DATA, usecols=(2), dtype='string',
                                   skip_header=1)

    for i in xrange(len(cornell_number_animal)):
        if ((fatherQTL[i] == '0' or fatherQTL[i] == '') and 
            father_cornell[i] == 'NULL'):
            pass
        elif re.match(father_cornell[i], fatherQTL[i]):
            pass
        else:
            print(cornell_number_animal[i], cornell_number_mom_dad[i],
                  fatherQTL[i], father_cornell[i], 'DAD')

        if ((motherQTL[i] == '0' or motherQTL[i] == '') and 
            mother_cornell[i] == 'NULL'):
            pass
        elif re.match(mother_cornell[i], motherQTL[i]):
            pass
        else:
            print(cornell_number_animal[i], cornell_number_mom_dad[i],
                  motherQTL[i], mother_cornell[i], 'MOM')

        if (cornell_number_animal[i] == 'F05F307' or 
            cornell_number_animal[i] == 'F05F325'):
            print(cornell_number_animal[i], fatherQTL[i], father_cornell[i])
