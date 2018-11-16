import morpheuslib2
import urllib.request
import urllib.error
import requests
from lxml import etree
#from urllib.parse import urljoin
import logging

def recurseMe(node,lvl):
    offset = "\t".join(["" for _ in range(lvl)])

    print(offset + node.tag)
    print(offset + str(node.attrib))
    print(type(node.text))
    print(node.text)
    #print(node.text.decode('unicode_escape'))

    for child in node:
        recurseMe(child, lvl+1)

def to_xml(xml):
    """The XML text for this analysis. Not identical to the original, if
    fixes were applied.
    Returns:
        bytes.
    """
    return ElementTree.tostring(self.elem, encoding = "utf-8", method= "xml")


def tryMe(string):
    url = "http://www.perseus.tufts.edu/hopper/xmlmorph?lang=greek&lookup="+string
    a = None
    try:
        resp = etree.parse(url)
        iter = resp.getroot()
        a = list(set([b.text for b in iter.iterfind('.//lemma')]))

        if len(a) == 1:
            a = a[0]
    except OSError as e:   
        print("AAAAAAAAAAAAAAAAAAAAAH")
        logging.error(string)
    except Exception as e:
        print("OOOOOOOOOOOOOOOOHHH NOOOOOOOOOOOO!")
        logging.exception(e)

    return a

#url = "http://www.perseus.tufts.edu/hopper/xmlmorph?lang=greek&lookup=mhrusanto"
# url = "http://www.perseus.tufts.edu/hopper/xmlmorph?lang=greek&lookup=gar"

if __name__ == "__main__":
    try:
        response = urllib.request.urlopen(url)
        t = response.read()
        print(t)
        #u = requests.get(url)
        #print(t)
        test = etree.parse(url)
        #iter = test.getiterator()
        #for p in iter:

        iter2 = test.getroot()
        recurseMe(iter2,1)
        #print(type(test))
        #print(test.docinfo.encoding)
        exit()
        #print(test.docinfo.encoding)
        recurseMe(test)
    #    print(test)
        #print(u.content)
        #print("SUCCESS!!!")
        #print("11111111111111111111")
        exit()
        root = ElementTree.fromstring(str(t).encode('utf-8'))
        # print(root)
        # ElementTree.dump(root)
        print(t)
        print(root.docinfo.encoding)
        exit()
        recurseMe(root,1)
        '''
        print(t)
        for xmlChild in root:
        if xmlChild.tag:
            print(xmlChild.tag)
            print(xmlChild.attrib)
        '''
        ##elemList = []
        ##for elem in root.iter():
        ##    elemList.append(elem.tag)
        #print(set(elemList))
        #take2.write('output.xml')
        #print("555555555555555555")
        #return MorpheusResponse(self, t, None)
    except urllib.error.HTTPError as ex2:
        # These errors are intermittent (403s mostly). Processing can
        # continue.
        print("ERROR 1")
        print(ResponseErrorInfo(ex2))
        #return MorpheusResponse(self, t, ResponseErrorInfo(ex2))
    except urllib.error.URLError as ex1:
        # This error typically indicates a connection problem. Best to
        # report it at once.
        print("ERROR 2")
        print(ResponseErrorInfo(ex1))
        #raise ex1
