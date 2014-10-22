'''Functions for querying, inserting rows, and deleting rows from FoxDB.'''

from flask import flash
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
                               'genotype2']
}

def db_insert(table, attributes):
    """Function for inserting a new row into table. Note if you ever change
    the schema, you need to change the number of '%s' that appear in the
    return string!!"""
    list_of_data = []
    for attribute in attributes:
        if attribute.data == '' or attribute.data == None:
            list_of_data.append('NULL')
        elif (attribute.type == 'StringField' or
              attribute.type == 'TextAreaField'):
            list_of_data.append("""'""" + attribute.data + """'""")
        elif attribute.type == 'RadioField':
            list_of_data.append(attribute.data)
        else:
            list_of_data.append(str(attribute.data))

    attribute_string = ATTRIBUTES[table][0]
    for i in xrange(1, len(attributes)):
        attribute_string += ', ' + ATTRIBUTES[table][i]

    sql_string = ("""INSERT INTO """ + table + """ (""" + attribute_string +
                  """) VALUES (""")

    if table == SAMPLE_TABLE:
        return (sql_string + """%s, %s, %s, %s, %s, %s, %s);""" %
                tuple(list_of_data))
    elif table == MARKER_TABLE:
        return (sql_string + """%s, %s, %s, %s, %s, %s, %s);""" %
                tuple(list_of_data))
    elif table == GENOTYPE_TABLE:
        return sql_string + """%s, %s, %s, %s);""" % tuple(list_of_data)

def db_update(table, key, attributes):
    """Function for updating attributes of table. Note key will be a list for
    genotype table which has more than one key attribute."""
    set_string = ''
    for i, attribute in enumerate(attributes):
        if attribute.data != '' and attribute.data != None:
            set_string += ATTRIBUTES[table][i] + "="
            if (attribute.type == 'StringField' or
                attribute.type == 'TextAreaField'):
                set_string += """'""" + attribute.data + """', """
            elif attribute.type == 'RadioField':
                set_string += attribute.data + ", "
            else:
                set_string += str(attribute.data) + ", "
    set_string = set_string.rstrip(", ")

    sql_string = ("""UPDATE """ + table + """ SET """ + set_string +
                  """ WHERE """)

    if table == SAMPLE_TABLE or table == MARKER_TABLE:
        return(sql_string + ATTRIBUTES[table][0] + """='""" +
               key.data + """';""")
    elif table == GENOTYPE_TABLE:
        return(sql_string + ATTRIBUTES[table][0] + """='""" +
               key[0].data + """' AND """ + ATTRIBUTES[table][1] + """='""" +
               key[1].data + """';""")

def db_delete(table, key):
    """Function for deleting a row in table. Note key will be a list for
    genotype table which has more than one key attribute."""

    sql_string = """DELETE FROM """ + table + """ WHERE """

    if table == SAMPLE_TABLE or table == MARKER_TABLE:
        return sql_string + ATTRIBUTES[table][0] + """='%s';""" % (key)
    elif table == GENOTYPE_TABLE:
        return(sql_string + ATTRIBUTES[table][0] + """='%s' AND """ % key[0] +
               ATTRIBUTES[table][1] + """='%s';""" % key[1])

def import_data(table, csvname):
    """Function to declare table and initalize it with values from csvfile"""

    conn = MySQLdb.connect(db=DB_NAME, host=DB_HOST, passwd=DB_PASSWD,
                           user=DB_USER)
    c = conn.cursor()
    c.execute("""DROP TABLE IF EXISTS """ + table)

    if table == MARKER_TABLE:
        c.execute("""CREATE TABLE """ + table + """(""" +
                  ATTRIBUTES[table][0] + """ VARCHAR(15) PRIMARY KEY, """ +
                  ATTRIBUTES[table][1] + """ VARCHAR(5), """ +
                  ATTRIBUTES[table][2] + """ VARCHAR(2), """ +
                  ATTRIBUTES[table][3] + """ INTEGER, """ +
                  ATTRIBUTES[table][4] + """ VARCHAR(15), """ +
                  ATTRIBUTES[table][5] + """ VARCHAR(15), """ +
                  ATTRIBUTES[table][6] + """ INTEGER);""")

        data = list(csv.reader(open(csvname, 'r'), delimiter=','))

        for line in data[1:]:
            markername = "'" + line[0] + "'"
            MeioticPos = "'" + line[1] + "'"
            DogChr = "'" + line[2] + "'"
            DogPos = line[3]
            FoxChrSeg = "'" + line[4] + "'"
            FoxChr = "'" + line[5] + "'"
            FoxChrPos = line[6]
            c.execute("INSERT INTO markers(markername, MeioticPos, " +
                      "DogChr, DogPos, FoxChrSeg, FoxChr, FoxChrPos) " +
                      "VALUES({0},{1},{2},{3},{4},{5},{6});"
                      .format(markername, MeioticPos, DogChr, DogPos,
                              FoxChrSeg, FoxChr, FoxChrPos))
    elif table == SAMPLE_TABLE:
        c.execute("""CREATE TABLE """ + table + """(""" +
                  ATTRIBUTES[table][0] + """ VARCHAR(8) PRIMARY KEY, """ +
                  ATTRIBUTES[table][1] + """ VARCHAR(20), """ +
                  ATTRIBUTES[table][2] + """ VARCHAR(9), """ +
                  ATTRIBUTES[table][3] + """ INTEGER, """ +
                  ATTRIBUTES[table][4] + """ VARCHAR(8), """ +
                  ATTRIBUTES[table][5] + """ VARCHAR(8), """ +
                  ATTRIBUTES[table][6] + """ VARCHAR(255));""")

        data = list(csv.reader(open(csvname, 'r'), delimiter=','))

        for line in data[1:]:
            cornellnumber = "'" + line[0].replace('"', '') + "'"
            name = "'" + line[1].replace('"', '') + "'"
            generation = "'" + line[2].replace('"', '') + "'"
            sex = line[3].replace('"', '')
            mother = "'" + line[4].replace('"', '') + "'"
            father = "'" + line[5].replace('"', '') + "'"
            notes = "'" + line[6].replace('"', '') + "'"
            c.execute("INSERT INTO sample_info_clean(cornellnumber, name, " +
                      "generationdescription, sex_male1, mother, father, " +
                      "notes) VALUES({0}, {1}, {2}, {3}, {4}, {5}, {6});"
                      .format(cornellnumber, name, generation, sex, mother,
                              father, notes))
    elif table == GENOTYPE_TABLE:
        c.execute("""CREATE TABLE """ + table + """(""" +
                  ATTRIBUTES[table][0] + """ VARCHAR(8), """+
                  ATTRIBUTES[table][1] + """ VARCHAR(15), """ +
                  ATTRIBUTES[table][2] + """ INTEGER, """ +
                  ATTRIBUTES[table][3] + """ INTEGER,""" +
                  """PRIMARY KEY (""" + ATTRIBUTES[table][0] + """, """ +
                  ATTRIBUTES[table][1] + """),""" +
                  """FOREIGN KEY (""" + ATTRIBUTES[table][0] + """) """ +
                  """REFERENCES """ + SAMPLE_TABLE + """(""" + 
                  ATTRIBUTES[SAMPLE_TABLE][0] + 
                  """) ON DELETE CASCADE ON UPDATE CASCADE, """ +
                  """FOREIGN KEY (""" + ATTRIBUTES[table][1] + """) """ +
                  """REFERENCES """ + MARKER_TABLE + """(""" + 
                  ATTRIBUTES[MARKER_TABLE][0] +
                  """) ON DELETE CASCADE ON UPDATE CASCADE);""")

        data = list(csv.reader(open(csvname, 'r'), delimiter=','))

        for line in data[1:]:
            cornellnumber = "'" + line[0].replace('"', '') + "'"
            markername = "'" + line[1].replace('"', '') + "'"
            genotype1 = line[2].replace('"', '')
            genotype2 = line[3].replace('"', '')
            c.execute("""INSERT INTO has_genotype(cornellnumber, """ +
                      """markername, genotype1, genotype2) """ +
                      """VALUES({0}, {1}, {2}, {3});"""
                      .format(cornellnumber, markername, genotype1, genotype2))

    conn.commit()
    c.close()
    conn.close()

if __name__ == '__main__':
    import_data(MARKER_TABLE, MARKER_FILE)
    import_data(SAMPLE_TABLE, SAMPLE_FILE)
    import_data(GENOTYPE_TABLE, GENOTYPE_FILE)
