from urllib2 import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup
from sys import exit, stdout
import os, arff

# open github
def gitMiner(url, base='https://github.com'):
    done = 0
    try:
        response = urlopen(url, timeout=5)
    except HTTPError as err:
        if err.code == 404:
            return 0
        else:
            print(url + ","+err.message)
            return 0
    except URLError as err:
        print(url+"--URLError,"+err.message)
        return 0
    except Exception as err:
        print(url+"--Other Exception,"+err.message)
        return 0
    html = response.read()
    #soup = BeautifulSoup(html, 'lxml')
    soup = BeautifulSoup(html, "html.parser")

    for possibles in soup.find_all('td'):
        if 'class' in possibles.attrs and possibles['class'][0] == 'content':
            folders = possibles.find_all('a')

            if len(folders) > 0:
                if '.csv' in possibles.text.strip():
                    try:
                        done += copyToLocal(folders[0].get('href'), base)
                    except Exception as e:
                        print("Problem")
                        print(folders[0].get('href')+",")
                        print(e.message)
                elif '.' in possibles.text:
                    continue
                else:
                    for link in folders:
                        done += gitMiner(base+link.get('href'), base)

    return done

def copyToLocal(url, base='https://github.com'):
    print(url)
    name = url.split('/')[-1].strip()
    scriptDir = os.getcwd()
    response = None
    response = urlopen(base+url, timeout=5)
    if response is None:
        return 0
    html = response.read()
    #soup = BeautifulSoup(html, 'lxml')
    soup = BeautifulSoup(html)
    for link in soup.find_all('a'):
        if link.text == 'Raw':
            file = urlopen(base + link.get('href'), timeout=5)
            with open(scriptDir+'/TransferLearning/Data/' + name, 'w') as ctmp:
                ctmp.write(file.read())
            return 1

"""
# read in the arff files
path = './TransferLearning/ArffData/'
cout = open('./TransferLearning/Data/Summary2.csv', 'w')
# ...figure out something to do with them
files = [f for f in os.listdir(path) if '.arff' in f]
print(files)
for f in files:
    data = arff.load(open(path+f, 'r'))
    attr = [a[0] for a in data['attributes']]
    cout.write(f + ',,')
    cout.write(','.join(attr))
    cout.write("\n")
cout.close()


with open('./TransferLearning/uniqueFeatures.csv','r') as cin:
    tmp = [t for t in cin.read().strip().split('\r')]
data = [t.lower() for t in tmp]
data.sort()
print(data)
"""

with open('../tester.txt', 'r') as cin:
    data = [line for line in cin]
with open('../MANIFEST.MF', 'w') as cout:
    for line in data:
        if 'SHA1' not in line:
            cout.write(line)
