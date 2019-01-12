# This file contains helper functions for parsing specific values from message
import re
from collections import defaultdict
import sys


# This function should rarely be used
# It is only used for messages with more than one bonuses value
def save_2_items(msg, data, hyperlink, page, row):
    # This first part determines which item the DC/DA tags are associated with
    # If the image with the tag appears in the first 15 elements, it is associated with first item
    # Otherwise it is associated with the second
    first_da = False
    first_dc = False
    first_rare = False
    first_seasonal = False
    first_so = False
    first_g = False
    first_dm = False
    second_da = False
    second_dc = False
    second_rare = False
    second_seasonal = False
    second_so = False
    second_g = False
    second_dm = False
    msg_contents = msg.find("td", attrs={'class': 'msg'}).contents
    for i in range(len(msg_contents)):
        try:
            if msg_contents[i].name == "img":
                imgs = msg_contents[i]["src"]
                if i < 15:
                    if "DA" in imgs:
                        first_da = True
                    if "DC" in imgs:
                        first_dc = True
                    if "Rare" in imgs:
                        first_rare = True
                    if "Seasonal" in imgs:
                        first_seasonal = True
                    if "DM" in imgs:
                        first_dm = True
                    if "SpecialOffer" in imgs or "DoomKnight" in imgs:
                        first_so = True
                    if "Guardian" in imgs:
                        first_g = True
                else:
                    if "DA" in imgs:
                        second_da = True
                    if "DC" in imgs:
                        second_dc = True
                    if "Rare" in imgs:
                        second_rare = True
                    if "Seasonal" in imgs:
                        second_seasonal = True
                    if "DM" in imgs:
                        second_dm = True
                    if "SpecialOffer" in imgs or "DoomKnight" in imgs:
                        second_so = True
                    if "Guardian" in imgs:
                        second_g = True
        except AttributeError:
            continue

    # ---------------------------- Add First item ----------------------------
    # Same code as save_item()
    equip = get_equip(msg)
    name = get_name(msg)
    level = get_level(msg)
    element = get_element(msg)
    item_type = get_type(msg)
    bonuses = get_bonus(msg)

    if equip != "Head" and equip != "Neck" and equip != "Armor" \
            and equip != "Back" and equip != "Trinket" \
            and equip != "Finger" and equip != "Waist" \
            and equip != "Hand" and equip != "Wrist":
        m = ("Page: " + str(page) + ", Row: " + str(row) + "; Attack Type Error\n")
        out = open("accessories" + str(sys.argv[1]) + "errors.txt", "a")
        out.write(name + ": " + m + "\n")

    # Creates dict of bonuses with key equal to the first word of the bonus (ex. Pierce Def->Pierce)
    bonus_dict = defaultdict(int)
    if bonuses != 'None':
        for bonus in bonuses.split(', '):
            if bonus.lower() == bonus and "???" not in bonus:
                m = ("Page: " + str(page) + ", Row: " + str(row) + "; Case Error\n")
                out = open("accessories" + str(sys.argv[1]) + "errors.txt", "a")
                out.write(name + ": " + m + "\n")
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

            "dc": first_dc,
            "da": first_da,
            "rare": first_rare,
            "seasonal": first_seasonal,
            "so": first_so,
            "dm": first_dm,
            "g": first_g,
        }
    })
    to_print = name + " (Level: " + level + "): " + equip + "|" + bonuses + "|"
    print to_print
    out = open("accessories" + str(sys.argv[1]) + ".txt", "a")
    out.write(str(to_print) + "\n")

    # ---------------------------- Add second item ----------------------------
    # Have to find the second appearance of each of the values
    text = msg.getText()
    second_tag_index_level = text.find("Level: ", text.find("Level: ") + 1)
    second_tag_index_element = text.find("Element: ", text.find("Element: ") + 1)
    second_tag_index_bonuses = text.find("Bonuses: ", text.find("Bonuses: ") + 1)
    second_level = text[second_tag_index_level + len("Level: "):second_tag_index_element]
    second_element = text[second_tag_index_element + len("Element: "):second_tag_index_bonuses]

    if text[second_tag_index_element:].find("Bonuses: None") != -1:
        second_bonuses = 'None'
    else:
        regex = re.compile("([0-9][a-zA-Z])|([0-9],[a-zA-Z])|([0-9]\.[a-zA-Z])")
        m = regex.search(text[second_tag_index_bonuses:])
        second_tag_index_bonuses_end = text.find(m.group(0)) + 1
        second_bonuses = text[second_tag_index_bonuses + len("Bonuses: "):second_tag_index_bonuses_end]

    # Creates dict of bonuses with key equal to the first word of the bonus (ex. Pierce Def->Pierce)
    bonus_dict = defaultdict(int)
    if second_bonuses != 'None':
        for bonus in second_bonuses.split(', '):
            if bonus.lower() == bonus and "???" not in bonus:
                m = ("Page: " + str(page) + ", Row: " + str(row) + "; Case Error\n")
                out = open("accessories" + str(sys.argv[1]) + "errors.txt", "a")
                out.write(name + ": " + m + "\n")
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
            "level": second_level,
            "link": hyperlink,
            "element": second_element,
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

            "dc": second_dc,
            "da": second_da,
            "rare": second_rare,
            "seasonal": second_seasonal,
            "so": second_so,
            "dm": second_dm,
            "g": second_g,
        }
    })
    to_print = name + " (Level: " + level + "): " + equip + "|" + bonuses + "|"
    print to_print
    out = open("accessories" + str(sys.argv[1]) + ".txt", "a")
    out.write(str(to_print) + "\n")


def save_item(msg, data, hyperlink, page, row):
    equip = get_equip(msg)
    name = get_name(msg)
    level = get_level(msg)
    element = get_element(msg)
    item_type = get_type(msg)
    if name == "Glowing Helm of Destiny":
        bonuses = "Crit +2, Magic Def +3, Pierce Def +3, Melee Def +3, WIS +2, CHA +2, INT +4, DEX +4, STR +4, " \
                  "Bonus +2, Poison +2, Disease +2, Darkness +5, Evil +5"
    else:
        bonuses = get_bonus(msg)

    '''
    Exceptions due to typos in the forums
    Patrick's Emerald Green Hat: has 2 spaces after "Equip Spot:" instead of 1
    '''
    if name == "Patrick's Emerald Green Hat":
        equip = "Head"

    if equip != "Head" and equip != "Neck" and equip != "Armor" \
            and equip != "Back" and equip != "Trinket" \
            and equip != "Finger" and equip != "Waist" \
            and equip != "Hand" and equip != "Wrist":
        m = ("Page: " + str(page) + ", Row: " + str(row) + "; Attack Type Error\n")
        out = open("accessories" + str(sys.argv[1]) + "errors.txt", "a")
        out.write(name + ": " + m + "\n")


    # Creates dict of bonuses with key equal to the first word of the bonus (ex. Pierce Def->Pierce)
    bonus_dict = defaultdict(int)
    if bonuses != 'None':
        for bonus in bonuses.split(', '):
            if bonus.lower() == bonus and "???" not in bonus:
                m = ("Page: " + str(page) + ", Row: " + str(row) + "; Case Error\n")
                out = open("accessories" + str(sys.argv[1]) + "errors.txt", "a")
                out.write(name + ": " + m + "\n")
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
            "g": is_g(msg),
        }
    })
    to_print = name + " (Level: " + level + "): " + equip + "|" + bonuses + "|"
    print to_print
    out = open("accessories" + str(sys.argv[1]) + ".txt", "a")
    out.write(str(to_print) + "\n")


# Determines if the message received contains the attributes of an item
def is_item(html):
    return 'Equip Spot:' in html.text and 'Category: ' in html.text and 'Level: ' in html.text \
           and 'Bonuses: ' in html.text


# Helper function used to find the specific value between the text of 2 different tags
def find_between_tags(html, tag, next_tag):
    text = html.getText()

    # Handles the unknown text that follows bonuses (Effect, Ability, DC, etc.) Comedy Cloak (page 13)
    # The bonuses category ends with a number and is followed by a letter that is the next category
    # The code finds that index and gets values in between
    if next_tag == "bonus_case":
        # Handles items without bonuses
        if text.find("Bonuses: None") != -1:
            return 'None'
        text = text[text.find(tag) + len(tag):]
        regex = re.compile("([0-9][a-zA-Z])|([0-9],[a-zA-Z])|([0-9]\.[a-zA-Z])")
        m = regex.search(text)
        text = text[:text.find(m.group(0)) + 1]
        return text

    # All other values
    tag_index = text.find(tag)
    next_index = text.find(next_tag)
    if tag_index == -1 or next_index == -1:
        if tag_index != next_index:
            to_print = "'" + tag + "'" + str(tag_index) + "|'" + next_tag + "'" + str(next_index)
            print to_print
            out = open("accessories" + str(sys.argv[1]) + ".txt", "a")
            out.write(str(to_print))
        return ''
    item_value = text[text.find(tag) + len(tag): text.find(next_tag)]
    return item_value


def get_name(html):
    msg = html.find('td', attrs={'class': 'msg'})
    name = msg.b.getText()
    return name


def get_level(html):
    tag = 'Level: '
    next_tag = 'Element: '
    return find_between_tags(html, tag, next_tag)


def get_equip(html):
    tag = 'Equip Spot: '
    next_tag = 'Category: '
    return find_between_tags(html, tag, next_tag)


def get_type(html):
    tag = 'Item Type: '
    next_tag = 'Equip Spot: '
    return find_between_tags(html, tag, next_tag)


def get_bonus(html):
    tag = 'Bonuses: '
    return find_between_tags(html, tag, "bonus_case")


def get_element(html):
    tag = 'Element: '
    next_tag = 'Bonuses: '
    return find_between_tags(html, tag, next_tag)


def get_link(html):
    # Finds tag with the link and gets the value of onclick
    link = html.find(onclick=re.compile("fwdwin"))['onclick']
    link = link[link.find("=") + 1:link.find("')")]
    hyperlink = "http://forums2.battleon.com/f/fb.asp?m=" + link
    return hyperlink


# For DC, Rare, Seasonal, and DA tags we check if there are more than 1 entry (determined by multiple price: tags)
# If there are multiple entries, we find the count of the given tag
# If tag count is 0, then it is False
# If tag count is same as entries, then it is True (each entry has it so it is not optional)
# If tag count is neither, then it is optional (it only shows up on some of the entries)
# Assumes Guardian, Special Offer, DM has no optional
def is_dc(html):
    images = len(html.findAll('img', src=re.compile("DC\.((jpg)|(png))")))
    entry_count = html.getText().lower().count('price:')
    if (images < entry_count) and entry_count > 1 and images != 0:
        return "optional"
    return html.find('img', src=re.compile("DC\.((jpg)|(png))")) is not None


def is_rare(html):
    images = len(html.findAll('img', src=re.compile("Rare\.((jpg)|(png))")))
    entry_count = html.getText().lower().count('price:')
    if (images < entry_count) and entry_count > 1 and images != 0:
        return "optional"
    return html.find('img', src=re.compile("Rare\.((jpg)|(png))")) is not None


def is_seasonal(html):
    images = len(html.findAll('img', src=re.compile("Seasonal\.((jpg)|(png))")))
    entry_count = html.getText().lower().count('price:')
    if (images < entry_count) and entry_count > 1 and images != 0:
        return "optional"
    return html.find('img', src=re.compile("Seasonal\.((jpg)|(png))")) is not None


def is_da(html):
    images = len(html.findAll('img', src=re.compile("DA\.((jpg)|(png))")))
    entry_count = html.getText().lower().count('price:')
    if (images < entry_count) and entry_count > 1 and images != 0:
        return "optional"
    return html.find('img', src=re.compile("DA\.((jpg)|(png))")) is not None


def is_so(html):
    return (html.find('img', src=re.compile("SpecialOffer\.((jpg)|(png))")) is not None) \
           or (html.find('img', src=re.compile("DoomKnight\.((jpg)|(png))")) is not None)


def is_dm(html):
    return html.find('img', src=re.compile("DM\.((jpg)|(png))")) is not None


def is_g(html):
    return html.find('img', src=re.compile("Guardian\.((jpg)|(png))")) is not None


def has_special(html):
    return 'special effect:' in html.text.lower()
