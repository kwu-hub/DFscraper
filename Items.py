# Helper functions for parsing specific values from message
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

def isItem(html):
    return 'Equip Spot:' in html.text and 'Category: ' in html.text and 'Level: ' in html.text and 'Bonuses: ' in html.text

def findBetweenTags(html, tag, nextTag):
    text = html.getText()
    tag = tag
    nextTag = nextTag
    tagIndex = text.find(tag)
    nextIndex = text.find(nextTag)
    if tagIndex == -1 or nextIndex == -1:
        if tagIndex != nextIndex:
            print "First Index: " + str(tagIndex) + " Next Index: " + str(nextIndex)
        return ''
    itemValue = text[text.find(tag)+len(tag): text.find(nextTag)]
    return itemValue

def getName(html):
    name = html.b.getText()
    return name

def getLevel(html):
    tag = 'Level: '
    nextTag = 'Element: '
    return findBetweenTags(html, tag, nextTag)

def getEquip(html):
    tag = 'Equip Spot: '
    nextTag = 'Category: '
    return findBetweenTags(html, tag, nextTag)


def getType(html):
    tag = 'Item Type: '
    nextTag = 'Equip Spot: '
    return findBetweenTags(html, tag, nextTag)
