# python_scraper

## Description

A basic Python web scraper that scrapes Wikipedia pages from a user inputted valid Wikipedia page.  Users specify the maximum number of links to scrape on each encountered page and the maximum number of links away from original starting page.  The output is a directed graphical representation of the connections between all the scraped pages identified by the page titles.  This is based on the idea from Quora [post](https://www.quora.com/What-are-some-interesting-web-scraping-projects-you-have-done).

## Installation & Getting Started

Ensure python BeautifulSoup and Graphviz libraries are installed.

## Usage

Execute file

```$ python scraper.py```

Specify the starting Wikipedia page to scrape, the page stray limit, and the page visit limit.  For example, running the following would out the following graph that represents all the connections from the Cat Wikipedia page.

```$ python scraper.py Cat 3 3```

<img src="https://github.com/thuang123/python_scraper/blob/master/res/preview_cat_graph_output.png">

## Credits

Luke Deen Taylor for providing the web scraping idea from Quora [answer](https://www.quora.com/What-are-some-interesting-web-scraping-projects-you-have-done).
