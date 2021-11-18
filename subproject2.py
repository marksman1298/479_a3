import math, json, os, string, re
from typing import List, Dict
from nltk import word_tokenize
from datetime import datetime
from collections import defaultdict


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
    index = defaultdict(list)
    numberOfDocumentsInCollection = 0
    averageLengthCollection = 0
    for i in range(len(listOfArticles)-1): 
        foundNewID = re.search('(NEWID=")([0-9]+)"', listOfArticles[i])
        if foundNewID.group(2):
            postingTable, numberOfDocumentsInCollection, averageLengthCollection, index = documentTermDocIdPairs(word_tokenize(extractBody(listOfArticles[i])), #tokenizes the articles one at a time 
            foundNewID.group(2), postingTable, numberOfDocumentsInCollection, averageLengthCollection, index)
    averageLengthCollection /= numberOfDocumentsInCollection
    return postingTable, numberOfDocumentsInCollection, averageLengthCollection, index
   
def extractBody(document: str) -> str: #remove everything that isn't between the body tags, if there are no body tags present return empty string 
    startText = document.find("<BODY>")
    endText = document.find("</BODY>")
    if startText != -1 and endText != -1:
        document = document[startText:endText+7]
        return document
    return ""

# Construct the postings table directly by adding the term as the key of the dictionary and adding the docID to the list
def documentTermDocIdPairs(tokenizedDocument: List, ID: str, postingTable: Dict, numberOfDocumentsInCollection: int, averageLengthCollection: int, index): 
    specialChar = string.punctuation
    exp = "[{schar}]".format(schar = specialChar)
    numberOfDocumentsInCollection += 1
    for token in tokenizedDocument:
        if not bool(re.match(exp, token)):
            index[int(ID)].append(token)
            if token not in postingTable:
                postingTable[token] = [int(ID)]
            elif int(ID) != postingTable[token][-1]: 
                postingTable[token].append(int(ID))
            averageLengthCollection += 1
    return (postingTable, numberOfDocumentsInCollection, averageLengthCollection, index)


def queryProcessor(postings, numberOfDocs: int, averageLength: float, index, bm25=False, andQuery = False, orQuery = False, singleQuery = False):
    while True: 
        query = input("Enter a query or nothing to exit: ")
        result = defaultdict(int)
        posts = []
        if not query: #exit condition
            break
        keywords = query.split(" ") #split query into list of terms 
        if bm25: #if doing bm25 search
            result = BM25(keywords, postings, numberOfDocs, averageLength, result, index)
            sorted_dict = {}
            sorted_keys = sorted(result, key=result.get, reverse=True)
            for w in sorted_keys:
                sorted_dict[w] = result[w]
            with open("bm25Query1.5_0.85.txt", "a") as outfile:
                json.dump(sorted_dict, outfile)
        elif singleQuery or len(keywords) == 1:
            if len(keywords) == 1 and keywords[0] in postings:
                print(postings[keywords[0]])
                with open("singleQuery.txt", "a") as outfile:
                    json.dump(f'{query} {postings[keywords[0]]}', outfile)
        elif andQuery or orQuery:
            if andQuery: #if doing unranked boolean retrieval (AND)
                posts = postings[keywords[0]]
                for term in keywords:
                    posts = list(set(posts).intersection(postings[term]))
                print(list(sorted(posts)))
            elif orQuery: #if doing unranked boolean retrieval (OR)
                posts = set(postings[keywords[0]])
                for term in keywords:
                    if term in postings:
                        posts = list(set(posts).union(postings[term]))
                print(sorted(posts))
            with open("andQuery.txt", "a") as outfile:
                json.dump(f'{query} {list(sorted(posts))}', outfile)

def BM25(keywords: List, postings: dict, numberOfDocs: int, averageLength: float, result, index): 
    k1 = 1.5
    b = 0.85
    for term in keywords:
        #retrieve posting list of term
        if term in postings: #ensure term exists 
            postingsList = postings[term]
            for docID in postingsList:
                #get length of document
                #get number of occurences of term in document
                docLength = len(index[docID])
                freqOfTerm = index[docID].count(term)
                #calculate the BM25 for each document, add value to dictionary
                result[docID] += round((math.log10(numberOfDocs/len(postingsList))) * (((k1 + 1)*freqOfTerm)/(k1*( (1-b) + b * (docLength/averageLength)) + freqOfTerm)), 3)
    return result

def run():
    starttime = datetime.now()
    postings, numberOfDocs, averageLength, index  = splitIntoArticles()
    print(datetime.now()- starttime)
    print(queryProcessor(postings, numberOfDocs, averageLength, index, bm25=True))

run()