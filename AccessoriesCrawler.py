try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
import urllib2
import json

ROWS_TO_SKIP_ON_FIRST_PAGE = 3
TOTAL_PAGES = 1
ROWS_ON_PAGE = 11


# Opens given page number and returns response
def openPage(pageNumber):
    response = urllib2.urlopen(
        'http://forums2.battleon.com/f/tt.asp?forumid=118&p=' + str(pageNumber) + '&tmode=10&smode=1')
    return response.read()


# Opens first item in given page substring
def openItem(html):
    link = html[html.find('tm.asp?m='):]
    link = link[:link.find('"')]
    sub_response = urllib2.urlopen("http://forums2.battleon.com/f/" + link)
    return sub_response.read()


# Find each item on the page and it to the json file
def parseItem(html):
    parsed_html = BeautifulSoup(html)
    items = parsed_html.body.findAll('td', attrs={'class': 'msg'})
    for item in items:
        print item.text
    # item type

    # link
    # name
    # level
    # bonuses
    # element

    # dc
    # rare
    # seasonal
    # da
    # so
    # dm
    # g


if __name__ == '__main__':
    for page in range(1, TOTAL_PAGES + 1):
        tablePage = openPage(page)
        for row in range(1, ROWS_ON_PAGE + 1):

            # Find first instance of an accessory link in html range
            # When found, we take a substring of the index+1 (removing '<') so exact string is not found again
            rowIndex = tablePage.find('<a href="tm.asp?m=') + 1
            tablePage = tablePage[rowIndex:]

            # If we are scraping the first page, we skip the pinned topics at the top of the table
            if page == 1 and row <= ROWS_TO_SKIP_ON_FIRST_PAGE:
                continue

            itemPage = openItem(tablePage)
            parseItem(itemPage)
    exit()
