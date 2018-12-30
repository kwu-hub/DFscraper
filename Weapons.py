# This file contains helper functions for parsing specific values from message
import re
from collections import defaultdict


# This function should rarely be used
# It is only used for messages with more than one bonuses value
def save_2_items(msg, data, hyperlink):
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
                    if "Rare" in imgs :
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
    damage = get_damage(msg)
    damage_low = damage.split("-")[0]
    damage_high = damage.split("-")[1]

    # Creates dict of bonuses with key equal to the first word of the bonus (ex. Pierce Def->Pierce)
    bonus_dict = defaultdict(int)
    if bonuses != 'None':
        for bonus in bonuses.split(', '):
            if "+" in bonus:
                nb = bonus.split("+")
                bonus_dict[nb[0].split(" ")[0]] = int(nb[1])
            else:
                nb = bonus.split("-")
                bonus_dict[nb[0].split(" ")[0]] = int(nb[1]) * -1

    data[attack_type].append({
        name + " (Level " + level + ")": {
            "name": name,
            "level": level,
            "damage_low": damage_low,
            "damage_high": damage_high,
            "element": element,
            "item_type": item_type,
            "attack_type": attack_type,
            "link": hyperlink,

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

            "dc": first_dc,
            "da": first_da,
            "rare": first_rare,
            "seasonal": first_seasonal,
            "so": first_so,
            "dm": first_dm,
            "g": first_g,

            "has_special": has_special(msg)
        }
    })
    print name + " (Level: " + level + "): " + attack_type + "|" + damage_low + "-" + damage_high + "|" + bonuses + "|"

    # ---------------------------- Add second item ----------------------------
    # Have to find the second appearance of each of the values
    text = msg.getText().lower()
    second_tag_index_level = text.find("level: ", text.find("level: ")+1)
    second_tag_index_damage = text.find("damage: ", text.find("damage: ")+1)
    second_tag_index_element = text.find("element: ", text.find("element: ")+1)
    second_tag_index_bonuses = text.find("bonuses: ", text.find("bonuses: ")+1)
    second_level = text[second_tag_index_level + len("level: "):second_tag_index_damage]
    second_damage = text[second_tag_index_damage + len("damage: "):second_tag_index_element]
    second_damage_low = second_damage.split("-")[0]
    second_damage_high = second_damage.split("-")[1]
    second_element = text[second_tag_index_element + len("element: "):second_tag_index_bonuses]

    if text[second_tag_index_element:].find("bonuses: none") != -1:
        second_bonuses = 'None'
    else:
        regex = re.compile("([0-9][a-zA-Z])|([0-9],[a-zA-Z])|([0-9]\.[a-zA-Z])")
        m = regex.search(text[second_tag_index_bonuses:])
        second_tag_index_bonuses_end = text.find(m.group(0))+1
        second_bonuses = text[second_tag_index_bonuses + len("bonuses: "):second_tag_index_bonuses_end]

    # Creates dict of bonuses with key equal to the first word of the bonus (ex. Pierce Def->Pierce)
    bonus_dict = defaultdict(int)
    if second_bonuses != 'None':
        for bonus in second_bonuses.split(', '):
            if "+" in bonus:
                nb = bonus.split("+")
                bonus_dict[nb[0].split(" ")[0]] = int(nb[1])
            else:
                nb = bonus.split("-")
                bonus_dict[nb[0].split(" ")[0]] = int(nb[1]) * -1

    data[second_damage].append({
        name + " (Level " + level + ")": {
            "name": name,
            "level": second_level,
            "damage_low": second_damage_low,
            "damage_high": second_damage_high,
            "element": second_element,
            "item_type": item_type,
            "attack_type": attack_type,
            "link": hyperlink,

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

            "dc": second_dc,
            "da": second_da,
            "rare": second_rare,
            "seasonal": second_seasonal,
            "so": second_so,
            "dm": second_dm,
            "g": second_g,

            "has_special": has_special(msg)
        }
    })
    print "*" + name + " (Level: " + level + "): " + attack_type + "|" + damage_low + "-" + damage_high + "|" + bonuses + "|"


def save_item(msg, data, hyperlink):
    name = get_name(msg)
    level = get_level(msg)
    element = get_element(msg)
    item_type = get_type(msg)
    bonuses = get_bonus(msg)
    attack_type = get_type_attack(msg)
    damage = get_damage(msg)
    damage_low = damage.split("-")[0]
    damage_high = damage.split("-")[1]

    '''
    Exceptions due to typos in the forums
    '''

    # Creates dict of bonuses with key equal to the first word of the bonus (ex. Pierce Def->Pierce)
    bonus_dict = defaultdict(int)
    if bonuses != 'None':
        for bonus in bonuses.split(', '):
            if "+" in bonus:
                nb = bonus.split("+")
                bonus_dict[nb[0].split(" ")[0]] = int(nb[1])
            else:
                nb = bonus.split("-")
                bonus_dict[nb[0].split(" ")[0]] = int(nb[1]) * -1

    data[attack_type].append({
        name + " (Level " + level + ")": {
            "name": name,
            "level": level,
            "damage_low": damage_low,
            "damage_high": damage_high,
            "element": element,
            "item_type": item_type,
            "attack_type": attack_type,
            "link": hyperlink,

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
            "g": is_g(msg),

            "has_special": has_special(msg)
        }
    })

    print name + " (Level: " + level + "): " + attack_type + "|" + damage_low + "-" + damage_high + "|" + bonuses + "|"


# Determines if the message received contains the attributes of an item
def is_item(html):
    return 'equip spot:' in html.text.lower() and 'category: ' in html.text.lower() and 'level: ' in html.text.lower() \
           and 'bonuses: ' in html.text.lower()


# Helper function used to find the specific value between the text of 2 different tags
def find_between_tags(html, tag, next_tag):
    text = html.getText().lower()

    # Handles the unknown text that follows bonuses (Effect, Ability, DC, etc.) Comedy Cloak (page 13)
    # The bonuses category ends with a number and is followed by a letter that is the next category
    # The code finds that index and gets values in between
    if next_tag == "bonus_case":
        # Handles items without bonuses
        if text.find("bonuses: none") != -1:
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
            print "'" + tag + "'" + str(tag_index) + "|'" + next_tag + "'" + str(next_index)
        return ''
    item_value = text[text.find(tag) + len(tag): text.find(next_tag)]
    return item_value


def get_name(html):
    msg = html.find('td', attrs={'class': 'msg'})
    name = msg.b.getText()
    return name


def get_level(html):
    tag = 'level: '
    next_tag = 'damage: '
    return find_between_tags(html, tag, next_tag)


def get_damage(html):
    tag = 'damage: '
    next_tag = 'element: '
    return find_between_tags(html, tag, next_tag)


def get_element(html):
    tag = 'element: '
    next_tag = 'bonuses: '
    return find_between_tags(html, tag, next_tag)


def get_bonus(html):
    tag = 'bonuses: '
    return find_between_tags(html, tag, "bonus_case")


def get_type(html):
    tag = 'item type: '
    next_tag = 'attack type: '
    return find_between_tags(html, tag, next_tag)


def get_type_attack(html):
    tag = 'attack type: '
    next_tag = 'category: '
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
