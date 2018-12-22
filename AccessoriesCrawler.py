import urllib2
import json
from collections import defaultdict

from BeautifulSoup import BeautifulSoup
from Items import *

ROWS_TO_SKIP_ON_FIRST_PAGE = 3
ROWS_ON_PAGE = 30
STARTING_PAGE = 1
TOTAL_PAGES = 81
ROWS_ON_LAST_PAGE = 16


# STARTING_PAGE = 1
# TOTAL_PAGES = 81
# ROWS_ON_LAST_PAGE = 16


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
    # Gets every post on the page
    msgs = parsed_html.body.findAll('td', attrs={'class': 'msg'})
    for msg in msgs:
        # Need to use parent.parent to get the entire message (including the hyperlink)
        msg = msg.parent.parent
        if is_item(msg):
            equip = get_equip(msg)
            name = get_name(msg)
            level = get_level(msg)
            hyperlink = get_link(msg)
            element = get_element(msg)
            item_type = get_type(msg)
            bonuses = get_bonus(msg)
            print name + " (Level: " + level + "): " + bonuses + "|" + equip

            bonus_dict = defaultdict(int)
            # Creates dict of bonuses with key equal to the first word of the bonus (Pierce Def->Pierce)
            if bonuses != 'None':
                for bonus in bonuses.split(', '):
                    if "+" in bonus:
                        nb = bonus.split("+")
                        bonus_dict[nb[0].split(" ")[0]] = int(nb[1])
                    else:
                        nb = bonus.split("-")
                        bonus_dict[nb[0].split(" ")[0]] = int(nb[1]) * -1

            data[equip].append({
                name + " (Level " + level + ")": {
                    "equip": equip,
                    "name": name,
                    "level": level,
                    "link": hyperlink,
                    "element": element,
                    "item_type": item_type,

                    "crit": bonus_dict["Crit"],
                    "bonus": bonus_dict["Bonus"],
                    "str": bonus_dict["STR"],
                    "dex": bonus_dict["DEX"],
                    "int": bonus_dict["INT"],
                    "cha": bonus_dict["CHA"],
                    "luk": bonus_dict["LUK"],
                    "melee": bonus_dict["Melee"],
                    "pierce": bonus_dict["Pierce"],
                    "magic": bonus_dict["Magic"],
                    "parry": bonus_dict["Parry"],
                    "block": bonus_dict["Block"],
                    "dodge": bonus_dict["Dodge"],
                    "end": bonus_dict["END"],
                    "wis": bonus_dict["WIS"],

                    "???": bonus_dict["???"],
                    "bacon": bonus_dict["Bacon"],
                    "darkness": bonus_dict["Darkness"],
                    "disease": bonus_dict["Disease"],
                    "energy": bonus_dict["Energy"],
                    "evil": bonus_dict["Evil"],
                    "fear": bonus_dict["Fear"],
                    "fire": bonus_dict["Fire"],
                    "good": bonus_dict["Good"],
                    "ice": bonus_dict["Ice"],
                    "light": bonus_dict["Light"],
                    "metal": bonus_dict["Metal"],
                    "nature": bonus_dict["Nature"],
                    "none": bonus_dict["None"],
                    "poison": bonus_dict["Poison"],
                    "silver": bonus_dict["Silver"],
                    "stone": bonus_dict["Stone"],
                    "water": bonus_dict["Water"],
                    "wind": bonus_dict["Wind"],
                    "shrink": bonus_dict["Shrink"],
                    "immobility": bonus_dict["Immobility"],
                    "health": bonus_dict["Health"],
                    "mana": bonus_dict["Mana"],
                    "all": bonus_dict["All"],

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
    for page in range(STARTING_PAGE, TOTAL_PAGES + 1):
        table_page = open_page(page)
        rows = ROWS_ON_PAGE
        if page == TOTAL_PAGES:
            rows = ROWS_ON_LAST_PAGE
        for row in range(1, rows + 1):

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
