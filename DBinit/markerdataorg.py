import csv
in_name='./has_genotype_clean.csv'
data = list(csv.reader(open(in_name,'r'), delimiter=','))

header = 0

out_name1='./newmarkerdata.csv'
with open(out_name1, 'wb') as csvfile:
    writerbot = csv.writer(csvfile, delimiter=',',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
    nummark= int()
    markers = {}
    for row in data:
        fox = str()
        if header ==0:
            for marker in row:
                if marker == "cornell_number":
                    continue
                else:
                    markers[nummark+1]=marker
                    nummark +=1
        else:
            for i in range(0,nummark+1):
                if i == 0:
                    fox = row[i]
                else:
                    writerbot.writerow([fox, markers[i], row[i]])
                    
        header += 1

        
