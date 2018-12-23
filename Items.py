# This file contains helper functions for parsing specific values from message
import re
from collections import defaultdict


def save_item(msg, data, hyperlink):
    equip = get_equip(msg)
    name = get_name(msg)
    level = get_level(msg)
    element = get_element(msg)
    item_type = get_type(msg)
    bonuses = get_bonus(msg)

    '''
    Exceptions due to typos in the forums
    Boxing Ring: Category and Equip Spot are in reverse order
    Patrick's Emerald Green Hat: has 2 spaces after "Equip Spot:" instead of 1
    '''
    if name == "Boxing Ring":
        equip = "finger"
    if name == "Patrick's Emerald Green Hat":
        equip = "head"

    if name == "Grenwog Basket II":  # missing + in Pierce Def
        bonuses = "None +1"
    if name == "Golden Arbitrator VII":  # missing + in dodge
        bonuses = "None +1"
    if name == "Golden Arbitrator VIII":
        bonuses = "None +1"
    if name == "Golden Arbitrator IX":
        bonuses = "None +1"
    if name == "Grand Guardian Helm":  # missing + in pierce def
        bonuses = "None +1"
    if name == "Golden Battlespell Helm VII":  # missing + in dodge
        bonuses = "None +1"
    if name == "Golden Battlespell Helm VIII":
        bonuses = "None +1"
    if name == "Golden Battlespell Helm IX":
        bonuses = "None +1"
    if name == "High Commander Helm" and level == "28":  # missing WIS +
        bonuses = "None +1"
    if name == "Rokpol Ring":  # Missing comma before Bonus
        bonuses = "None +1"
    if name == "Silver Laurels V":  # Extra comma after immobility 64
        bonuses = "None +1"
    if name == "Silvered Bells Cape VII":  # . after water 64
        bonuses = "None +1"
    if name == "Silvered Bells Cape VIII":
        bonuses = "None +1"
    if name == "Wings of the Unchained" and level == "70":  # Parry probably isn't 34 and missing comma after
        bonuses = "None +1"

    print name + " (Level: " + level + "): " + bonuses + "|" + equip

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


# Determines if the message received contains the attributes of an item
def is_item(html):
    return 'equip spot:' in html.text.lower() and 'category: ' in html.text.lower() and 'level: ' in html.text.lower()\
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
    next_tag = 'element: '
    return find_between_tags(html, tag, next_tag)


def get_equip(html):
    tag = 'equip spot: '
    next_tag = 'category: '
    return find_between_tags(html, tag, next_tag)


def get_type(html):
    tag = 'item type: '
    next_tag = 'equip spot: '
    return find_between_tags(html, tag, next_tag)


def get_bonus(html):
    tag = 'bonuses: '
    '''
    next_tag = 'Rarity:'  # Boondock's Saintly Cloak (page 8) has no space after "Rarity"
    if html.getText().find("Abilities") != -1:  # Bacon Storm (page 4) has Ability
        next_tag = 'Abilities:'
    if html.getText().find("Modifies") != -1:  # Baltael's Aventail (page 4) has Modifies
        next_tag = 'Modifies:'
    # Beacon of Hope has strikethrough boost and Ability, Boost must come last since it is before Ability on the page
    if html.getText().find(",Boost") != -1:  
        next_tag = ',Boost'
    '''
    return find_between_tags(html, tag, "bonus_case")


def get_element(html):
    tag = 'element: '
    next_tag = 'bonuses: '
    return find_between_tags(html, tag, next_tag)


def get_link(html):
    # Finds tag with the link and gets the value of onclick
    link = html.find(onclick=re.compile("fwdwin"))['onclick']
    link = link[link.find("=")+1:link.find("')")]
    hyperlink = "http://forums2.battleon.com/f/fb.asp?m=" + link
    return hyperlink


# For DC, Rare, Seasonal, and DA tags we check if there are more than 1 entry (determined by multiple location: tags)
# If there are multiple entries, we find the count of the given tag
# If tag count is 0, then it is False
# If tag count is same as entries, then it is True (each entry has it so it is not optional)
# If tag count is neither, then it is optional (it only shows up on some of the entries)
# Assumes Guardian, Special Offer, DM has no optional
def is_dc(html):
    images = len(html.findAll('img', src=re.compile("DC\.((jpg)|(png))")))
    entry_count = html.getText().lower().count('location:')
    if (images < entry_count) and entry_count > 1 and images != 0:
        return "optional"
    return html.find('img', src=re.compile("DC\.((jpg)|(png))")) is not None


def is_rare(html):
    images = len(html.findAll('img', src=re.compile("Rare\.((jpg)|(png))")))
    entry_count = html.getText().lower().count('location:')
    if (images < entry_count) and entry_count > 1 and images != 0:
        return "optional"
    return html.find('img', src=re.compile("Rare\.((jpg)|(png))")) is not None


def is_seasonal(html):
    images = len(html.findAll('img', src=re.compile("Seasonal\.((jpg)|(png))")))
    entry_count = html.getText().lower().count('location:')
    if (images < entry_count) and entry_count > 1 and images != 0:
        return "optional"
    return html.find('img', src=re.compile("Seasonal\.((jpg)|(png))")) is not None


def is_da(html):
    images = len(html.findAll('img', src=re.compile("DA\.((jpg)|(png))")))
    entry_count = html.getText().lower().count('location:')
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

