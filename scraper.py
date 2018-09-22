from bs4 import BeautifulSoup
from graphviz import Digraph

import urllib2
import igraph
import re
import sys

def poplulateGraph(initialPage, graph, strayLimit, visitLimit):
    try:
        # Setup: Create soup object and retrieve hyperlinks
        page = urllib2.urlopen(initialPage)
        soup = BeautifulSoup(page, "html.parser")

        if strayLimit > 0:
            links = getPageLinks(soup, visitLimit)
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
            graph = poplulateGraph(childPage, graph, strayLimit, visitLimit)

        return graph
    except urllib2.HTTPError:
        raise Exception("Invalid wiki page encountered.")

def vertexExists(graph, vertex):
    return "label=" + vertex in graph.source

def getPageTitleFromLink(link):
    title = link.split("/wiki/")[1]
    if title is not None:
        return title
    else:
        raise Exception("Unable to numberOfLinksToRetrieve page title.  Invalid wiki page encountered.")

def getPageLinks(soupObject, visitLimit):
    allDivs = soupObject.find_all("div")
    allBodyContent = []
    for div in allDivs:
        divId = div.get("id")
        if divId is not None:
            if "mw-content-text" in divId:
                allBodyContent.append(div);
    allLinks = []
    for bodyContent in allBodyContent:
        if len(allLinks) < visitLimit:
            allLinks = allLinks + getLinksHelper(bodyContent, visitLimit)
        else:
            break
    return allLinks

def getLinksHelper(bodyContent, visitLimit):
    anchors = bodyContent.find_all("a")
    links = []
    validWikiPagePattern = "\/wiki\/[A-Z|a-z|_]*[A-Z|a-z]$"
    for anchor in anchors:
        if len(links) < visitLimit:
            link = anchor.get("href")
            if link is not None and re.match(validWikiPagePattern, link):
                links.append(link)
        else:
            break
    return links

def main():
    try:
        wikiInitialPage =  "https://en.wikipedia.org/wiki/" + sys.argv[1]
        strayLimit = int(sys.argv[2])
        visitLimit = int(sys.argv[3])
        graph = poplulateGraph(wikiInitialPage, Digraph(), strayLimit, visitLimit)
        # Graphviz representation output in generated pdf file
        graph.render()
        print graph.source
    except IndexError as ie:
        print "Provide appropriate arguments: search topic, page stray limit, and page visit limit."
    except (TypeError, ValueError) as e:
        print "Type error encountered.  Provided arguments must be of type string, int, and int."

if __name__ == '__main__':
    main()
