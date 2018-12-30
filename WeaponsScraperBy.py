import urllib2
import json

from BeautifulSoup import BeautifulSoup
from WeaponsBy import *

ROW_LINKS_TO_SKIP_ON_FIRST_PAGE = int(sys.argv[2])
STARTING_PAGE = int(sys.argv[1])
TOTAL_PAGES = int(STARTING_PAGE)+9


# Opens given page number and returns response
def open_page(page_number):
    while True:
        try:
            response = urllib2.urlopen(
                'http://forums2.battleon.com/f/tt.asp?forumid=119&p=' + str(page_number) + '&tmode=10&smode=1')
            html_source = response.read()
            if response.getcode() == 200:
                break
        except Exception as inst:
            print inst
            out = open("weapons" + str(sys.argv[1]) + ".txt", "a")
            out.write(str(inst) + "\n")
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
            out = open("weapons" + str(sys.argv[1]) + ".txt", "a")
            out.write(str(inst))
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
            # Handles single message with multiple versions of item which have different stats
            if msg.getText().lower().count("bonuses:") > 1:
                save_2_items(msg, data, hyperlink)
            else:
                save_item(msg, data, hyperlink)


if __name__ == '__main__':
    data = defaultdict(list)
    for page in range(STARTING_PAGE, TOTAL_PAGES + 1):
        table_page = open_page(page)
        rows = table_page.count('<a href="tm.asp?m=')
        for row in range(1, rows + 1):
            index = "\nPage: " + str(page) + ", Row: " + str(row)
            print index
            out = open("weapons" + str(sys.argv[1]) + ".txt", "a")
            out.write(str(index)+"\n")
            out.close()

            # Find first instance of an accessory link in html range
            # When found, we take a substring of the index+1 (removing '<') so exact string is not found again
            row_index = table_page.find('<a href="tm.asp?m=') + 1
            table_page = table_page[row_index:]

            # If we are scraping the first page, we skip the pinned topics at the top of the table
            if page == STARTING_PAGE and row <= ROW_LINKS_TO_SKIP_ON_FIRST_PAGE:
                continue

            # Go through all versions of an item and store it
            item_page = open_item(table_page)
            try:
                parse_item(item_page, data)
            except IndexError as e:
                f = open("weapons" + str(sys.argv[1]) + "errors.txt", "a")
                f.write("Page: " + str(page) + ", Row: " + str(row) + "\n")
                out = open("weapons" + str(sys.argv[1]) + ".txt", "a")
                out.write(str(e))
                print e

    with open('weapons'+str(sys.argv[1])+'.json', 'w') as outfile:
        json.dump(data, outfile)
    exit()
