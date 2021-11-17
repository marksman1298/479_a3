# #Need term frequency in document
# #Need average length of document in collection
# #From posting list determine which documents need to be revised 

# #Make dictionary key docId value tokenized body of text
# #From posting list determine which documents to scan
# import math
# from subproject1 import *
# from collections import defaultdict

# #dictionary of dictionary
# # keyof outer dictionary is the query term, key of inner dictionary is the docID, value of inner dictionary is the result of BM25
# # result = defaultdict(dict)
# Result = {}
# # abc and abd or abe
# def queryProcessor():
#     while True:
#         query = input("Enter a query or nothing to exit: ")
#         if not query:
#             break
#         # queryList
#         # andQuery = False
#         # orQuery = False
#         # if "and" in query:
#         #     queryList = query.split("and")
#         #     andQuery = True
#         # elif "or" in query:
#         #     queryList = query.split("or")
#         #     orQuery = True
#         # if queryList:
#         #     for terms in queryList:
#         #         keywords = terms.split() #can be multiple keywords ie: Democrats’ welfare and healthcare reform policies
#         #         BM25(keywords)
#         else:
#             keywords = query.split()
#             BM25(keywords)

# def BM25(keywords: List): #consider if and/or
#     for term in keywords:
#         #retrieve posting list of term
#         if term in Postings: #ensure term exists 
#             postingsList = Postings[term]
#             for docId in postingsList:
#                 #get length of document
#                 #get number of occurences of term in document
#                 docLength = len(Index[docId])
#                 freqOfTerm = Index[docId].count(docLength)
#                 Result[term] = {docId, bm25Equation(len(postingsList), freqOfTerm, docLength)}
#     return Result

# def bm25Equation(numDocsWithTerm: int, frequencyTermDoc: int, lenOfDoc: int):
#     # k1 = input("Enter value for constant k1: ")
#     k1 = 1.2
#     b = 0.75
#     rank = (math.log10(NumberOfDocs/numDocsWithTerm)) * (((k1 + 1)*frequencyTermDoc)/(k1*( (1-b) + b * (lenOfDoc/AverageLength)) + frequencyTermDoc))
#     return rank

# # def run():
# #     Postings, NumberOfDocs, AverageLength  = splitIntoArticles()
# #     print(queryProcessor())
# #     print(Result)
# # run()