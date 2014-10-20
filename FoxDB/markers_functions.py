import MySQLdb
import csv

def import_marker_data(csvname):
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor () 
    c.execute ("SELECT VERSION()") 
    row = c.fetchone () 
    print "server version:", row[0]
    
    c.execute("DROP TABLE IF EXISTS markers") #Will want to remove after we initialize db
    c.execute("CREATE TABLE markers(MarkerName VARCHAR(15), MeioticPos VARCHAR(5), DogChr VARCHAR(2), DogPos INTEGER, FoxChrSeg VARCHAR(15), FoxChr CHAR(5), FoxChrPos INTEGER)")#talks to SQL database

    in_name=csvname
    data = list(csv.reader(open(in_name,'r'), delimiter=','))

    header=0
    for line in data:
        if header == 0:
            header=1
        else:
            markername="'" + line[0] + "'"
            MeioticPos="'" + line[1] + "'"
            DogChr="'" + line[2] + "'"
            DogPos=line[3]
            FoxChrSeg="'" + line[4] + "'"
            FoxChr="'" + line[5] + "'"
            FoxChrPos= line[6]
            c.execute("INSERT INTO markers(markername, MeioticPos, DogChr, DogPos, FoxChrSeg, FoxChr, FoxChrPos) VALUES({0},{1},{2},{3},{4},{5},{6})"
                      .format(markername, MeioticPos, DogChr, DogPos, FoxChrSeg, FoxChr, FoxChrPos))
            #"'{0}' is longer than '{1}'".format(name1, name2)

    #c.execute("DROP TABLE IF EXISTS duplicates")
    #c.execute("CREATE TABLE duplicates AS SELECT * FROM sam WHERE qname IN (SELECT qname FROM sam  GROUP BY qname HAVING count(*)>1)")
    conn.commit()
    conn.close()

def insert_marker_data(markername_in, MeioticPos_in, DogChr_in, DogPos_in, FoxChrSeg_in, FoxChr_in, FoxChrPos_in):
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor () 
    c.execute ("SELECT VERSION()") 
    row = c.fetchone () 
    print "server version:", row[0]

    markername="'" + markername_in + "'"
    MeioticPos="'" + MeioticPos_in + "'"
    DogChr="'" + DogChr_in + "'"
    DogPos=DogPos_in
    FoxChrSeg="'" + FoxChrSeg_in + "'"
    FoxChr="'" + FoxChr_in + "'"
    FoxChrPos= FoxChrPos_in
    c.execute("INSERT INTO markers(markername, MeioticPos, DogChr, DogPos, FoxChrSeg, FoxChr, FoxChrPos) VALUES({0},{1},{2},{3},{4},{5},{6})"
              .format(markername, MeioticPos, DogChr, DogPos, FoxChrSeg, FoxChr, FoxChrPos))

    c.execute("SELECT * FROM markers WHERE markername = 'marker1';")
    justadded = c.fetchall()
    for record in justadded:
        allofit = '\t'.join([str(i) for i in record])
        print allofit + '\n'
    conn.commit()
    conn.close()

def delete_marker_data(markername_in):
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor () 
    c.execute ("SELECT VERSION()") 
    row = c.fetchone () 
    print "server version:", row[0]

    markername_del="'" + markername_in + "'"
    c.execute("DELETE FROM markers WHERE markername={0}".format(markername_del))

    c.execute("SELECT * FROM markers WHERE markername = 'marker1';")
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
    
import_marker_data('./markersOct19.csv')
insert_marker_data(markername, MeioticPos, DogChr, DogPos, FoxChrSeg, FoxChr, FoxChrPos)
delete_marker_data(markername)
