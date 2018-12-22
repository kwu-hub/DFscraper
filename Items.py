# Helper functions for parsing specific values from message

import re


# Determines if the message received contains the attributes of an item
def is_item(html):
    return 'Equip Spot:' in html.text and 'Category: ' in html.text and 'Level: ' in html.text and 'Bonuses: ' in html.text


# Helper function used to find the specific value between the text of 2 different tags
def find_between_tags(html, tag, next_tag):
    text = html.getText()
    tag = tag
    next_tag = next_tag
    tag_index = text.find(tag)
    next_index = text.find(next_tag)
    if tag_index == -1 or next_index == -1:
        if tag_index != next_index:
            print "First Index: " + str(tag_index) + " Next Index: " + str(next_index)
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
    next_tag = 'Rarity: '
    return find_between_tags(html, tag, next_tag)


def get_element(html):
    tag = 'Element: '
    next_tag = 'Bonuses: '
    return find_between_tags(html, tag, next_tag)


def get_link(html):
    # Finds tag with the link and gets the value of onclick
    link = html.find(onclick=re.compile("fwdwin"))['onclick']
    link = link[link.find("=")+1:link.find("')")]
    hyperlink = "http://forums2.battleon.com/f/fb.asp?m=" + link
    return hyperlink


def is_dc(html):
    return html.find('img', src=re.compile("DC\.png")) is not None
