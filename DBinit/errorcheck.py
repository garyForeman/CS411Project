import MySQLdb
import csv

"""When we display, display DISTINCT so that we lose cases where the fox is homozygous for a questionable allele"""

conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "foxdb@CS411", db = "foxdb") 
c = conn.cursor () 

c.execute("SELECT has_genotype.cornellnumber, has_genotype.markername, has_genotype.genotype1, has_genotype.genotype2, sample_info_clean.mother, sample_info_clean.father FROM has_genotype, sample_info_clean WHERE has_genotype.cornellnumber=sample_info_clean.cornellnumber")
tocheck = c.fetchall()

c.execute("SHOW TABLES")
tables = c.fetchall()
alltables = []
for table in tables:
    alltables.append('\t'.join([str(i) for i in table]))
if "questionable" not in alltables:
    c.execute("CREATE TABLE IF NOT EXISTS questionable(cornellnumber VARCHAR(15), markername VARCHAR(15), genotype1 INTEGER, genotype2 INTEGER, problem_genotype INTEGER)")


totalchecks =0
totalOK = 0
totalall = 0
oneparent = 0
totalnull = 0
totalsent = 0

def plusone(totalsent):
    totalsent +=1
    return totalsent

def checkoffspring(testfox, testmarker):
    validtypes = []
    validoffspring = 0
    c.execute("SELECT has_genotype.genotype1,has_genotype.genotype2 FROM sample_info_clean, has_genotype WHERE (sample_info_clean.mother = {0} OR sample_info_clean.father = {0}) AND sample_info_clean.cornellnumber=has_genotype.cornellnumber AND has_genotype.markername={1}"
              .format(testfox, testmarker))
    inherited = c.fetchall()

    if len(inherited)>0:
        for offspring in inherited:
            print offspring
            twogenotypes = ','.join([str(i) for i in offspring]) #returns as comma-separated list
            toadd = twogenotypes.split(",")
            for genotype in toadd:
                validtypes.append(int(genotype)) #list of all offpsring genotypes (as available)
        return validtypes
    else:
        return []
    
    
for row in tocheck:
    testfox = "'"+row[0]+"'"
    testmarker = "'"+row[1]+"'"
    
    genotypes = [int(row[2]), int(row[3])]
    mother = "'"+row[4]+"'"
    father = "'"+row[5]+"'"

    offspringcheck = 0 #records whether there are inconsistencies
    OKcheck = 0
    if mother!="'NULL'" or father!="'NULL'": #if either parent is known
        c.execute("SELECT genotype1, genotype2 from has_genotype WHERE (cornellnumber = {0} OR cornellnumber = {1}) AND markername = {2}"
                  .format(mother, father, testmarker))
        inherited = c.fetchall()
        validtypes = []
        if len(inherited)>0:
            totalall +=1
            for parent in inherited:
                twogenotypes = ','.join([str(i) for i in parent]) #returns as ,-separated list
                toadd = twogenotypes.split(",")
                for genotype in toadd:
                    validtypes.append(int(genotype)) #list of 4 parental genotypes (as available)
            totalall +=1
            for genotype in genotypes:
                if genotype in validtypes:
                    OKcheck+=1
                elif genotype not in validtypes:
                    offspringcheck =1
            
            if offspringcheck ==1:
                totalchecks+=1
                totalsent = plusone(totalsent)
                offspringgen = checkoffspring(testfox, testmarker)
                for genotype in genotypes:
                    if genotype not in offspringgen:
                       c.execute("INSERT INTO questionable VALUES({0}, {1}, {2}, {3}, {4})".format(testfox, testmarker, genotypes[0], genotypes[1], genotype))
                       
            elif OKcheck == 2:
                totalOK+=1
            elif OKcheck ==1 and len(inherited)==1:
                oneparent +=1
            else: print "Anomaly!"
        else:
            totalnull +=1
    else:
        totalnull +=1
        checkoffspring(testfox, testmarker)
        offspringgen = checkoffspring(testfox, testmarker)
        for genotype in genotypes:
            if genotype not in offspringgen:
               c.execute("INSERT INTO questionable VALUES({0}, {1}, {2}, {3}, {4})".format(testfox, testmarker, genotypes[0], genotypes[1], genotype))
     
conn.commit()
conn.close()
