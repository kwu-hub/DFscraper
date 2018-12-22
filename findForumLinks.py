import urllib2
import json

json_file = open("DFAccessories.json", "r")
#json_file_tmp = open("DFAccessories.tmp.json", "w")
json_str = json_file.read()
data = json.loads(json_str)


def update(weapon, level, hyperlink):
    print weapon + " (Level " + level + ")"

    for key, value in data.iteritems():

        try:
            if value["Name"] == weapon and value["Level"] == int(level):
                print weapon + " (" + level + ")"
                data[key]["Name"] = '=HYPERLINK("' + hyperlink + '";"' + weapon + '")'
        except:
            print "Error"
#type>name>


for i1 in range(1, 2):
    response = urllib2.urlopen('http://forums2.battleon.com/f/tt.asp?forumid=118&p=' + str(i1) + '&tmode=10&smode=1')
    html = response.read()
    num = 31

    if (i1 == 18):
        num = 35

    for i2 in range(1, num):
        html = html[html.find('<a href="tm.asp?m=', num):]
        if (i1 == 1 and i2 < 4):
            continue

        link = html[html.find('tm.asp?m='):]
        link = link[:link.find('"')]
        # link = "tm.asp?m=21920257"
        # print link
        sub_response = urllib2.urlopen("http://forums2.battleon.com/f/" + link)

        sub_html = sub_response.read()

        sub_html = sub_html[sub_html.find("Message Starts Here"):sub_html.find(
            "<!-- Google Adsense Table REMOVED NOT WORKING -->")]
        while True:
            start_of_post = sub_html.find('<table width="98%" cellpadding="0" cellspacing="0" border="0">', 10)
            # print start_of_post
            if (start_of_post == -1):
                break
            sub_html = sub_html[start_of_post:]
            # print sub_html
            weapon_name_start = sub_html.find("<font size='3'>") + 15
            # print weapon_name_start
            if weapon_name_start == 14:
                break
            weapon = sub_html[weapon_name_start:sub_html.find("</font>")]
            # print weapon
            if weapon.find("<b>") != -1:
                weapon = weapon[3:]
            # print weapon
            weapon = weapon.strip();
            if weapon.find("</b>") != -1:
                weapon = weapon[:-4]
            level = sub_html[sub_html.find("<br> Level: ") + 12:]
            level = level[:level.find("<br>")]
            level = level.strip()
            weapon = weapon.strip();
            hyperlink = sub_html[sub_html.find("fwdwin('postnumber.asp?id=") + 26:]
            hyperlink = hyperlink[:hyperlink.find("')")]
            hyperlink = "http://forums2.battleon.com/f/fb.asp?m=" + hyperlink
            # print hyperlink
            update(weapon, level, hyperlink)

    json_file_tmp = open("DFAccessories.tmp.json", "w")
    json_file_tmp.write(json.dumps(data))
    json_file_tmp.close()
