'''Functions for querying, inserting rows, and deleting rows from FoxDB.'''

from flask import flash
import MySQLdb
import csv
import re


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
NUM_SAMPLE_COLS = len(ATTRIBUTES[SAMPLE_TABLE])
NUM_GENOTYPE_COLS = len(ATTRIBUTES[GENOTYPE_TABLE])
NUM_MARKER_COLS = len(ATTRIBUTES[MARKER_TABLE])

def db_query(attributes, where_clause):
    """Returns a string containing a SQL query where the SELECT and FROM
    clauses are determined by the attributes argument and the WHERE clause is
    given by the where_clause argument."""

    #Strip the where_clause, we'll add these portions later DOESN'T WORK!!!!!
    where_clause = re.sub('WHERE ', '', where_clause)
    where_clause = re.sub('where ', '', where_clause)
    where_clause = re.sub('Where ', '', where_clause)
    where_clause = where_clause.rstrip(';').replace('\n', ' ').rstrip()

    sample_all = attributes.pop(0)
    genotype_all = attributes.pop(NUM_SAMPLE_COLS)
    marker_all = attributes.pop(NUM_SAMPLE_COLS + NUM_GENOTYPE_COLS)

    #Handles the "all" switches"
    if sample_all:
        sample_attributes = [True] * NUM_SAMPLE_COLS
    else:
        sample_attributes = attributes[:NUM_SAMPLE_COLS]
    if genotype_all:
        genotype_attributes = [True] * NUM_GENOTYPE_COLS
    else:
        genotype_attributes = attributes[NUM_SAMPLE_COLS:NUM_SAMPLE_COLS +
                                         NUM_GENOTYPE_COLS]
    if marker_all:
        marker_attributes = [True] * NUM_MARKER_COLS
    else:
        marker_attributes = attributes[NUM_SAMPLE_COLS + NUM_GENOTYPE_COLS:]

    #Don't use repeated columns
    if sample_attributes[0]:
        genotype_attributes[0] = False
    if marker_attributes[0]:
        genotype_attributes[1] = False

    #Determines the FROM clause
    use_sample = any(sample_attributes)
    use_genotype = any(genotype_attributes)
    use_marker = any(marker_attributes)

    #Handles an empty query
    if not use_sample and not use_genotype and not use_marker:
        return 1

    #Handles an ill advised query
    if use_sample and not use_genotype and use_marker:
        return 2

    from_query = " FROM"
    if use_sample:
        from_query += ' ' + SAMPLE_TABLE
    if use_genotype:
        if from_query != " FROM":
            from_query += ","
        from_query += ' ' + GENOTYPE_TABLE
    if use_marker:
        if from_query != " FROM":
            from_query += ","
        from_query += ' ' + MARKER_TABLE

    #Determines the SELECT clause
    select_query = "SELECT "
    if use_sample:
        for i in xrange(NUM_SAMPLE_COLS):
            if sample_attributes[i]:
                select_query += (SAMPLE_TABLE + '.' +
                                 ATTRIBUTES[SAMPLE_TABLE][i] + ', ')
    if use_genotype:
        for i in xrange(NUM_GENOTYPE_COLS):
            if genotype_attributes[i]:
                select_query += (GENOTYPE_TABLE + '.' +
                                 ATTRIBUTES[GENOTYPE_TABLE][i] + ', ')
    if use_marker:
        for i in xrange(NUM_MARKER_COLS):
            if marker_attributes[i]:
                select_query += (MARKER_TABLE + '.' +
                                 ATTRIBUTES[MARKER_TABLE][i] + ', ')
    select_query = select_query.rstrip().rstrip(',')

    #Handles WHERE clause
    where_query = ""
    if use_sample and use_genotype:
        where_query += (' WHERE ' + SAMPLE_TABLE + '.' +
                        ATTRIBUTES[SAMPLE_TABLE][0] + '=' + GENOTYPE_TABLE +
                        '.' + ATTRIBUTES[GENOTYPE_TABLE][0])
    if use_genotype and use_marker:
        if where_query != '':
            where_query += " AND"
        else:
            where_query += ' WHERE'
        where_query += (' ' + GENOTYPE_TABLE + '.' +
                        ATTRIBUTES[GENOTYPE_TABLE][1] + '=' +
                        MARKER_TABLE + '.' + ATTRIBUTES[MARKER_TABLE][0])
    if where_clause != '':
        if where_query != '':
            where_query += ' AND'
        else:
            where_query += ' WHERE'
        where_query += ' ' + where_clause

    #Handles GROUP BY clause
    #group_by_query = ''
    #if use_sample:
    #    group_by_query = ("GROUP BY " + SAMPLE_TABLE + '.' +
    #                      ATTRIBUTES[SAMPLE_TABLE][0])
    #elif use_marker:
    #    group_by_query = ("GROUP BY " + MARKER_TABLE + '.' +
    #                      ATTRIBUTES[MARKER_TABLE][0])

    return (select_query + ' ' + from_query + ' ' + where_query + ';')

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

def db_pedigree(attributes):
    """Function for generating the query to produce the pedigree tree."""

    if attributes[0].data == '':
        return 1

    sql_string = ("""SELECT * FROM """ + MARKER_TABLE +
                  """ WHERE markername=""" + attributes[0].data + """;""")
    return sql_string

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
