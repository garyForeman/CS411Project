import MySQLdb
import re

def unfetchall_single(raw):
    out = []
    for x in raw:
        out.append(','.join([str(i) for i in x]))
    return out

def unfetchall_multi(raw):
    out = []
    for x in raw:
        out.append(','.join([str(i) for i in x]).split(","))
    return out

def unfetchone_multi(raw):
    if raw == None:
        return None
    out = ""
    for x in raw:
        out += (','.join(str(i) for i in x))
    return out.split(",")

def unfetchone_list(raw):
    if raw == None:
        return None
    out = []
    for x in raw:
        out.append(','.join(str(i) for i in x))
    return out.split(",")

#def openconn():
#    conn = MySQLdb.connect (host = "localhost", user = "root",
#                            passwd = "foxdb@CS411", db = "foxdb")
#    c = conn.cursor ()
#    return c, conn

#def closeconn(conn):
#    conn.commit()
#    conn.close()

def init(c):
    c.execute("SHOW TABLES")
    tables = c.fetchall()

    alltables = []
    for table in tables:
        alltables.append('\t'.join([str(i) for i in table]))

    if "questionable" in alltables:
        c.execute("DROP TABLE IF EXISTS questionable;")
    c.execute("""CREATE TABLE IF NOT EXISTS questionable(""" +
              """cornellnumber VARCHAR(15), """+
              """markername VARCHAR(15), """ +
              """checkedagainst VARCHAR(50), """ +
              """setname VARCHAR(50), """ +
              """ped VARCHAR(50), """+
              """PRIMARY KEY(cornellnumber, markername, checkedagainst, """ +
              """setname, ped));""")

    if "consistent_parents" in alltables:
        c.execute("DROP TABLE IF EXISTS consistent_parents;")
    c.execute("""CREATE TABLE consistent_parents(""" +
              """cornellnumber VARCHAR(15), """ +
              """markername VARCHAR(15),"""+
              """setname VARCHAR(50), """ +
              """pedigree VARCHAR(50), """ +
              """PRIMARY KEY(cornellnumber, markername, setname, pedigree));""")

    if "consistent_offspring" in alltables:
        c.execute("DROP TABLE IF EXISTS consistent_offspring;")
    c.execute("""CREATE TABLE consistent_offspring(""" +
              """cornellnumber VARCHAR(15), """ +
              """markername VARCHAR(15), """+
              """setname VARCHAR(50), """ +
              """pedigree VARCHAR(50), """ +
              """OS_ID VARCHAR(15), """ +
              """PRIMARY KEY(cornellnumber, markername, setname, """ +
              """pedigree, OS_ID));""")

def addtoquest(CN, marker, checkedagainst, setname, ped, c):
    if CN != "NULL":
        c.execute(("""SELECT * FROM questionable WHERE cornellnumber='{0}' """ +
                   """and markername='{1}' and setname='{2}' and ped='{3}'""")
                  .format(CN, marker, setname, ped))
        if c.fetchone() == None:
            c.execute("""INSERT INTO questionable """ +
                      """VALUES('{0}','{1}','{2}','{3}','{4}')"""
                      .format(CN, marker, checkedagainst, setname, ped))

def checkgen(genotype_target, possible_inheritance, elders, target_CN,
             marker, setname, ped, genotypedict, c):
    changedtogrand = 0
    if "NULL" in elders:
        if elders == ['NULL', 'NULL']:
            c.execute("INSERT INTO consistent_parents " +
                      "VALUES('{0}','{1}','{2}','{3}')"
                      .format(target_CN, marker, setname, ped))
            return

        for sample_over in elders:
            if sample_over != "NULL":
                if (genotype_target[0] in genotypedict[sample_over] and
                    genotype_target[1] in genotypedict[sample_over]):
                    c.execute("INSERT INTO consistent_parents " +
                              "VALUES('{0}','{1}','{2}','{3}')"
                              .format(target_CN, marker, setname, ped))
                    c.execute("INSERT INTO consistent_offspring " +
                              "VALUES('{0}','{1}','{2}','{3}','{4}')"
                              .format(sample_over, marker, setname, ped,
                                      target_CN))
                    return
                elif (genotype_target[0] in genotypedict[sample_over] or 
                      genotype_target[1] in genotypedict[sample_over]):
                    c.execute("INSERT INTO consistent_parents " +
                              "VALUES('{0}','{1}','{2}','{3}')"
                              .format(target_CN, marker, setname, ped))
                    c.execute("INSERT INTO consistent_offspring " +
                              "VALUES('{0}','{1}','{2}','{3}','{4}')"
                              .format(sample_over, marker, setname, ped,
                                      target_CN))
                    return
                elif genotype_target==['0','0']:
                    c.execute("INSERT INTO consistent_offspring " +
                              "VALUES('{0}','{1}','{2}','{3}','{4}')"
                              .format(sample_over, marker, setname, ped,
                                      target_CN))
                    return
                else:
                    addtoquest(sample_over, marker, 'offspring', setname, ped,
                               c)
                    return

    if 'ped8sire' in elders:
        genotypedict['ped8sire'] = ['0', '0']
        if '0' in possible_inheritance.keys():
            possible_inheritance['0'].append('ped8sire')
        else:
            possible_inheritance['0'] = ['ped8sire']
    if 'ped37dam' in elders:
        genotypedict['ped37dam'] = ['0', '0']
        if '0' in possible_inheritance.keys():
            possible_inheritance['0'].append('ped37dam')
        else:
            possible_inheritance['0'] = ['ped37dam']

    if ('0' in possible_inheritance.keys() and
        possible_inheritance['0'] != "NULL"):
        zeroparents = possible_inheritance['0'] #even if they only have one, bad
        for parent in zeroparents:
            grandgen_perparent = []
            #it has a zero, and should be checked
            addtoquest(parent, marker, 'offspring', setname, ped, c)
            c.execute(("SELECT mother, father FROM sample_info_clean WHERE " +
                       "cornellnumber='{0}' AND mother <>'NULL' AND " +
                       "father <>'NULL';").format(parent))
            grandparents = c.fetchone()
            if grandparents == None:
                c.execute(("SELECT mother FROM sample_info_clean WHERE " +
                           "cornellnumber='{0}' AND mother <>'NULL';")
                          .format(parent))
                grandparents = c.fetchone()
                if grandparents == None:
                    c.execute(("SELECT father FROM sample_info_clean " +
                               "WHERE cornellnumber='{0}' AND " +
                               "father <>'NULL';").format(parent))
            if grandparents == None:
                continue
            elif grandparents != None:
                changedtogrand = 1
                grandparents = list(grandparents)
                for grandparent in grandparents:
                    grand_genotypes = []
                    c.execute(("SELECT genotype1, genotype2 " +
                               "FROM has_genotype " +
                               "WHERE cornellnumber='{0}' " +
                               "AND markername ='{1}'")
                              .format(grandparent, marker))
                    genotypes_long = list(c.fetchone())
                    for gen_temp in genotypes_long:
                        grand_genotypes.append(str(int(gen_temp)))
                    if len(grand_genotypes) == 2:
                        grand_genotypes.append('0')
                        grand_genotypes.append('0')
                    for genotype_temp in grand_genotypes:
                        grandgen_perparent.append(genotype_temp)
            genotypedict[parent] = grandgen_perparent
            possible_inheritance = {}
            for elder in elders:
                e_genotypes = genotypedict[elder]
                 #for each of the grandparents' alleles, record which gp(s)
                 #contributed allele
                for gen_e in e_genotypes:
                    if gen_e not in possible_inheritance.keys():
                        possible_inheritance[gen_e] = [elder]
                    elif elder not in possible_inheritance[gen_e]:
                        possible_inheritance[gen_e].append(elder)

    #if the genotype of the target sample has 2 known values
    if '0' not in genotype_target:
        #both alleles found in parents
        if (genotype_target[0] in possible_inheritance.keys() and
            genotype_target[1] in possible_inheritance.keys()):
            if genotype_target[0] == genotype_target[1]: #if homozygotic
                #normal homozygote, both parents have it
                if len(possible_inheritance[genotype_target[0]]) == 2:
                    c.execute("""INSERT INTO consistent_parents """ +
                              """VALUES('{0}','{1}','{2}','{3}')"""
                              .format(target_CN, marker, setname, ped))
                    c.execute("INSERT INTO consistent_offspring " +
                              "VALUES('{0}','{1}','{2}','{3}','{4}')"
                              .format(elders[0], marker, setname, ped,
                                      target_CN))
                    c.execute("INSERT INTO consistent_offspring " +
                              "VALUES('{0}','{1}','{2}','{3}','{4}')"
                              .format(elders[1], marker, setname, ped,
                                      target_CN))
                #normal heterozygote is next line
                elif genotype_target[0] in possible_inheritance.keys():
                    goodparent = possible_inheritance[genotype_target[0]][0]
                    for elder in elders:
                        if elder == goodparent:
                            c.execute("INSERT INTO consistent_offspring " +
                                      "VALUES('{0}','{1}','{2}','{3}','{4}')"
                                      .format(elder, marker, setname, ped,
                                              target_CN))
                            c.execute("INSERT INTO consistent_parents " +
                                      "VALUES('{0}','{1}','{2}','{3}')"
                                      .format(target_CN, marker, setname, ped))
                        else:
                            #seems wrong, probably 0
                            addtoquest(elder, marker, 'offspring', setname,
                                       ped, c)

                else:
                    addtoquest(target_CN, marker, 'parent', setname, ped, c)
                    addtoquest(elders[0], marker, 'offspring', setname, ped, c)
                    addtoquest(elders[1], marker, 'offspring', setname, ped, c)
            #if heterozygote
            elif genotype_target[0] != genotype_target[1]:
                if (genotype_target[0] in genotypedict[elders[0]] and
                    genotype_target[1] in genotypedict[elders[1]]):
                    c.execute("INSERT INTO consistent_parents " +
                              "VALUES('{0}','{1}','{2}','{3}')"
                              .format(target_CN, marker, setname, ped))
                    c.execute("INSERT INTO consistent_offspring " +
                              "VALUES('{0}','{1}','{2}','{3}','{4}')"
                              .format(elders[0], marker, setname, ped,
                                      target_CN))
                    c.execute("INSERT INTO consistent_offspring " +
                              "VALUES('{0}','{1}','{2}','{3}','{4}')"
                              .format(elders[1], marker, setname, ped,
                                      target_CN))
                elif (genotype_target[1] in genotypedict[elders[0]] and
                      genotype_target[0] in genotypedict[elders[1]]):
                    c.execute("INSERT INTO consistent_parents " +
                              "VALUES('{0}','{1}','{2}','{3}')"
                              .format(target_CN, marker, setname, ped))
                    c.execute("INSERT INTO consistent_offspring " +
                              "VALUES('{0}','{1}','{2}','{3}','{4}')"
                              .format(elders[0], marker, setname, ped,
                                      target_CN))
                    c.execute("INSERT INTO consistent_offspring " +
                              "VALUES('{0}','{1}','{2}','{3}','{4}')"
                              .format(elders[1], marker, setname, ped,
                                      target_CN))
                elif (genotype_target[0] in genotypedict[elders[0]] or
                      genotype_target[1] in genotypedict[elders[0]]):
                    c.execute("INSERT INTO consistent_parents " +
                              "VALUES('{0}','{1}','{2}','{3}')"
                              .format(target_CN, marker, setname, ped))
                    addtoquest(elders[1], marker, 'offspring', setname, ped, c)
                    c.execute("INSERT INTO consistent_offspring " +
                              "VALUES('{0}','{1}','{2}','{3}','{4}')"
                              .format(elders[0], marker, setname, ped,
                                      target_CN))
                elif (genotype_target[0] in genotypedict[elders[1]] or
                      genotype_target[1] in genotypedict[elders[1]]):
                    c.execute("INSERT INTO consistent_parents " +
                              "VALUES('{0}','{1}','{2}','{3}')"
                              .format(target_CN, marker, setname, ped))
                    addtoquest(elders[0], marker, 'offspring', setname, ped, c)
                    c.execute("INSERT INTO consistent_offspring " +
                              "VALUES('{0}','{1}','{2}','{3}','{4}')"
                              .format(elders[1], marker, setname, ped,
                                      target_CN))
                else:
                    addtoquest(target_CN, marker, 'parent', setname, ped, c)
                    addtoquest(elders[1], marker, 'offspring', setname, ped, c)
                    addtoquest(elders[0], marker, 'offspring', setname, ped, c)
            else: #this doesn't happen. SCORE!
                addtoquest(target_CN, marker, 'parent', setname, ped, c)
                addtoquest(elders[1], marker, 'offspring', setname, ped, c)
                addtoquest(elders[0], marker, 'offspring', setname, ped, c)
        #if one or more parent has blanks
        elif '0' in possible_inheritance.keys():
            if changedtogrand == 1:
                if (genotype_target[1] in possible_inheritance.keys() and
                    genotype_target[0] in possible_inheritance.keys()):
                    c.execute(("INSERT INTO consistent_parents " +
                               "VALUES('{0}','{1}','{2}','{3}')")
                              .format(target_CN, marker, setname, ped))
                    c.execute(("INSERT INTO consistent_offspring " +
                               "VALUES('{0}','{1}','{2}','{3}','{4}')")
                              .format(elders[0], marker, setname, ped,
                                      target_CN))
                    c.execute(("INSERT INTO consistent_offspring " +
                               "VALUES('{0}','{1}','{2}','{3}','{4}')")
                              .format(elders[1], marker, setname, ped,
                                      target_CN))
                else:
                    changedtogrand = 0
            if changedtogrand == 0:
                if len(possible_inheritance['0']) == 1:
                    #CN of the one that gets a pass, Gary's change added
                    canskip = possible_inheritance['0'][0]
                    for elder in elders:
                        if elder == canskip:
                            #have no idea whether it's right or wrong
                            addtoquest(elder, marker, 'offspring', setname,
                                       ped, c)
                        else:
                            #if the other one has this version
                            if genotype_target[0] in genotypedict[elder]:
                                c.execute(("INSERT INTO consistent_parents " +
                                           "VALUES('{0}','{1}','{2}','{3}')")
                                          .format(target_CN, marker, setname,
                                                  ped))
                                c.execute(("INSERT INTO consistent_offspring " +
                                           "VALUES('{0}','{1}','{2}','{3}'," +
                                           "'{4}')")
                                          .format(elder, marker, setname, ped,
                                                  target_CN))
                            #if the other one has this version
                            elif genotype_target[1] in genotypedict[elder]:
                                c.execute(("INSERT INTO consistent_parents " +
                                           "VALUES('{0}','{1}','{2}','{3}')")
                                          .format(target_CN, marker, setname,
                                                  ped))
                                c.execute(("INSERT INTO consistent_offspring " +
                                           "VALUES('{0}','{1}','{2}','{3}'," +
                                           "'{4}')")
                                          .format(elder, marker, setname, ped,
                                                  target_CN))
                            else:
                                addtoquest(target_CN, marker, 'parent',
                                           setname, ped, c)
                                addtoquest(elder, marker, 'offspring',
                                           setname, ped, c)
                elif len(possible_inheritance['0']) == 2:#both parents have a 0
                    addtoquest(elders[0], marker, 'offspring', setname, ped, c)
                    addtoquest(elders[1], marker, 'offspring', setname, ped, c)
                else: #this doesn't happen!
                    addtoquest(target_CN, marker, 'parent', setname, ped, c)
                    addtoquest(elders[0], marker, 'offspring', setname, ped, c)
                    addtoquest(elders[1], marker, 'offspring', setname, ped, c)
        #if parental alleles aren't in grandparental genotypes and it's not
        #because of blanks
        else:
            #definitely wrong
            addtoquest(target_CN, marker, 'parent', setname, ped, c)
            #have no idea whether it's right or wrong
            addtoquest(elders[0], marker, 'offspring', setname, ped, c)
            #have no idea whether it's right or wrong
            addtoquest(elders[1], marker, 'offspring', setname, ped, c)

    else: #if target's genotype includes blanks
        #have no idea whether it's right or wrong
        addtoquest(target_CN, marker, 'offspring', setname, ped, c)
        #have no idea whether it's right or wrong
        addtoquest(target_CN, marker, 'parent', setname, ped, c)

def error_checker(c):
    init(c)
    c.execute("SELECT DISTINCT markername FROM has_genotype")
    allmarkers = unfetchall_single(c.fetchall())

    c.execute("SHOW TABLES LIKE 'SET2%';")
    allsets = unfetchall_single(c.fetchall())

    for setname in allsets: #set by set
        #print setname
        c.execute("SELECT DISTINCT pedigree FROM {0};".format(setname))
        pedigrees = unfetchall_single(c.fetchall())

        for ped in pedigrees: #pedigree by pedigree

            c.execute(("SELECT cornellnumber FROM {0} " +
                       "WHERE pedigree='{1}' AND generation=2;")
                      .format(setname, ped))
            samples_II = unfetchall_single(c.fetchall())

            c.execute(("SELECT cornellnumber FROM {0} " +
                       "WHERE pedigree='{1}' and generation=3;")
                      .format(setname, ped))
            samples_III = unfetchall_single(c.fetchall())

            for marker in allmarkers:
                #dict of genotypes for each gen I
                #(Key: grandparent cornellnumber, value: list of alleles)
                I_genotypes = {}
                #dict of genotypes for each gen II
                #(Key: parent cornellnumber, value: list of alleles)
                II_genotypes = {}

                #all alleles in generation II
                #(Key: allele, value: list of parents with that allele)
                possible_inheritance_p = {}
                for CN_p in samples_II: #cornellnumber of each parent
                    c.execute("""SELECT genotype1, genotype2 """ +
                              """FROM has_genotype WHERE """+
                              """cornellnumber ='{0}' AND markername='{1}';"""
                              .format(CN_p, marker))
                    genotype_p = unfetchone_multi(c.fetchall())
                    II_genotypes[CN_p] = genotype_p

                    #this will happen for 'ped37dam' and 'ped8sire'
                    if genotype_p == ['']:
                        #definitely wrong
                        c.execute("INSERT INTO questionable " +
                                  "VALUES('{0}','{1}','parent','{2}','{3}');"
                                  .format(CN_p, marker, setname, ped))
                        continue

                    #for each of the grandparents' alleles,
                    #record which gp(s) contributed allele
                    for gen in genotype_p:
                        if gen not in possible_inheritance_p.keys():
                            possible_inheritance_p[gen] = [CN_p]
                        elif CN_p not in possible_inheritance_p[gen]:
                            possible_inheritance_p[gen].append(CN_p)

                    #all alleles in generation I
                    #(Key: allele, value: list of grandparents with that allele)
                    possible_inheritance_gp = {}
                    c.execute("SELECT mother, father FROM sample_info_clean " +
                              "WHERE cornellnumber='{0}';"
                              .format(CN_p))
                    grandparents = unfetchone_multi(c.fetchall())

                    for CN_gp in grandparents:
                        if CN_gp != "NULL":
                            c.execute(("""SELECT genotype1, genotype2 """ +
                                       """FROM has_genotype """ +
                                       """WHERE cornellnumber ='{0}' AND """ +
                                       """markername='{1}';""")
                                      .format(CN_gp, marker))
                            gp_genotype = unfetchone_multi(c.fetchall())
                        else:
                            gp_genotype = ['0', '0']
                        I_genotypes[CN_gp] = gp_genotype

                        #for each of the grandparents' alleles,
                        #record which gp(s) contributed allele
                        for gen in gp_genotype:
                            if gen not in possible_inheritance_gp.keys():
                                possible_inheritance_gp[gen] = [CN_gp]
                            elif CN_gp not in possible_inheritance_gp[gen]:
                                possible_inheritance_gp[gen].append(CN_gp)

                    checkgen(genotype_p, possible_inheritance_gp, grandparents,
                             CN_p, marker, setname, ped, I_genotypes, c)

                for CN_kit in samples_III:
                    c.execute(("""SELECT genotype1, genotype2 """ +
                               """FROM has_genotype """+
                               """WHERE cornellnumber ='{0}' AND """ +
                               """markername='{1}';""")
                              .format(CN_kit, marker))
                    genotype_k = unfetchone_multi(c.fetchall())

                    #this will happen for 'ped37dam' and 'ped8sire'
                    if genotype_k == ['']:
                        #definitely wrong
                        c.execute("INSERT INTO questionable " +
                                  "VALUES('{0}','{1}','parent','{2}','{3}');"
                                  .format(CN_kit, marker, setname, ped))
                        continue

                    checkgen(genotype_k, possible_inheritance_p, samples_II,
                             CN_kit, marker, setname, ped, II_genotypes, c)
