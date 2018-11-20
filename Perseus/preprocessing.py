from os.path import basename, join as pathjoin
from lxml import etree
import re
from vulcan import tryMe
import logging
from pathlib import Path 
from multiprocessing import Pool
from threading import Thread
from queue import Queue


def write(lst, filename, append=False):
    '''
        input:  a list, where each element is either a word in greek or a list of greek words (representing different possible roots)
        output: None
        effect: write <lst> to <filename> in the format word,word,word-word-word (multiples),word...\n, where each line is in this format
        '''
    with open(filename,'a+' if append else 'w+', encoding="utf-8") as cout:
        outstring = ' '.join(lst) + "\n"
        cout.write(outstring)

def writeOut2(lst, filename):
    '''TODO - replace writeOut1'''
    print(lst)
    print(filename)
    Path(filename).write_text("\n".join(lst),encoding='utf-8')


def prepAndWrite(lst, filename, append=False):
    ''' prepare output according to following rules:
    *** how to deal with unsure parsings?
    -- if fewer than 4 (1,2,3):
        make a new sentence that includes all of the possible dictionary forms (?!)
    if >= 4:
        see what happens if you get rid of all things that are the same up to a number
            (i.e. a, a2, a3, a4, a6)
        if still >= 4:
            throw that whole word away (too unclear)
        if now down to <= 3:
                make a new sentence that includes all
    ''' 
    preppedList, n = [], 3
    lst = [l for l in lst if l is not None]

    # If a "sentence has fewer than 5 words, it's probably a mistake.  Get rid of it"
    if len(lst) < 5:
        return

    for l in lst:
        if isinstance(l, list):
            if len(l) < n:
                preppedList.extend(l)
            else:
                secondL = list(set([re.sub("\d", "", s) for s in l]))
                if len(secondL) < n:
                    preppedList.extend(secondL)
                else:
                    continue
        else:
            preppedList.append(l)
     
    write(preppedList, filename, append)


def prepAndWrite2(allLists, filename, append=False):
    ''' prepare output according to following rules:
    *** how to deal with unsure parsings?
    -- if fewer than 4 (1,2,3):
        make a new sentence that includes all of the possible dictionary forms (?!)
    if >= 4:
        see what happens if you get rid of all things that are the same up to a number
            (i.e. a, a2, a3, a4, a6)
        if still >= 4:
            throw that whole word away (too unclear)
        if now down to <= 3:
                make a new sentence that includes all
    ''' 
    finalList = []

    print(allLists)
    exit()

    for lst in allLists:
        preppedList, n = [], 3
        lst = [l for l in lst if l is not None]

        # If a "sentence has fewer than 5 words, it's probably a mistake.  Get rid of it"
        if len(lst) < 5:
            return

        for l in lst:
            if isinstance(l, list):
                if len(l) < n:
                    preppedList.extend(l)
                else:
                    secondL = list(set([re.sub("\d", "", s) for s in l]))
                    if len(secondL) < n:
                        preppedList.extend(secondL)
                    else:
                        continue
            else:
                preppedList.append(l)
        finalList.append(' '.join(preppedList))
     
    writeOut2(finalList, filename)



def writeOut(output, filename):
    cheater = "C:\\Users\\adhill\\Documents\\Perseus\\IntermediateOutput\\ProcessedTexts\\" + filename.name.replace(".xml",".txt")
    # print(cheater)
    Path(cheater).write_text("\n".join(output),encoding='utf-8')
    

def worker(tree, xmlFile, splitterTag):

    data = ""
    
    for b in tree.iterfind(splitterTag):
        # several of these texts were generated via optical character recognition, which is mentioned
        # in a <p> tag in the header. 
        # TODO - find the right way to only look at stuff that is in <body> / in <text>
        if isinstance(b.text,str) and 'optical' in b.text:
            continue
        txt = b.text.replace("\n"," ") + " " if isinstance(b.text, str) else ""
        for c in b.getchildren():
            if isinstance(c.tail, str):
                txt += c.tail.replace("\n"," ")

        data += txt
    
    data = data.strip()

    data = re.findall(r"[^.;]+", data) 

    writeOut(data,xmlFile)

def parseXML(xmlFile):
    
    # print(xmlFile)
    
    try:
        parser = etree.XMLParser(ns_clean=True,remove_comments=True,remove_blank_text=True,recover=True)
        tree = etree.parse(xmlFile.open(),parser)
    except Exception as e:
        logging.exception(e)
        return

    #figure out whether I'm doign this by p, l, div, etc.
    a,b,splitterTag = None,None,None
    if tree.find('//p') is not None:
        worker(tree,xmlFile, "//p")
    elif tree.find('//lb') is not None:
        worker(tree,xmlFile, "//lb")
    elif tree.find('//l') is not None:
        worker(tree,xmlFile, "//l")
    else:
        print(xmlFile)

def toDictionaryForm(filename, outpath):
    ''' This assumes the preprocessing step 'parseXML' has already taken place, 
    and that there are processed files in the ProcessedTexts directory.'''
    def processMe(words, outpath, filename):
        tmp = [tryMe(w) for w in words]
        answers.append(tmp)
        # prepAndWrite(tmp,pathjoin(outpath,filename),True)
        
    # read in processed texts,
    # for each sentence, run perseus call
    #TODO - figure out how to make these all lower case
    sentences = filename.read_text(encoding='utf-8')
    sentences = sentences.split("\n")


    # process quickly, using threads so that URL calls are made as soon as possible rather than waiting
    # for the previous one to complete
    # Output saved to intermediate files -- now you have something to feed into word2vec
    threads = []
    answers = []


    for words in sentences:
        if words is None:
            continue
        words = words.split(' ')
        # print(tmp)
        regex = re.compile('[^a-zA-Z]')
        #First parameter is the replacement, second parameter is your input string
        words = [regex.sub('', w) for w in words]

        # processMe(words, outpath, filename.name)

        process = Thread(target = processMe, args=[words, outpath, filename.name])
        process.start()
        threads.append(process)
    print(len(threads))
    print(answers)
    # exit()
    # prepAndWrite2(answers, pathjoin(outpath,filename))




if __name__ == "__main__":
    logging.basicConfig(filename='logs\log.txt', level=logging.INFO)
    logging.info("Beginning Preprocessing")

    '''
    path = Path("C:\\Users\\adhill\\Documents\\Perseus\\texts")
    fileList = path.rglob("*_gk.xml")
    for f in fileList:
        # logging.info(f.name)
        parseXML(f)
    logging.info("ParseXML Complete")
    '''

    dictPath = Path("C:\\Users\\adhill\\Documents\\Perseus\\IntermediateOutput\\ProcessedTexts")
    dictOutPath = "C:\\Users\\adhill\\Documents\\Perseus\\IntermediateOutput\\word2vecInput"

    # fileList = path.rglob("*")
    for f in dictPath.rglob("*.txt"):
        # logging.info(f.name)
        print(f.name)
        toDictionaryForm(f, dictOutPath)
        exit()
    logging.info("Conversion to Dictionary Form Complete")    

    exit()
    word2vecPath = Path("C:\\Users\\adhill\\Documents\\Perseus\\IntermediateOutput\\word2vecInput")
    # fileList = path.rglob("*")
    for f in word2vecPath.rglob("*.txt"):
        # logging.info(f.name)
        word2vec(f)
    logging.info("Conversion to Dictionary Form Complete")
    
