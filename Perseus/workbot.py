from os.path import basename, join as pathjoin
from lxml import etree
import re
from vulcan import tryMe
import logging
from pathlib import Path 
from multiprocessing import Pool
from threading import Thread
from queue import Queue


def listFiles(dir, lang):
    print("almost")


def openFile(file):
    print("almost")


def preprocess(data):
    print("almost")


def process(data):
    print("almost")


def postprocess(data):
    print("almost")


def analysis(data):
    print("almost")


def output(what, where):
    print("almost")


#if __name__ == '__main__':
#    print("almost")


def write(lst, filename, append=False):
    '''
        input:  a list, where each element is either a word in greek or a list of greek words (representing different possible roots)
        output: None
        effect: write <lst> to <filename> in the format word,word,word-word-word (multiples),word...\n, where each line is in this format
        '''
    #print(type(lst[0]))
    
    with open(filename,'a' if append else 'w', encoding="utf-8") as cout:
        outstring = [t if not isinstance(t,list) else "-".join(t) for t in lst]
        outstring = ','.join(outstring) + "\n"
        #print(outstring)
        cout.write(outstring)

'''but first!!!

print out <p> and every tag below it, and find out how many words are in each.'''


def parseXML(xmlFile):
    def processMe(words, filename):
        tmp = [tryMe(w) for w in words]
        write(tmp,cheater,True)

    print(xmlFile)
    
    try:
        parser = etree.XMLParser(ns_clean=True,remove_comments=True,remove_blank_text=True,recover=True)
        tree = etree.parse(xmlFile.open(),parser)
    except Exception as e:
        print(e)
        logging.exception(e)

    #a = [b for b in tree.iterfind('.//l')]
    i = 0
    threads = []
        
    #for b in a:
    for b in tree.iterfind('//l'):
        if i%100 == 0:
            print(i//100)
            logging.info('%d',i//100)
        tmp = b.text
        if tmp is None:
            continue
        tmp = tmp.split(' ')
        # print(tmp)
        regex = re.compile('[^a-zA-Z]')
        #First parameter is the replacement, second parameter is your input string
        tmp = [regex.sub('', t) for t in tmp]
        #Out: 'abdE'
        # print(tmp)
        cheater = "C:\\Users\\adhill\\Documents\\Perseus\\IntermediateOutput\\storageTest.csv"

        process = Thread (target=processMe, args=[tmp,cheater])
        process.start()
        threads.append(process)
        #with Pool(None) as pool:
        #    tmp2 = pool.map(tryMe,tmp)
        #write(tmp2,cheater,True)
        
        '''
        tmp2 = [tryMe(t) for t in tmp]
        
        # print(tmp2)
        cheater = "C:\\Users\\adhill\\Documents\\Perseus\\IntermediateOutput\\storageTest.csv"
        write(tmp2,cheater,True)
        '''
        i += 1
    logging.info('%s Complete', basename(xmlFile))


if __name__ == "__main__":
    logging.basicConfig(filename='logs\log.txt', level=logging.INFO)
    logging.info("Started")

    path = Path("C:\\Users\\adhill\\Documents\\Perseus\\texts")
    #path = Path("C:\\Users\\adhill\\Documents\\Perseus\\texts\\hopper-texts-GreekRoman\\Classics\\Apollonius\\")
    # TODO - remove the '2' in the line below
    fileList = path.rglob("*2_gk.xml")
    for f in fileList:
        logging.info(f.name)
        parseXML(f)
    logging.info("All Files Complete")