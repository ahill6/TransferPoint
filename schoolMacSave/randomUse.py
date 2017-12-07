from os import listdir
from os.path import isdir, split as ossplit, join as osjoin

def makeTestsList(heldout=False):
    baseDir = '/Users/ahill6/Documents/Python/afsoonRepair/codeflaws/'
    #for each folder in baseDir
    directories = [d for d in listdir(baseDir) if isdir(baseDir+d)]

    for di in directories:
        print(di)
        if heldout:
            files = [d.replace("pos","p").replace("neg","n").replace("heldout-input-","") for d in listdir(baseDir+di)
            if 'heldout' in d if 'input' in d if 'my_output' not in d]
            with open(baseDir+di+"/heldout-tests-list.txt", 'w') as cout:
                cout.write("\n".join(files))
        else:
            files = [d.replace("pos","p").replace("neg","n").replace("input-","") for d in listdir(baseDir+di)
            if 'heldout' not in d if 'input' in d if 'my_output' not in d]
            with open(baseDir+di+"/tests_list.txt", 'w') as cout:
                cout.write("\n".join(files))
    print("done")

def makeSearchRepairSH(heldout=False):
    baseDir = '/Users/ahill6/Documents/Python/afsoonRepair/codeflaws/'
    #inputFile = '/Users/ahill6/Downloads/test-searchrepair.sh'
    inputFile = '/Users/ahill6/Documents/Python/afsoonRepair/patches/validation-template.sh'
    #inputFile = '/Users/ahill6/Documents/Python/afsoonRepair/patches/prepatch-template.sh'
    with open(inputFile, 'r') as cin:
        template = [d for d in cin]

    #for each folder in baseDir
    directories = [d for d in listdir(baseDir) if isdir(baseDir+d)]

    for di in directories:
        print(di)
        testsList = []
        if heldout:
            with open(baseDir+di+"/heldout-tests-list.txt", 'r') as cin:
                testsList = [d.strip() for d in cin]
        else:
            with open(baseDir+di+"/tests_list.txt", 'r') as cin:
                testsList = [d.strip() for d in cin]
        for te in range(len(testsList)):
            if 'n' in testsList[te]:
                testsList[te] = testsList[te] + ') run_test "$NEGINPUT_NAME"'+testsList[te].replace("n","")+ ' "$MY_PATH/$NEGOUTPUT_NAME"'+testsList[te].replace("n","")+' ;;'
            elif 'p' in testsList[te]:
                testsList[te] = testsList[te] + ') run_test "$INPUT_NAME"'+testsList[te].replace("p","")+ ' "$MY_PATH/$OUTPUT_NAME"'+testsList[te].replace("p","")+' ;;'
        #with open(baseDir+di+"/test-searchrepair.sh", 'w') as cout:
        with open(baseDir+di+"/validation.sh", 'w') as cout:
        #with open(baseDir+di+"/prepatch.sh", 'w') as cout:
            for t in template:
                if 'XXXXXX' in t:
                    cout.write(t.replace('XXXXXX', "-".join(di.split("-")[:2]+[di.split('-')[3]])+'.c'))
                elif 'YYYYYY' in t:
                    cout.write(t.replace('YYYYYY', "-".join(di.split("-")[:2]+[di.split('-')[3]])))
                elif 'ZZZZZZ' in t:
                    cout.write(t.replace('ZZZZZZ', "\n".join(testsList)))
                else:
                    cout.write(t)
    print("done")

def summarizeAfsoonRepairLogs(filename):
    keepers = [":*****************************",'Tests Positives','Negative: [','Suspicious lines : [','Suspicious block range (',
    'profile.profile:[{',':Candidate snippets ','were unsatistfiable from',':No block found for',
    ':Total time','Start time']

    tmp = ossplit(filename)
    fixedFile = osjoin(tmp[0],tmp[1].replace('.log','-summary.log'))
    cout = open(fixedFile,'w')
    # get what bug we're talking about

    with open(filename, 'r') as cin:
        for c in cin:
            if any([a in c for a in keepers]):
                cout.write(c)
    cout.close()

#-- takes DKT almost exactly 2 minutes (call it 00:02:15) to run 1 epoch
#-- when fixed so that it actually does a test/train split, only takes about 00:01:04 sec
# 42.37 GB --> 862.9 MB
    # record the suspicious-lines output

    # record final number of fine-nopos-noneg-err (will have to input manually)


#makeTestsList()
makeSearchRepairSH(True)
exit()
filename = '/Users/ahill6/Documents/Python/afsoonRepair/results_logs/HBRN.log'
summarizeAfsoonRepairLogs(filename)
#print("no tasks active.  View source file")
'''
p1
p2
p3
n1
1) make the tests_list files (make them p1, n1, etc) -- or don't, whatever

2) read randomUse.sh
    - for each line, if it has XXXXXX, replace with the first part of the directory (parse rules here)
    - if it has YYYYYY, replace with XXXXXX's replacement ".replace(".c", "")"
    - if it has ZZZZZZ, delete that, and instead read in the tests_lists file and put those in the
        appropriate format
    - write that whole thing to a test-searchrepair.sh file in the same directory
'''
