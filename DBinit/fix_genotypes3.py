import csv
import re

in_name='./markernames_on_VVU12.csv' #only markers on VVU12
OKmarkers = list(csv.reader(open(in_name,'r'), delimiter=','))
markers12_single = []
markers12_double = []
for row in OKmarkers[1:]:
    markers12_single.append(row[0])
    markers12_double.append(row[0])
    markers12_double.append(str(row[0]+" copy"))
    

in_name='./raw_genotype_data.csv' #raw data
genotypes = list(csv.reader(open(in_name,'r'), delimiter=','))
problem =0
marker_order = [] #list of all markers, in order, incl copy
all_genotypes = {} #dictionary of dictionaries
problematic = {}
for row in genotypes:
    if len(marker_order)==0:
        for column in row[1:]:
            marker_order.append(column)
    else:
        foxid = row[0]
        for column_position in range(0,len(marker_order)):
            marker_name = marker_order[column_position]
            
            if marker_name in markers12_double:
                if foxid not in all_genotypes.keys(): #first time this fox is up
                    all_genotypes[foxid]={} #define "of dictionaries" part
                if marker_name in all_genotypes[foxid].keys():#if marker already defined for fox
                    if all_genotypes[foxid][marker_name]==row[column_position+1]:
                        continue
                    elif row[column_position+1] != '0':
                        if foxid not in problematic.keys():
                            problematic[foxid]= {}
                            problematic[foxid][marker_name]=[all_genotypes[foxid][marker_name],row[column_position+1]]
                        elif marker_name not in problematic[foxid].keys():
                            problematic[foxid][marker_name]=[all_genotypes[foxid][marker_name],row[column_position+1]]
                        else:
                            problematic[foxid][marker_name].append(row[column_position+1])
                        
                else:
                    all_genotypes[foxid][marker_name]=row[column_position+1] #set gen
            
            

with open('genotypes_11-9.csv', 'wb') as csvfile:
    writerbot = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    header = ["cornellnumber", "markername", "genotype1", "genotype2"]
    writerbot.writerow(header)
    
    for foxid in all_genotypes.keys(): #for each cornellnum
        if foxid not in problematic.keys(): #if it's not causing problems
            for column_pos in range(0, len(marker_order),2): #for each marker
                if marker_order[column_pos] in markers12_single: #if it's a marker in VVU12
                    writerbot.writerow([foxid, marker_order[column_pos], all_genotypes[foxid][marker_order[column_pos]],
                                        all_genotypes[foxid][marker_order[column_pos+1]]])
