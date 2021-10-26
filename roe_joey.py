from urllib import request
from bs4 import BeautifulSoup
import re


def downloadHTMLPage(urlName):

    url = urlName
    response = request.urlopen(url)
    page = response.read().decode('utf-8')
    return page


#gets the URLs from the HTML page
#returns a list of the URLs found on the page
def getURLs(HTMLpage, urls):

    #urls = [] #list containing all of the URLs on the page

    htmlString = BeautifulSoup(HTMLpage, "html.parser")
    for link in htmlString.find_all('a'):
        if(link.get('href').strip(".") not in urls): #gets rid of duplicate URLs
            urls.append(link.get('href').strip(".")) #gets rid of the "." at the very beginning

    for i in range(0, len(urls)):
        urls[i] = "http://www.cs.utep.edu/makbar/A3" + urls[i] #adds the first half of the URL

    return urls


def parseHTML_Page(HTMLpage):

    htmlString = BeautifulSoup(HTMLpage, 'html.parser')
    raw = htmlString.get_text()
    raw = raw.split()
    return raw


#removes puncuation from the raw list provided
def removePuncuation(rawList):

    for i in range(0, len(rawList)):
        rawList[i] = re.sub(r'[^\w\s]','',rawList[i])
    val = ''
    rawList = list(filter(lambda x: x != val, rawList)) #gets rid of the empty spaces
    return rawList


#reads the stop_text file
#puts all of the stop words in a list
def readFile(fileName):

    stopWordsFile = open(fileName, 'r')
    stopWords = stopWordsFile.readlines()

    for i in range(0, len(stopWords)):
        stopWords[i] = stopWords[i].strip("\n") #get rid of the new line

    return stopWords


#removes the stop words from the rawList
def removeStopWords(rawList, stopWords):

    newList = [] #list for words that aren't stop words
    for word in rawList:
        if(word in stopWords): #word is a stop word
            continue
        else:
            newList.append(word)

    return newList


#wordCounter counts the amount of times
#a word occurs in a document. It stores
#the word along with it's number of time it appears
#in a dictionary, with the key being the word and the
#value being the number of times the word appears.
def wordCounter(rawList):

    word_Dic = {}
    for i in rawList:
        key = i
        value = 0 #initially set it to 0
        word_Dic[key] = value

    for i in rawList:
        word_Dic[i] += 1 #increment it every time word is ecountered

    return word_Dic



if __name__ == '__main__':

    stopWords = readFile("stop_text.txt")

    #only do the main url manually
    url = "http://www.cs.utep.edu/makbar/A3/A2.html"
    page = downloadHTMLPage(url)
    htmlString = BeautifulSoup(page, "html.parser")
    raw = parseHTML_Page(page)
    raw = removePuncuation(raw)
    newRaw = removeStopWords(raw, stopWords)
    word_Dic = wordCounter(newRaw)

    newFile = open("roe_joey.txt", 'w')
    newFile.write("url: " + url + " -> " + str(word_Dic) +"\n")

    urls = getURLs(page, []) #all of the URLs from the home page

    newURLs = [] #New list for all of the URLs that have not been visited yet
    for i in range(0, len(urls)):
        tempPage = downloadHTMLPage(urls[i]) #go to the URLs in the list
        newURLs.append(getURLs(tempPage, []))

    for i in range(0, len(newURLs)):
        for j in range(0, len(newURLs[i])):

            if(newURLs[i][j] is not None or newURLs[i][j]not in urls):
                urls.append(newURLs[i][j])


    for url in urls:  #the rest of  the URLs are done here
        tempPage = downloadHTMLPage(url)
        tempRaw = parseHTML_Page(tempPage)
        tempRaw = removePuncuation(tempRaw)
        tempRaw = removeStopWords(tempRaw, stopWords)
        tempWord_Dic = wordCounter(tempRaw)

        newFile.write("url: " + url + " -> " + str(tempWord_Dic) + "\n")

    newFile.close()
