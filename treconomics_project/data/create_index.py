from xml.dom import minidom 
from whoosh.index import create_in
from whoosh.fields import *
import os

schema = Schema(docid=TEXT(stored=True), title=TEXT(stored=True), content=TEXT(stored=True, vector=True), timedate=TEXT(stored=True), source=TEXT(stored=True) )

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
MAKE_SUBSET = True


def readDocids( docidfile ):
    docids = {}
    f = open(docidfile,"r")
    for line in f.readlines():
        tmp = line.strip()
        #tmp = tmp.decode("utf-8")
        docids[tmp] = 1

    f.close()
    return docids


def readDataFiles( datafile ):
    filelist = []
    f = open(datafile,"r")
    for line in f.readlines():
        filelist.append(line.rstrip())
        #print line
    f.close()
    return filelist

def getText(nodelist):
    rc = [u'']
    for nl in nodelist:
        if nl.firstChild:
            rc.append(nl.firstChild.data)
    tmp = u''.join(rc)
    tmp = tmp.strip()
    return tmp

def getTextFromPTags(nodelist):
    tmp = getText(nodelist)
    tmp = f'{tmp}{os.linesep}'
    
    for nl in nodelist:
        for child in nl.childNodes:
            if child.nodeType == 1:  # P NODE
                tmp = f'{tmp}{getText([child])}\r\t'
    
    tmp = tmp.strip()

    # A little more tidying up required.
    tmp = tmp.replace('\n', ' ')
    tmp = tmp.replace('\r\t', '\n\n')  # Should cover the XIE documents.

    return tmp


index_name = os.path.join(BASE_DIR, 'data/newindex')
subset_name = os.path.join(BASE_DIR, 'data/aquaint500subset.docids')
aquaint_filename = os.path.join(BASE_DIR, 'data/aquaint_xml_files')

if MAKE_SUBSET:
    docid_subset = readDocids(subset_name)
    print("docids read in: " + str(len(docid_subset)))
    #print(docid_subset)
    index_name = os.path.join(BASE_DIR, 'data/new500index2')

ix = create_in(index_name, schema)

count = 0
filesToProcess = readDataFiles(aquaint_filename)


writer = ix.writer(limitmb=1024)
for dfile in filesToProcess:        
    print("processing file: ", dfile)
    xmldoc = minidom.parse( dfile )
    for node in xmldoc.getElementsByTagName("DOC"):
        tmp = node.getElementsByTagName('DOCNO')
        ndocid = getText(tmp)

        tmp = node.getElementsByTagName('HEADLINE')
        ntitle = getText(tmp)

        tmp = node.getElementsByTagName('TEXT')
        ncontent = getTextFromPTags(tmp)


        if not ncontent:
            ncontent = "No content"

        if not ntitle:
            ntitle = ncontent[:60]


        tmp = node.getElementsByTagName('DATE_TIME')
        ntimedate = getText(tmp)
        nsource = ""

        if ndocid.startswith('APW'):
            nsource = u"Associated Press Worldwide News Service"
        if ndocid.startswith('XIE'):
            nsource = u"Xinhua News Service"
        if ndocid.startswith('NYT'):
            nsource = u"New York Times News Service"

        write_doc = True
        #print("* "+ndocid+" *")
        if MAKE_SUBSET:
            if ndocid in docid_subset:
                write_doc = True
            else:
                write_doc = False

        if write_doc:
            print("* "+ndocid+" * " +nsource + " * " + ntitle + " * " )
            writer.add_document(docid=ndocid, title=ntitle, content=ncontent, timedate=ntimedate, source=nsource)
            
            count = count + 1


writer.commit()
print("total number of documents index:" +  str(count))
