import os, re, json, string, math
from nltk import word_tokenize
from typing import List, Dict
from datetime import datetime
from collections import defaultdict

# Index = defaultdict(list) #contains tokenized documents without punctuation, needed for subproject2
# Postings = {}
# NumberOfDocs = 0
# AverageLength = 0.0


def splitIntoArticles() -> List[str]: #read all files in directory, put everything into one string, split into list of articles 
    data = ""
    try:
        # dir = input("Enter the directory: ")
        dir = 'C:/Users/marks/OneDrive/Desktop/Fall-2021/COMP 479/479_a3/479_a3/testFiles'
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
    # counter = 0
    numberOfDocumentsInCollection = 0
    averageLengthCollection = 0
    for i in range(len(listOfArticles)-1): 
        foundNewID = re.search('(NEWID=")([0-9]+)"', listOfArticles[i])
        if foundNewID.group(2):
            # index[foundNewID.group(2)] = word_tokenize(extractBody(listOfArticles[i]))
            # listOfArticles[i] = extractBody(listOfArticles[i])
            # postingTable, counter = documentTermDocIdPairs(word_tokenize(extractBody(listOfArticles[i])), foundNewID.group(2), postingTable, counter) #tokenizes the articles one at a time 
            postingTable, numberOfDocumentsInCollection, averageLengthCollection, index = documentTermDocIdPairs(word_tokenize(extractBody(listOfArticles[i])), foundNewID.group(2), postingTable, numberOfDocumentsInCollection, averageLengthCollection, index)
    averageLengthCollection /= numberOfDocumentsInCollection
    return postingTable, numberOfDocumentsInCollection, averageLengthCollection, index
   
def extractBody(document: str) -> str: #remove everything that isn't between the body tags, if there are no body tags present return empty string 
    startText = document.find("<BODY>")
    endText = document.find("</BODY>")
    if startText != -1 and endText != -1:
        document = document[startText:endText+7]
        return document
    return ""
# Figure something out for 10000 thingy
def documentTermDocIdPairs(tokenizedDocument: List, ID: str, postingTable: Dict, numberOfDocumentsInCollection: int, averageLengthCollection: int, index): #makes list of tuples (term, docID) 
    specialChar = string.punctuation
    exp = "[{schar}]".format(schar = specialChar)
    numberOfDocumentsInCollection += 1
    for token in tokenizedDocument:
        if not bool(re.match(exp, token)):
            index[int(ID)].append(token)
            # if counter >= 10000:
            #     return postingTable, counter
            if token not in postingTable:
                postingTable[token] = [int(ID)]
            elif int(ID) != postingTable[token][-1]:
                postingTable[token].append(int(ID))
            # counter += 1
            averageLengthCollection += 1
    return (postingTable, numberOfDocumentsInCollection, averageLengthCollection, index)
    # return postingTable, counter


# def queryProcessor(postings, numberOfDocs: int, averageLength: float, index, bm25=False, andQuery = False, orQuery = False):
#     while True:
#         query = input("Enter a query or nothing to exit: ")
#         # result = defaultdict(list)
#         result = defaultdict(int)
#         posts = []
#         if not query:
#             break
#         if query:
#             keywords = query.split()
#             if bm25:
#                 result = BM25(keywords, postings, numberOfDocs, averageLength, result, index)
#                 for docID in sorted(result, key=result.get, reverse=True):
#                     print(docID, result[docID])
#             elif len(keywords) == 1 and keywords[0] in postings:
#                 print(postings[keywords[0]])
#             elif andQuery:
#                 for term in keywords:
#                     if term in postings:
#                         if not posts:
#                             posts = postings[term]
#                         else:
#                             posts = list(set(posts).intersection(postings[term]))
#                 print(sorted(posts))
#             elif orQuery:
#                 for term in keywords:
#                     if term in postings:
#                         posts = list(set(posts).union(postings[term]))
#                 print(sorted(posts))

# def BM25(keywords: List, postings: dict, numberOfDocs: int, averageLength: float, result, index): #consider if and/or
#     k1 = 1.2
#     b = 0.75
#     for term in keywords:
#         #retrieve posting list of term
#         if term in postings: #ensure term exists 
#             postingsList = postings[term]
#             for docID in postingsList:
#                 #get length of document
#                 #get number of occurences of term in document
#                 docLength = len(index[docID])
#                 freqOfTerm = index[docID].count(term)
#                 #calculate the BM25 for each document, add value to dictionary
#                 result[docID] += round((math.log10(numberOfDocs/len(postingsList))) * (((k1 + 1)*freqOfTerm)/(k1*( (1-b) + b * (docLength/averageLength)) + freqOfTerm)), 3)
#     return result

# def run():
#     # starttime = datetime.now()
#     postings, numberOfDocs, averageLength, index  = splitIntoArticles()
#     # splitIntoArticles()
#     # with open("hihi2.txt", "w") as outfile:
#     #     json.dump(Index, outfile)
#     # print(NumberOfDocs)
#     # print(AverageLength)
#     # print(datetime.now()- starttime)
#     print(queryProcessor(postings, numberOfDocs, averageLength, index, bm25=True))
#     # print(Result)

# run()