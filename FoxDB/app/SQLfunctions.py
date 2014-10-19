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
    list_of_data = []
    for attribute in attributes:
        if attribute.data == '':
            list_of_data.append('NULL')
        elif attribute.type != 'RadioField':
            list_of_data.append("""'""" + attribute.data + """'""")

    attribute_string = '';
    value_string = '';
    for i in xrange(len(attributes-1)):
        attribute_string += ATTRIBUTES[table][i] + ', '
        value_string += '%s, '
    attribute_string += ATTRIBUTES[table][len(attributes)-1]
    value_string += '%s'
            
    return ("""INSERT INTO """ + table + """ (""" + attribute_string + 
            """) VALUES (""" + value_string + """);""" % 
            tuple(list_of_data))

def db_delete(table, attributes):
    """Function for deleting a row in table."""

    return("""DELETE FROM """ + table + """ WHERE """ + ATTRIBUTES[table][0] +
           """='%s';""" % (attributes))
