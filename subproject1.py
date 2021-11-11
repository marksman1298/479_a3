import os, re, json, string
from nltk import word_tokenize
from typing import List, Dict
from datetime import datetime

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

def makePostingsList(listOfArticles: List) -> List: 
    postingTable = {}
    counter = 0
    for i in range(len(listOfArticles)-1): 
        foundNewID = re.search('(NEWID=")([0-9]+)"', listOfArticles[i])
        if foundNewID.group(2):
            listOfArticles[i] = extractBody(listOfArticles[i])
            postingTable, counter = documentTermDocIdPairs(word_tokenize(extractBody(listOfArticles[i])), foundNewID.group(2), postingTable, counter) #tokenizes the articles one at a time 
    return postingTable
   
def extractBody(document: str) -> str: #remove everything that isn't between the body tags, if there are no text tags present return empty string 
    startText = document.find("<BODY>")
    endText = document.find("</BODY>")
    if startText != -1 and endText != -1:
        document = document[startText:endText+7]
        return document
    return ""

def documentTermDocIdPairs(tokenizedDocument: List, ID: str, postingTable: Dict, counter: int): #makes list of tuples (term, docID) 
    specialChar = string.punctuation
    exp = "[{schar}]".format(schar = specialChar)
    for token in tokenizedDocument:
        if not bool(re.match(exp, token)):
            if counter >= 10000:
                return postingTable, counter
            if token not in postingTable:
                postingTable[token] = [int(ID)]
            elif int(ID) != postingTable[token][-1]:
                postingTable[token].append(int(ID))
            counter += 1
    return postingTable, counter

starttime = datetime.now()
table = splitIntoArticles()
with open("10000.txt", "w") as outfile:
    json.dump(table, outfile)
print(datetime.now()- starttime)