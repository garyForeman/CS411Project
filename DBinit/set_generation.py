"""Converts the Set206.csv and Set207.csv file from having columns
cornellnumber, pedigree, fatherpedigree, motherpedigree to having columns
cornellnumber, pedigree, generation. Generation 1 corresponds to a grandparent,
generation 2 is a parent, generation 3 is a child."""

GRANDPARENT = 1
PARENT = 2
CHILD = 3

def set_generation(filename):
    with open(filename) as set206:
        lines = set206.readlines()[1:]

    outfilename = filename.split('.')
    outfilename = outfilename[0] + '_gen.' + outfilename[1]
    with open(outfilename, 'w') as outfile:
        outfile.write('cornellnumber,pedigree,generation\n')
        for line in lines:
            line = line.strip().split(',')
            outfile.write(line[0] +',')
            #Note an empty string evaluates to false
            if line[1]:
                outfile.write(line[1] + ',')
                if line[2] or line[3]:
                    outfile.write('{0}\n'.format(PARENT))
                else:
                    outfile.write('{0}\n'.format(GRANDPARENT))
            elif line[2]:
                outfile.write(line[2] + ',{0}\n'.format(CHILD))
            elif line[3]:
                outfile.write(line[3] + ',{0}\n'.format(CHILD))
            else:
                outfile.write(',,\n')

if __name__ == '__main__':
    set_generation('Set206.csv')
    set_generation('Set207.csv')
