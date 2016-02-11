#!/usr/bin/python


import datetime
import json
import time
from slackclient import SlackClient

token = "PRIVATE"
today = int(datetime.datetime.today().weekday()) + 1
menu = json.load(file('menu.json'))
todays_menu = menu[str(today)]
soup = todays_menu["soup"]["name"]
meal = todays_menu["meal"]["name"]
message = "Dagens meny er %s og %s" % (soup, meal)
sc = SlackClient(token)
sc.rtm_connect()
channel = sc.server.channels.find("kantine")
channel.send_message(message)
