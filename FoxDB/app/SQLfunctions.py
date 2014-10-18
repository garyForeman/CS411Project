'''Functions for querying, inserting rows, and deleting rows from FoxDB.'''

import MySQLdb


DB_NAME = 'gforema2$foxdb'
DB_HOST = 'mysql.server'
DB_USER = 'gforema2'
DB_PASSWD = 'Genesis411'
SAMPLE_TABLE = 'sample_info_clean'
GENOTYPE_TABLE = 'HasGenotypeAt'
MARKER_TABLE = 'Marker'

def db_insert(table, attributes):
    '''Function for inserting a new row into table'''

    return ("""INSERT INTO """ + table + """ (cornellnumber) VALUES ('%s')""" %
            (attributes))
