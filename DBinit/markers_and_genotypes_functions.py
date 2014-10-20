import MySQLdb
import csv

def import_marker_data(csvname): #initialize our DB from csv files
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor () 

    c.execute("DROP TABLE IF EXISTS markers") #Will want to remove after we initialize db first time
    c.execute("CREATE TABLE markers(MarkerName VARCHAR(15), MeioticPos VARCHAR(5), DogChr VARCHAR(2), DogPos INTEGER, FoxChrSeg VARCHAR(15), FoxChr CHAR(5), FoxChrPos INTEGER)")#talks to SQL database
    c.execute("ALTER TABLE markers ADD PRIMARY KEY (MarkerName)")
    
    in_name=csvname
    data = list(csv.reader(open(in_name,'r'), delimiter=','))

    header=0
    for line in data:
        if header == 0:
            header=1 #skips the header row
        else: # goes through and formats according to TYPE above
            markername="'" + line[0] + "'"
            MeioticPos="'" + line[1] + "'"
            DogChr="'" + line[2] + "'"
            DogPos=line[3]
            FoxChrSeg="'" + line[4] + "'"
            FoxChr="'" + line[5] + "'"
            FoxChrPos= line[6]
            c.execute("INSERT INTO markers(markername, MeioticPos, DogChr, DogPos, FoxChrSeg, FoxChr, FoxChrPos) VALUES({0},{1},{2},{3},{4},{5},{6})"
                      .format(markername, MeioticPos, DogChr, DogPos, FoxChrSeg, FoxChr, FoxChrPos))

    conn.commit()
    conn.close()

def import_genotype_data(csvname):
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor () 
    
    c.execute("DROP TABLE IF EXISTS has_genotype") #Will want to remove after we initialize db
    c.execute("CREATE TABLE has_genotype(cornellnumber VARCHAR(15), markername VARCHAR(15), genotype1 INTEGER, genotype2 INTEGER)")#talks to SQL database
    c.execute("ALTER TABLE has_genotype ADD PRIMARY KEY (cornellnumber, markername)")
    #c.execute("ALTER TABLE has_genotype ADD FOREIGN KEY (cornellnumber) REFERENCES Samples(cornellnumber)") #activate this once we've integrated with Gary's
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

    conn.commit()
    conn.close()

def insert_marker_data(markername_in, MeioticPos_in, DogChr_in, DogPos_in, FoxChrSeg_in, FoxChr_in, FoxChrPos_in):
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor () 

    markername="'" + str(markername_in) + "'"
    MeioticPos="'" + str(MeioticPos_in) + "'"
    DogChr="'" + str(DogChr_in) + "'"
    DogPos= int(DogPos_in)
    FoxChrSeg="'" + str(FoxChrSeg_in) + "'"
    FoxChr="'" + str(FoxChr_in) + "'"
    FoxChrPos= int(FoxChrPos_in)
    c.execute("INSERT INTO markers(markername, MeioticPos, DogChr, DogPos, FoxChrSeg, FoxChr, FoxChrPos) VALUES({0},{1},{2},{3},{4},{5},{6})"
              .format(markername, MeioticPos, DogChr, DogPos, FoxChrSeg, FoxChr, FoxChrPos))

    c.execute("SELECT * FROM markers WHERE markername = 'marker1';") #check that it was added
    justadded = c.fetchall()
    for record in justadded:
        allofit = '\t'.join([str(i) for i in record]) #returns as \t-separated list
        print allofit + '\n'
    conn.commit()
    conn.close()

def insert_genotype_data(cornellnumber_in, markername_in, genotype1_in, genotype2_in):
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor () 

    cornellnumber="'" + str(cornellnumber_in) + "'"
    MarkerName="'" + str(markername_in) + "'"
    genotype1=int(genotype1_in)
    genotype2=int(genotype2_in)

    c.execute("INSERT INTO has_genotype(cornellnumber, markername, genotype1, genotype2) VALUES({0},{1},{2},{3})"
              .format(cornellnumber, MarkerName, genotype1, genotype2))

    c.execute("SELECT * FROM has_genotype WHERE markername = 'marker1';")#check that it was added
    justadded = c.fetchall()
    for record in justadded:
        allofit = '\t'.join([str(i) for i in record]) #returns as \t-separated list
        print allofit + '\n'
    conn.commit()
    conn.close()

def update_marker_data(markername_in, MeioticPos_in, DogChr_in, DogPos_in, FoxChrSeg_in, FoxChr_in, FoxChrPos_in):
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor () 

    allattributes = {'markername': "'" + str(markername_in) + "'", 'MeioticPos':"'" + str(MeioticPos_in) + "'", 'DogChr': "'" + str(DogChr_in) + "'" ,
                     'DogPos': int(DogPos_in), 'FoxChrSeg': "'" + str(FoxChrSeg_in) + "'", 'FoxChr': "'" + str(FoxChr_in) + "'" , 'FoxChrPos': int(FoxChrPos_in)}

    SQLstring = "UPDATE markers SET "
    for attribute in allattributes.keys():
        if attribute != 'markername': #I'm not letting this function change the primary key, but I can modify this if we want
            if allattributes[attribute]!= "": #or however we end up representing NULL with flask
                if SQLstring != "UPDATE markers SET ": #if it's not the first one
                    SQLstring += ", " # need to separate from previous attribute
                SQLstring += attribute + "=" + str(allattributes[attribute]) # add this attribute-value pair to function
    SQLstring += " WHERE markername = " + allattributes["markername"]
    c.execute(SQLstring)

    c.execute("SELECT * FROM markers WHERE markername = 'marker1';")
    justadded = c.fetchall()
    for record in justadded:
        allofit = '\t'.join([str(i) for i in record])
        print allofit + '\n'
    conn.commit()
    conn.close()

def update_genotype_data(cornellnumber_in, markername_in, genotype1_in, genotype2_in):
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor ()
    
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

def delete_marker_data(markername_in):
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor () 

    markername_del="'" + str(markername_in) + "'"
    c.execute("DELETE FROM markers WHERE markername={0}".format(markername_del))#check whether it's still there

    c.execute("SELECT * FROM markers WHERE markername = 'marker1';")
    justadded = c.fetchall()
    for record in justadded:
        allofit = '\t'.join([str(i) for i in record])
        print allofit + '\n' #should be nothing
    conn.commit()
    conn.close()

def delete_genotype_data(cornellnumber_in, markername_in):
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
    c = conn.cursor () 

    markername_del="'" + str(markername_in) + "'"
    cornellnumb_del = "'" + str(cornellnumber_in) + "'"
    
    c.execute("DELETE FROM has_genotype WHERE cornellnumber = {0} AND markername={1}".format(cornellnumb_del, markername_del))

    c.execute("SELECT * FROM has_genotype WHERE cornellnumber = {0} AND markername={1}".format(cornellnumb_del, markername_del))
    justadded = c.fetchall()
    for record in justadded:
        allofit = '\t'.join([str(i) for i in record]) #should return blank
        print allofit + '\n'
    conn.commit()
    conn.close()
