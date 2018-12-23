import urllib2
import json
from collections import defaultdict

from BeautifulSoup import BeautifulSoup
from Items import *

ROWS_TO_SKIP_ON_FIRST_PAGE = 3
STARTING_PAGE = 1
TOTAL_PAGES = 81

# STARTING_PAGE = 1
# TOTAL_PAGES = 81


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


            if name == "Grenwog Basket II":  # missing + in Pierce Def
                bonuses = "Magic Def +1, Pierce Def +1, Melee Def +1, END +2, CHA +2, LUK +2, Bonus +1, Immobility +1, Stone +3, Wind +3 "
            if name == "Golden Arbitrator VII":  # missing + in dodge
                bonuses = "Magic Def +1, Pierce Def +1, Melee Def +1, END +2, CHA +2, LUK +2, Bonus +1, Immobility +1, Stone +3, Wind +3 "
            if name == "Golden Arbitrator VIII":
                bonuses = "Magic Def +1, Pierce Def +1, Melee Def +1, END +2, CHA +2, LUK +2, Bonus +1, Immobility +1, Stone +3, Wind +3 "
            if name == "Golden Arbitrator IX":
                bonuses = "Magic Def +1, Pierce Def +1, Melee Def +1, END +2, CHA +2, LUK +2, Bonus +1, Immobility +1, Stone +3, Wind +3 "
            if name == "Grand Guardian Helm":  # missing + in pierce def
                bonuses = "Magic Def +1, Pierce Def +1, Melee Def +1, END +2, CHA +2, LUK +2, Bonus +1, Immobility +1, Stone +3, Wind +3 "
            if name == "Golden Battlespell Helm VII":  # missing + in dodge
                bonuses = "Magic Def +1, Pierce Def +1, Melee Def +1, END +2, CHA +2, LUK +2, Bonus +1, Immobility +1, Stone +3, Wind +3 "
            if name == "Golden Battlespell Helm VIII":
                bonuses = "Magic Def +1, Pierce Def +1, Melee Def +1, END +2, CHA +2, LUK +2, Bonus +1, Immobility +1, Stone +3, Wind +3 "
            if name == "Golden Battlespell Helm IX":
                bonuses = "Magic Def +1, Pierce Def +1, Melee Def +1, END +2, CHA +2, LUK +2, Bonus +1, Immobility +1, Stone +3, Wind +3 "
            if name == "High Commander Helm" and level == "28":  # missing WIS +
                bonuses = "Magic Def +1, Pierce Def +1, Melee Def +1, END +2, CHA +2, LUK +2, Bonus +1, Immobility +1, Stone +3, Wind +3 "
            if name == "Rokpol Ring":  # Missing comma before Bonus
                bonuses = "Magic Def +1, Pierce Def +1, Melee Def +1, END +2, CHA +2, LUK +2, Bonus +1, Immobility +1, Stone +3, Wind +3 "
            if name == "Silver Laurels V":  # Extra comma after immobility 64
                bonuses = "Magic Def +1, Pierce Def +1, Melee Def +1, END +2, CHA +2, LUK +2, Bonus +1, Immobility +1, Stone +3, Wind +3 "
            if name == "Silvered Bells Cape VII":  # . after water 64
                bonuses = "Magic Def +1, Pierce Def +1, Melee Def +1, END +2, CHA +2, LUK +2, Bonus +1, Immobility +1, Stone +3, Wind +3 "
            if name == "Silvered Bells Cape VIII":
                bonuses = "Magic Def +1, Pierce Def +1, Melee Def +1, END +2, CHA +2, LUK +2, Bonus +1, Immobility +1, Stone +3, Wind +3 "
            if name == "Wings of the Unchained" and level == "70":  # Parry probably isn't 34 and missing comma after
                bonuses = "Magic Def +1, Pierce Def +1, Melee Def +1, END +2, CHA +2, LUK +2, Bonus +1, Immobility +1, Stone +3, Wind +3 "

            print name + " (Level: " + level + "): " + bonuses + "|" + equip

            bonus_dict = defaultdict(int)
            # Creates dict of bonuses with key equal to the first word of the bonus (ex. Pierce Def->Pierce)
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

                    "crit": bonus_dict["crit"],
                    "bonus": bonus_dict["bonus"],
                    "str": bonus_dict["str"],
                    "dex": bonus_dict["dex"],
                    "int": bonus_dict["int"],
                    "cha": bonus_dict["cha"],
                    "luk": bonus_dict["luk"],
                    "melee": bonus_dict["melee"],
                    "pierce": bonus_dict["pierce"],
                    "magic": bonus_dict["magic"],
                    "parry": bonus_dict["parry"],
                    "block": bonus_dict["block"],
                    "dodge": bonus_dict["dodge"],
                    "end": bonus_dict["end"],
                    "wis": bonus_dict["wis"],

                    "???": bonus_dict["???"],
                    "bacon": bonus_dict["bacon"],
                    "darkness": bonus_dict["darkness"],
                    "disease": bonus_dict["disease"],
                    "energy": bonus_dict["energy"],
                    "evil": bonus_dict["evil"],
                    "fear": bonus_dict["fear"],
                    "fire": bonus_dict["fire"],
                    "good": bonus_dict["good"],
                    "ice": bonus_dict["ice"],
                    "light": bonus_dict["light"],
                    "metal": bonus_dict["metal"],
                    "nature": bonus_dict["nature"],
                    "none": bonus_dict["none"],
                    "poison": bonus_dict["poison"],
                    "silver": bonus_dict["silver"],
                    "stone": bonus_dict["stone"],
                    "water": bonus_dict["water"],
                    "wind": bonus_dict["wind"],
                    "shrink": bonus_dict["shrink"],
                    "immobility": bonus_dict["immobility"],
                    "health": bonus_dict["health"],
                    "mana": bonus_dict["mana"],
                    "all": bonus_dict["all"],

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
        rows = table_page.count('<a href="tm.asp?m=')
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
