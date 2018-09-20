import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import igraph
import re
import Queue

# Max number of child pages to scrape for each visited page
PAGE_VISIT_LIMIT = 1

def makeGraph(initialPage, graph):
    page = urllib2.urlopen(initialPage)
    soup = BeautifulSoup(page, "html.parser")
    links = getPageLinks(soup)

    pageTitle = getPageTitleFromLink(initialPage)
    graph.add_vertex(pageTitle)

    childPagesToVisit = []

    for link in links:
        childPageTitle = getPageTitleFromLink(link)
        if not vertexExists(graph, childPageTitle):
            childPagesToVisit.append("https://en.wikipedia.org/wiki/" + childPageTitle)
            print initialPage + childPageTitle
            graph.add_vertex(childPageTitle)
        graph.add_edges([(pageTitle, childPageTitle)])
        graph.add_edges([(childPageTitle, pageTitle)])

    for childPage in childPagesToVisit:
        graph = makeGraph(childPage, graph)

    return graph

def vertexExists(graph, vertex):
    try:
        graph.vs.find(name=vertex)
    except ValueError:
        return False
    return True

def getPageTitleFromLink(link):
    title = link.split("/wiki/")[1]
    if title is not None:
        return title
    else:
        raise Exception("Unable to numberOfLinksToRetrieve page title.  Invalid wiki page encountered.")

def getPageLinks(soupObject):
    allDivs = soupObject.find_all("div")
    allBodyContent = []
    for div in allDivs:
        divId = div.get("id")
        if divId is not None:
            if "mw-content-text" in divId:
                allBodyContent.append(div);
    allLinks = []
    for bodyContent in allBodyContent:
        if len(allLinks) < PAGE_VISIT_LIMIT:
            allLinks = allLinks + getLinksHelper(bodyContent, PAGE_VISIT_LIMIT)
        else:
            break
    return allLinks

def getLinksHelper(bodyContent, PAGE_VISIT_LIMIT):
    anchors = bodyContent.find_all("a")
    links = []
    validWikiPagePattern = "\/wiki\/[A-Z|a-z|_]*[A-Z|a-z]$"
    for anchor in anchors:
        if len(links) < PAGE_VISIT_LIMIT:
            link = anchor.get("href")
            if link is not None and re.match(validWikiPagePattern, link):
                links.append(link)
        else:
            break
    return links

def main():
    graph = makeGraph("https://en.wikipedia.org/wiki/Cat", igraph.Graph(directed=True))
    print graph

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
