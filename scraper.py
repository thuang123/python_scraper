import urllib2
from bs4 import BeautifulSoup
import pandas as pd
from graphviz import Digraph
import igraph
import re

# Max number of child pages to scrape for each visited page
PAGE_VISIT_LIMIT = 3
# Max numbers of connections of links from original parent page
STRAY_LIMIT = 4

def poplulateGraph(initialPage, graph, strayLimit):
    # Setup: Create soup object and retrieve hyperlinks
    page = urllib2.urlopen(initialPage)
    soup = BeautifulSoup(page, "html.parser")

    if strayLimit > 0:
        links = getPageLinks(soup)
        strayLimit -= 1

    # Create graph node for current page
    pageTitle = getPageTitleFromLink(initialPage)
    graph.node(pageTitle, pageTitle)

    childPagesToVisit = []

    # Create child graph nodes and save childPagesToVisit next
    for link in links:
        childPageTitle = getPageTitleFromLink(link)
        if not vertexExists(graph, childPageTitle):
            print childPageTitle
            graph.node(childPageTitle, childPageTitle)
            if strayLimit > 0:
                childPagesToVisit.append("https://en.wikipedia.org/wiki/" + childPageTitle)
        graph.edges([(pageTitle, childPageTitle)])

    # Continue with child pages
    for childPage in childPagesToVisit:
        graph = poplulateGraph(childPage, graph, strayLimit)

    return graph

def vertexExists(graph, vertex):
    return "label=" + vertex in graph.source

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
    # Starter page
    starterPage = "https://en.wikipedia.org/wiki/Cat"
    graph = poplulateGraph(starterPage, Digraph(), STRAY_LIMIT)
    # Graphviz representation output in generated pdf file
    graph.render()
    print graph.source

if __name__ == '__main__':
    main()
