from BeautifulSoup import BeautifulSoup
import urllib2
from Items import *


ROWS_TO_SKIP_ON_FIRST_PAGE = 3
TOTAL_PAGES = 1
ROWS_ON_PAGE = 6


# Opens given page number and returns response
def open_page(page_number):
    response = urllib2.urlopen(
        'http://forums2.battleon.com/f/tt.asp?forumid=118&p=' + str(page_number) + '&tmode=10&smode=1')
    return response.read()


# Opens first item in given page substring
def open_item(html):
    link = html[html.find('tm.asp?m='):]
    link = link[:link.find('"')]
    sub_response = urllib2.urlopen("http://forums2.battleon.com/f/" + link)
    return sub_response.read()


# Find each item on the page and it to the json file
def parse_item(html):
    parsed_html = BeautifulSoup(html)
    msgs = parsed_html.body.findAll('td', attrs={'class': 'msg'})
    for msg in msgs:
        if is_item(msg):
            name = get_name(msg)
            equip = get_equip(msg)
            itemType = get_type(msg)
            level = get_level(msg)
            bonuses = get_bonus(msg)
            print name + "( "+level+" ):" + bonuses + ":" + equip + ":" + itemType

    #   equip spot

    # link
    #   name
    #   level
    # element
    # bonuses
    #   item type

    # dc
    # rare
    # seasonal
    # da
    # so
    # dm
    # g


if __name__ == '__main__':
    for page in range(1, TOTAL_PAGES + 1):
        table_page = open_page(page)
        for row in range(1, ROWS_ON_PAGE + 1):

            # Find first instance of an accessory link in html range
            # When found, we take a substring of the index+1 (removing '<') so exact string is not found again
            row_index = table_page.find('<a href="tm.asp?m=') + 1
            table_page = table_page[row_index:]

            # If we are scraping the first page, we skip the pinned topics at the top of the table
            if page == 1 and row <= ROWS_TO_SKIP_ON_FIRST_PAGE:
                continue

            # Go through all versions of an item and store it
            item_page = open_item(table_page)
            parse_item(item_page)
    exit()
