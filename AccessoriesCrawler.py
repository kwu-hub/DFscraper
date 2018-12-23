import urllib2
import json

from BeautifulSoup import BeautifulSoup
from Items import *

ROWS_TO_SKIP_ON_FIRST_PAGE = 3
STARTING_PAGE = 73
TOTAL_PAGES = 73

# STARTING_PAGE = 1
# TOTAL_PAGES = 81


# Opens given page number and returns response
def open_page(page_number):
    while True:
        try:
            response = urllib2.urlopen(
                'http://forums2.battleon.com/f/tt.asp?forumid=118&p=' + str(page_number) + '&tmode=10&smode=1')
            html_source = response.read()
            if response.getcode() == 200:
                break
        except Exception as inst:
            print inst
    return html_source


# Opens first item in given page substring
def open_item(html):
    link = html[html.find('tm.asp?m='):]
    link = link[:link.find('"')]
    while True:
        try:
            response = urllib2.urlopen("http://forums2.battleon.com/f/" + link)
            html_source = response.read()
            if response.getcode() == 200:
                break
        except Exception as inst:
            print inst
    return html_source


# Find each item on the page and it to the json file
def parse_item(html, data):
    parsed_html = BeautifulSoup(html)
    # Gets every post on the page
    msgs = parsed_html.body.findAll('td', attrs={'class': 'msg'})
    for msg in msgs:
        # Need to use parent.parent to get the entire message (including the hyperlink)
        msg = msg.parent.parent

        if is_item(msg):
            hyperlink = get_link(msg)
            # Handles single message with multiple versions of item
            if msg.getText().lower().count("bonuses") > 1:
                print "yeet"
            save_item(msg, data, hyperlink)


if __name__ == '__main__':
    data = defaultdict(list)
    for page in range(STARTING_PAGE, TOTAL_PAGES + 1):
        table_page = open_page(page)
        rows = table_page.count('<a href="tm.asp?m=')
        for row in range(1, rows + 1):
            print "\nPage: " + str(page) + ", Row: " + str(row)

            # Find first instance of an accessory link in html range
            # When found, we take a substring of the index+1 (removing '<') so exact string is not found again
            row_index = table_page.find('<a href="tm.asp?m=') + 1
            table_page = table_page[row_index:]

            # If we are scraping the first page, we skip the pinned topics at the top of the table
            if page == 1 and row <= ROWS_TO_SKIP_ON_FIRST_PAGE:
                continue

            # Go through all versions of an item and store it
            item_page = open_item(table_page)
            parse_item(item_page, data)

    with open('accessories.json', 'w') as outfile:
        json.dump(data, outfile)
    exit()
