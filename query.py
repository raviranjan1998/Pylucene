import lucene
import csv
import pandas as pd
import nltk
import sys
nltk.download('punkt')
from nltk import word_tokenize
porter = nltk.PorterStemmer()
from java.io import File

lucene.initVM()


from org.apache.lucene.index import IndexReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search.similarities import BM25Similarity

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory, FSDirectory
import org.apache.lucene.document as document

indexPath = File("/content/index/").toPath()
qry = sys.argv[1]
res_path = sys.argv[2]

def search(q, qnum):

    analyzer = StandardAnalyzer()
    directory = FSDirectory.open(indexPath)
    searcher = IndexSearcher(DirectoryReader.open(directory))
    
    searcher.setSimilarity(BM25Similarity(1.8, 0.3))

    query = QueryParser("TEXT", analyzer).parse(q)

    scoreDocs = searcher.search(query, 1000).scoreDocs
   

    i = 1
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        with open(res_path, 'a') as result:
          data_row = str(qnum) + ' Q0 ' + str(doc.get("DOCNO")) + ' ' + str(i) + ' ' + str(scoreDoc.score)
          result.write(data_row)
          result.write('\n')
        i = i + 1

from bs4 import BeautifulSoup
import glob
import csv
import pandas as pd
query = open(qry)
anchor = BeautifulSoup(query, "html.parser")

num = []
for each in anchor.find_all("num"):
    num.append(each.text)

title = []
for each in anchor.find_all("title"):
    title.append(each.text)

desc = []
for each in anchor.find_all("desc"):
    desc.append(each.text)


case = int(input("ENTER 1 Query only or  2 for Query with description"))

if case == 1:
  for i in range(len(title)):
    search(title[i], num[i])
elif case == 2:
  for i in range(len(title)):
    mod_qry = title[i] + ' ' + desc[i]
    search(mod_qry, num[i])