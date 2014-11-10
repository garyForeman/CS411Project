'''Functions for querying, inserting rows, and deleting rows from FoxDB.'''
#Initialization
import MySQLdb
import csv
import re

DB_NAME = 'foxdb'
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWD = 'foxdb@CS411'
conn = MySQLdb.connect(db=DB_NAME, host=DB_HOST, passwd=DB_PASSWD,
                           user=DB_USER)
c = conn.cursor()


#ACTUAL CODE BEGINS
"""GENOTYPE OUTPUT CODE BEGINS HERE"""
genotype_file = open('genotype_file.txt', 'w')
c.execute("SELECT markername FROM markers;") #need a way for user to select which markers
markers = c.fetchall()

c.execute("DROP VIEW IF EXISTS SetOfSamples;")
c.execute("CREATE VIEW SetOfSamples AS SELECT set206.cornellnumber, pedigree, set206.generation AS pedigree_val, sample_info_clean.generation AS breeding_pop, sex_male1, mother, father FROM set206, sample_info_clean WHERE set206.cornellnumber = sample_info_clean.cornellnumber;") #Need a way to define which individuals (using 206 here)
foxes = c.fetchall()
alloutput = ""

genotype_file.write(str(len(markers)) + "\n")
markerlist = [] #ordered list
for marker in markers:
    markerlist.append('\t'.join([str(i) for i in marker]))

genotype_file.write('\t'.join([str(i) for i in markerlist]))
genotype_file.write("\n")

c.execute("SELECT DISTINCT breeding_pop, pedigree_val FROM SetOfSamples;")
generations = c.fetchall()
I_level = []
II_level = []
III_level = []
for generation in generations:
    sample_list =','.join(str(x) for x in generation).split(",")
    if sample_list[1]=="1" and sample_list[0] not in I_level:
        I_level.append(sample_list[0])
    elif sample_list[1]=="2" and sample_list[0] not in II_level:
        II_level.append(sample_list[0])
    elif sample_list[1]=="3" and sample_list[0] not in III_level:
        III_level.append(sample_list[0])

allgen = []
first = 1
for list_of_gen in [I_level, II_level, III_level]:
    for gen in list_of_gen:
        if gen not in allgen:
            allgen.append(gen)
genotype_file.write('\t'.join([str(i) for i in allgen]))
genotype_file.write("\n")

genotype_file.write("1\t2\n0\n") #male and female coding, missing data value

c.execute("SELECT cornellnumber, father, mother, sex_male1, breeding_pop  FROM SetOfSamples;")
foxinfo = c.fetchall()
c.execute("DROP TABLE IF EXISTS Export;")
c.execute("CREATE TABLE Export(cornellnumber VARCHAR(15) PRIMARY KEY, sire VARCHAR(15), dam VARCHAR(15), sex INTEGER, line VARCHAR(15));")

fakefox = 000

inventive_matings = {} #tells invented pairs by child
fakes = []
for fox in foxinfo:
    fox_list =','.join(str(x) for x in fox).split(",")
    (foxid, sire, dam, sex, line) = fox_list[0:5]
    
    c.execute("SELECT * FROM Export WHERE cornellnumber = {0}".format("'"+foxid+"'"))
    this_fox = c.fetchone()
    if this_fox == None: #skip dups
        allgenotypes = []
        fakesire = str()
        fakedam = str()
        if foxid not in inventive_matings.keys():
            inventive_matings[foxid]={}
        
        if sire == "NULL" and line not in I_level:
            fakesire = "F000"+str(fakefox)
            sire = fakesire
            fakefox +=1
            fakes.append([sire, 1, foxid])
          
        if dam == "NULL" and line not in I_level:
            fakedam = "F000"+str(fakefox)
            dam = fakedam
            fakefox +=1
            fakes.append([dam, 2, foxid])
        
        if fakesire != "":
            inventive_matings[foxid][sire]=dam
            
        if fakedam != "":
            inventive_matings[foxid][dam]=sire
        
        c.execute("INSERT INTO Export VALUES({0},{1},{2},{3},{4})".format("'"+foxid+"'", "'"+sire+"'", "'"+dam+"'", sex, "'"+line+"'"))

        genotype_file.write(foxid+"\t"+sire+"\t"+dam+"\t"+str(sex)+"\t"+line+"\t")

        for marker in markerlist:
            c.execute("SELECT genotype1, genotype2 FROM has_genotype WHERE cornellnumber = {0} AND markername = {1}".format("'"+foxid+"'", "'"+marker+"'"))
            genotypes = c.fetchone()
            if genotypes !=None:
                gen_list =','.join([str(i) for i in genotypes]).split(",")
            else:
                gen_list=[0,0]
            for gen in gen_list:
                genotype_file.write(str(gen) + "\t")
        genotype_file.write("\n")

for fake in fakes:
    (foxid, sex, child) = fake[0:4]
    c.execute("SELECT * FROM Export WHERE cornellnumber = {0}".format("'"+foxid+"'"))
    foxinfo = c.fetchone()

    c.execute("SELECT line FROM Export WHERE cornellnumber = {0}".format("'"+child+"'"))
    childinfo_raw = c.fetchone()
    childinfo = '\t'.join([str(i) for i in childinfo_raw])
    
    if foxinfo == None:
        this_line = str()
        if childinfo=="aggr" or childinfo=="tame": #child is purebred
            this_line = childinfo
        elif childinfo=="F2": #F2 child always has 2 F1 parents
            this_line = "F1"
            
        elif childinfo=="F1": #F1 child from tame x aggr
            other_parent=inventive_matings[child][foxid]
            c.execute("SELECT line FROM Export WHERE cornellnumber = {0}".format("'"+other_parent+"'"))
            other_line_raw = c.fetchone()
            other_line = '\t'.join([str(i) for i in childinfo_raw])
            if other_line != None: #if other_line is assigned
                if other_line == "tame": #should be opposite of other parent
                    this_line = "aggr"
                elif other_line == "aggr":
                    this_line = "tame"
            else:
                this_line = "tame"
                other_line = "aggr"
                if sex == 1:
                    other_sex = 2
                else:
                    other_sex = 1
                c.execute("INSERT INTO Export VALUES({0},NULL,NULL,{1},{2})".format("'"+other_parent+"'", other_sex, "'"+other_line+"'"))
        
        c.execute("INSERT INTO Export VALUES({0},NULL,NULL,{1},{2})".format("'"+fake[0]+"'", fake[1], "'"+this_line+"'"))
        genotype_file.write(foxid+"\tNULL\tNULL\t"+str(sex)+"\t"+this_line+"\t")
   
        for marker in markerlist:
            c.execute("SELECT genotype1, genotype2 FROM has_genotype WHERE cornellnumber = {0} AND markername = {1}".format("'"+foxid+"'", "'"+marker+"'"))
            genotypes = c.fetchone()
            if genotypes !=None:
                gen_list =','.join([str(i) for i in genotypes]).split(",")
            else:
                gen_list=[0,0]
            for gen in gen_list:
                genotype_file.write(str(gen) + "\t")
        genotype_file.write("\n")

c.execute("DROP TABLE Export;") #it's just for the sake of writing out   
genotype_file.close()


"""MAP FILE OUTPUT CODE BEGINS HERE
We'll have to make this fancier if we want to add more chromosomes"""
map_file = open('map_file.txt', 'w')
num_of_chr = 1 #by necessity, since we're only using VVU12 right now
name_chr = "VVU12" #only data we included
num_markers = len(markerlist) #easy because only 1 chr

map_file.write(str(num_of_chr)+"\n1\n"+ name_chr + "\t" + str(num_markers) + "\t1\n")

c.execute("SELECT markername, MeioticPos FROM markers")
marker_pos = {}
marker_info = c.fetchall()
for marker in marker_info:
    marker_tuple = ','.join([str(i) for i in marker]).split(",")
    marker_pos[float(marker_tuple[1])]=marker_tuple[0]

marker_pos_ordered = marker_pos.keys()
marker_pos_ordered.sort()

for p in range(0,len(marker_pos_ordered)): #need to list out markers with distances in cM in between
    cM_raw = marker_pos_ordered[p]
    if p == 0:
        map_file.write(marker_pos[cM_raw]+"\t")
    else:
        cM_last = marker_pos_ordered[p-1]
        cM_dif = float(cM_raw)-float(cM_last)
        map_file.write(str(cM_dif)+"\t"+marker_pos[cM_raw]+"\t")
            
map_file.close()  
    

conn.commit()
c.close()
conn.close()
