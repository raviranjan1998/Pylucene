import lucene
import os
import csv
import pandas as pd

import nltk
nltk.download('punkt')
from nltk import word_tokenize
porter = nltk.PorterStemmer()
from java.io import File

lucene.initVM()




from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory, FSDirectory
import org.apache.lucene.document as document

from org.apache.lucene.index import IndexReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search.similarities import BM25Similarity



filepath = '/content/data.csv'
indexPath = File("/content/index/").toPath()
indexDir = FSDirectory.open(indexPath)
writerConfig = IndexWriterConfig(StandardAnalyzer())
writer = IndexWriter(indexDir, writerConfig)


def index_News(docno,title, news):
    doc = document.Document()
    doc.add(document.Field("DOCNO", docno, document.TextField.TYPE_STORED))
    doc.add(document.Field("TITLE", title, document.TextField.TYPE_STORED))
    doc.add(document.Field("TEXT", news, document.TextField.TYPE_STORED))
    writer.addDocument(doc)
def closeWriter():
    writer.close()

def makeIndex(file_path):
    df = pd.read_csv(file_path, nrows = 100)
    docid = 0
    for i in df.index:
        index_News(df['DOCNO'][i], df['TITLE'][i], df['TEXT'][i])
        docid += 1

makeIndex(filepath)
closeWriter()