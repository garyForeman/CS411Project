import MySQLdb
import csv

def openconn():
    conn = MySQLdb.connect (host = "localhost", user = "root",
                            passwd = "foxdb@CS411", db = "foxdb")
    c = conn.cursor ()
    return c, conn

def init(c):
    c.execute("SHOW TABLES")
    tables = c.fetchall()

    alltables = []
    for table in tables:
        alltables.append('\t'.join([str(i) for i in table]))
    if "questionable" in alltables:
        c.execute("DROP TABLE IF EXISTS questionable;")
        
    c.execute("""CREATE TABLE IF NOT EXISTS questionable(cornellnumber VARCHAR(15),"""+
              """markername VARCHAR(15),genotype1 INTEGER, genotype2 INTEGER,"""+
              """mateID VARCHAR(50), mate_gen1 INTEGER, mate_gen2 INTEGER,"""+
              """os_ID VARCHAR(50), os_gen1 INTEGER, os_gen2 INTEGER,"""+
              """PRIMARY KEY (markername, os_ID));""")

    if "checked" in alltables:
        c.execute("DROP TABLE IF EXISTS checked;")
    c.execute("CREATE TABLE checked(cornellnumber VARCHAR(15), markername VARCHAR(15), checkedas VARCHAR(50), PRIMARY KEY(cornellnumber, markername));")


    if "duds" in alltables:
        c.execute("DROP TABLE IF EXISTS duds;")
        
    c.execute("""CREATE TABLE IF NOT EXISTS duds(cornellnumber VARCHAR(15),"""+
              """markername VARCHAR(15),genotype1 INTEGER, genotype2 INTEGER,"""+
              """PRIMARY KEY (cornellnumber, markername));""")

def findmates(cornellnumber, sex):
    if sex == "1": #if male
        c.execute("SELECT DISTINCT mother FROM sample_info_clean WHERE father = {0};"
                  .format("'"+cornellnumber+"'"))
        mates_raw = c.fetchall()
    else: #if female
        c.execute("SELECT DISTINCT father FROM sample_info_clean WHERE mother = {0};"
                  .format("'"+cornellnumber+"'"))
        mates_raw = c.fetchall()

    if len(mates_raw) == 0:
        return []
    else:
        mates = []
        for mate in mates_raw:
            mates.append(','.join(str(i) for i in mate))

        return mates

def findgenotypes(cornellnumber, marker):
    if marker == "NULL":
        c.execute("SELECT markername, genotype1, genotype2 FROM has_genotype WHERE cornellnumber = {0};".format("'"+cornellnumber+"'"))
        all_genotypes_raw = c.fetchall()
        if len(all_genotypes_raw) == 0:
            return 0
        all_genotypes = []
        for genpair in all_genotypes_raw:
            all_genotypes.append(','.join(str(i) for i in genpair).split(","))

        return all_genotypes
    else:
        c.execute("SELECT genotype1, genotype2 FROM has_genotype WHERE cornellnumber = {0} and markername = {1};"
                    .format("'"+cornellnumber+"'", "'"+marker+"'"))
        x = c.fetchone()
        if x == None:
            return 0
        else:
            genotype = ','.join(str(i) for i in x).split(",")
            return genotype
                   
def findoffspring(primary, sex, mate, marker):
    if sex == "1":
        c.execute("""SELECT S.cornellnumber, genotype1, genotype2 FROM sample_info_clean AS S, has_genotype AS G WHERE S.cornellnumber=G.cornellnumber AND """+
                  """father={0} AND mother={1} AND markername = {2};""".format("'"+primary+"'", "'"+mate+"'", "'"+marker+"'"))
        offspring_gen_raw = c.fetchall()
        
    else:
        c.execute("""SELECT S.cornellnumber, genotype1, genotype2 FROM sample_info_clean AS S, has_genotype AS G WHERE S.cornellnumber=G.cornellnumber AND """+
                  """mother={0} AND father={1} AND markername = {2};""".format("'"+primary+"'", "'"+mate+"'", "'"+marker+"'"))
        offspring_gen_raw = c.fetchall()
        
    if offspring_gen_raw == None:
        return 0
    else:
        offsprings_gens=[]
        for genpair in offspring_gen_raw:
            offsprings_gens.append(','.join(str(i) for i in genpair).split(",")) 

        return offsprings_gens

def findvalid(this_gen, mate_gen):
    all_valid = [
    [this_gen[0], mate_gen[0]],
    [this_gen[0], mate_gen[1]],
    [this_gen[1], mate_gen[0]],
    [this_gen[1], mate_gen[1]]]

    return all_valid


def closeconn(conn):
    conn.commit()
    conn.close()

def nextgen(c, tocheck_raw):
    tocheck = []
    for line in tocheck_raw:
        tocheck.append(','.join([str(i) for i in line]).split(","))
    
    for sample in tocheck: #for each cornellnumber
        (cornellnumber, sex) = sample[0:2]

        mates = findmates(cornellnumber, sex) #get a list of everyone it mated with
        if len(mates) == 0: #if it doesn't have mates, it's an offspring (level III). need to make sure it's been checked
            c.execute("SELECT * FROM checked WHERE cornellnumber='{0}';".format(cornellnumber))
            if len(c.fetchall())>0:
                continue
            
            c.execute("SELECT * FROM questionable WHERE os_ID='{0}';".format(cornellnumber))
            if len(c.fetchall()) > 0:
                continue

            c.execute("SELECT * FROM duds WHERE cornellnumber='{0}';".format(cornellnumber))
            if len(c.fetchall()) > 0:
                continue
        
            c.execute("SELECT mother, father FROM sample_info_clean WHERE cornellnumber='{0}';".format(cornellnumber))
            [mother, father] = ','.join([str(i) for i in c.fetchone()]).split(",") #must have a row in the table

            all_genotypes = findgenotypes(cornellnumber, "NULL")
            if all_genotypes == 0:
                print "No genotypes" #this shouldn't happen, except for "ped" fillers
                continue

            for genotype in all_genotypes: #for this sample, at each marker
                marker= genotype[0]
                this_gen = genotype[1:3]

                if this_gen == ['0','0']: #if we have no data at this marker, tally it as a dud and skip to next marker
                    c.execute("SELECT * FROM duds WHERE cornellnumber = '{0}' AND markername = '{1}';".format(cornellnumber, marker))
                    if c.fetchone() == None:
                        c.execute("INSERT INTO duds VALUES({0},{1},{2},{3});"
                                  .format("'"+cornellnumber+"'","'"+marker+"'",this_gen[0], this_gen[1]))
                    continue

                if mother != "ped37dam" and mother != "NULL": 
                    c.execute("SELECT genotype1, genotype2 FROM has_genotype WHERE cornellnumber='{0}' and markername ='{1}';".format(mother, marker))
                    mother_gen = ','.join([str(i) for i in c.fetchone()]).split(",") #tuple of mother's genotype
                else: #if we don't know anything about the mother
                    mother_gen = ['0','0']
                
                if father != "ped8sire" and father != "NULL":
                    c.execute("SELECT genotype1, genotype2 FROM has_genotype WHERE cornellnumber='{0}' and markername ='{1}';".format(father, marker))
                    father_gen = ','.join([str(i) for i in c.fetchone()]).split(",") #tuple of father's genotype
                else: #if we don't know anything about the father
                    father_gen = ['0','0']

                if this_gen[0]=='0': #if this sample's first allele is empty
                    if this_gen[1] in mother_gen or this_gen[1] in father_gen: #just check the second one
                        c.execute("INSERT INTO checked VALUES({0},{1},'focus');".format("'"+cornellnumber+"'","'"+marker+"'"))
                elif this_gen[1]=='0': #vice versa if the second allele is empty
                    if this_gen[0] in mother_gen or this_gen[0] in father_gen:
                        c.execute("INSERT INTO checked VALUES({0},{1},'focus');".format("'"+cornellnumber+"'","'"+marker+"'"))                    
                elif mother_gen != ['0','0'] and father_gen != ['0','0']: #if it's just a normal case
                    possibilities = findvalid(mother_gen, father_gen) #all 4 possible arrangements of parental alleles
                    
                    if this_gen in possibilities or [this_gen[1], this_gen[0]] in possibilities: #look for either order
                        c.execute("INSERT INTO checked VALUES({0},{1},'focus');".format("'"+cornellnumber+"'","'"+marker+"'"))
                    else:#if neither order is found, potential error
                        c.execute("INSERT INTO questionable VALUES({0},{1},{2},{3},{4},{5},{6},{7},{8},{9});"
                                  .format("'"+mother+"'","'"+marker+"'",mother_gen[0], mother_gen[1], "'"+father+"'",father_gen[0],
                                                  father_gen[1], "'"+cornellnumber+"'", this_gen[0], this_gen[1]))
                elif mother_gen == ['0','0']:
                    if this_gen[0] in father_gen or this_gen[1] in father_gen:
                        c.execute("INSERT INTO checked VALUES({0},{1},'focus');".format("'"+cornellnumber+"'","'"+marker+"'"))                    
                elif father_gen == ['0','0']:
                    if this_gen[0] in mother_gen or this_gen[1] in mother_gen:
                        c.execute("INSERT INTO checked VALUES({0},{1},'focus');".format("'"+cornellnumber+"'","'"+marker+"'"))                    

        """Assuming it does have mates, i.e. level I or II"""
        all_genotypes = findgenotypes(cornellnumber, "NULL") #pull all the genotypes for this cornellnumber
        if all_genotypes == 0: #shouldn't happen except for "ped"
            #print "No genotypes"
            continue
        for genotype in all_genotypes: #for each marker, gen1, gen2 set
            marker= genotype[0]
            this_gen = genotype[1:3]
            
            if this_gen == ['0','0']: #if no data, add to duds and skip
                c.execute("SELECT * FROM duds WHERE cornellnumber = '{0}' AND markername = '{1}';".format(cornellnumber, marker))
                if c.fetchone() == None:
                    c.execute("INSERT INTO duds VALUES({0},{1},{2},{3});"
                              .format("'"+cornellnumber+"'","'"+marker+"'",this_gen[0], this_gen[1]))
                continue

            
            founderror = 0 #tracks number of potential errors per offspring with single mate
            noerror = 0 #tracks number of non-errors per offspring with single mate
                
            for mate in mates: #going through each of this sample's mates
                if mate == "NULL" or mate == "ped37dam" or mate == "ped8sire":#mate isn't really known
                    offsprings_gens = findoffspring(cornellnumber, sex, mate, marker)
                    if offsprings_gens == 0:
                        continue #but this should never happen
                            
                    for offspring_gen_info in offsprings_gens:
                        os_ID = offspring_gen_info[0]
                        offspring_gen = offspring_gen_info[1:3]
                        
                        if offspring_gen == ['0','0']: #if it failed
                            c.execute("SELECT * FROM duds WHERE cornellnumber = '{0}' AND markername = '{1}';".format(os_ID, marker))
                            if c.fetchone() == None:
                                c.execute("INSERT INTO duds VALUES({0},{1},{2},{3});"
                                          .format("'"+os_ID+"'","'"+marker+"'",offspring_gen[0], offspring_gen[1]))                            
                            continue #chalk it up as a failure and move on
                        elif offspring_gen[0] == '0': #if one of them is 0, check the other one
                            if offspring_gen[1] in this_gen or offspring_gen[1] in mate_gen:
                                noerror+=1
                        elif offspring_gen[1]== '0':
                            if offspring_gen[0] in this_gen or offspring_gen[0] in mate_gen:
                                noerror +=1
                        elif offspring_gen[0] not in this_gen and offspring_gen[1] not in this_gen: # if no allele comes from this parent
                            c.execute("SELECT * FROM questionable WHERE os_ID='{0}' AND markername='{1}'".format(os_ID, marker))
                            if c.fetchone()==None:
                                c.execute("INSERT INTO questionable VALUES({0},{1},{2},{3},{4},{5},{6},{7},{8},{9});".format("'"+cornellnumber+"'","'"+marker+"'",this_gen[0], this_gen[1], "'"+mate+"'",mate_gen[0],
                                                  mate_gen[1], "'"+os_ID+"'", offspring_gen[0],offspring_gen[1]))
                            founderror +=1
                        else:
                            noerror +=1
                            c.execute("SELECT * FROM checked WHERE cornellnumber = '{0}' AND markername = '{1}';".format(os_ID, marker))
                            out = c.fetchone()
                            if out == None:
                                c.execute("INSERT INTO checked VALUES({0},{1},'offspring');".format("'"+os_ID+"'","'"+marker+"'"))
                else:
                    mate_gen = findgenotypes(mate, marker)
                    if mate_gen == 0: #skips 'pedsire' and 'peddam' entries
                        continue

                    offsprings_gens = findoffspring(cornellnumber, sex, mate, marker)
                    if offsprings_gens == 0:
                        c.execute("SELECT * FROM duds WHERE cornellnumber = '{0}' AND markername = '{1}';".format(cornellnumber, marker))
                        if c.fetchone() == None:
                            c.execute("INSERT INTO duds VALUES({0},{1},{2},{3});"
                                      .format("'"+cornellnumber+"'","'"+marker+"'",this_gen[0], this_gen[1]))
                        continue #if there aren't any offspring, don't check it

                    if mate_gen != ['0', '0']: #we won't know where the other allele came from
                        all_valid = findvalid(this_gen, mate_gen)
                        
                        for offspring_gen_info in offsprings_gens: #for each tuple of 2 alleles corresponding to one offspring's genotype
                            os_ID = offspring_gen_info[0]
                            offspring_gen = offspring_gen_info[1:3]
                            
                        if offspring_gen == ['0','0']: #would need to autoupdate list of sets...
                            c.execute("SELECT generation FROM set206 WHERE cornellnumber ='{0}';".format(os_ID))
                            x = c.fetchone()
                            if x == None:
                                c.execute("SELECT * FROM set207 WHERE cornellnumber ='{0}';".format(os_ID))
                                x = c.fetchone()
                            if ','.join(str(i) for i in x) == '3':
                                c.execute("SELECT * FROM duds WHERE cornellnumber = '{0}' AND markername = '{1}';".format(os_ID, marker))
                                if c.fetchone() == None:
                                    c.execute("INSERT INTO duds VALUES({0},{1},{2},{3});"
                                              .format("'"+os_ID+"'","'"+marker+"'",offspring_gen[0], offspring_gen[1]))
                            continue
                        elif offspring_gen[0] == '0':
                            if offspring_gen[1] in this_gen or offspring_gen[1] in mate_gen:
                                noerror+=1
                        elif offspring_gen[1]== '0':
                            if offspring_gen[0] in this_gen or offspring_gen[0] in mate_gen:
                                noerror +=1
                        elif offspring_gen not in all_valid and [offspring_gen[1], offspring_gen[0]] not in all_valid:
                            c.execute("SELECT * FROM questionable WHERE os_ID='{0}' AND markername='{1}'".format(os_ID, marker))
                            if c.fetchone()==None:
                                c.execute("INSERT INTO questionable VALUES({0},{1},{2},{3},{4},{5},{6},{7},{8},{9});"
                                          .format("'"+cornellnumber+"'","'"+marker+"'",this_gen[0], this_gen[1], "'"+mate+"'",mate_gen[0],
                                                  mate_gen[1],"'"+os_ID+"'",offspring_gen[0],offspring_gen[1]))
                            founderror +=1
                        else:
                            noerror +=1
                
                    else:
                        for offspring_gen_info in offsprings_gens:
                            os_ID = offspring_gen_info[0]
                            offspring_gen = offspring_gen_info[1:3]
                            
                            if offspring_gen == ['0', '0']:
                                #print "0,0 offspring_gen"
                                c.execute("SELECT generation FROM set206 WHERE cornellnumber ='{0}';".format(os_ID))
                                x = c.fetchone()
                                if x == None:
                                    c.execute("SELECT * FROM set207 WHERE cornellnumber ='{0}';".format(os_ID))
                                    x = c.fetchone()
                                if ','.join(str(i) for i in x) == '3':
                                    c.execute("SELECT * FROM duds WHERE cornellnumber = '{0}' AND markername = '{1}';".format(os_ID, marker))
                                    if c.fetchone() == None:
                                        c.execute("INSERT INTO duds VALUES({0},{1},{2},{3});"
                                                  .format("'"+os_ID+"'","'"+marker+"'",offspring_gen[0], offspring_gen[1]))                            
                                continue

                            elif offspring_gen[0] == '0':
                                if offspring_gen[1] in this_gen or offspring_gen[1] in mate_gen:
                                    noerror+=1
                            elif offspring_gen[1]== '0':
                                if offspring_gen[0] in this_gen or offspring_gen[0] in mate_gen:
                                    noerror +=1
                            elif offspring_gen[0] not in this_gen and offspring_gen[1] not in this_gen: # if no allele comes from this parent
                                c.execute("SELECT * FROM questionable WHERE os_ID='{0}' AND markername='{1}'".format(os_ID, marker))
                                if c.fetchone()==None:
                                    c.execute("INSERT INTO questionable VALUES({0},{1},{2},{3},{4},{5},{6},{7},{8},{9});".format("'"+cornellnumber+"'","'"+marker+"'",this_gen[0], this_gen[1], "'"+mate+"'",mate_gen[0],
                                                      mate_gen[1], "'"+os_ID+"'", offspring_gen[0],offspring_gen[1]))
                                founderror +=1
                            else:
                                noerror +=1
                                c.execute("SELECT * FROM checked WHERE cornellnumber = '{0}' AND markername = '{1}';".format(os_ID, marker))
                                out = c.fetchone()
                                if out == None:
                                    c.execute("INSERT INTO checked VALUES({0},{1},'offspring');".format("'"+os_ID+"'","'"+marker+"'"))
                    
                    if (founderror == 0 or noerror >= founderror) and mate_gen !=['0','0']:
                        c.execute("SELECT * FROM checked WHERE cornellnumber = '{0}' AND markername = '{1}';".format(mate, marker))
                        out = c.fetchone()
                        if out== None:
                            c.execute("INSERT INTO checked VALUES('{0}','{1}','mate');".format(mate,marker))

            if founderror == 0 or noerror >= founderror:
                c.execute("SELECT * FROM checked WHERE cornellnumber = '{0}' AND markername = '{1}';".format(cornellnumber, marker))
                out = c.fetchone()
                if out== None:
                    c.execute("INSERT INTO checked VALUES('{0}','{1}','focus');".format(cornellnumber,marker))
                else:
                    c.execute("UPDATE checked SET checkedas = 'focus' WHERE cornellnumber='{0}' AND markername='{1}';".format(cornellnumber,marker))


[c, conn] = openconn()
init(c)
c.execute("SELECT DISTINCT cornellnumber, sex_male1 FROM sample_info_clean WHERE mother = 'NULL' AND father = 'NULL';")
tocheck_raw = c.fetchall()
print "NULLS:"
print len(tocheck_raw)
nextgen(c, tocheck_raw)
c.execute("SELECT DISTINCT cornellnumber, sex_male1 FROM sample_info_clean WHERE mother = 'ped37dam' OR father = 'ped8sire' AND cornellnumber NOT IN (SELECT cornellnumber FROM checked) AND cornellnumber NOT IN (SELECT cornellnumber from questionable);")
tocheck_raw = c.fetchall()
nextgen(c, tocheck_raw)
c.execute("""SELECT S.cornellnumber, sex_male1 FROM sample_info_clean AS S,"""+
              """(SELECT cornellnumber FROM checked WHERE checkedas = 'offspring' OR checkedas = 'mate')"""+
              """AS C WHERE S.cornellnumber=C.cornellnumber;""")
tocheck_raw = c.fetchall()
while len(tocheck_raw) >0:
    print len(tocheck_raw)
    nextgen(c, tocheck_raw)
    c.execute("""SELECT S.cornellnumber, sex_male1 FROM sample_info_clean AS S,"""+
                  """(SELECT cornellnumber FROM checked WHERE checkedas = 'offspring' OR checkedas = 'mate')"""+
                  """AS C WHERE S.cornellnumber=C.cornellnumber;""")
    tocheck_raw_new = c.fetchall()
    if tocheck_raw != tocheck_raw_new:
        tocheck_raw = tocheck_raw_new
    else:
        tocheck_raw = ""
c.execute("""SELECT cornellnumber, sex_male1 FROM sample_info_clean WHERE mother ='F05F335'"""+
          """OR father = 'F06F479' or father = 'F05F320' or mother = 'F05F299';""")
tocheck_raw = c.fetchall()
print "new buffer"
print len(tocheck_raw)
nextgen(c, tocheck_raw)
c.execute("""SELECT cornellnumber, sex_male1 FROM sample_info_clean WHERE cornellnumber NOT IN (SELECT cornellnumber FROM checked)"""+
          """AND cornellnumber NOT IN (SELECT cornellnumber FROM questionable) AND cornellnumber NOT IN (SELECT cornellnumber FROM duds);""")
tocheck_raw = c.fetchall()
print len(tocheck_raw)
nextgen(c, tocheck_raw)
closeconn(conn)
