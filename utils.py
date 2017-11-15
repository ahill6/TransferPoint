from clang.cindex import *
import plyj.parser as plyj
#import plyj.model
from urllib2 import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup
from numpy import median, mean, std
from sys import exit, stdout
from random import sample
from shutil import rmtree
from os import listdir, rename, makedirs
from os.path import join as pathjoin, exists as pathexists
import tarfile

def massDownload(url, outdir, cerr, nots=[], has=[]):
    try:
        response = urlopen(url)
    except HTTPError as err:
        if err.code == 404:
            return
        else:
            cerr.write(url + ","+err.message)
            return
    except URLError as err:
        cerr.write(url+"--URLError,"+err.message)
        return
    except Exception as err:
        cerr.write(url+"--Other Exception,"+err.message)
        return
    html = response.read()
    #soup = BeautifulSoup(html, 'lxml')
    soup = BeautifulSoup(html, "html.parser")

    for possible in soup.find_all('a'):
        pos = possible.get('href')
        if any([n in pos for n in nots]):
            continue
        if not any([h in pos for h in has]):
            continue
        try:
            copyDown(url, pos, outdir)
        except Exception as e:
            cerr.write(url+"//"+pos+","+e.message+"\n")

def copyDown(base, name, outdir):
    f = urlopen(base + name)
    with open(outdir+name, "wb") as code:
        code.write(f.read())

def extractTars(directory):
    todo = [f for f in listdir(directory) if 'tar' in f]
    if not pathexists(pathjoin(directory,"Archive")):
        makedirs(pathjoin(directory,"Archive"))
    for t in todo:
        tar = tarfile.open(pathjoin(directory,t))
        tar.extractall(path=directory)
        tar.close()
        exit()
        rename(pathjoin(directory,t), pathjoin(directory,"Archive",t))


basePage = 'http://repairbenchmarks.cs.umass.edu/ManyBugs/scenarios/'
out = 'C:\\Users\\Andrew\\Downloads\\ManyBugs\\'
errorFile = 'C:\\Users\\Andrew\\Downloads\\ManyBugs\\error.txt'
#err = open(errorFile, 'w')
negatories = ['brun']
posses = ['tar']
#massDownload(basePage,out,err,negatories, posses)
#err.close()
extractTars(out)

#too many tars.  Plan is to extract, analyze, delete.