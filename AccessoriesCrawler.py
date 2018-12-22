import urllib2
import json
from collections import defaultdict

from BeautifulSoup import BeautifulSoup
from Items import *


ROWS_TO_SKIP_ON_FIRST_PAGE = 3
TOTAL_PAGES = 1
ROWS_ON_PAGE = 11


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
def parse_item(html, data):
    parsed_html = BeautifulSoup(html)
    msgs = parsed_html.body.findAll('td', attrs={'class': 'msg'})
    for msg in msgs:
        # Need to use parent.parent to get the entire message (including the hyperlink)
        msg = msg.parent.parent
        if is_item(msg):
            name = get_name(msg)
            equip = get_equip(msg)
            item_type = get_type(msg)
            level = get_level(msg)
            bonuses = get_bonus(msg)
            element = get_element(msg)
            hyperlink = get_link(msg)
            print name + "( "+level+" ):" + bonuses + ":" + equip + ":" + item_type + ":" + element
            print hyperlink
            print "DC" + str(is_dc(msg))
            print "rare" + str(is_rare(msg))
            print "seasonal" + str(is_seasonal(msg))
            print "da" + str(is_da(msg))
            print "so" + str(is_so(msg))
            print "dm" + str(is_dm(msg))
            print "g" + str(is_g(msg))
            data[equip].append({
                name + " (Level " + level + ")": {
                    "name": name,
                    "level": level,
                    "link": hyperlink,
                    "crit": 10,
                    "bonus": 10,
                    "str": 12,
                    "dex": 12,
                    "int": 12,
                    "cha": 8,
                    "luk": 8,
                    "melee": 6,
                    "pierce": 6,
                    "magic": 6,
                    "parry": 6,
                    "block": 6,
                    "dodge": 6,
                    "end": 6,
                    "wis": 6,
                    "???": 0,
                    "bacon": 0,
                    "darkness": 0,
                    "disease": 0,
                    "energy": 0,
                    "evil": 0,
                    "fear": 0,
                    "fire": 0,
                    "good": 0,
                    "ice": 0,
                    "light": 0,
                    "metal": 0,
                    "nature": 10,
                    "none": 0,
                    "poison": 0,
                    "silver": 0,
                    "stone": 0,
                    "water": 0,
                    "wind": 0,
                    "shrink": 0,
                    "immobility": 0,
                    "health": 0,
                    "mana": 0,
                    "all": 0,
                    "dc": is_dc(msg),
                    "da": is_da(msg),
                    "rare": is_rare(msg),
                    "seasonal": is_seasonal(msg),
                    "so": is_so(msg),
                    "dm": is_dm(msg),
                    "g": is_g(msg)
                }
            })



if __name__ == '__main__':
    data = defaultdict(list)
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
            parse_item(item_page, data)

    with open('accessories.json', 'w') as outfile:
        json.dump(data, outfile)
    exit()
