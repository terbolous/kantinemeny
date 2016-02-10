#!/usr/bin/env python

import json
import re
import posixpath
import urlparse
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

def addDay(day):
    global meny
    day_literal = dayindex[day]
    print("Please inform of the meals for %s:" % day_literal)
    daysoup = raw_input("Soup: ")
    daymeal = raw_input("Warm meal: ")
    menu[day] = {}
    menu[day]["name"] = day_literal
    menu[day]["soup"] = {}
    menu[day]["soup"]["name"] = daysoup
    menu[day]["soup"]["picture"] = findPicture(daysoup)
    menu[day]["meal"] = {}
    menu[day]["meal"]["name"] = daymeal
    menu[day]["meal"]["picture"] = findPicture(daymeal)

def findPicture(meal):
    search_term = "https://www.google.pt/search?q=%s&biw=80&bih=80&source=lnms&tbm=isch&sa=X&tbs=isz:l&tbm=isch" % meal
    page = myopener.open(search_term)
    html = page.read()
    for mymatch in re.finditer(r'<a href="/imgres\?imgurl=(.*?)&amp;imgrefurl', html, re.IGNORECASE | re.DOTALL | re.MULTILINE):
        for match in re.finditer(r'(.*\.(?:jpg|png))', mymatch.group(1), re.IGNORECASE):
            path = match.group(0)
            return path

def saveMenu():
    with open('menu.json', 'w') as f:
        f.write(json.dumps(menu))

if __name__ == "__main__":
    for day in range(1, 6):
        addDay(day)
    saveMenu()
