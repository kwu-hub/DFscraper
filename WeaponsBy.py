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
    name = get_name(msg)
    level = get_level(msg)
    element = get_element(msg)
    item_type = get_type(msg)
    bonuses = get_bonus(msg)
    attack_type = get_type_attack(msg)
    if attack_type != "Magic" and attack_type != "Melee" and attack_type != "Pierce" and \
            attack_type != "Magic/Pierce/Melee" and attack_type != "Magic/Melee":
        m = ("Page: " + str(page) + ", Row: " + str(row) + "; Attack Type Error 2\n")
        out = open("weapons" + str(sys.argv[1]) + "errors.txt", "a")
        out.write(name + ": " + m + "\n")
    damage = get_damage(msg)
    if 'scaled' in damage:
        print ("scaled")
        out = open("weapons" + str(sys.argv[1]) + ".txt", "a")
        out.write("scaled" + "\n")
        return
    damage_low = damage.split("-")[0]
    damage_high = damage.split("-")[1]

    # Creates dict of bonuses with key equal to the first word of the bonus (ex. Pierce Def->Pierce)
    bonus_dict = defaultdict(int)
    if bonuses != 'None':
        for bonus in bonuses.split(', '):
            if bonus.lower() == bonus and "???" not in bonus:
                m = ("Page: " + str(page) + ", Row: " + str(row) + "; Case Error\n")
                out = open("weapons" + str(sys.argv[1]) + "errors.txt", "a")
                out.write(name + ": " + m + "\n")
            if "+" in bonus:
                nb = bonus.split("+")
                bonus_dict[nb[0].split(" ")[0]] = int(nb[1])
            else:
                nb = bonus.split("-")
                bonus_dict[nb[0].split(" ")[0]] = int(nb[1]) * -1

    data[attack_type].append({
        "name": name,
        "damage": str((float(damage_high)+float(damage_low))//2),
        "level": level,
        "damage_low": damage_low,
        "damage_high": damage_high,
        "element": element,
        "item_type": item_type,
        "attack_type": attack_type,
        "link": hyperlink,

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

        "???+all": int(bonus_dict["???"])+int(bonus_dict["All"]),
        "bacon+all": int(bonus_dict["Bacon"])+int(bonus_dict["All"]),
        "darkness+all": int(bonus_dict["Darkness"])+int(bonus_dict["All"]),
        "disease+all": int(bonus_dict["Disease"])+int(bonus_dict["All"]),
        "energy+all": int(bonus_dict["Energy"])+int(bonus_dict["All"]),
        "evil+all": int(bonus_dict["Evil"])+int(bonus_dict["All"]),
        "fear+all": int(bonus_dict["Fear"])+int(bonus_dict["All"]),
        "fire+all": int(bonus_dict["Fire"])+int(bonus_dict["All"]),
        "good+all": int(bonus_dict["Good"])+int(bonus_dict["All"]),
        "ice+all": int(bonus_dict["Ice"])+int(bonus_dict["All"]),
        "light+all": int(bonus_dict["Light"])+int(bonus_dict["All"]),
        "metal+all": int(bonus_dict["Metal"])+int(bonus_dict["All"]),
        "nature+all": int(bonus_dict["Nature"])+int(bonus_dict["All"]),
        "none+all": int(bonus_dict["None"])+int(bonus_dict["All"]),
        "poison+all": int(bonus_dict["Poison"])+int(bonus_dict["All"]),
        "silver+all": int(bonus_dict["Silver"])+int(bonus_dict["All"]),
        "stone+all": int(bonus_dict["Stone"])+int(bonus_dict["All"]),
        "water+all": int(bonus_dict["Water"])+int(bonus_dict["All"]),
        "wind+all": int(bonus_dict["Wind"])+int(bonus_dict["All"]),
        "shrink+all": int(bonus_dict["Shrink"])+int(bonus_dict["All"]),
        "immobility+all": int(bonus_dict["Immobility"])+int(bonus_dict["All"]),
        "health+all": int(bonus_dict["Health"])+int(bonus_dict["All"]),
        "mana+all": int(bonus_dict["Mana"])+int(bonus_dict["All"]),

        "dc": first_dc,
        "da": first_da,
        "rare": first_rare,
        "seasonal": first_seasonal,
        "so": first_so,
        "dm": first_dm,
        "g": first_g,

        "has_special": has_special(msg)
    })
    to_print = name + " (Level: " + level + "): " + attack_type + "|" + damage_low + "-" + damage_high + "|" + bonuses + "|"
    print to_print
    out = open("weapons" + str(sys.argv[1]) + ".txt", "a")
    out.write(str(to_print)+"\n")

    # ---------------------------- Add second item ----------------------------
    # Have to find the second appearance of each of the values
    text = msg.getText()
    second_tag_index_level = text.find("Level: ", text.find("Level: ")+1)
    second_tag_index_damage = text.find("Damage: ", text.find("Damage: ")+1)
    second_tag_index_element = text.find("Element: ", text.find("Element: ")+1)
    second_tag_index_bonuses = text.find("Bonuses: ", text.find("Bonuses: ")+1)
    second_level = text[second_tag_index_level + len("Level: "):second_tag_index_damage]
    second_damage = text[second_tag_index_damage + len("Damage: "):second_tag_index_element]
    if 'Scaled' in second_damage:
        print ("Scaled")
        out = open("weapons" + str(sys.argv[1]) + ".txt", "a")
        out.write("Scaled" + "\n")
        return
    second_damage_low = second_damage.split("-")[0]
    second_damage_high = second_damage.split("-")[1]
    second_element = text[second_tag_index_element + len("Element: "):second_tag_index_bonuses]

    if text[second_tag_index_element:].find("Bonuses: None") != -1:
        second_bonuses = 'None'
    else:
        regex = re.compile("([0-9][a-zA-Z])|([0-9],[a-zA-Z])|([0-9]\.[a-zA-Z])")
        m = regex.search(text[second_tag_index_bonuses:])
        second_tag_index_bonuses_end = text.find(m.group(0))+1
        second_bonuses = text[second_tag_index_bonuses + len("Bonuses: "):second_tag_index_bonuses_end]

    # Creates dict of bonuses with key equal to the first word of the bonus (ex. Pierce Def->Pierce)
    bonus_dict = defaultdict(int)
    if second_bonuses != 'None':
        for bonus in second_bonuses.split(', '):
            if bonus.lower() == bonus and "???" not in bonus:
                m = ("Page: " + str(page) + ", Row: " + str(row) + "; Case Error\n")
                out = open("weapons" + str(sys.argv[1]) + "errors.txt", "a")
                out.write(name + ": " + m + "\n")
            if "+" in bonus:
                nb = bonus.split("+")
                bonus_dict[nb[0].split(" ")[0]] = int(nb[1])
            else:
                nb = bonus.split("-")
                bonus_dict[nb[0].split(" ")[0]] = int(nb[1]) * -1

    data[attack_type].append({
        "name": name,
        "damage": str((float(second_damage_high)+float(second_damage_low))/2.0),
        "level": second_level,
        "damage_low": second_damage_low,
        "damage_high": second_damage_high,
        "element": second_element,
        "item_type": item_type,
        "attack_type": attack_type,
        "link": hyperlink,

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

        "???+all": int(bonus_dict["???"])+int(bonus_dict["All"]),
        "bacon+all": int(bonus_dict["Bacon"])+int(bonus_dict["All"]),
        "darkness+all": int(bonus_dict["Darkness"])+int(bonus_dict["All"]),
        "disease+all": int(bonus_dict["Disease"])+int(bonus_dict["All"]),
        "energy+all": int(bonus_dict["Energy"])+int(bonus_dict["All"]),
        "evil+all": int(bonus_dict["Evil"])+int(bonus_dict["All"]),
        "fear+all": int(bonus_dict["Fear"])+int(bonus_dict["All"]),
        "fire+all": int(bonus_dict["Fire"])+int(bonus_dict["All"]),
        "good+all": int(bonus_dict["Good"])+int(bonus_dict["All"]),
        "ice+all": int(bonus_dict["Ice"])+int(bonus_dict["All"]),
        "light+all": int(bonus_dict["Light"])+int(bonus_dict["All"]),
        "metal+all": int(bonus_dict["Metal"])+int(bonus_dict["All"]),
        "nature+all": int(bonus_dict["Nature"])+int(bonus_dict["All"]),
        "none+all": int(bonus_dict["None"])+int(bonus_dict["All"]),
        "poison+all": int(bonus_dict["Poison"])+int(bonus_dict["All"]),
        "silver+all": int(bonus_dict["Silver"])+int(bonus_dict["All"]),
        "stone+all": int(bonus_dict["Stone"])+int(bonus_dict["All"]),
        "water+all": int(bonus_dict["Water"])+int(bonus_dict["All"]),
        "wind+all": int(bonus_dict["Wind"])+int(bonus_dict["All"]),
        "shrink+all": int(bonus_dict["Shrink"])+int(bonus_dict["All"]),
        "immobility+all": int(bonus_dict["Immobility"])+int(bonus_dict["All"]),
        "health+all": int(bonus_dict["Health"])+int(bonus_dict["All"]),
        "mana+all": int(bonus_dict["Mana"])+int(bonus_dict["All"]),

        "dc": second_dc,
        "da": second_da,
        "rare": second_rare,
        "seasonal": second_seasonal,
        "so": second_so,
        "dm": second_dm,
        "g": second_g,

        "has_special": has_special(msg)
    })
    to_print = "*" + name + " (Level: " + level + "): " + attack_type + "|" + damage_low + "-" + damage_high + "|" + bonuses + "|"
    print to_print
    out = open("weapons" + str(sys.argv[1]) + ".txt", "a")
    out.write(str(to_print)+"\n")


def save_item(msg, data, hyperlink, page, row):
    name = get_name(msg)
    level = get_level(msg)
    element = get_element(msg)
    item_type = get_type(msg)
    bonuses = get_bonus(msg)
    attack_type = get_type_attack(msg)
    damage = get_damage(msg)

    if attack_type != "Magic" and attack_type != "Melee" and attack_type != "Pierce" \
            and attack_type != "Magic/Pierce/Melee" and attack_type != "Magic/Melee":
        m = ("Page: " + str(page) + ", Row: " + str(row) + "; Attack Type Error\n")
        out = open("weapons" + str(sys.argv[1]) + "errors.txt", "a")
        out.write(name + ": " + m + "\n")

    '''
    Exceptions
    '''
    '''
    Scaled Damage Values:
        Blade of Destiny (damage is "Scaled to Ash's level")
        Vanilla Ice Katana
        Frozen Claymore
        Foam Rolith's Hammer
        All 12 Drops from "The Lymcrest Labrynth
    '''
    if 'scaled' in damage.lower():
        print ("Scaled")
        out = open("weapons" + str(sys.argv[1]) + ".txt", "a")
        out.write("Scaled" + "\n")
        return
    '''
    CorDemi Codex has 2 Damage values (use the higher value (Sword/Dagger/Staff)):
        Basic CorDemi Codex
        Advanced CorDemi Codex
        Master CorDemi Codex
    '''
    if name == 'Basic CorDemi Codex':
        damage = '11-15'
    if name == 'Advanced CorDemi Codex':
        damage = '25-40'
    if name == 'Master CorDemi Codex':
        damage = '35-51'
    '''
    Spear Tip name is not scraped
    '''
    if hyperlink == "http://forums2.battleon.com/f/fb.asp?m=5042008":
        name = "Spear Tip"

    damage_low = damage.split("-")[0]
    damage_high = damage.split("-")[1]
    # Creates dict of bonuses with key equal to the first word of the bonus (ex. Pierce Def->Pierce)
    bonus_dict = defaultdict(int)
    if bonuses != 'None':
        for bonus in bonuses.split(', '):
            if bonus.lower() == bonus and "???" not in bonus:
                m = ("Page: " + str(page) + ", Row: " + str(row) + "; Case Error\n")
                out = open("weapons" + str(sys.argv[1]) + "errors.txt", "a")
                out.write(name + ": " + m + "\n")
            if "+" in bonus:
                nb = bonus.split("+")
                bonus_dict[nb[0].split(" ")[0]] = int(nb[1])
            else:
                nb = bonus.split("-")
                bonus_dict[nb[0].split(" ")[0]] = int(nb[1]) * -1

    data[attack_type].append({
        "name": name,
        "damage": str((float(damage_high)+float(damage_low))//2),
        "level": level,
        "damage_low": damage_low,
        "damage_high": damage_high,
        "element": element,
        "item_type": item_type,
        "attack_type": attack_type,
        "link": hyperlink,

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

        "???+all": int(bonus_dict["???"])+int(bonus_dict["All"]),
        "bacon+all": int(bonus_dict["Bacon"])+int(bonus_dict["All"]),
        "darkness+all": int(bonus_dict["Darkness"])+int(bonus_dict["All"]),
        "disease+all": int(bonus_dict["Disease"])+int(bonus_dict["All"]),
        "energy+all": int(bonus_dict["Energy"])+int(bonus_dict["All"]),
        "evil+all": int(bonus_dict["Evil"])+int(bonus_dict["All"]),
        "fear+all": int(bonus_dict["Fear"])+int(bonus_dict["All"]),
        "fire+all": int(bonus_dict["Fire"])+int(bonus_dict["All"]),
        "good+all": int(bonus_dict["Good"])+int(bonus_dict["All"]),
        "ice+all": int(bonus_dict["Ice"])+int(bonus_dict["All"]),
        "light+all": int(bonus_dict["Light"])+int(bonus_dict["All"]),
        "metal+all": int(bonus_dict["Metal"])+int(bonus_dict["All"]),
        "nature+all": int(bonus_dict["Nature"])+int(bonus_dict["All"]),
        "none+all": int(bonus_dict["None"])+int(bonus_dict["All"]),
        "poison+all": int(bonus_dict["Poison"])+int(bonus_dict["All"]),
        "silver+all": int(bonus_dict["Silver"])+int(bonus_dict["All"]),
        "stone+all": int(bonus_dict["Stone"])+int(bonus_dict["All"]),
        "water+all": int(bonus_dict["Water"])+int(bonus_dict["All"]),
        "wind+all": int(bonus_dict["Wind"])+int(bonus_dict["All"]),
        "shrink+all": int(bonus_dict["Shrink"])+int(bonus_dict["All"]),
        "immobility+all": int(bonus_dict["Immobility"])+int(bonus_dict["All"]),
        "health+all": int(bonus_dict["Health"])+int(bonus_dict["All"]),
        "mana+all": int(bonus_dict["Mana"])+int(bonus_dict["All"]),

        "dc": is_dc(msg),
        "da": is_da(msg),
        "rare": is_rare(msg),
        "seasonal": is_seasonal(msg),
        "so": is_so(msg),
        "dm": is_dm(msg),
        "g": is_g(msg),

        "has_special": has_special(msg)
    })
    to_print = name + " (Level: " + level + "): " + attack_type + "|" + damage_low + "-" + damage_high + "|" + bonuses + "|"
    print to_print
    out = open("weapons" + str(sys.argv[1]) + ".txt", "a")
    out.write(str(to_print)+"\n")


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
        text = text[:text.find(m.group(0))+1]
        return text

    # All other values
    tag_index = text.find(tag)
    next_index = text.find(next_tag)
    if tag_index == -1 or next_index == -1:
        if tag_index != next_index:
            to_print = "'" + tag + "'" + str(tag_index) + "|'" + next_tag + "'" + str(next_index)
            print to_print
            out = open("weapons" + str(sys.argv[1]) + ".txt", "a")
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
    next_tag = 'Damage: '
    return find_between_tags(html, tag, next_tag)


def get_damage(html):
    tag = 'Damage: '
    next_tag = 'Element: '
    return find_between_tags(html, tag, next_tag)


def get_element(html):
    tag = 'Element: '
    next_tag = 'Bonuses: '
    return find_between_tags(html, tag, next_tag)


def get_bonus(html):
    tag = 'Bonuses: '
    return find_between_tags(html, tag, "bonus_case")


def get_type(html):
    tag = 'Item Type: '
    next_tag = 'Attack Type: '
    return find_between_tags(html, tag, next_tag)


def get_type_attack(html):
    tag = 'Attack Type: '
    next_tag = 'Category: '
    return find_between_tags(html, tag, next_tag)


def get_link(html):
    # Finds tag with the link and gets the value of onclick
    link = html.find(onclick=re.compile("fwdwin"))['onclick']
    link = link[link.find("=")+1:link.find("')")]
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
