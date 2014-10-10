#! /usr/bin/env python


from __future__ import print_function
import numpy as np

###Note: Check if the markers were switched which doesn't matter!!!!!!!


ANIMAL_DATA = 'AnimalData.csv'
MARKER_DATA = 'cleanMarkerData.csv'
MARKER_LIST = ['VV1127', 'VV1118', 'VV1112', 'FH2019', 'FH3393', 'REN245N06',
               'CM11.33', 'CM11.27', 'CM11.15', 'CM11.13', 'FH4031',
               'REN172L08', 'REN94K23', 'REN01G01', 'CM35.13d', 'CM35.11b', 
               'CM35.9a', 'CM35.7a', 'CM35.4a', 'CM5.34', 'CM5.37', 'CM5.41',
               'CM5.60', 'CM5.63', 'FH3928', 'FH3004', 'FH3320', 'DTR05.8',
               'CM5.41b', 'FH3278', 'FH3978', 'CM5.627', 'REN175P10',
               'CM5.701', 'CM5.761', 'FH3089', 'CM5.832', 'CM5.894']

N = len(MARKER_LIST)*2

def getColumnNumbers(column_numbers):
    with open('AnimalData.csv') as infile:
        line = infile.readline().split(',')

    for i in xrange(0,N,2):
        for j in xrange(len(line)):
            if MARKER_LIST[i/2] == line[j]:
                column_numbers[i] = j
                column_numbers[i+1] = j + 1
                break
        else:
            print('Double check', MARKER_LIST[i/2])

def checkSampleData(cornell_number, marker_data, cleanZeros=False):
    for i in xrange(len(cornell_number)-1):
        for j in xrange(i+1,len(cornell_number)):
            if cornell_number[i] == cornell_number[j]:
                if not np.array_equal(marker_data[i], marker_data[j]):
                    print("Inconsistency in", cornell_number[i], 'at rows',
                          i, j)
                    for k in xrange(N):
                        if marker_data[i,k] != marker_data[j,k]:
                            print(MARKER_LIST[k/2], i, marker_data[i,k], j,
                                  marker_data[j,k])
                            if cleanZeros:
                                if marker_data[i,k] == 0:
                                    marker_data[i,k] = marker_data[j,k]
                                elif marker_data[j,k] == 0:
                                    marker_data[j,k] = marker_data[i,k]
                    print()

def writeNewMarkerFile(cornell_number, marker_data):
    with open(MARKER_DATA, 'w') as outfile:
        outfile.write('cornell_number,')
        for i in xrange(0,N,2):
            outfile.write(MARKER_LIST[i/2] + ',' + MARKER_LIST[i/2] + '.copy,')
        outfile.write('\n')
        for i in xrange(len(cornell_number)):
            outfile.write(cornell_number[i] + ',')
            for j in xrange(N-1):
                outfile.write(str(marker_data[i,j]) + ',')
            outfile.write(str(marker_data[N-1,j]) + '\n')

if __name__ == '__main__':
    column_numbers = np.empty(N, dtype=np.int16)
    getColumnNumbers(column_numbers)

    cornell_number = np.genfromtxt(MARKER_DATA, usecols=(0), delimiter=',',
                                   dtype='string', skip_header=1)

    #marker_data = np.genfromtxt(ANIMAL_DATA, usecols=column_numbers,
    #                            delimiter=',', dtype=np.int32, skip_header=1)
    marker_data = np.genfromtxt(MARKER_DATA, usecols=range(1, N + 1),
                                delimiter=',', dtype=np.int32, skip_header=1)

    checkSampleData(cornell_number, marker_data, cleanZeros=False)

    #writeNewMarkerFile(cornell_number, marker_data)
