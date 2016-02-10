#!/usr/bin/env python

import json
import re
import posixpath
import urlparse
import yaml
from urllib import FancyURLopener

class MyOpener(FancyURLopener, object):
    version = "Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"

myopener = MyOpener()

menu = {}
dayindex = { 1: 'Mandag',
             2: 'Tirsdag',
             3: 'Onsdag',
             4: 'Torsdag',
             5: 'Fredag'
           }
dayindex_rev = { 'monday': '1',
             'tuesday': '2',
             'wednesday': '3',
             'thursday': '4',
             'friday': '5'

}

def parseYaml():
    with open('menu.yaml') as file:
        yaml_data = file.read()
    yaml_dump = yaml.load(yaml_data)
    for day, meals in yaml_dump.iteritems():
        # day is the literal, convert to day of week number
        dayofweek = int(dayindex_rev[day])
        addDay(dayofweek, meals)

def addDay(day, meals):
    global menu
    day_literal = dayindex[day]
    daymeal = meals["meal"]
    daysoup = meals["soup"]
    menu[day] = {}
    menu[day]["name"] = day_literal
    menu[day]["soup"] = {}
    menu[day]["soup"]["name"] = daysoup
    menu[day]["soup"]["picture"] = findPicture(daysoup)
    menu[day]["meal"] = {}
    menu[day]["meal"]["name"] = daymeal
    menu[day]["meal"]["picture"] = findPicture(daymeal)

def findPicture(meal):
    search_term = (u"https://www.google.pt/search?q=%s&biw=80&bih=80&source=lnms&tbm=isch&sa=X&tbs=isz:l&tbm=isch" % meal).encode('utf-8')
    page = myopener.open(search_term)
    html = page.read()
    for mymatch in re.finditer(r'<a href="/imgres\?imgurl=(.*?)&amp;imgrefurl', html, re.IGNORECASE | re.DOTALL | re.MULTILINE):
        for match in re.finditer(r'(.*\.(?:jpg|png))', mymatch.group(1), re.IGNORECASE):
            path = match.group(0)
            path_split = path.split("://")
            new_path = "//%s" % path_split[1]
            return new_path

def saveMenu():
    with open('menu.json', 'w') as f:
        f.write(json.dumps(menu))

if __name__ == "__main__":
    parseYaml()
    saveMenu()
