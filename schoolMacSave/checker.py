'''
from numpy import mean, std

def mode(lst):
    lst.sort()
    if len(lst)%2 == 1:
        return lst[len(lst)//2]
    else:
        return 0.5*(lst[len(lst)//2 - 1] + lst[len(lst)//2])

vals = [33,18,59,40,5,9,57,85,28,470,102,12,244,8,118,21,9,21,14,308,18,6,159,
179,31,9,17,101,193,7,21,226,325,409,128,13,12,77,311]
mode(vals)
print(min(vals)) # 5
print(max(vals)) # 470
print(mean(vals))# 100
print(std(vals)) # 122
print(mode(vals))# 33
exit()

# only doing classes with > 25 instances gets rid of 17/39 defect classes
'''
from numpy.random import choice
from os import makedirs, walk, listdir
from os.path import exists as ospathexists, dirname, join as pathjoin


def makeSettingsFile(file, outfolder, n):
    # read in settings template
    with open('settingsTemplate.py','r') as cin:
        lines = [c for c in cin]

    tmp = file.split('-')
    buggyFile = '-'.join(tmp[:2]+[tmp[-2]])
    bugType = outfolder.split('/')[-1]
    # output to outfolder/settingsX.py for some number X
    # replace keywords with "file"-derived data
    with open(pathjoin(outfolder,"settings" + str(n) + ".py"), 'w') as cout:
        for l in lines:
            cout.write(l.replace('bugFolder', file).replace('buggyFile',buggyFile).replace('bugType',bugType))



def makeExperimentalList():
    #open file
    with open('codeflaws-defect-detail-info.txt','r') as cin:
        data = [d.strip().split('\t') for d in cin]

    options = [{} for _ in range(len(data[0]))]

    #categorize
    for d in data:
        for e in range(len(d)):
            if e == 0 or e == 3:
                continue
            elif d[e] in options[e]:
                options[e][d[e]].append(d[0])
            else:
                options[e][d[e]] = [d[0]]

    theElected = {}
    for d in options[1].keys():
        #if len(options[1][d]) > 30:
        #    theElected[d] = choice(options[1][d], 30, replace=False)
        if len(options[1][d]) < 30:
            theElected[d] = options[1][d]

    with open('thingToRun2.txt','w') as cout:
        for d in theElected.keys():
            cout.write('***,'+str(d)+"\n")
            cout.write(",".join(theElected[d])+"\n")

    #report summary statistics
    #print(options[1])
    #print(options[2])
    #print(len(options[1]), len(options[2]))

def makeMakefiles(folder,pairs):
    # read Makefile in folder
    with open(pathjoin(folder,"Makefile"),'r') as cin:
        data = [c for c in cin]

    # replace x with y
    for d in range(len(data)):
        for p in pairs:
            data[d] = data[d].replace(p[0],p[1])

    # write back out to same file
    with open(pathjoin(folder,"Makefile"),'w') as cout:
        cout.write("".join(data))


'''
topFolder = '/Users/ahill6/Documents/Python/afsoonRepair/codeflaws'
p = []
p.append(["-fno-optimize-sibling-calls -fno-strict-aliasing -fno-asm -std=c99",'-fprofile-arcs -ftest-coverage'])
p.append(['-lm -s -O2','-lgcov --coverage'])
p.append(['-lgcov --coverage','-lm -lgcov --coverage'])
for root, dirs, _ in walk(topFolder):
    for d in dirs:
        tmp = pathjoin(root,d)
        lst = listdir(tmp)
        if 'Makefile' in lst:
            print(d)
            makeMakefiles(tmp,p)
        else:
            print("No")
            exit()
exit()
'''
#/Users/ahill6/Downloads/codeflaws


makeExperimentalList()
# open thingToRun.txt, for each name, make a settings.py file
with open('thingToRun2.txt','r') as cin:
    rawdata = [c.strip() for c in cin]


bugs = {}
currentBug = -1
base = pathjoin(dirname(__file__),"Settings")
for r in rawdata:
    if "***" in r:
        tmp = r.split(',')[1]
        bugs[tmp] = []
        currentBug = tmp
    else:
        tmp = r.split(',')
        bugs[currentBug].extend(tmp)

'''
for b in bugs:
    print(len(bugs[b]))
print("CHECK COMPLETE")
'''

for b in bugs:
    # make dir
    if not ospathexists(pathjoin(base,b)):
        makedirs(pathjoin(base,b))
    for i in range(len(bugs[b])):
        makeSettingsFile(bugs[b][i], pathjoin(base,b), i) # file string, folder to put in

'''
will be put in "/home/ahill6/searchrepair3/" + "settingsFiles/" + bugType

/home/ahill6/searchrepair3/...
or /home/ahill6/codeflaws/...
'''

'''
{'OAAN': 33, 'OLLN': 18, 'SISF': 59, 'SISA': 40, 'DRAC': 5, 'OMOP': 9, 'SRIF': 57, 'HBRN': 85,
'OAID': 28, 'DCCR': 470, 'SMOV': 102, 'OITC': 12, 'OAIS': 244, 'OIRO': 8, 'DRWV': 118,
'SDIF': 21, 'SDIB': 9, 'OEDE': 21, 'DMAA': 14, 'ORRN': 308, 'SIIF': 18, 'OICD': 6, 'STYP': 159,
 'DCCA': 179, 'HCOM': 31, 'SIRT': 9, 'SMVB': 17, 'SDFN': 101, 'HDMS': 193, 'HDIM': 7,
 'OFFN': 21, 'DRVA': 226, 'OILN': 325, 'HIMS': 409, 'OFPF': 128, 'SDLA': 13, 'OFPO': 12,
 'HEXP': 77, 'HOTH': 311}

 smallest: 5
 biggest:
'''
