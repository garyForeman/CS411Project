import MySQLdb
import csv

conn = MySQLdb.connect (host = "localhost", user = "root",
                        passwd = "foxdb@CS411", db = "foxdb") 
c = conn.cursor () 

c.execute("SHOW TABLES")
tables = c.fetchall()
alltables = []
for table in tables:
    alltables.append('\t'.join([str(i) for i in table]))

if "dubious" in alltables:
    c.execute("DROP TABLE IF EXISTS dubious;")
c.execute("""CREATE TABLE IF NOT EXISTS dubious(cornellnumber VARCHAR(15),"""+
          """markername VARCHAR(15),genotype1 INTEGER, genotype2 INTEGER,"""+
          """mateID VARCHAR(50), mate_gen1 INTEGER, mate_gen2 INTEGER,"""+
          """os_ID VARCHAR(50), os_gen1 INTEGER, os_gen2 INTEGER,"""+
          """PRIMARY KEY (cornellnumber, markername, os_ID));""")

if "checked" in alltables:
    c.execute("DROP TABLE IF EXISTS checked;")
c.execute("CREATE TABLE checked(cornellnumber VARCHAR(15), markername VARCHAR(15), checkedas VARCHAR(50), PRIMARY KEY(cornellnumber, markername));")

"""STEP 1: PULL TOP GENERATION"""

c.execute("SELECT DISTINCT cornellnumber, sex_male1 FROM sample_info_clean WHERE mother ='NULL' AND father='NULL';")
tocheck_raw = c.fetchall()
tocheck = []
for line in tocheck_raw:
    tocheck.append(','.join([str(i) for i in line]).split(","))

for sample in tocheck:
    (cornellnumber, sex) = sample[0:5]

    if sex == "1": #if male
        c.execute("SELECT DISTINCT mother FROM sample_info_clean WHERE father = {0};"
                  .format("'"+cornellnumber + "'"))
        mates_raw = c.fetchall()
    else: #if female
        c.execute("SELECT DISTINCT father FROM sample_info_clean WHERE father = {0};"
                  .format("'"+cornellnumber + "'"))
        mates_raw = c.fetchall()

    if len(mates_raw) == 0:
        continue
    mates = []
    for mate in mates_raw:
        mates.append(','.join(str(i) for i in mate))

    c.execute("SELECT markername, genotype1, genotype2 FROM has_genotype WHERE cornellnumber = {0};".format("'"+cornellnumber+"'"))
    all_genotypes_raw = c.fetchall()
    all_genotypes = []
    for genpair in all_genotypes_raw:
        all_genotypes.append(','.join(str(i) for i in genpair).split(","))

    for genotype in all_genotypes: #for each marker, gen1, gen2 set
        marker= genotype[0]
        this_gen = genotype[1:3]
        if this_gen == ['0','0']:
            continue
        
        founderror = 0
        noerror = 0
        for mate in mates:
            c.execute("SELECT genotype1, genotype2 FROM has_genotype WHERE cornellnumber = {0} and markername = {1};"
                      .format("'"+mate+"'", "'"+marker+"'"))
            mate_gen = ','.join(str(i) for i in c.fetchone()).split(",")
            
            if sex == "1":
                c.execute("""SELECT S.cornellnumber, genotype1, genotype2 FROM sample_info_clean AS S, has_genotype AS G WHERE S.cornellnumber=G.cornellnumber AND """+
                          """father={0} AND mother={1} AND markername = {2};""".format("'"+cornellnumber+"'", "'"+mate+"'", "'"+marker+"'"))
                offspring_gen_raw = c.fetchall()
            else:
                c.execute("""SELECT S.cornellnumber, genotype1, genotype2 FROM sample_info_clean AS S, has_genotype AS G WHERE S.cornellnumber=G.cornellnumber AND """+
                          """mother={0} AND father={1} AND markername = {2};""".format("'"+cornellnumber+"'", "'"+mate+"'", "'"+marker+"'"))
                offspring_gen_raw = c.fetchall()
            
            offsprings_gens = []

            if offspring_gen_raw == None:
                continue
            else:
                for genpair in offspring_gen_raw:
                    offsprings_gens.append(','.join(str(i) for i in genpair).split(","))              
            #now we have tuples: this_gen, mate_gen, and offspring_gen (though the last is a tuple of tuples)

            if mate_gen != ['0', '0']: #we won't know where the other allele came from
                all_valid = [
                    [this_gen[0], mate_gen[0]],
                    [this_gen[0], mate_gen[1]],
                    [this_gen[1], mate_gen[0]],
                    [this_gen[1], mate_gen[1]]]
                
                for offspring_gen_info in offsprings_gens: #for each tuple of 2 alleles corresponding to one offspring's genotype
                    offspring_gen = offspring_gen_info[1:3]
                    
                    if offspring_gen == ['0','0']:
                        continue
                    elif offspring_gen not in all_valid and [offspring_gen[1], offspring_gen[0]] not in all_valid:
                        c.execute("INSERT INTO dubious VALUES({0},{1},{2},{3},{4},{5},{6},{7},{8},{9});"
                                  .format("'"+cornellnumber+"'","'"+marker+"'",this_gen[0], this_gen[1], "'"+mate+"'",mate_gen[0],
                                          mate_gen[1],"'"+offspring_gen_info[0]+"'",offspring_gen_info[1],offspring_gen_info[2]))
                        founderror +=1
                    else:
                        noerror +=1
            else:
                for offspring_gen_info in offsprings_gens:
                    offspring_gen = offspring_gen_info[1:3]
                    if offspring_gen == ['0', '0']:
                        continue
                    if offspring_gen[0] not in this_gen and offspring_gen[1] not in this_gen: # if the first allele comes from this parent
                        c.execute("INSERT INTO dubious VALUES({0},{1},{2},{3},{4},{5},{6},{7},{8},{9});"
                                  .format("'"+cornellnumber+"'","'"+marker+"'",this_gen[0], this_gen[1], "'"+mate+"'",mate_gen[0],
                                          mate_gen[1], "'"+offspring_gen_info[0]+"'", offspring_gen[0],offspring_gen[1]))
                        founderror +=1
                    else:
                        noerror +=1
        if founderror == 0:
            c.execute("INSERT INTO checked VALUES({0},{1},{2});".format("'"+cornellnumber+"'","'"+marker+"'", "'parent'"))
            c.execute("INSERT INTO checked VALUES({0},{1},{2});".format("'"+offspring_gen_info[0]+"'","'"+marker+"'", "'offspring1'"))
        elif noerror >= founderror:
            c.execute("INSERT INTO checked VALUES({0},{1},{2});".format("'"+cornellnumber+"'","'"+marker+"'", "'parent'"))


conn.commit()
conn.close()
