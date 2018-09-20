import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import igraph
import re
import Queue

def makeGraph(initialPage, visitLimit):
    page = urllib2.urlopen(initialPage)
    soup = BeautifulSoup(page, "html.parser")
    links = getPageLinks(soup, visitLimit)

    graph = igraph.Graph(directed=True)
    pageTitle = getPageTitleFromLink(initialPage)
    graph.add_vertex(pageTitle)

    for link in links:
        childPageTitle = getPageTitleFromLink(link)
        graph.add_vertex(childPageTitle)
        graph.add_edges([(pageTitle, childPageTitle)])
        graph.add_edges([(childPageTitle, pageTitle)])

    return graph

def getPageTitleFromLink(link):
    title = link.split("/wiki/")[1]
    if title is not None:
        return title
    else:
        raise Exception("Unable to numberOfLinksToRetrieve page title.  Invalid wiki page encountered.")

def getPageLinks(soupObject, numberOfLinksToRetrieve):
    allDivs = soupObject.find_all("div")
    allBodyContent = []
    for div in allDivs:
        divId = div.get("id")
        if divId is not None:
            if "mw-content-text" in divId:
                allBodyContent.append(div);
    allLinks = []
    for bodyContent in allBodyContent:
        if len(allLinks) < numberOfLinksToRetrieve:
            allLinks = allLinks + getLinksHelper(bodyContent, numberOfLinksToRetrieve)
        else:
            break
    return allLinks

def getLinksHelper(bodyContent, numberOfLinksToRetrieve):
    anchors = bodyContent.find_all("a")
    links = []
    validWikiPagePattern = "\/wiki\/[A-Z|a-z|_]*[A-Z|a-z]$"
    for anchor in anchors:
        if len(links) < numberOfLinksToRetrieve:
            link = anchor.get("href")
            if link is not None and re.match(validWikiPagePattern, link):
                links.append(link)
        else:
            break
    return links

def main():
    graph = makeGraph("https://en.wikipedia.org/wiki/Cat", 5)
    print graph

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
