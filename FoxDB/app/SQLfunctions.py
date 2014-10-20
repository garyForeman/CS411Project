'''Functions for querying, inserting rows, and deleting rows from FoxDB.'''

import MySQLdb
from flask import flash


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
    list_of_data = []
    for attribute in attributes:
        if attribute.data == '':
            list_of_data.append('NULL')
        elif attribute.type != 'RadioField':
            list_of_data.append("""'""" + attribute.data + """'""")
        else:
            list_of_data.append(attribute.data)

    #for datum in list_of_data:
    #    flash(type(datum))

    attribute_string = ATTRIBUTES[table][0]
    for i in xrange(1, len(attributes)):
        attribute_string += ', ' + ATTRIBUTES[table][i]
     
    #flash(attribute_string)
    #flash(value_string)
    return ("""INSERT INTO """ + table + """ (""" + attribute_string + 
            """) VALUES (%s, %s, %s, %s, %s, %s, %s);""" % 
            tuple(list_of_data))

def db_delete(table, attributes):
    """Function for deleting a row in table."""

    return("""DELETE FROM """ + table + """ WHERE """ + ATTRIBUTES[table][0] +
           """='%s';""" % (attributes))
