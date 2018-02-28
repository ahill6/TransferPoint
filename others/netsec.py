from sklearn.svm import OneClassSVM
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
import numpy as np

def synScan():
    # read synscan
    file = 'synScan.txt'

    a = []

    with open(file, 'r') as cin:
        a = [int(v.strip()) for v in cin]

    b = list(set(range(max(a))) - set(a))

    with open('notSynScan.txt', 'w') as cout:
        cout.write('\n'.join([str(c) for c in b]))

def is_outlier(points, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor.
    """
    #if len(points) == 1:
    #    points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    #modified_z_score = 0.6745 * diff / med_abs_deviation
    modified_z_score = 06745 * points / med_abs_deviation

    #return modified_z_score > thresh
    print(sum([1 if x > thresh else 0 for x in modified_z_score]))
    return modified_z_score > thresh

def analyzeAllIPs():
    adfd

def analyzeConversations():
    file = 'conversations.txt'
    a = []
    with open(file, 'r') as cin:
        #skip first 5 lines
        for i in range(5):
            cin.readline()
        a = [c.strip().split(' ') for c in cin]
    del a[-1]

    for i in range(len(a)):
        a[i] = filter(None, a[i]) # fastest

    print("creating datasets")
    duration, sendersFr, sendersBy, receiversFr, receiversBy, talkersFr, talkersBy, overall  = [],[],[],[],[],[],[],[]
    techniques = {'OneClSVM': OneClassSVM()}
    ''',
    'ElipEnv':EllipticEnvelope(),
    'IsoFor':IsolationForest()}
    '''
    datasets = [duration, sendersFr, sendersBy, receiversFr, receiversBy, talkersFr, talkersBy, overall]

    for i in a:
        if len(i) < 11:
            print(i)
            continue
        duration.append(float(i[-1]))
        sendersFr.append(int(i[5]))
        sendersBy.append(float(i[6]))
        receiversFr.append(int(i[3]))
        receiversBy.append(float(i[4]))
        talkersFr.append(int(i[7]))
        talkersBy.append(float(i[8]))
        #overall.append([i[j] for j in (0,2,3,4,5,6,-2,-1)])

    print("beginning analysis")
    ans = []
    for d in range(len(datasets)):
        #print(d)
        #if d == len(datasets)-1:
        #    continue
        t1 = is_outlier(datasets[d])
        ans.append([i for i,x in enumerate(t1) if x])

    with open('answers.txt','w') as cout:
        cout.write('\n'.join([','.join([i]) for i in ans]))

    exit()

    for d in datasets:
        for t in techniques:
            techniques[t].fit(overall)
            ans = techniques[t].predict(overall)
            print(ans)
            exit()


    #FORMAT: ip1	<-> ip2	frames<- bytes<-  frames->  bytes->  totalFr  totalBy  relStart  Duration
    #['192.168.23.202', '<->', '192.168.202.102', '132780', '15981060', '141530', '112264122', '274310', '128245182', '0.010000000', '1727.6800']
    #DURATION [0+1,-1]
    #SEND TOO MUCH [0,5,6] (then combine items with same 0)
    #RECEIVE TOO MUCH [0,3,4] (then combine items with same 0)
    #LOTS OF TALKING [totalByte] <-- find outliers, match to conversations
    #overall? [0,2,3,4,5,6,-2,-1] <-- go through, see if any predict the others


def analyzeEndpoints():
    asdfasdf

def analyzeHosts():
    asdfasdf

#analyzeConversations()

for x in list of files ending in '.log':
    open them, break them into 1 minute bins, output amount of traffic per 1 minute bin with
    offset for when bins start (i.e. time of earliest bin) -- maybe don't do this is seconds
    1 second bins, 1 minute bins 
