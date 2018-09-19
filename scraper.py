import urllib2
from bs4 import BeautifulSoup
import pandas as pd

# Setup
wiki = "https://en.wikipedia.org/wiki/Cat"
page = urllib2.urlopen(wiki)
soup = BeautifulSoup(page, "html.parser")

def getPageLinks():
    allDivs = soup.find_all("div")
    allBodyContent = []
    for div in allDivs:
        divId = div.get("id")
        if divId is not None:
            if "bodyContent" in divId:
                allBodyContent.append(div);
    allLinks = []
    for bodyContent in allBodyContent:
        allLinks = allLinks + getLinksHelper(bodyContent)
    return allLinks

def getLinksHelper(bodyContent):
    anchors = bodyContent.find_all("a")
    links = []
    for anchor in anchors:
        link = anchor.get("href")
        if link is not None:
            links.append(link)
    return links

def main():
    print(getPageLinks())

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
