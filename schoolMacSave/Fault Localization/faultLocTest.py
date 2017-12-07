'''
1) make this batch script in every folder
-- have an example
2) batch script to call this batch script in every folder
3) python script to go through the gcov files and write the dataset
'''
import os, subprocess, signal, threading
from collections import Counter
from c_run import run_command_with_timeout
from math import sqrt, log
import sys

kill_check = threading.Event()


def timeout_function(p):
    if p.poll() is None:
        try:
            #os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            #os.kill(p.pid, signal.CTRL_BREAK_EVENT)
            os.system("taskkill /im faultLocalizationDBCreator.bat")
            print('Error: process taking too long to complete--terminating')
            kill_check.set()
        except OSError as e:
            print(e)
            return


def timeout_interrupt(p):
    if p.poll() is None:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGINT)
            print('Error: process taking too long to complete--terminating')
        except OSError as e:
            return


def counter_subset(list1, list2):
    c1, c2 = Counter(list1), Counter(list2)
    for k, n in c1.items():
        if n < c2[k]:
            return False
    for k, n in c2.items():
        if n > c1[k]:
            return False
    return True


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def read(fn):
    with open(fn,'r',encoding="utf8") as cin:
        text = [c for c in cin]
    return text




base_dir = 'C:\\Users\\Andrew\\Downloads\\codeflaws\\'
#base_dir = 'C:\\Users\\Andrew\\Documents\\Schools\\Grad School\\NCSU - Comp Sci\\Research\\Fault Localization'
out_file = 'C:\\Users\\Andrew\\Documents\\Schools\\Grad School\\NCSU - Comp Sci\\Research\\Fault Localization\\codeflaws2.txt'
template_file = 'C:\\Users\\Andrew\\Documents\\Schools\\Grad School\\NCSU - Comp Sci\\Research\\Fault Localization\\faultLocalizationTemplate-windows.bat'

def massProduceBatchFiles(base_dir, template_file):
    template = read(template_file)
    for d in get_immediate_subdirectories(base_dir):
        print(d)
        tmp = d.split('-')
        numPosTests = len([i for i in os.listdir(os.path.join(base_dir,d)) if 'heldout' not in i if 'input-pos' in i if 'my_output' not in i])
        numNegTests = len([i for i in os.listdir(os.path.join(base_dir,d)) if 'heldout' not in i if 'input-neg' in i if 'my_output' not in i])
        buggyFile =  '-'.join(tmp[:2] + [tmp[3]])
        patchedFile = '-'.join(tmp[:2] + [tmp[-1]])
        with open(os.path.join(base_dir,d,"faultLocalizationDBCreator.bat"),'w') as cout:
            for te in template:
                cout.write(te.replace('numPosTests',str(numPosTests)).replace('numNegTests',str(numNegTests)).replace('buggyFile',buggyFile+'.c').replace('buggyFleMin',buggyFile).replace('patchedFile',patchedFile+'.c'))

knownFailures = ['103-A-bug-18288288-18288294','118-A-bug-18071189-18071250','12-C-bug-1919840-1919852','122-A-bug-17968248-17968373','122-B-bug-1446831-1446834',
        '131-D-bug-10939480-10939524','131-E-bug-1151811-1151812','133-A-bug-17969403-17975791','136-B-bug-1117154-1117156',
         '141-A-bug-17550753-17550774','149-B-bug-1170222-1170231','165-B-bug-10695403-10695423','171-C-bug-15508274-15508297',
         '182-D-bug-1966493-1966534','185-A-bug-1914016-1914022','190-C-bug-1704844-1704847','192-C-bug-1743547-1743565',
         '192-C-bug-1764940-1764944','194-D-bug-1761507-1761527','20-A-bug-13625510-13625531','21-A-bug-1835149-1835180',
         '218-A-bug-2052209-2052217','219-A-bug-15266694-15266709','24-D-bug-103331-103377','242-A-bug-16500031-16500336',
         '242-A-bug-7284170-7284175','257-B-bug-2893394-2893555','257-C-bug-2895327-2895332','258-A-bug-18295429-18295457',
         '263-C-bug-2945363-2945487','268-A-bug-18293322-18293350','269-A-bug-3222520-3222525','282-B-bug-14583951-14584067',
         '282-B-bug-14695553-14695568','285-A-bug-3845963-3845975','285-B-bug-15537732-15538242','288-C-bug-3459393-3459497',
         '289-E-bug-3467587-3467599','291-B-bug-5094504-5095107','291-C-bug-12020290-12020359','291-C-bug-3539579-3539599',
         '293-A-bug-3825824-3825830','298-A-bug-5138379-5138386','299-A-bug-14347069-14347114','30-A-bug-14267923-14268715',
         '304-A-bug-14290012-14290016','331-C1-bug-4092299-4092486','339-B-bug-18022309-18022318','339-D-bug-4534806-4534829',
         '34-B-bug-17597636-17597702','340-A-bug-15598421-15598438','340-B-bug-9369797-9369822','342-B-bug-4426110-4426125',
         '357-A-bug-17835626-17835664','357-B-bug-17317912-17317915','358-B-bug-5017905-5017917','359-A-bug-5182085-5182096',
         '363-A-bug-9556316-9556344','366-B-bug-5357852-5357857','369-C-bug-5354958-5359647','37-A-bug-16085824-16085923',
         '370-B-bug-5376603-5376642','371-C-bug-5389891-5390013','376-C-bug-7329404-7329433','379-B-bug-6978141-6978150',
         '379-B-bug-9358367-9358407','38-B-bug-6659899-6677432','382-A-bug-8368809-8368827','384-B-bug-5754794-5755196',
         '393-A-bug-14052177-14052206','401-C-bug-12842371-12842402','401-C-bug-16438208-16438233','403-A-bug-6100742-6100800',
         '404-B-bug-12272628-12272658','404-B-bug-14578678-14578704','404-B-bug-6125713-6125721','404-B-bug-6259125-6259373',
         '404-B-bug-9794164-9794203','404-C-bug-11837655-11837677','413-C-bug-6427798-6427987','414-A-bug-8342658-8342695',
         '416-C-bug-6343870-6347436','427-B-bug-12334151-12334160','430-B-bug-10625991-10626001','432-B-bug-12883038-12883124',
         '439-C-bug-6867884-6867935','441-C-bug-11338932-11338959','448-A-bug-16630703-16630712','450-A-bug-17137475-17137504',
         '454-C-bug-7452422-7452449','456-A-bug-18227110-18227127','462-B-bug-17911104-17911122','464-A-bug-7812986-7813009',
         '472-B-bug-9390780-9390795','483-A-bug-15165128-15165240','483-C-bug-11168180-11168213','488-A-bug-15322815-15322872',
         '488-A-bug-15683618-15683685','488-A-bug-15694141-15694156','488-A-bug-16435750-16442472','488-A-bug-17499195-17499231',
         '49-A-bug-11842934-11842941','493-B-bug-15602247-15602350','496-B-bug-11341123-11341181','50-A-bug-17963690-17963710',
         '500-A-bug-17067750-17067776','500-A-bug-17197349-17197373','500-A-bug-18298093-18298124','505-B-bug-11838805-11838927',
         '508-C-bug-9606566-9606584','518-E-bug-10046940-10047080','519-B-bug-15906702-15907261','520-B-bug-15514872-15514956',
         '548-A-bug-13402608-13402780','55-A-bug-267060-267063','550-A-bug-17137160-17137213','551-A-bug-13415047-13415071',
         '552-A-bug-12313531-12313565','570-A-bug-16196292-16196313','579-B-bug-14171209-14171224','58-B-bug-13514418-13514452',
         '586-C-bug-13615252-13615263','588-B-bug-14559572-14559603','588-B-bug-15570992-15571069','593-B-bug-14669840-14669876',
         '598-C-bug-17600539-17600555','598-C-bug-17600586-17600597','6-C-bug-11536006-11536039','61-D-bug-13942552-13942558',
         '612-A-bug-17136026-17136126','618-C-bug-15910677-15910744','625-A-bug-17251074-17251099','626-B-bug-16061439-16061452',
         '630-B-bug-17359301-17359319','630-R-bug-17825199-17825235','633-A-bug-17465999-17468921','652-A-bug-16935508-16935759',
         '652-A-bug-16949859-16949977','652-A-bug-16950639-16950705','660-A-bug-17240602-17240979','670-C-bug-17764828-17764874',
         '670-D1-bug-17917073-17917152','670-E-bug-17742117-17743180','670-E-bug-18043530-18043600','677-A-bug-18331987-18332002',
         '677-E-bug-18204655-18204717','7-B-bug-17996348-17996371','75-A-bug-14683488-14683500','78-A-bug-17026157-17026164',
         '82-B-bug-1147223-1147225','99-A-bug-3759651-3759654']

def runMama():

    failures = []
    timeout = 15
    var = ""

    go = True
    for d in get_immediate_subdirectories(base_dir):
        print(d)
        if not go:
            if '285-B-bug-15537732-15538242' in d:
                go = True
            continue
        if d in knownFailures:
            continue
        #if not run_command_with_timeout("cd " + os.path.join(base_dir,d) + "& faultLocalizationDBCreator.bat", timeout):
        #    failures.append(d)
        # run the XXX file in that folder (timeout of X sec)
        with open(os.path.join(base_dir,d,"stdout.txt"), 'w') as stdout_file:
            proc = subprocess.Popen("cd "+os.path.join(base_dir,d)+" & faultLocalizationDBCreator.bat", shell=True, stdout=stdout_file)
            t = threading.Timer(timeout, timeout_function, [proc])
            t.start()
            (out, err) = proc.communicate()
        t.cancel()

        #os.system('rm -r ' + output_dir)
        if err:
            failures.append(d)

    print(failures)

'''
# open positives
split on whitespace (multiple whitespace characters?), combine all into one (?)
0 is the number of times a line was executed (variable declarations, blank lines, and "else" statements aren't counted')
ex. "1:"
1 is the line number (ex. "12:")
2 is the line of code (well, possibly including more spaces, but still)
--store as tuples
"#####" in 0 means that line was never executed (so, replace with 0)
'''

def runGcov(filename):
    '''Analyzes .gcov files

    These files are of the form
        executionCount:   lineNum:  code
    Sometimes the space between lineNum and code is absent

    Initial header-type information gives the file executed, number of unit tests run to get the data displayed, etc.
    This only keeps the number of runs, because it is the only part that is relevant to the present work.
    '''
    pairs, runcount = [], 0
    try:
        with open(filename, 'r', encoding="utf8") as cin:
            data = [list(filter(None,c.strip().split(' '))) for c in cin]
    except FileNotFoundError:
        return pairs, runcount

    for datum in data:
        if 'Runs' in datum[1]:
            runcount = int(datum[1].split(":")[-1])
            continue
        try:
            count = int(datum[0].replace(':','').replace("#####","0"))
            line = int(datum[1].split(':')[0])
            pairs.append([count, line])
        except ValueError:
            continue
    return pairs, runcount

def runTrue(filename):
    '''This analyzes a pc (windows version of diff) file that compares buggy-patched programs of the following form
    *****106 - A - 18253717.c
        41:
        42:          else if (s2[1] == s1[0] & & s1[0] != s3[0])
        43: printf("YES");
    *****106 - A - 18253726.c
        40:
        41:          else if (s2[1] == s1[0] & & s1[0] != s3[1])
        42: printf("YES");
    *****

    The first file is the buggy one, and the faulty line is the middle of the first section.  If there are multiple bugs,
    they will be the middle (i.e. start + 2) line of the even-indexed instances of ***** .  Thus the return statement.
    '''
    bugs = []
    with open(filename, 'r', encoding="utf8") as cin:
        data = [c.strip() for c in cin]

    lines =  [i+2 for i, x in enumerate(data) if '***** ' in x][::3]

    for l in lines:
        t = data[l].strip().split(":")[0]
        if "***" not in t:
            bugs.append(t)

    return bugs


def generateFLDataset(baseDir, outfile):
    dataset = []
    go = True
    cout = open (outfile, 'w')
    cout.write("posgcov,numPosRuns,neggcov,numNegRuns,trueBuggyLines\n")

    for d in get_immediate_subdirectories(baseDir):
        print(d)
        go = True
        if not go:
            if '535-B-bug-16455139-16455151' in d:
                go = True
            else:
                continue

        contents = list(filter(bool,[a for a in os.listdir(os.path.join(baseDir,d)) if ('.gcov' in a or '.txt' in a) if '.c.gov' not in a]))
        posStuff, negStuff, trueStuff = [], [], []
        positives, negatives = 0, 0
        for c in contents:
            print(c)
            if 'pos' in c:
                posStuff, positives = runGcov(os.path.join(baseDir,d,c))
            elif 'neg' in c:
                negStuff, negatives = runGcov(os.path.join(baseDir, d, c))
            elif 'true' in c:
                trueStuff = runTrue(os.path.join(baseDir, d, c))
            else:
                print("uh...what is this??")
                print(c)
        cout.write(','.join([str(e[0])+"-"+str(e[1]) for e in posStuff]))
        cout.write(";" + str(positives) + ";")
        cout.write(','.join([str(e[0]) + "-" + str(e[1]) for e in negStuff]))
        cout.write(";" + str(negatives) + ";")
        cout.write(','.join([str(e) for e in trueStuff]) + "\n")
        #dataset.append([posStuff,positives,negStuff,negatives,trueStuff])
    cout.close()

def sizeOfBuggyFile(file):
    with open(file, 'r', encoding='utf8') as cin:
        l = len([c for c in cin])
    return l

def readStdOutFile(directory):
    tests = {'+':[], '-':[]}
    with open(os.path.join(directory, "stdout.txt"), 'r') as cin:
        data = [c.strip() for c in cin]
    for d in range(len(data)):
        if 'input-' in data[d]:
            if 'PASS' in data[d+1]:
                tests['+'].append(data[d].replace('input-pos','p').replace('input-neg','n'))
            elif 'FAIL' in data[d+1]:
                tests['-'].append(data[d].replace('input-pos','p').replace('input-neg','n'))
    return tests

def doSuspiciousness(inputDir, outdir, skips):
    # {'+': 0, '-':0}
    suspiciousness = {}
    suspiciousnessRaw = {}
    go = True
    cout = open(os.path.join(outdir,'suspiciousnessScores.txt'), 'w')
    coutRaw = open(os.path.join(outdir, 'suspiciousnessRawScores.txt'), 'w')
    # go through subfolders
    # for each, folder, make a list of lines executed + and -
    for d in get_immediate_subdirectories(inputDir):
        if d in skips:
            continue
        print(d)
        if not go:
            if '31-A-bug-17852743-17861117' in d:
                go = True
                continue
            else:
                continue
        passFail = readStdOutFile(os.path.join(inputDir,d))

        g = [a for a in os.listdir(os.path.join(inputDir, d)) if ('.gcov' in a or '.txt' in a) if '.c.gcov' not in a if 'pos' not in a if 'neg' not in a]
        suspiciousness[d] = [{'+': 0, '-': 0} for _ in range(
            sizeOfBuggyFile(os.path.join(inputDir, d, '-'.join(d.split('-')[:2] + [d.split('-')[3]]) + ".c")) + 1)]
        suspiciousness[d][0]['totalPassed'] = 0
        suspiciousness[d][0]['totalFailed'] = 0
        suspiciousnessRaw[d] = [{'+': 0, '-':0} for _ in range(sizeOfBuggyFile(os.path.join(inputDir,d, '-'.join(d.split('-')[:2] + [d.split('-')[3]])+".c"))+1)]
        suspiciousnessRaw[d][0]['totalPassed'] = 0
        suspiciousnessRaw[d][0]['totalFailed'] = 0

        contents = list(filter(bool,[a for a in os.listdir(os.path.join(inputDir,d)) if ('.gcov' in a or 'trueBugs.txt' in a) if '.c.gcov' not in a if 'pos' not in a if 'neg' not in a]))

        for c in contents:
            print(c)
            try:
                if any([a in c for a in passFail['+']]):
                    posStuff, _ = runGcov(os.path.join(inputDir,d,c))
                    for p in posStuff:
                        suspiciousness[d][p[1]]['+'] += 1
                        suspiciousnessRaw[d][p[1]]['+'] += p[0]
                    suspiciousness[d][0]['totalPassed'] += 1
                elif any([a in c for a in passFail['-']]):
                    negStuff, _ = runGcov(os.path.join(inputDir, d, c))
                    for n in negStuff:
                        suspiciousness[d][n[1]]['-'] += 1
                        suspiciousnessRaw[d][n[1]]['-'] += n[0]
                    suspiciousness[d][0]['totalFailed'] += 1
                elif 'true' in c:
                    trueStuff = runTrue(os.path.join(inputDir, d, c))
                    suspiciousness[d].append(trueStuff)
                    suspiciousnessRaw[d].append(trueStuff)
                else:
                    print("uh...what is this??")
                    print(c)
            except IndexError as e:
                print(e)
                exit()
        tmp = [(i,sqrt((a['-'] / (suspiciousness[d][0]['totalFailed'] + 0.0)) * (a['-'] / (a['-'] + a['+'] + 0.0))) if a['-'] +a['+'] > 0
                    and suspiciousness[d][0]['totalFailed'] > 0 else 0) for i, a in enumerate(suspiciousness[d][:-1])]
        tmp.sort(reverse=True, key=lambda student: student[1])
        data = [str(t[0]) + "-" + str(t[1]) for t in tmp if t[1] > 0]
        cout.write(d+";"+','.join(data)+";" + ",".join([str(a) for a in suspiciousness[d][-1]])+"\n")

        tmpRaw = [(i,sqrt((a['-'] / (suspiciousnessRaw[d][0]['totalFailed'] + 0.0)) * (a['-'] / (a['-'] + a['+'] + 0.0))) if a['-'] +a['+'] > 0
                    and suspiciousnessRaw[d][0]['totalFailed'] > 0 else 0) for i, a in enumerate(suspiciousnessRaw[d][:-1])]
        tmpRaw.sort(reverse=True, key=lambda student: student[1])
        dataRaw = [str(t[0]) + "-" + str(t[1]) for t in tmp if t[1] > 0]
        coutRaw.write(d+";"+','.join(dataRaw)+";" + ",".join([str(a) for a in suspiciousnessRaw[d][-1]])+"\n")

    cout.close()


def doTfIdf(inputDir,outdir, skips):
    # {'+': 0, '-':0}
    suspiciousness = {}
    suspiciousnessRaw = {}
    go = True
    # go through subfolders
    # for each, folder, make a list of lines executed + and -
    for d in get_immediate_subdirectories(inputDir):
        if d in skips:
            continue
        print(d)
        if not go:
            if '622-B-bug-16391438-16391464' in d:
                go = True
                continue
            else:
                continue
        passFail = readStdOutFile(os.path.join(inputDir, d))

        suspiciousness[d] = [{'+': 0, '-': 0} for _ in range(
            sizeOfBuggyFile(os.path.join(inputDir, d, '-'.join(d.split('-')[:2] + [d.split('-')[3]]) + ".c")) + 1)]
        suspiciousness[d][0]['totalPassed'] = 0
        suspiciousness[d][0]['totalFailed'] = 0
        suspiciousnessRaw[d] = [{'+': 0, '-':0} for _ in range(sizeOfBuggyFile(os.path.join(inputDir,d, '-'.join(d.split('-')[:2] + [d.split('-')[3]])+".c"))+1)]
        suspiciousnessRaw[d][0]['totalPassed'] = 0
        suspiciousnessRaw[d][0]['totalFailed'] = 0

        contents = list(filter(bool,[a for a in os.listdir(os.path.join(inputDir,d)) if ('.gcov' in a or 'trueBugs.txt' in a) if '.c.gcov' not in a if 'pos' not in a if 'neg' not in a]))

        for c in contents:
            print(c)
            try:
                if any([a in c for a in passFail['+']]):
                    posStuff, _ = runGcov(os.path.join(inputDir,d,c))
                    suspiciousness[d][0]['totalPassed'] += 1
                    suspiciousnessRaw[d][0]['totalPassed'] += 1
                    for p in posStuff:
                        suspiciousness[d][p[1]]['+'] += 1
                        suspiciousnessRaw[d][p[1]]['+'] += p[0]
                elif any([a in c for a in passFail['-']]):
                    negStuff, _ = runGcov(os.path.join(inputDir, d, c))
                    suspiciousness[d][0]['totalFailed'] += 1
                    suspiciousnessRaw[d][0]['totalFailed'] += 1
                    for n in negStuff:
                        suspiciousness[d][n[1]]['-'] += 1
                        suspiciousnessRaw[d][n[1]]['-'] += n[0]
                elif 'true' in c:
                    trueStuff = runTrue(os.path.join(inputDir, d, c))
                    suspiciousness[d].append(trueStuff)
                    suspiciousnessRaw[d].append(trueStuff)
                else:
                    print("uh...what is this??")
                    print(c)
            except IndexError as e:
                print(e)
                exit()


    '''
    try (# times part of a failing test) * (number of times this line executed overall)
    try (this might work better)
    tf = K + (1 - K) * (number of times this line executed as part of failing test / max number of times a line executed as part of a failing test)
    idf = log(number of tests / number of tests in which this line is executed)
    tf * idf  -- try idf both with and without log
    '''

    K = 0.5
    idf1 = {}
    idflog = {}
    idfNotlog = {}
    idf1Raw = {}
    idflogRaw = {}
    idfNotlogRaw = {}

    for s in suspiciousness:
        tmp1 = [(i, (a['-'] / (0.0 + a['-'] + a['+'])) if a['-'] + a['+'] > 0 and suspiciousness[s][0]['totalFailed'] > 0 else 0) for i, a in enumerate(suspiciousness[s][:-1])]
        tmp1Raw = [(i, (a['-'] / (0.0 + a['-'] + a['+']))
            if a['-'] + a['+'] > 0 and suspiciousness[s][0]['totalFailed'] > 0 else 0) for i, a in enumerate(suspiciousness[s][:-1])]
        tmplog = [(i, K + (1 - K) * ((a['-'] / (max([b['-'] for b in suspiciousness[s][:-1]]) + 0.0))) * log(
            (suspiciousness[s][0]['totalFailed'] + suspiciousness[s][0]['totalPassed']) / (a['-'] + a['+'] + 0.0))
            if a['-'] + a['+'] > 0 and suspiciousness[s][0]['totalFailed'] > 0 else 0)
                  for i, a in enumerate(suspiciousness[s][:-1])]
        tmplogRaw = [(i, K + (1 - K) * ((a['-'] / (max([b['-'] for b in suspiciousness[s][:-1]]) + 0.0))) * log(
            (suspiciousness[s][0]['totalFailed'] + suspiciousness[s][0]['totalPassed']) / (a['-'] + a['+'] + 0.0))
            if a['-'] + a['+'] > 0 and suspiciousness[s][0]['totalFailed'] > 0 else 0)
                  for i, a in enumerate(suspiciousness[s][:-1])]

        tmpNotlog = [(i, K + (1 - K) * ((a['-'] / (max([b['-'] for b in suspiciousness[s][:-1]]) + 0.0))) * (
            (suspiciousness[s][0]['totalFailed'] + suspiciousness[s][0]['totalPassed']) / (a['-'] + a['+'] + 0.0))
            if a['-'] + a['+'] > 0 and suspiciousness[s][0]['totalFailed'] > 0 else 0)
                  for i, a in enumerate(suspiciousness[s][:-1])]

        tmpNotlogRaw = [(i, K + (1 - K) * ((a['-'] / (max([b['-'] for b in suspiciousness[s][:-1]]) + 0.0))) * (
            (suspiciousness[s][0]['totalFailed'] + suspiciousness[s][0]['totalPassed']) / (a['-'] + a['+'] + 0.0))
            if a['-'] + a['+'] > 0 and suspiciousness[s][0]['totalFailed'] > 0 else 0)
                  for i, a in enumerate(suspiciousness[s][:-1])]


        tmp1.sort(reverse=True, key=lambda student: student[1])
        tmplog.sort(reverse=True, key=lambda student: student[1])
        tmpNotlog.sort(reverse=True, key=lambda student: student[1])
        tmp1Raw.sort(reverse=True, key=lambda student: student[1])
        tmplogRaw.sort(reverse=True, key=lambda student: student[1])
        tmpNotlogRaw.sort(reverse=True, key=lambda student: student[1])

        idf1[s] = [str(t[0])+"-"+str(t[1]) for t in tmp1 if t[1] > 0]
        idflog[s] = [str(t[0])+"-"+str(t[1]) for t in tmplog if t[1] > 0]
        idfNotlog[s] = [str(t[0])+"-"+str(t[1]) for t in tmpNotlog if t[1] > 0]
        idf1Raw[s] = [str(t[0])+"-"+str(t[1]) for t in tmp1 if t[1] > 0]
        idflogRaw[s] = [str(t[0])+"-"+str(t[1]) for t in tmplog if t[1] > 0]
        idfNotlogRaw[s] = [str(t[0])+"-"+str(t[1]) for t in tmpNotlog if t[1] > 0]


    with open(os.path.join(outdir,'idf.txt'), 'w') as cout:
        for d in idf1:
            cout.write(d+";"+','.join(idf1[d])+";"+str(suspiciousness[d][-1])+"\n")

    with open(os.path.join(outdir,'idfLog.txt'), 'w') as cout:
        for d in idflog:
            cout.write(d+";"+','.join(idflog[d])+";"+str(suspiciousness[d][-1])+"\n")

    with open(os.path.join(outdir,'idfNotLog.txt'), 'w') as cout:
        for d in idfNotlog:
            cout.write(d+";"+','.join(idfNotlog[d])+";"+str(suspiciousness[d][-1])+"\n")

    with open(os.path.join(outdir,'idfRaw.txt'), 'w') as cout:
        for d in idf1Raw:
            cout.write(d+";"+','.join(idf1Raw[d])+";"+str(suspiciousnessRaw[d][-1])+"\n")

    with open(os.path.join(outdir,'idfLogRaw.txt'), 'w') as cout:
        for d in idflogRaw:
            cout.write(d+";"+','.join(idflogRaw[d])+";"+str(suspiciousnessRaw[d][-1])+"\n")

    with open(os.path.join(outdir,'idfNotLogRaw.txt'), 'w') as cout:
        for d in idfNotlogRaw:
            cout.write(d+";"+','.join(idfNotlogRaw[d])+";"+str(suspiciousnessRaw[d][-1])+"\n")

outdir = 'C:\\Users\\Andrew\\Documents\\Schools\\Grad School\\NCSU - Comp Sci\\Research\\Fault Localization\\Scores'
#massProduceBatchFiles(base_dir,template_file)
#runMama()

# still need to add something that goes through the stdout.txt file in each directory and gets which unit tests passed/did not.
# ALSO, if there is not a stdout.txt, skip?

#generateFLDataset(base_dir, out_file)

doSuspiciousness(base_dir, outdir, knownFailures)
doTfIdf(base_dir, outdir, knownFailures)



'''

'''
# setup seems consistent.  Actual error is on second line of first (first?)
# section (double check that first section is the buggy one) (e.g. here, 42)
