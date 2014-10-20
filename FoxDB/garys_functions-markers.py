import MySQLdb

DB_NAME = 'gforema2$foxdb'
DB_HOST = 'mysql.server'
DB_USER = 'gforema2'
DB_PASSWD = 'Genesis411'
SAMPLE_TABLE = 'sample_info_clean'
GENOTYPE_TABLE = 'HasGenotypeAt'
MARKER_TABLE = 'markers'
ATTRIBUTES = {MARKER_TABLE: ['markername', 'meioticpos', 
                             'dogchr', 'dogpos', 
                             'foxchrseg', 'foxchr', 'foxchrpos']
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

def db_update(table, key, attributes):
    """Function for updating attributes of table"""
    set_string = ''
    for i, attribute in enumerate(attributes):
        if attribute.data != '':
            set_string += ATTRIBUTES[table][i] + "="
            if attribute.type != 'RadioField':
                set_string += """'""" + attribute.data + """', """
            else:
                set_string += attribute.data + ", "
    set_string = set_string.rstrip(", ")

    return("""UPDATE """ + table + """ SET """ + set_string + """ WHERE """ + 
           ATTRIBUTES[table][0] + """='""" + key.data + """';""")

def db_delete(table, attributes):
    """Function for deleting a row in table."""

    return("""DELETE FROM """ + table + """ WHERE """ + ATTRIBUTES[table][0] +
           """='%s';""" % (attributes))
