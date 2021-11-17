import math
from typing import List
from datetime import datetime
from collections import defaultdict
from subproject1 import *

def queryProcessor(postings, numberOfDocs: int, averageLength: float, index, bm25=False, andQuery = False, orQuery = False):
    while True:
        query = input("Enter a query or nothing to exit: ")
        # result = defaultdict(list)
        result = defaultdict(int)
        posts = []
        if not query:
            break
        if query:
            keywords = query.split()
            if bm25:
                result = BM25(keywords, postings, numberOfDocs, averageLength, result, index)
                for docID in sorted(result, key=result.get, reverse=True):
                    print(docID, result[docID])
            elif len(keywords) == 1 and keywords[0] in postings:
                print(postings[keywords[0]])
            elif andQuery:
                for term in keywords:
                    if term in postings:
                        if not posts:
                            posts = postings[term]
                        else:
                            posts = list(set(posts).intersection(postings[term]))
                print(sorted(posts))
            elif orQuery:
                for term in keywords:
                    if term in postings:
                        posts = list(set(posts).union(postings[term]))
                print(sorted(posts))

def BM25(keywords: List, postings: dict, numberOfDocs: int, averageLength: float, result, index): #consider if and/or
    k1 = 1.2
    b = 0.75
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
    # starttime = datetime.now()
    postings, numberOfDocs, averageLength, index  = splitIntoArticles()
    # splitIntoArticles()
    # with open("hihi2.txt", "w") as outfile:
    #     json.dump(Index, outfile)
    # print(NumberOfDocs)
    # print(AverageLength)
    # print(datetime.now()- starttime)
    print(queryProcessor(postings, numberOfDocs, averageLength, index, bm25=True))
    # print(Result)

run()