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
        "Equip Spot": equip,
        "Name": name,
        "Level": level,
        "Link": hyperlink,
        "Element": element,
        "Item Type": item_type,

        "Crit": bonus_dict["Crit"],
        "Bonus": bonus_dict["Bonus"],
        "STR": bonus_dict["STR"],
        "DEX": bonus_dict["DEX"],
        "INT": bonus_dict["INT"],
        "CHA": bonus_dict["CHA"],
        "LUK": bonus_dict["LUK"],
        "Melee Def": bonus_dict["Melee"],
        "Pierce Def": bonus_dict["Pierce"],
        "Magic Def": bonus_dict["Magic"],
        "Parry": bonus_dict["Parry"],
        "Block": bonus_dict["Block"],
        "Dodge": bonus_dict["Dodge"],
        "END": bonus_dict["END"],
        "WIS": bonus_dict["WIS"],

        "???": bonus_dict["???"],
        "Bacon": bonus_dict["Bacon"],
        "Darkness": bonus_dict["Darkness"],
        "Disease": bonus_dict["Disease"],
        "Energy": bonus_dict["Energy"],
        "Evil": bonus_dict["Evil"],
        "Fear": bonus_dict["Fear"],
        "Fire": bonus_dict["Fire"],
        "Good": bonus_dict["Good"],
        "Ice": bonus_dict["Ice"],
        "Light": bonus_dict["Light"],
        "Metal": bonus_dict["Metal"],
        "Nature": bonus_dict["Nature"],
        "None": bonus_dict["None"],
        "Poison": bonus_dict["Poison"],
        "Silver": bonus_dict["Silver"],
        "Stone": bonus_dict["Stone"],
        "Water": bonus_dict["Water"],
        "Wind": bonus_dict["Wind"],
        "Shrink": bonus_dict["Shrink"],
        "Immobility": bonus_dict["Immobility"],
        "Health": bonus_dict["Health"],
        "Mana": bonus_dict["Mana"],
        "All": bonus_dict["All"],

        "???+All": int(bonus_dict["???"])+int(bonus_dict["All"]),
        "Bacon+All": int(bonus_dict["Bacon"])+int(bonus_dict["All"]),
        "Darkness+All": int(bonus_dict["Darkness"])+int(bonus_dict["All"]),
        "Disease+All": int(bonus_dict["Disease"])+int(bonus_dict["All"]),
        "Energy+All": int(bonus_dict["Energy"])+int(bonus_dict["All"]),
        "Evil+All": int(bonus_dict["Evil"])+int(bonus_dict["All"]),
        "Fear+All": int(bonus_dict["Fear"])+int(bonus_dict["All"]),
        "Fire+All": int(bonus_dict["Fire"])+int(bonus_dict["All"]),
        "Good+All": int(bonus_dict["Good"])+int(bonus_dict["All"]),
        "Ice+All": int(bonus_dict["Ice"])+int(bonus_dict["All"]),
        "Light+All": int(bonus_dict["Light"])+int(bonus_dict["All"]),
        "Metal+All": int(bonus_dict["Metal"])+int(bonus_dict["All"]),
        "Nature+All": int(bonus_dict["Nature"])+int(bonus_dict["All"]),
        "None+All": int(bonus_dict["None"])+int(bonus_dict["All"]),
        "Poison+All": int(bonus_dict["Poison"])+int(bonus_dict["All"]),
        "Silver+All": int(bonus_dict["Silver"])+int(bonus_dict["All"]),
        "Stone+All": int(bonus_dict["Stone"])+int(bonus_dict["All"]),
        "Water+All": int(bonus_dict["Water"])+int(bonus_dict["All"]),
        "Wind+All": int(bonus_dict["Wind"])+int(bonus_dict["All"]),
        "Shrink+All": int(bonus_dict["Shrink"])+int(bonus_dict["All"]),
        "Immobility+All": int(bonus_dict["Immobility"])+int(bonus_dict["All"]),
        "Health+All": int(bonus_dict["Health"])+int(bonus_dict["All"]),
        "Mana+All": int(bonus_dict["Mana"])+int(bonus_dict["All"]),

        "DC": first_dc,
        "DA": first_da,
        "Rare": first_rare,
        "Seasonal": first_seasonal,
        "Special Offer": first_so,
        "DM": first_dm,
        "Guardian": first_g,
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
        "Equip Spot": equip,
        "Name": name,
        "Level": second_level,
        "Link": hyperlink,
        "Element": second_element,
        "Item Type": item_type,

        "Crit": bonus_dict["Crit"],
        "Bonus": bonus_dict["Bonus"],
        "STR": bonus_dict["STR"],
        "DEX": bonus_dict["DEX"],
        "INT": bonus_dict["INT"],
        "CHA": bonus_dict["CHA"],
        "LUK": bonus_dict["LUK"],
        "Melee Def": bonus_dict["Melee"],
        "Pierce Def": bonus_dict["Pierce"],
        "Magic Def": bonus_dict["Magic"],
        "Parry": bonus_dict["Parry"],
        "Block": bonus_dict["Block"],
        "Dodge": bonus_dict["Dodge"],
        "END": bonus_dict["END"],
        "WIS": bonus_dict["WIS"],

        "???": bonus_dict["???"],
        "Bacon": bonus_dict["Bacon"],
        "Darkness": bonus_dict["Darkness"],
        "Disease": bonus_dict["Disease"],
        "Energy": bonus_dict["Energy"],
        "Evil": bonus_dict["Evil"],
        "Fear": bonus_dict["Fear"],
        "Fire": bonus_dict["Fire"],
        "Good": bonus_dict["Good"],
        "Ice": bonus_dict["Ice"],
        "Light": bonus_dict["Light"],
        "Metal": bonus_dict["Metal"],
        "Nature": bonus_dict["Nature"],
        "None": bonus_dict["None"],
        "Poison": bonus_dict["Poison"],
        "Silver": bonus_dict["Silver"],
        "Stone": bonus_dict["Stone"],
        "Water": bonus_dict["Water"],
        "Wind": bonus_dict["Wind"],
        "Shrink": bonus_dict["Shrink"],
        "Immobility": bonus_dict["Immobility"],
        "Health": bonus_dict["Health"],
        "Mana": bonus_dict["Mana"],
        "All": bonus_dict["All"],

        "???+All": int(bonus_dict["???"])+int(bonus_dict["All"]),
        "Bacon+All": int(bonus_dict["Bacon"])+int(bonus_dict["All"]),
        "Darkness+All": int(bonus_dict["Darkness"])+int(bonus_dict["All"]),
        "Disease+All": int(bonus_dict["Disease"])+int(bonus_dict["All"]),
        "Energy+All": int(bonus_dict["Energy"])+int(bonus_dict["All"]),
        "Evil+All": int(bonus_dict["Evil"])+int(bonus_dict["All"]),
        "Fear+All": int(bonus_dict["Fear"])+int(bonus_dict["All"]),
        "Fire+All": int(bonus_dict["Fire"])+int(bonus_dict["All"]),
        "Good+All": int(bonus_dict["Good"])+int(bonus_dict["All"]),
        "Ice+All": int(bonus_dict["Ice"])+int(bonus_dict["All"]),
        "Light+All": int(bonus_dict["Light"])+int(bonus_dict["All"]),
        "Metal+All": int(bonus_dict["Metal"])+int(bonus_dict["All"]),
        "Nature+All": int(bonus_dict["Nature"])+int(bonus_dict["All"]),
        "None+All": int(bonus_dict["None"])+int(bonus_dict["All"]),
        "Poison+All": int(bonus_dict["Poison"])+int(bonus_dict["All"]),
        "Silver+All": int(bonus_dict["Silver"])+int(bonus_dict["All"]),
        "Stone+All": int(bonus_dict["Stone"])+int(bonus_dict["All"]),
        "Water+All": int(bonus_dict["Water"])+int(bonus_dict["All"]),
        "Wind+All": int(bonus_dict["Wind"])+int(bonus_dict["All"]),
        "Shrink+All": int(bonus_dict["Shrink"])+int(bonus_dict["All"]),
        "Immobility+All": int(bonus_dict["Immobility"])+int(bonus_dict["All"]),
        "Health+All": int(bonus_dict["Health"])+int(bonus_dict["All"]),
        "Mana+All": int(bonus_dict["Mana"])+int(bonus_dict["All"]),

        "DC": second_dc,
        "DA": second_da,
        "Rare": second_rare,
        "Seasonal": second_seasonal,
        "Special Offer": second_so,
        "DM": second_dm,
        "Guardian": second_g,
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
        "Equip Spot": equip,
        "Name": name,
        "Level": level,
        "Link": hyperlink,
        "Element": element,
        "Item Type": item_type,

        "Crit": bonus_dict["Crit"],
        "Bonus": bonus_dict["Bonus"],
        "STR": bonus_dict["STR"],
        "DEX": bonus_dict["DEX"],
        "INT": bonus_dict["INT"],
        "CHA": bonus_dict["CHA"],
        "LUK": bonus_dict["LUK"],
        "Melee Def": bonus_dict["Melee"],
        "Pierce Def": bonus_dict["Pierce"],
        "Magic Def": bonus_dict["Magic"],
        "Parry": bonus_dict["Parry"],
        "Block": bonus_dict["Block"],
        "Dodge": bonus_dict["Dodge"],
        "END": bonus_dict["END"],
        "WIS": bonus_dict["WIS"],

        "???": bonus_dict["???"],
        "Bacon": bonus_dict["Bacon"],
        "Darkness": bonus_dict["Darkness"],
        "Disease": bonus_dict["Disease"],
        "Energy": bonus_dict["Energy"],
        "Evil": bonus_dict["Evil"],
        "Fear": bonus_dict["Fear"],
        "Fire": bonus_dict["Fire"],
        "Good": bonus_dict["Good"],
        "Ice": bonus_dict["Ice"],
        "Light": bonus_dict["Light"],
        "Metal": bonus_dict["Metal"],
        "Nature": bonus_dict["Nature"],
        "None": bonus_dict["None"],
        "Poison": bonus_dict["Poison"],
        "Silver": bonus_dict["Silver"],
        "Stone": bonus_dict["Stone"],
        "Water": bonus_dict["Water"],
        "Wind": bonus_dict["Wind"],
        "Shrink": bonus_dict["Shrink"],
        "Immobility": bonus_dict["Immobility"],
        "Health": bonus_dict["Health"],
        "Mana": bonus_dict["Mana"],
        "All": bonus_dict["All"],

        "???+All": int(bonus_dict["???"])+int(bonus_dict["All"]),
        "Bacon+All": int(bonus_dict["Bacon"])+int(bonus_dict["All"]),
        "Darkness+All": int(bonus_dict["Darkness"])+int(bonus_dict["All"]),
        "Disease+All": int(bonus_dict["Disease"])+int(bonus_dict["All"]),
        "Energy+All": int(bonus_dict["Energy"])+int(bonus_dict["All"]),
        "Evil+All": int(bonus_dict["Evil"])+int(bonus_dict["All"]),
        "Fear+All": int(bonus_dict["Fear"])+int(bonus_dict["All"]),
        "Fire+All": int(bonus_dict["Fire"])+int(bonus_dict["All"]),
        "Good+All": int(bonus_dict["Good"])+int(bonus_dict["All"]),
        "Ice+All": int(bonus_dict["Ice"])+int(bonus_dict["All"]),
        "Light+All": int(bonus_dict["Light"])+int(bonus_dict["All"]),
        "Metal+All": int(bonus_dict["Metal"])+int(bonus_dict["All"]),
        "Nature+All": int(bonus_dict["Nature"])+int(bonus_dict["All"]),
        "None+All": int(bonus_dict["None"])+int(bonus_dict["All"]),
        "Poison+All": int(bonus_dict["Poison"])+int(bonus_dict["All"]),
        "Silver+All": int(bonus_dict["Silver"])+int(bonus_dict["All"]),
        "Stone+All": int(bonus_dict["Stone"])+int(bonus_dict["All"]),
        "Water+All": int(bonus_dict["Water"])+int(bonus_dict["All"]),
        "Wind+All": int(bonus_dict["Wind"])+int(bonus_dict["All"]),
        "Shrink+All": int(bonus_dict["Shrink"])+int(bonus_dict["All"]),
        "Immobility+All": int(bonus_dict["Immobility"])+int(bonus_dict["All"]),
        "Health+All": int(bonus_dict["Health"])+int(bonus_dict["All"]),
        "Mana+All": int(bonus_dict["Mana"])+int(bonus_dict["All"]),

        "DC": is_dc(msg),
        "DA": is_da(msg),
        "Rare": is_rare(msg),
        "Seasonal": is_seasonal(msg),
        "Special Offer": is_so(msg),
        "DM": is_dm(msg),
        "Guardian": is_g(msg),
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
    images = len(html.findAll('img', src=re.compile("DC\.((jpg)|(png))", re.I)))
    entry_count = html.getText().lower().count('price:')
    if (images < entry_count) and entry_count > 1 and images != 0:
        return "optional"
    return html.find('img', src=re.compile("DC\.((jpg)|(png))", re.I)) is not None


def is_rare(html):
    images = len(html.findAll('img', src=re.compile("Rare\.((jpg)|(png))", re.I)))
    entry_count = html.getText().lower().count('price:')
    if (images < entry_count) and entry_count > 1 and images != 0:
        return "optional"
    return html.find('img', src=re.compile("Rare\.((jpg)|(png))", re.I)) is not None


def is_seasonal(html):
    images = len(html.findAll('img', src=re.compile("Seasonal\.((jpg)|(png))", re.I)))
    entry_count = html.getText().lower().count('price:')
    if (images < entry_count) and entry_count > 1 and images != 0:
        return "optional"
    return html.find('img', src=re.compile("Seasonal\.((jpg)|(png))", re.I)) is not None


def is_da(html):
    images = len(html.findAll('img', src=re.compile("DA\.((jpg)|(png))", re.I)))
    entry_count = html.getText().lower().count('price:')
    if (images < entry_count) and entry_count > 1 and images != 0:
        return "optional"
    return html.find('img', src=re.compile("DA\.((jpg)|(png))", re.I)) is not None


def is_so(html):
    return (html.find('img', src=re.compile("SpecialOffer\.((jpg)|(png))", re.I)) is not None) \
           or (html.find('img', src=re.compile("DoomKnight\.((jpg)|(png))", re.I)) is not None)


def is_dm(html):
    return html.find('img', src=re.compile("DM\.((jpg)|(png))", re.I)) is not None


def is_g(html):
    return html.find('img', src=re.compile("Guardian\.((jpg)|(png))", re.I)) is not None


def has_special(html):
    return 'special effect:' in html.text.lower()
