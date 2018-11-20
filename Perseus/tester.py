from pathlib import Path 
from lxml import etree

yes, no, fail = [], [], []

def parseXML(xmlFile, flag=False):
    try:
        parser = etree.XMLParser(ns_clean=True,remove_comments=True,remove_blank_text=True,recover=True)
        tree = etree.parse(xmlFile.open(),parser)
  
        #for b in a:
        if not flag:
            if tree.find('//l') is not None:
                yes.append(xmlFile)
            else:
                no.append(xmlFile)
        else:
            if tree.find('//sp') is not None:
                no.remove(xmlFile)
    except Exception as e:
        fail.append(xmlFile)


if __name__ == "__main__":

    path = Path("C:\\Users\\adhill\\Documents\\Perseus\\texts")
    #path = Path("C:\\Users\\adhill\\Documents\\Perseus\\texts\\hopper-texts-GreekRoman\\Classics\\Apollonius\\")
    # TODO - remove the '2' in the line below
    fileList = path.rglob("*_gk.xml")
    i = 1
    for f in fileList:
        parseXML(f)
        print(i)
        i += 1

    # print("YES: ")
    # for n in yes:
    #     print(n)
    # print("********************************")
    print("NO: ")
    # for n in no:
    #     parseXML(n,True)
    for n in no:
        print(n)
    print("********************************")
    print("FAIL: ")
    for n in fail:
        print(n)
    