import os, re, json, string, math
from nltk import word_tokenize
from typing import List, Dict
from datetime import datetime
from collections import defaultdict

Index = defaultdict(list) #contains tokenized documents without punctuation, needed for subproject2
Postings = {}
NumberOfDocs = 0
AverageLength = 0.0
Result = {}

def splitIntoArticles() -> List[str]: #read all files in directory, put everything into one string, split into list of articles 
    data = ""
    try:
        dir = input("Enter the directory: ")
        listOfFiles = os.listdir(dir)
    except Exception as e: 
        print(e)
        return 
    for filename in listOfFiles: #read each file in the directory that ends with .sgm
        if filename.endswith(".sgm"):
            filepath = dir + "/" + filename
            with open(filepath, "r") as f:
                data += f.read()
    return makePostingsList(data.split("</REUTERS>")) #creates list of articles split on the </REUTERS> tag 

def makePostingsList(listOfArticles: List): 
    postingTable = {}
    # counter = 0
    numberOfDocumentsInCollection = 0
    averageLengthCollection = 0
    for i in range(len(listOfArticles)-1): 
        foundNewID = re.search('(NEWID=")([0-9]+)"', listOfArticles[i])
        if foundNewID.group(2):
            # index[foundNewID.group(2)] = word_tokenize(extractBody(listOfArticles[i]))
            # listOfArticles[i] = extractBody(listOfArticles[i])
            # postingTable, counter = documentTermDocIdPairs(word_tokenize(extractBody(listOfArticles[i])), foundNewID.group(2), postingTable, counter) #tokenizes the articles one at a time 
            postingTable, numberOfDocumentsInCollection, averageLengthCollection = documentTermDocIdPairs(word_tokenize(extractBody(listOfArticles[i])), foundNewID.group(2), postingTable, numberOfDocumentsInCollection, averageLengthCollection)
    averageLengthCollection /= numberOfDocumentsInCollection
    return postingTable, numberOfDocumentsInCollection, averageLengthCollection
   
def extractBody(document: str) -> str: #remove everything that isn't between the body tags, if there are no body tags present return empty string 
    startText = document.find("<BODY>")
    endText = document.find("</BODY>")
    if startText != -1 and endText != -1:
        document = document[startText:endText+7]
        return document
    return ""
# Figure something out for 10000 thingy
def documentTermDocIdPairs(tokenizedDocument: List, ID: str, postingTable: Dict, numberOfDocumentsInCollection: int, averageLengthCollection: int): #makes list of tuples (term, docID) 
    specialChar = string.punctuation
    exp = "[{schar}]".format(schar = specialChar)
    numberOfDocumentsInCollection += 1
    for token in tokenizedDocument:
        if not bool(re.match(exp, token)):
            Index[int(ID)].append(token)
            # if counter >= 10000:
            #     return postingTable, counter
            if token not in postingTable:
                postingTable[token] = [int(ID)]
            elif int(ID) != postingTable[token][-1]:
                postingTable[token].append(int(ID))
            # counter += 1
            averageLengthCollection += 1
    return (postingTable, numberOfDocumentsInCollection, averageLengthCollection)
    # return postingTable, counter


def queryProcessor(Postings):
    while True:
        query = input("Enter a query or nothing to exit: ")
        if not query:
            break
        # queryList
        # andQuery = False
        # orQuery = False
        # if "and" in query:
        #     queryList = query.split("and")
        #     andQuery = True
        # elif "or" in query:
        #     queryList = query.split("or")
        #     orQuery = True
        # if queryList:
        #     for terms in queryList:
        #         keywords = terms.split() #can be multiple keywords ie: Democrats’ welfare and healthcare reform policies
        #         BM25(keywords)
        else:
            keywords = query.split()
            BM25(keywords)

def BM25(keywords: List): #consider if and/or
    for term in keywords:
        #retrieve posting list of term
        if term in Postings: #ensure term exists 
            postingsList = Postings[term]
            for docId in postingsList:
                #get length of document
                #get number of occurences of term in document
                docLength = len(Index[docId])
                freqOfTerm = Index[docId].count(docLength)
                Result[term] = {docId, bm25Equation(len(postingsList), freqOfTerm, docLength)}
    return Result

def bm25Equation(numDocsWithTerm: int, frequencyTermDoc: int, lenOfDoc: int):
    # k1 = input("Enter value for constant k1: ")
    k1 = 1.2
    b = 0.75
    rank = (math.log10(NumberOfDocs/numDocsWithTerm)) * (((k1 + 1)*frequencyTermDoc)/(k1*( (1-b) + b * (lenOfDoc/AverageLength)) + frequencyTermDoc))
    return rank



def run():
    # starttime = datetime.now()
    Postings, NumberOfDocs, AverageLength  = splitIntoArticles()
    # splitIntoArticles()
    # with open("hihi2.txt", "w") as outfile:
    #     json.dump(Index, outfile)
    # print(NumberOfDocs)
    # print(AverageLength)
    # print(datetime.now()- starttime)
    print(queryProcessor(Postings))
    print(Result)

run()