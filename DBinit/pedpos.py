'''Functions for querying, inserting rows, and deleting rows from FoxDB.'''

from flask import flash
import MySQLdb
import csv
import re


DB_NAME = 'foxdb'
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWD = 'foxdb@CS411'
SAMPLE_TABLE = 'sample_info_clean'
SAMPLE_FILE = '../../DBinit/sample_infoOct19.csv'
GENOTYPE_TABLE = 'has_genotype'
GENOTYPE_FILE = '../../DBinit/genotypesOct19.csv'
MARKER_TABLE = 'markers'
MARKER_FILE = '../../DBinit/markersOct19.csv'
SET206_TABLE = 'SET206'
SET206_FILE = '../Set206.csv'
SET207_TABLE = 'SET207'
SET207_FILE = '../Set207.csv'
ATTRIBUTES = {SAMPLE_TABLE: ['cornellnumber', 'name',
                             'generationdescription', 'sex_male1',
                             'mother', 'father', 'notes'],
              MARKER_TABLE: ['markername', 'MeioticPos', 'DogChr', 'DogPos',
                             'FoxChrSeg', 'FoxChr', 'FoxChrPos'],
              GENOTYPE_TABLE: ['cornellnumber', 'markername', 'genotype1',
                               'genotype2'],
              SET206_TABLE: ['cornellnumber', 'pedigree'],
              SET207_TABLE: ['cornellnumber', 'pedigree']
}
NUM_SAMPLE_COLS = len(ATTRIBUTES[SAMPLE_TABLE])
NUM_GENOTYPE_COLS = len(ATTRIBUTES[GENOTYPE_TABLE])
NUM_MARKER_COLS = len(ATTRIBUTES[MARKER_TABLE])
NUM_SET206_COLS = len(ATTRIBUTES[SET206_TABLE])
NUM_SET207_COLS = len(ATTRIBUTES[SET207_TABLE])

table = "SET206"
pedigree = "ped1"

conn = MySQLdb.connect(db=DB_NAME, host=DB_HOST, passwd=DB_PASSWD,
                           user=DB_USER)
c = conn.cursor()

c.execute("SELECT SET206.cornellnumber, pedigree, mother, motherpedigree, father, fatherpedigree, sex_male1 FROM "+ table +", sample_info_clean WHERE sample_info_clean.cornellnumber= SET206.cornellnumber AND (pedigree = '{0}' OR motherpedigree = '{0}' OR fatherpedigree='{0}')"
          .format(pedigree))

inped = c.fetchall()
allinped = []
I_level = []
II_level = []
III_level = []
grandparent={} #stores mother, father for I-level gen

for fox in inped:
    entry = ','.join([str(i) for i in fox]).split(",")
    for i in range(0,len(entry)):
        if entry[i]=='':
            entry[i]="NULL"
    allinped.append(entry)
    if entry[1]!="NULL": #if this fox was bred
        if entry[3]!="NULL" or entry[5]!="NULL": #if >=1 parent is provided
            II_level.append(entry)
            grandparent[entry[0]]=[entry[2],entry[4]]
        else:
            I_level.append(entry)
    else:
        III_level.append(entry)



conn.commit()
c.close()
conn.close()
