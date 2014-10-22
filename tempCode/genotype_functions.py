import MySQLdb
import csv

def import_genotype_data(csvname):
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor () 
    c.execute ("SELECT VERSION()") 
    row = c.fetchone () 
    print "server version:", row[0]
    
    c.execute("DROP TABLE IF EXISTS has_genotype") #Will want to remove after we initialize db
    c.execute("CREATE TABLE has_genotype(cornellnumber VARCHAR(15), markername VARCHAR(15), genotype1 INTEGER, genotype2 INTEGER)")#talks to SQL database
    c.execute("ALTER TABLE has_genotype ADD PRIMARY KEY (cornellnumber, markername)")
    #c.execute("ALTER TABLE has_genotype ADD FOREIGN KEY (cornellnumber) REFERENCES Samples(cornellnumber)")
    c.execute("ALTER TABLE has_genotype ADD FOREIGN KEY (markername) REFERENCES markers(MarkerName)")

    in_name=csvname
    data = list(csv.reader(open(in_name,'r'), delimiter=','))
    
    header=0
    for line in data:
        if header == 0:
            header=1
        else:
            cornellnumber="'" + line[0] + "'"
            MarkerName="'" + line[1] + "'"
            genotype1 = int(line[2])
            genotype2 = int(line[3])
            c.execute("INSERT INTO has_genotype(cornellnumber, markername, genotype1, genotype2) VALUES({0},{1},{2},{3})"
                      .format(cornellnumber, MarkerName, genotype1, genotype2))
            #"'{0}' is longer than '{1}'".format(name1, name2)

    #c.execute("DROP TABLE IF EXISTS duplicates")
    #c.execute("CREATE TABLE duplicates AS SELECT * FROM sam WHERE qname IN (SELECT qname FROM sam  GROUP BY qname HAVING count(*)>1)")

    conn.commit()
    conn.close()

def insert_genotype_data(cornellnumber_in, markername_in, genotype1_in, genotype2_in):
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor () 
    c.execute ("SELECT VERSION()") 
    row = c.fetchone () 
    print "server version:", row[0]

    cornellnumber="'" + cornellnumber_in + "'"
    MarkerName="'" + markername_in + "'"
    genotype1=genotype1_in
    genotype2=genotype2_in

    c.execute("INSERT INTO has_genotype(cornellnumber, markername, genotype1, genotype2) VALUES({0},{1},{2},{3})"
              .format(cornellnumber, MarkerName, genotype1, genotype2))

    c.execute("SELECT * FROM has_genotype WHERE markername = 'marker1';")
    justadded = c.fetchall()
    for record in justadded:
        allofit = '\t'.join([str(i) for i in record])
        print allofit + '\n'
    conn.commit()
    conn.close()

def update_genotype_data(cornellnumber_in, markername_in, genotype1_in, genotype2_in):
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor () 
    c.execute ("SELECT VERSION()") 
    row = c.fetchone () 
    print "server version:", row[0]

    allattributes = {'cornellnumber': "'" + str(cornellnumber_in) + "'", 'markername': "'" + str(markername_in) + "'", 'genotype1': int(genotype1_in),
                     'genotype2': int(genotype2_in)}

    SQLstring = "UPDATE has_genotype SET "
    for attribute in allattributes.keys():
        if attribute != 'markername' and attribute != 'cornellnumber': #I'm not letting this function change the primary key
            if allattributes[attribute]!= "": #or however we end up representing NULL with flask
                if SQLstring != "UPDATE has_genotype SET ": #if it's not the first one
                    SQLstring += ", " # need to separate from previous attribute
                SQLstring += attribute + "=" + str(allattributes[attribute]) # add this attribute-value pair to function
    SQLstring += " WHERE markername = " + allattributes["markername"] + " AND cornellnumber = " + allattributes["cornellnumber"]
    c.execute(SQLstring)

    c.execute("SELECT * FROM has_genotype WHERE markername = 'marker1';")
    justadded = c.fetchall()
    for record in justadded:
        allofit = '\t'.join([str(i) for i in record])
        print allofit + '\n'
    conn.commit()
    conn.close()

def delete_genotype_data(cornellnumber_in, markername_in):
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor () 
    c.execute ("SELECT VERSION()") 
    row = c.fetchone () 
    print "server version:", row[0]

    markername_del="'" + markername_in + "'"
    cornellnumb_del = "'" + cornellnumber_in + "'"
    
    c.execute("DELETE FROM has_genotype WHERE cornellnumber = {0} AND markername={1}".format(cornellnumb_del, markername_del))

    c.execute("SELECT * FROM has_genotype WHERE cornellnumber = {0} AND markername={1}".format(cornellnumb_del, markername_del))
    justadded = c.fetchall()
    for record in justadded:
        allofit = '\t'.join([str(i) for i in record])
        print allofit + '\n'
    conn.commit()
    conn.close()


markername="marker1"
MeioticPos = '13.5'
DogChr = '1'
DogPos = 283482934
FoxChrSeg = 'VVU1.4'
FoxChr = 'VVU1'
FoxChrPos = 283478923
    
#import_genotype_data('./genotypesOct19.csv')
#insert_genotype_data('F0000', 'marker1', 134, 134)
update_genotype_data('F0000', 'marker1', 334, 334)
#delete_genotype_data('F0000', 'marker1')
