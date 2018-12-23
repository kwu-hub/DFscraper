# This file contains helper functions for parsing specific values from message
import re


def save_item():
    return


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
    if html.getText().find(",Boost") != -1:  # Beacon of Hope (page 5) has strikethrough boost and Ability, Boost must come last because it is before Ability on the page
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


def is_dc(html):
    return html.find('img', src=re.compile("DC")) is not None


def is_rare(html):
    return html.find('img', src=re.compile("Rare")) is not None


def is_seasonal(html):
    return html.find('img', src=re.compile("Seasonal")) is not None


def is_da(html):
    return html.find('img', src=re.compile("DA")) is not None


def is_so(html):
    return (html.find('img', src=re.compile("SpecialOffer")) is not None) or (html.find('img', src=re.compile("DoomKnight")) is not None)


def is_dm(html):
    return html.find('img', src=re.compile("DM")) is not None


def is_g(html):
    return html.find('img', src=re.compile("Guardian")) is not None

