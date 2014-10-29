"""Dummy Variables"""
sample_all = bool(0)
genotype_all = bool(1)
marker_all = bool(1)

"""HTML NEEDS TO LINK INTO THESE VARIABLES"""

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

where_clause = "WHERE FoxChr='VVU12'"
where_temp = where_clause.lstrip('WHERE ')
where_temp = where_temp.lstrip('where ')
where_temp = where_temp.lstrip('Where ')
where_temp = where_temp.rstrip(';')
where_clause = where_temp

if sample_all == bool(1):
    for variable in sample_var.keys():
        sample_var[variable] = bool(1)

if genotype_all == bool(1):
    for variable in genotype_var.keys():
        genotype_var[variable] = bool(1)

if marker_all == bool(1):
    for variable in marker_var.keys():
        marker_var[variable] = bool(1)

usesample = any(sample_var.values())
usegenotype = any(genotype_var.values())
usemarkers = any(marker_var.values())

"""DRAWS FROM SQL"""
#from flask import flash
import MySQLdb
import csv


DB_NAME = 'gforema2$foxdb'
DB_HOST = 'mysql.server'
DB_USER = 'gforema2'
DB_PASSWD = 'Genesis411'
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

htmltosql = {'sample_sample_id': "sample_info_clean." + ATTRIBUTES[SAMPLE_TABLE][0],
             'sample_name': ATTRIBUTES[SAMPLE_TABLE][1],
             'sample_generation': ATTRIBUTES[SAMPLE_TABLE][2], 'sample_sex': ATTRIBUTES[SAMPLE_TABLE][3],
             'sample_mother': ATTRIBUTES[SAMPLE_TABLE][4], 'sample_father': ATTRIBUTES[SAMPLE_TABLE][5],
             'sample_notes': ATTRIBUTES[SAMPLE_TABLE][6],
             'genotype_sample_id': "has_genotype." + ATTRIBUTES[GENOTYPE_TABLE][0],
             'genotype_marker_id': "has_genotype." + ATTRIBUTES[GENOTYPE_TABLE][1],
             'genotype_genotype1': ATTRIBUTES[GENOTYPE_TABLE][2],
             'genotype_genotype2': ATTRIBUTES[GENOTYPE_TABLE][3],
             'marker_marker_id': "markers." + ATTRIBUTES[MARKER_TABLE][0],
             'marker_meiotic_pos': ATTRIBUTES[MARKER_TABLE][1], 'marker_dog_chrom': ATTRIBUTES[MARKER_TABLE][2],
             'marker_dog_pos': ATTRIBUTES[MARKER_TABLE][3], 'marker_fox_seg': ATTRIBUTES[MARKER_TABLE][4],
             'marker_fox_chrom': ATTRIBUTES[MARKER_TABLE][5], 'marker_fox_pos': ATTRIBUTES[MARKER_TABLE][6]}

"""str_types = ['sample_sample_id','sample_name', 'sample_generation',
'sample_mother', 'sample_father', 'sample_notes',
'genotype_sample_id', 'genotype_marker_id', 'marker_marker_id',
'marker_meiotic_pos', 'marker_dog_chrom', 'marker_fox_seg',
'marker_fox_chrom']"""

selectquery = "SELECT "
if usesample == bool(1) and usegenotype==bool(1):
    genotype_var['genotype_sample_id']=bool(1)
    sample_var['sample_sample_id'] = bool(0)
if usemarkers == bool(1) and usegenotype==bool(1):
    genotype_var['genotype_marker_id']=bool(1)
    marker_var['marker_marker_id'] = bool(0)

all_varlists = [sample_var, genotype_var, marker_var]
for varlist in all_varlists:
    for varkey in varlist.keys():
        if varlist[varkey] == bool(1):
            if selectquery != "SELECT ":
                selectquery += ", "
            selectquery += htmltosql[varkey]

fromquery = " FROM"
if usesample == bool(1):
    fromquery += " sample_info_clean"
if usegenotype == bool(1):
    if fromquery != " FROM":
        fromquery += ","
    fromquery += " has_genotype"
if usemarkers == bool(1):
    if fromquery != " FROM":
        fromquery += ","
    fromquery += " markers"

wherequery = " WHERE"
if usesample == bool(1) and usemarkers == bool(1):
    if usegenotype != bool(1):
        print "ERROR" #How do we actually want to handle this?
if usesample == bool(1) and usegenotype == bool(1):
    wherequery += " sample_info_clean.cornellnumber = has_genotype.cornellnumber"
if usegenotype == bool(1) and usemarkers == bool(1):
    if wherequery != " WHERE":
        wherequery += " AND"
    wherequery += " markers.markername = has_genotype.markername"
if where_clause != "":
    if wherequery != " WHERE":
        wherequery += " AND"
    wherequery += " " + where_clause

groupbyquery = "GROUP BY"
if sample_var['sample_sample_id']==bool(1) or genotype_var['genotype_sample_id']==bool(1):
    groupbyquery += " has_genotype.cornellnumber"
elif marker_var['marker_marker_id']==bool(1) or genotype_var['genotype_marker_id']==bool(1):
    groupbyquery += " has_genotype.markername"


query = selectquery + " " + fromquery + " " + wherequery
if groupbyquery != "GROUP BY":
    query += " " + groupbyquery + ";"
else:
    query += ";"

print query
"""conn = MySQLdb.connect(db=DB_NA ME, host=DB_HOST, passwd=DB_PASSWD,
user=DB_USER)"""

conn = MySQLdb.connect(db="foxdb", host="localhost", passwd="foxdb@CS411",
                       user="root")
c = conn.cursor()

c.execute(query)
test=c.fetchone()

conn.commit()
c.close()
