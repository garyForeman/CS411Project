'''Functions for querying, inserting rows, and deleting rows from FoxDB.'''

import MySQLdb


DB_NAME = 'gforema2$foxdb'
DB_HOST = 'mysql.server'
DB_USER = 'gforema2'
DB_PASSWD = 'Genesis411'
SAMPLE_TABLE = 'sample_info_clean'
GENOTYPE_TABLE = 'HasGenotypeAt'
MARKER_TABLE = 'Marker'
ATTRIBUTES = {SAMPLE_TABLE: ['cornellnumber', 'name', 
                             'generationdescription', 'sex_male1', 
                             'mother', 'father', 'notes']
              }

def db_insert(table, attributes):
    """Function for inserting a new row into table"""

    return ("""INSERT INTO """ + table + """ (""" + ATTRIBUTES[table][0] + 
            """) VALUES ('%s');""" % (attributes))

def db_delete(table, attributes):
    """Function for deleting a row in table."""

    return("""DELETE FROM """ + table + """ WHERE """ + ATTRIBUTES[table][0] +
           """='%s';""" % (attributes))
