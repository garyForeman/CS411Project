import re

"""Dummy Variables"""
sample_all = bool(1)
genotype_all = bool(0)
marker_all = bool(1)

"""DRAWS FROM HTML"""

sample_var = {'sample_sample_id': bool(0), 'sample_name': bool(0),
              'sample_generation': bool(0), 'sample_sex': bool(0),
              'sample_mother': bool(0), 'sample_father': bool(0),
              'sample_notes': bool(0)}

genotype_var = {'genotype_sample_id': bool(0), 'genotype_marker_id': bool(0),
                'genotype_genotype1': bool(0), 'genotype_genotype2': bool(0)}

marker_var = {'marker_marker_id': bool(0), 'marker_meiotic_pos': bool(0),
              'marker_dog_chrom': bool(0), 'marker_dog_pos': bool(0),
              'marker_fox_seg': bool(0), 'marker_fox_chrom': bool(0),
              'marker_fox_pos': bool(0)}

if sample_all == bool(1):
    for variable in sample_var.keys():
        sample_var[variable] = bool(1)
        
if genotype_all == bool(1):
    for variable in genotype_var.keys():
        genotype_var[variable] = bool(1)

if marker_all == bool(1):
    for variable in marker_var.keys():
        marker_var[variable] = bool(1)   

usesample = any(sample_var.keys())
usegenotype = any(genotype_var.keys())
usemarkers = any(marker_var.keys())

if usesample == bool(1) and usemarkers == bool(1):
    if usegenotype != bool(1):
        print "ERROR" #How do we actually want to handle this?

"""DRAWS FROM SQL"""
SAMPLE_TABLE = 'sample_info_clean'
SAMPLE_FILE = '../../DBinit/sample_infoOct19.csv'
GENOTYPE_TABLE = 'has_genotype'
GENOTYPE_FILE = '../../DBinit/genotypesOct19.csv'
MARKER_TABLE = 'markers'
MARKER_FILE = '../../DBinit/markersOct19.csv'
ATTRIBUTES = {SAMPLE_TABLE: ['cornellnumber', 'name',
                             'generationdescription', 'sex_male1',
                             'mother', 'father', 'notes'],
              MARKER_TABLE: ['markername', 'MeioticPos', 'DogChr', 'DogPos',
                             'FoxChrSeg', 'FoxChr', 'FoxChrPos'],
              GENOTYPE_TABLE: ['cornellnumber', 'markername', 'genotype1',
                               'genotype2']}

htmltosql = {'sample_sample_id': ATTRIBUTES[SAMPLE_TABLE][0], 'sample_name': ATTRIBUTES[SAMPLE_TABLE][1],
             'sample_generation': ATTRIBUTES[SAMPLE_TABLE][2], 'sample_sex': ATTRIBUTES[SAMPLE_TABLE][3],
             'sample_mother': ATTRIBUTES[SAMPLE_TABLE][4], 'sample_father': ATTRIBUTES[SAMPLE_TABLE][5],
             'sample_notes': ATTRIBUTES[SAMPLE_TABLE][6], 'genotype_sample_id': ATTRIBUTES[GENOTYPE_TABLE][0],
             'genotype_marker_id': ATTRIBUTES[GENOTYPE_TABLE][1], 'genotype_genotype1': ATTRIBUTES[GENOTYPE_TABLE][2],
             'genotype_genotype2': ATTRIBUTES[GENOTYPE_TABLE][3], 'marker_marker_id': ATTRIBUTES[MARKER_TABLE][0],
             'marker_meiotic_pos': ATTRIBUTES[MARKER_TABLE][1], 'marker_dog_chrom': ATTRIBUTES[MARKER_TABLE][2],
             'marker_dog_pos': ATTRIBUTES[MARKER_TABLE][3], 'marker_fox_seg': ATTRIBUTES[MARKER_TABLE][4],
             'marker_fox_chrom': ATTRIBUTES[MARKER_TABLE][5], 'marker_fox_pos': ATTRIBUTES[MARKER_TABLE][6]}

all_varlists = [sample_var, genotype_var, marker_var]
for varlist in all_varlists:
    for varkey in varlist.keys():
        
