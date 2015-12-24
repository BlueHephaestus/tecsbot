# -*- coding: utf-8 -*-
#^^this makes it so we can actually parse unicode
#TODO:
#TECSBot, Twitch Emote Chat Statistics Bot
#Made by DarkElement75, AKA Blake Edwards
"""
Don't forget:
sudo systemctl restart httpd, mysqld
SEPERATE IDEAS
20 bot network controlled by one main bot
	could be used to paste 1/20th of a copypasta at a time
	ascii art line by line
	have a small channel come alive with bots
	
allow users to program question responses like ALICE? <-- interesting idea for a solo channel

GUI
more channel functionality
create own commands functionality
	needs to be very user-friendly
	currently !addcom and !delcom
	need to add in ability to do <user>, reference user who wrote message.
timezone for streamer	
need to make it possible to enable/disable everything -checkboxes
need help for each command
	!help <command>
	putting it all in documentation instead of this will likely be better.
		warn about dangerous commands
	<command> will output this
allow customization of (almost?) any response to a command. Should allow default customisation but give a warning. Need reset to default as well.
different responses input for 8ball?
checkbox to enable/disable errors in chat, such as usage/have to be mod
checkbox for whispers for warning messages ie excessive use of caps warning/etc?
ban use of some emotes or all emotes <-checkbox gui option
expiration dates for repeat timers
!x delete 21, 1, 5 <--- multiple deleting possibility, better put this in gui since we can't delete things with commas in it if this is in the chat.
log/dict/array of recent commands? <-doubt this would actually help with an undo command
	do similar thing to moobot, have a chatbox of the commands said and run, without other misc messages
extra analytics for messages and emotes and shiznizzle(think past me meant in the gui)
default starting amount of points-change in gui
add default point value in gui

SERVER:
see stackoverflow response
link our access_token html file and this file 
	this is going to be completely different most likely when we do this on a server, so for now we are just doing a text file edit
multi channel processing for comparison stats?
famous person has joined chat
donations <-if this isnt already done very well
hours til next strim? <--countdown command?
score of current game/tourney/bo3/etc
song functionality
sub notifications
social media info?
overall and per day -time user has watched stream
	other user tracking stuff
overrall and per day -messages of user, high score, etc
figure out what to do with the other spamerino things
excludes for "regulars" and subs
offtime - time stream has been offline
the minimum number of symbols should be disabled by default
need to make friends with a twitch partner
need to have command to check if user is subscribed to channel 
	!subscribed /!subbed <user>
How to get bot in channel:
	1. User goes to website and gives oauth, so that we know it's them
	2. They type !join in their channel and then mod the bot
	3. bot joins, and if modded is good and oauth is good, then all is well and it is added to list of connections
https://apis.rtainc.co/twitchbot/status?user=Darkelement75 custom api link
	http://deepbot.tv/wiki/Custom+Commands
execute commands with streamer capabilities
http://deepbot.deep.sg/wiki/Bot+Commands
@customapi@[api link] where customapi is a variable that represents the data on the api link, ie how nightbot has uptime api link
oauth_on variable?
remember to update the default command list, the README, the sets, and the db
whisper mods list or whispers argument where mods can choose to have bot's responses whispered to them instead of printed
	!whisperme
3 main things:
	1. Song requests - website for streamer to use that bot is hooked up to, use the gui
	2. Database setting storage
	3. website and gui for the bot 
dont let it time out mods unless it can send messages on behalf of streamer
	a. Allows settings input
	b. Has connect with twitch button first
input time out duration for banphrases?
current_time = time.time() will not get fractions of a second, it will only get whole seconds < this leads to it be ing off by a second, is a problem needs to be fixed
	for now I don't want to implement this because why would you care so much about those fractions of a second
	maybe we will make it loop every second in the future instead of 0.003, i dont fucking know i just know i dont want to 
	do it right now
add a general spam prevention like r9k
what do we need to rename emote_warn to / we still need this function for the default emotes
!google <search query>
variable storage stuff

TRASHED STUFF:
!clever <user> to troll user
replace as many api requests as possible
!time to print current time
make link whitelist also look for false positives? i.e. dot com
"""
'''misc
 function loadEmotes() { $.getJSON("https://api.betterttv.net/emotes").done(function(data) { $emotes.text(''); parseEmotes(data.emotes); }).fail(function() { $('#emote').text("Error loading emotes.."); }); }
1:42 TimeoutBan Clearflare: https://api.betterttv.net/emotes/ will give you json
'''
'''
errors:
	
When internet fails
Traceback (most recent call last):
  File "C:\Python27\Scripts\tecsbot\tecsbot_main.py", line 169, in <module>
	server_json = get_json_servers()
  File "C:\Python27\Scripts\tecsbot\tecsbot_main.py", line 154, in get_json_servers
	response = urllib.urlopen(url)
  File "C:\Python27\lib\urllib.py", line 84, in urlopen
	return opener.open(url)
  File "C:\Python27\lib\urllib.py", line 205, in open
	return getattr(self, name)(url)
  File "C:\Python27\lib\urllib.py", line 342, in open_http
	h.endheaders(data)
  File "C:\Python27\lib\httplib.py", line 940, in endheaders
	self._send_output(message_body)
  File "C:\Python27\lib\httplib.py", line 803, in _send_output
	self.send(msg)
  File "C:\Python27\lib\httplib.py", line 755, in send
	self.connect( a
  File "C:\Python27\lib\httplib.py", line 736, in connect
	self.timeout, self.source_address)
  File "C:\Python27\lib\socket.py", line 551, in create_connection
	for res in getaddrinfo(host, port, 0, SOCK_STREAM):
IOError: [Errno socket error] [Errno 11004] getaddrinfo failed
'''
import thread, threading #imports module allowing timing functions
import sys, operator, time, urllib, json, math, os, random, unicodedata, requests, select
from py2casefold import casefold
from datetime import datetime, timedelta
import re#regex
import string#string constants
from twisted.internet import protocol, reactor
from twisted.words.protocols import irc
from twisted.internet.task import LoopingCall

import logging
import calendar
import traceback

import sqlalchemy
from sqlalchemy.engine import create_engine
from sqlalchemy import text

from sympy.solvers import solve#!math

def get_json_servers():
	url = "http://tmi.twitch.tv/servers?cluster=group"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return data
	
bot_owner = 'darkelement75'
nickname = 'tecsbot' 
ping_nick = "@%s" % nickname
#permit_nick = "Tmi.twitch.tv 001 %s" % nickname
#the group chat channel, do we need to automatically get this?


f = open("/home/darkelement/programming/tecsbot/bot_oauth.log", "r")
password = f.readlines()[0].rstrip()#removing hard coded oauth for streaming

#things to be input as settings

spam_cooldown = 30 #seconds
spam_timeout = 10 #seconds
emote_max = 8 #low for testing, max number of emotes allowed in a message before timing user out
#need to have different timeout durations for different types, also allow one universal timeout however.
emote_timeout_msg = "You have been timed out for sending a message that had %s emotes or more." % emote_max

#need to have 10 second warning for both of these
caps_perc_min_msg_len = 8
caps_perc_max = 60
#caps_num_max = 50


max_symbol_num = 8
min_symbol_chars = 15
max_symbol_perc = 40

min_spam_chars = 20
msg_length_max = 375

caps_timeout_msg = "You have been timed out for sending a message that had %s caps or more." % caps_perc_max
#caps_timeout_msg = "You have been timed out for sending a message that was %s% caps or more." % caps_num_max

permit_time = 30 #seconds

#This determines whether to do search_str == msg, or search_str in message when looking for commands
cmd_match_full = True

#initial connect
f = open("/home/darkelement/programming/tecsbot/bot_oauth.log", "r")
access_token = f.readlines()[1]
client_id = "jpf2a90oon0wqdnno5ygircwgomt9rz"

whisper_msg = ""
whisper_user = ""

#Chat Log Database
chat_log_engine = create_engine("mysql://root@localhost:3306/tecsbot_chat_log")
chat_log_conn = chat_log_engine.connect()

#for debugging
def full_exit():
	os._exit(1)

def start_log(log_file_path):
	#if log file already exists, delete it and create new one.
	#need to execute this when the stream starts, should wait for get_uptime_min to be less than 1?
	if os.path.exists(log_file_path):
		os.remove(log_file_path)
	new_log_file = open(log_file_path, 'w')
	new_log_file.close	

def print_dict_by_key(dictionary):
	for key, value in sorted(dictionary.items()):
		if len(key) < 7:
			print "%s:\t\t\t%s" % (key, value[0])
		elif len(key) < 15:
			print "%s:\t\t%s" % (key, value[0])
		else:
			print "%s:\t%s" % (key, value[0])
			
def print_dict_by_value(dictionary):
	value_dict = sorted(dictionary.items(), key=operator.itemgetter(1))
	#gotta parse this way so as not to sort by keys again
	for pair in value_dict:
		key = pair[0]
		value = pair[1]
		if len(key) < 7:
			print "%s:\t\t\t%s" % (key, value[0])
		elif len(key) < 15:
			print "%s:\t\t%s" % (key, value[0])
		else:
			print "%s:\t%s" % (key, value[0])

def get_json_stream(channel_parsed):
	'''Unhandled exception in thread started by <bound method channel_bot_start.main of <__main__.channel_bot_start object at 0x0000000002C4D828>>
	Traceback (most recent call last):
	  File "C:\Python27\Scripts\tecsbot_main.py", line 2347, in main
		if stream_online(channel_parsed):
	  File "C:\Python27\Scripts\tecsbot_main.py", line 317, in stream_online
		channel_json = get_json_stream(channel_parsed)
	  File "C:\Python27\Scripts\tecsbot_main.py", line 287, in get_json_stream
		return requests.get(url).json()
	  File "C:\Python27\lib\site-packages\requests\models.py", line 805, in json
		return complexjson.loads(self.text, **kwargs)
	  File "C:\Python27\lib\json\__init__.py", line 310, in loads
		return _default_decoder.decode(s)
	  File "C:\Python27\lib\json\decoder.py", line 346, in decode
		obj, end = self.raw_decode(s, idx=_w(s, 0).end())
	  File "C:\Python27\lib\json\decoder.py", line 364, in raw_decode
		raise ValueError("No JSON object could be decoded")
	ValueError: No JSON object could be decoded'''
	url = "https://api.twitch.tv/kraken/streams?channel=%s" % channel_parsed
	while True:
		try:			
			return requests.get(url).json()
		except Exception, err:
			print Exception, err
			
def get_json_views_follows(channel_parsed):
	url = "https://api.twitch.tv/kraken/channels/%s" % channel_parsed
	return requests.get(url).json()

def get_json_followers_list(channel_parsed):
	url = "https://api.twitch.tv/kraken/channels/%s/follows/" % channel_parsed
	while True:
		try:
			return requests.get(url).json()
		except:
			pass
	
def get_json_chatters(channel_parsed):
	url = "https://tmi.twitch.tv/group/user/%s/chatters" % channel_parsed
	while True:
		try:
			return requests.get(url).json()
		except:
			pass

def get_json_subs(channel_parsed):	
	url = "https://api.twitch.tv/kraken/channels/%s/subscriptions" % channel_parsed
	data = requests.get(url, params={'oauth_token': access_token})
	while True:
		try:
			return data.json()
		except:
			pass

def get_json_sub_user(channel_parsed, user):
	url = "https://api.twitch.tv/kraken/channels/%s/subscriptions/%s" % (channel_parsed, user)
	data = requests.get(url, params={'oauth_token': access_token})
	print data.json()
	return data.json()

def get_emote_list(channel_parsed):
	url = "https://api.twitch.tv/kraken/chat/%s/emoticons" % channel_parsed
	emote_json = requests.get(url).json()
	emote_arr = []
	for emote in emote_json["emoticons"]:
		if "\\\\" not in emote["regex"]:
			emote_arr.append(emote["regex"])
		#dont add the special ones
	return emote_arr

def start_commercial(length, channel_parsed):
	url = "https://api.twitch.tv/kraken/channels/%s/commercial" % channel_parsed
	data = requests.post(url, data={'oauth_token': access_token, 'length' : length})
	print data.json()
	return data.json()
	
def get_uptime_min(channel_parsed):
	channel_json = get_json_stream(channel_parsed)
	#parse out unnecessary stuffs
	start_time = channel_json["streams"][0]["created_at"].replace("Z", "").replace("T", " ")
	#convert to datetime object
	start_time = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
	#calendar.timegm assumes UTC/GMT and mktime assumed local time
	created_at = calendar.timegm(start_time)
	#get the current UTC time
	now_utc = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
	uptime = now_utc - created_at
	minute = uptime / 60
	#return the minutes for epm calculations
	return minute

def get_uptime_str(channel_parsed):	
	channel_json = get_json_stream(channel_parsed)
	try:
		#parse out unnecessary stuffs
		start_time = channel_json["streams"][0]["created_at"].replace("Z", "").replace("T", " ")
		#convert to datetime object
	except:
		return False
	start_time = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
	#calendar.timegm assumes UTC/GMT and mktime assumed local time
	created_at = calendar.timegm(start_time)
	#get the current UTC time
	now_utc = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
	uptime = now_utc - created_at
	uptime = int(uptime)
	return parse_sec_condensed(uptime)
	
def parse_sec(sec):
	#assumes that parameter is not 0
	sec = float(sec)	
	week = int(math.floor(sec/604800))
	day = int(math.floor((sec - week*604800) / 86400))
	hour = int(math.floor((sec - week*604800 - day*86400)/ 3600))#day = 5
	minute = int(math.floor((sec - week*604800 - day*86400 - hour *3600) / 60))
	sec = simplify_num((sec - week*604800 - day*86400 - hour *3600 - minute*60))
	
	time_values = [week, 'weeks', 'week', day, 'days', 'day', hour, 'hours', 'hour', minute, 'minutes', 'minute', sec, 'seconds', 'second']
	return_str = ''
	
	for time_unit_index, time_unit_value in enumerate(time_values):#every third
		if is_num(time_unit_value):
			if time_unit_value != 0:
				if time_values[time_unit_index+1] == "weeks" or time_values[time_unit_index+1] == "days":
					if time_unit_value == 1:
						return_str += "%s %s, " % (time_unit_value, time_values[time_unit_index+2])
					else:
						return_str += "%s %s, " % (time_unit_value, time_values[time_unit_index+1])
				else:
					if time_unit_value == 1:
						return_str += "%s %s, " % (time_unit_value, time_values[time_unit_index+2])
					else:
						return_str += "%s %s, " % (time_unit_value, time_values[time_unit_index+1])
					
	
	if return_str.endswith(", "):
		return_str = return_str[:-2]
	return return_str

def parse_sec_condensed(sec):
	sec = float(sec)
	
	week = int(math.floor(sec/604800))
	day = int(math.floor((sec - week*604800) / 86400))
	hour = int(math.floor((sec - week*604800 - day*86400)/ 3600))#day = 5
	minute = int(math.floor((sec - week*604800 - day*86400 - hour *3600) / 60))
	sec = simplify_num((sec - week*604800 - day*86400 - hour *3600 - minute*60))
	
	time_values = [week, 'weeks', 'week', day, 'days', 'day', hour, 'h', 'h', minute, 'm', 'm', sec, 's', 's']
	return_str = ''
	
	for time_unit_index, time_unit_value in enumerate(time_values):#every third
		if is_num(time_unit_value):
			if time_unit_value != 0:
				if time_values[time_unit_index+1] == "weeks" or time_values[time_unit_index+1] == "days":
					if time_unit_value == 1:
						return_str += "%s %s " % (time_unit_value, time_values[time_unit_index+2])
					else:
						return_str += "%s %s " % (time_unit_value, time_values[time_unit_index+1])
				else:
					if time_unit_value == 1:
						return_str += "%s%s " % (time_unit_value, time_values[time_unit_index+2])
					else:
						return_str += "%s%s " % (time_unit_value, time_values[time_unit_index+1])
	return return_str.rstrip()	
	
def is_mod(user, channel_parsed, user_type):
	'''
	itslikesnowboarding:	!8ball do you know how to make computers go faster?
	Unhandled exception in thread started by <bound method channel_bot_start.main of <__main__.channel_bot_start object at 0x0000000002C987F0>>
	Traceback (most recent call last):
	  File "C:\Python27\Scripts\tecsbot_main.py", line 2172, in main
		main_parse(user, msg, irc)
	  File "C:\Python27\Scripts\tecsbot_main.py", line 1890, in main_parse
		if self.ball_parse(user, msg, irc, channel_parsed) != False:
	  File "C:\Python27\Scripts\tecsbot_main.py", line 1586, in ball_parse
		if is_mod(user, channel_parsed, user_type):
	  File "C:\Python27\Scripts\tecsbot_main.py", line 394, in is_mod
		if user == str(mod):
	LookupError: unknown encoding: darkelement75'''
	'''channel_json = get_json_chatters(channel_parsed)
	mods_arr = channel_json["chatters"]["moderators"]
	if user == channel_parsed:
		#if the user is the streamer
		#can possibly add in new function to replace this and add for more different responses if triggered by streamer, is_owner
		#or just return a different value
		return True
	for mod in mods_arr:
		#if user == mod.encode("ascii"):#sure they'll be something wrong with this
		try:
			if user == str(mod):
				return True
		except LookupError:
			return False
	return False'''
	mod_types = ["admin", "global_mod", "staff", "mod"]
	if user == channel_parsed or user_type in mod_types:
		return True
	else:
		return False

def is_editor(self, user):
	query = text("SELECT COUNT(*) FROM editors WHERE `user` = :user LIMIT 1")
	res = result_to_dict(self.conn.execute(query, user=user))[0]["COUNT(*)"]
	if res > 0:
		return True
	else:
		return False
		
def has_level(self, user, channel_parsed, user_type, display_id):
	query = text("SELECT feature_level FROM main WHERE `display_id` = :display_id LIMIT 1")
	level = result_to_dict(self.conn.execute(query, display_id=display_id))[0]["feature_level"]
	user_level = get_user_level(self, user, channel_parsed, user_type)
	if user_level <= level:
		return True
	else:
		return False

def get_user_level(self, user, channel_parsed, user_type):
	if is_streamer(user, channel_parsed):
		return 1
	elif is_editor(self, user):
		return 2
	elif is_mod(user, channel_parsed, user_type):
		return 3
	else:
		return 4

def is_streamer(user, channel_parsed):
	if user == channel_parsed:
		return True
	else:
		return False

def get_new_viewers(viewer_arr, channel_parsed, self):
	viewers_json = get_json_chatters(channel_parsed)#this request returns the moderators and the viewers, viewers are closest thing we have to chatters
	new_viewer_arr = []
	for viewer in viewers_json["chatters"]["viewers"]:#twitch pls y u do dis
		if viewer not in viewer_arr:
			viewer_arr.append(viewer)
			new_viewer_arr.append(viewer)
	return viewer_arr, new_viewer_arr
	
def get_new_followers(follower_arr, channel_parsed, self):
	follows_json = get_json_followers_list(channel_parsed)
	new_follower_arr = []
	
	for follower in follows_json["follows"]:
		follower = follower["user"]["name"]
		if follower not in follower_arr:
			follower_arr.append(follower)
			new_follower_arr.append(follower)
	return follower_arr, new_follower_arr	
	
def timeout_thread(self, send_str):
	time.sleep(2)
	self.write(send_str)
	
def timeout(user, self, timeout):
	send_str = "/timeout %s %s" % (user, timeout)
	self.write(send_str)
	thread.start_new_thread(timeout_thread, (self, send_str))
	
def is_num(x):
	try:
		float(x)
		return True
	except ValueError:
		return False
		
	try:
		x.is_integer()
		return True
	except AttributeError:
		return False
		
def set_value(self, display_id, msg_arr):
	status = get_status(self, display_id)
	if display_id != self.set_display_id and not get_status(self, self.set_display_id):
		return
	if msg_arr[2] == "on":
		if status:
			send_str = "%s is already on." % (display_id.capitalize())
		else:
			set_status(self, display_id, True)
			send_str = "%s turned on. You can do \"!set %s off\" to turn it off again." % (display_id.capitalize(), display_id)
	elif msg_arr[2] == "off":
		if not status:
			send_str = "%s is already off." % (display_id.capitalize())
		else:
			set_status(self, display_id, False)
			send_str = "%s turned off. You can do \"!set %s on\" to turn it on again." % (display_id.capitalize(), display_id)
	else:
		#usage
		send_str = "Usage: \"!set %s on/off \"." % (display_id)
	self.write(send_str)

def caps_count(msg):
	caps = ''
	for letter in msg:
		if letter.isupper():
			caps+=letter
	return len(caps)

def caps_perc(msg):
	#number of caps divided by number of characters in the message
	caps = float(0)
	for letter in msg:
		if letter.isupper():
			caps+=1
	return (caps / len(msg)) * 100

def check_user_permit(self, user):
	#return True if they have a permit and can go on, False if not
	query = text("SELECT COUNT(*) FROM `%s` WHERE user = :user" % self.permit_display_id)
	res = result_to_dict(self.conn.execute(query, user=user))
	if res[0]["COUNT(*)"] <= 0:
	#user has no permits
		return False
	query = text("SELECT COUNT(*) FROM `%s` WHERE `user` = :user AND `type` = :type" % (self.permit_display_id))
	if result_to_dict(self.conn.execute(query, user=user, type="permanent"))[0]["COUNT(*)"] > 0:
		#user has a permanent permit
		return True
	permit_row = get_data_where(self, self.permit_display_id, "user", user)
	if len(permit_row) > 1:
		#if they have both a time and a message permit
		final_return_arr = ['','']
		for row_index, row in enumerate(permit_row):
			if row["type"] == "time":
				current_time = time.time()
				if current_time - float(row["set_time"]) > float(row["duration"]):
					delete_value_handler(self, self.permit_display_id, "index", row["index"])
					final_return_arr[row_index] = False
				else:
					final_return_arr[row_index] = True
			else:
				#message
				if int(row["duration"]) > 0:
					#they still have some left, update duration 
					query = text("UPDATE `%s` SET duration = duration - 1 WHERE `index` = :index" % self.permit_display_id)
					self.conn.execute(query, index=row["index"])
					final_return_arr[row_index] = True
				else:
					#they do not have any left, and need to gtfo
					delete_value_handler(self, self.permit_display_id, "index", row["index"])
					final_return_arr[row_index] = False
		if final_return_arr == [False, False]:
			#both are rip
			return False
		else:
			return True
	else:
		permit_row = permit_row[0]
		#if they only have one
		if permit_row["type"] == "time":
			current_time = time.time()
			if current_time - float(permit_row["set_time"]) > float(permit_row["duration"]):
				delete_value_handler(self, self.permit_display_id, "index", permit_row["index"])
				return False
			else:
				return True
		else:
			#message
			if int(permit_row["duration"]) > 0:
				#they still have some left, update duration 
				query = text("UPDATE `%s` SET duration = duration - 1 WHERE `index` = :index" % self.permit_display_id)
				self.conn.execute(query, index=permit_row["index"])
				return True
			else:
				#they do not have any left, and need to gtfo
				delete_value_handler(self, self.permit_display_id, "index", permit_row["index"])
				return False
	
def warn(user, msg, channel_parsed, self, warn_table, warn_duration, warn_cooldown, timeout_msg, timeout_duration):
	#function to warn if they havent already been warned, and time them out if they have.
	if not check_user_permit(self, user):
		query = text("SELECT COUNT(*) FROM `%s` WHERE user = :user" % warn_table)
		res = result_to_dict(self.conn.execute(query, table=warn_table, user=user))
		if res[0]["COUNT(*)"] > 0:
			current_time = time.time()
			#check if current time is longer than the warning duration from the last time name was entered
			query = text("SELECT * FROM `%s` WHERE user = :user and (:current_time - set_time <= :cooldown) LIMIT 1" % warn_table)
			row = result_to_dict(self.conn.execute(query, user=user, current_time=current_time, cooldown=warn_cooldown))
			if row != []:
				#they did a bad thing in a time less than the cooldown, time out for long duration
				#timeout user for long duration and remove from array
				timeout(user, self, timeout_duration)
				delete_value_handler(self, warn_table, "index", row[0]["index"])
				send_str = "No %s allowed (%s)" % (timeout_msg, user.capitalize())
				self.write(send_str)
				whisper_msg = "You were timed out for %s in %s (%s)" % (timeout_msg, channel_parsed, parse_sec(timeout_duration))
				whisper(self, user, whisper_msg)
			else:
				#they did a bad thing in a time more than the cooldown, time out for short duration
				#replace old entry with new one and send warning as well as timeout for warn_duration
				#short duration
				query = text("SELECT * FROM `%s` WHERE user = :user and (:current_time - set_time > :cooldown) LIMIT 1" % warn_table)
				row = result_to_dict(self.conn.execute(query, user=user, current_time=current_time, cooldown=warn_cooldown))
				timeout(user, self, warn_duration)
				delete_value_handler(self, warn_table, "index", row[0]["index"])
				query = text("INSERT INTO `%s` (`set_time`, `user`) VALUES (:time, :user)" % warn_table)
				self.conn.execute(query, time=current_time, user=user)
				send_str = "No %s allowed (%s)(warning)" % (timeout_msg, user.capitalize())
				self.write(send_str)
				whisper_msg = "You were timed out for %s in %s (%s, warning)" % (timeout_msg, channel_parsed, parse_sec(warn_duration))		
				whisper(self, user, whisper_msg)
		else:
			#add new entry and send warning, with timeout for warn_duration
			#short duration
			timeout(user, self, warn_duration)
			current_time = time.time()
			query = text("INSERT INTO `%s` (`set_time`, `user`) VALUES (:time, :user)" % warn_table)
			self.conn.execute(query, time=current_time, user=user)
			send_str = "No %s allowed (%s)(warning)" % (timeout_msg, user.capitalize())
			self.write(send_str)
			whisper_msg = "You were timed out for %s in %s (%s, warning)" % (timeout_msg, channel_parsed, parse_sec(warn_duration))
			whisper(self, user, whisper_msg)
		
def symbol_count(msg):
	reg_chars = [',','.',' ','\'','\"','?', ';']
	reg_chars.extend(list(string.letters))
	reg_chars.extend(list(string.digits))
	msg_symbol_count = 0
	for char in msg:
		if char not in reg_chars:
			msg_symbol_count += 1
	return msg_symbol_count		

def normalize_caseless(str):
        str = casefold(str.decode("utf-8"))
        return unicodedata.normalize("NFKD", str)

def in_front(str, msg):
	if normalize_caseless(str) in normalize_caseless(msg[:len(str)+1]):
		return True
	else:
		return False

def check_int(num):
	try:
		if num.is_integer():
			num = int(num)
		return num
	except AttributeError:
		pass
	return num

def get_mods_msg(self, msg):
	#self.write("/mods")
	while True:
		if self.mods_msg != '':
			msg = msg.replace("/mods", self.mods_msg)
			self.write(msg)
			self.mods_msg = ''
			return
			
def get_whisper_mods_msg(self, user, msg):
	self.whisper_mods_thread = True # so that we don't print it when the mods_msg is obtained in the notice function
	self.write("/mods")
	while True:
		if self.mods_msg != '':
			msg = msg.replace("/mods", self.mods_msg)
			send_whisper(self, user, msg)
			self.mods_msg = ''
			self.whisper_mods_thread = False
			return

def send_whisper(self, user, msg):
	whisper_str = "/w %s %s" % (user, msg)
	reactor.whisper_bot.write(whisper_str)

def whisper(self, user, msg):
	'''global whisper_user, whisper_msg
	if "/mods" in msg:
		thread.start_new_thread(get_whisper_mods_msg, (self, user, msg))
	else:
		whisper_user = user
		whisper_msg = msg'''
	if "/mods" in msg:
		thread.start_new_thread(get_whisper_mods_msg, (self, user, msg))
	else:
		send_whisper(self, user, msg)
	
def whisper_response(msg):
	#edit this when it's time for variables
	global whisper_msg, whisper_user
	
	msg_arr = msg.split(" ", 2)
	if len(msg_arr) == 3:
		whisper_user = msg_arr[1]
		whisper_msg = msg_arr[2].rstrip()
		
def long_print(next_str, send_str):
	#this accounts for any messages longer than the character cap
	if math.floor((len(send_str)+len(next_str)) / 500) > 0:
		self.write(send_str)
		send_str = next_str
	else:
		send_str += next_str
	return send_str	

def word_count(text, search):
	#number of exact copies of word in string
	#remove invalid characters
	
	'''if ":\\" in search:
		search = search.replace(":\\", "\:\\")
	if ":(" in search:
		search = search.replace(":(", "\:\(")
	if ":)" in search:
		search = search.replace(":)", "\:\)")
	result = re.findall('(?<!\S)'+search+'(?!\S)', text)
	return len(result)'''
	text = text.split()
	return text.count(search)

def disconnect_cmd(cmd):
	if in_front(".disconnect", cmd) or in_front("/disconnect", cmd):
		return True
	else:
		return False

def simplify_num(num):
	return check_int(float(num))

def prettify_num(num):
	if len(str(float(num))) / 3 > 1:
		if float(num) < 0:#so it doesn't screw up on the negative sign
			num = num * -1
			num_negative = True
		else:
			num_negative = False
		num = list(reversed(list(str(num))))#converts from int into reversed list
		for num_index in range(len(num)):#go through indexes of reversed list
			if num_index != len(num) - 1:#if not last element
				if (num_index + 1) % 3 == 0:#
					num[num_index] = "," + num[num_index]
		
		num = "".join(list(reversed(num)))#converts from reversed list into int
		if num_negative:
			num = "-" + num
		return num
	else:
		return num

def convert_to_sec(time, unit, self):
	if unit in self.time_unit_arr[:4]:#secs
		return time
	elif unit in self.time_unit_arr[4:8]:#mins
		return time*60
	elif unit in self.time_unit_arr[8:12]:#hours
		return time*3600
	elif unit in self.time_unit_arr[12:14]:#days
		return time*86400
	elif unit in self.time_unit_arr[14:16]:#weeks
		return time*604800

def insert_permit(self, permit_pair):
	#checks to only add permit if it is higher than an existing permit, otherwise it does nothing.
	permit_set_time = permit_pair[0]
	permit_high_user = permit_pair[1]
	permit_high_type = permit_pair[3]
	permit_high_duration = permit_pair[2]
	
	if permit_high_type == "permanent":
		query = text("DELETE FROM `%s` WHERE user = :user" % self.permit_display_id)
		self.conn.execute(query, user=permit_high_user)
		query = text("INSERT INTO `%s` (`set_time`, `user`, `duration`, `type`) VALUES (:time, :user, :duration, :type)" % self.permit_display_id)
		self.conn.execute(query, time=permit_set_time, user=permit_high_user, duration=permit_high_duration, type=permit_high_type)
		return True
	else:
		query = text("SELECT COUNT(*) FROM `%s` WHERE user = :user and type = :type" % self.permit_display_id)
		res = result_to_dict(self.conn.execute(query, user=permit_high_user, type=type))
		if res[0]["COUNT(*)"] <= 0:
			#this user does not have a permanent permit, check with the others
			query = text("DELETE FROM `%s` WHERE type = :type and duration < :duration" % self.permit_display_id)
			self.conn.execute(query, type=permit_high_type, duration=permit_high_duration)
			query = text("SELECT COUNT(*) FROM `%s` WHERE type = :type and duration > :duration" % self.permit_display_id)
			res = result_to_dict(self.conn.execute(query, type=permit_high_type, duration=permit_high_duration))
			if res[0]["COUNT(*)"] <= 0:
				#as long as there are none that are greater than ours(which means there are now no others of this type in the db), add it
				query = text("INSERT INTO `%s` (`set_time`, `user`, `duration`, `type`) VALUES (:time, :user, :duration, :type)" % self.permit_display_id)
				self.conn.execute(query, time=permit_set_time, user=permit_high_user, duration=permit_high_duration, type=permit_high_type)
				return True
	return False

def get_raw_general_stats(channel_parsed, stat_str):
	if stat_str == self.chatters_display_id:
		stat_data = get_json_chatters(channel_parsed.lower().strip())
		stat_count = stat_data["chatter_count"]
	elif stat_str == self.viewers_display_id:
		stat_data = get_json_stream(channel_parsed.lower().strip())
		stat_count = stat_data["streams"]
	elif stat_str == self.views_display_id:
		stat_data = get_json_views_follows(channel_parsed.lower().strip())
		stat_count = stat_data["views"]
	elif stat_str == self.followers_display_id:
		stat_data = get_json_views_follows(channel_parsed.lower().strip())
		stat_count = stat_data["followers"]
		
	if stat_count:
		if stat_str == self.viewers_display_id:
			stat_count = stat_count[0]["viewers"]
		return stat_count
	else:
		return '0'

def encode_list(list):
	for index, element in enumerate(list):
		list[index] = element.encode("utf-8")
	return list
	
def point_change(self, user, points):
	#if points != 0:#don't waste our time if it's 0 points#we actually remove this so that we tell them their new total of points and this may interfere with a custom setting
	if get_status(self, self.points_display_id):
		query = text("SELECT COUNT(*) FROM point_users WHERE user = :user")
		res = result_to_dict(self.conn.execute(query, user=user))[0]["COUNT(*)"]
		if res <= 0:
			query = text("INSERT INTO `point_users` (`user`, `points`) VALUES (:user, %d)" % self.default_point_value)
			self.conn.execute(query, user=user)
		query = text("UPDATE point_users SET points = points+%d WHERE user = :user" % (points))
		self.conn.execute(query, user=user)

def point_balance(self, user):
	query = text("SELECT points FROM point_users WHERE user = :user")
	res = result_to_dict(self.conn.execute(query, user=user))
	if res != []:
		return res[0]["points"]
	else:
		query = text("INSERT INTO `point_users` (`user`, `points`) VALUES (:user, %d)" % self.default_point_value)
		self.conn.execute(query, user=user)
		return self.default_point_value
	
def result_to_dict(res):
	return [dict(row) for row in res]

#ONLY USE THIS FOR DEBUGGING
def is_empty(self, table):
	if get_len_table(self, table) > 0:
		return False
	else:
		return True
		
def get_len_table(self, table):
	query = "SELECT COUNT(*) FROM `%s`" % table
	res = result_to_dict(self.conn.execute(query))
	len_table = res[0]["COUNT(*)"]
	return len_table

def get_sum(self, table, column):
	query = text("SELECT SUM(`%s`) FROM `%s`" % (column, table))
	res = int(result_to_dict(self.conn.execute(query))[0]["SUM(`%s`)"%column])
	return res
	
def get_count(self, table, columns, values):
	columns = "(" + ','.join(x for x in columns) + ")"
	values = '(' + repr(values)[1:-1] + ')'
	query = text("SELECT COUNT(*) FROM `%s` WHERE :columns = :values" % table)
	return result_to_dict(self.conn.execute(query, columns=columns, values=values))[0]["COUNT(*)"]
		
def has_count(self, table, column, value):
	#same as get_count but returns a bool instead of an int
	#columns = "(" + ','.join(x for x in columns) + ")"
	#if len(values) > 1:
	#values = '(' + repr(values)[1:-1] + ')'
	#else:
	#values = repr(values[0])
	query = text("SELECT COUNT(*) FROM `%s` WHERE `%s` = :value" % (table, column))
	if result_to_dict(self.conn.execute(query, value=value))[0]["COUNT(*)"] > 0:
		return True
	else:
		return False

def get_status(self, display_id):
	query = text("SELECT `feature_status` FROM main WHERE `display_id` = :display_id")
	status = result_to_dict(self.conn.execute(query, display_id=display_id))
	#print status[0]["feature_status"].encode("utf-8")
	try:
		if ord(status[0]["feature_status"]) == 1:
			return True
		else:
			return False
	except:
		return False
		
def set_status(self, feature, status):
	if status:
		query = text("UPDATE main SET feature_status = 1 where display_id = :feature")
	else:
		query = text("UPDATE main SET feature_status = 0 where display_id = :feature")
	self.conn.execute(query, feature=feature)
		
def insert_data(self, table, columns, values):
	#values is a string
	columns = "(" + ','.join(x for x in columns) + ")"
	query = text("INSERT INTO `%s` %s VALUES (:values)" % (table, columns))
	self.conn.execute(query, values=values)
	
def update_data(self, table, columns, values):
	if len(columns) > 1:
		columns = "(`" + ','.join(x for x in columns) + "`)"
	else:
		columns = columns[0]
	values = '("' + repr(values)[1:-1] + '")'
	query = text("UPDATE `%s` SET :columns = :values" % table)
	self.conn.execute(query, table=table, columns=columns, values=values)

def get_data_where(self, table, column, value):
	if isinstance(value, basestring):
		query = text("SELECT * FROM `%s` WHERE `%s` = :value" % (table, column))
	else:
		query = text("SELECT * FROM `%s` WHERE `%s` = :value" % (table, column))
	return result_to_dict(self.conn.execute(query, value=value))
	
def extend_data(self, table, column, values):
	values = encode_list(values)
	#values = repr(values)[1:-1]
	for index, value in enumerate(values):
		values[index] = "(%s)" % repr(value)
	values = ', '.join(x for x in values)
	query = text("INSERT INTO `%s` (`%s`) VALUES %s" % (table, column, values)) 
	self.conn.execute(query)
##def update_8ball_table(self, type, 

def delete_index_handler(self, table, index):
	len_table = get_len_table(self, table)
	if not index > 0 or not index <= len_table:
		return False
	query = "SELECT * FROM `%s` LIMIT %d" % (table, index)
	result = result_to_dict(self.conn.execute(query))
	if len(result) == index: #could be len -1 = delete_index -1 to be more readable but ehh
		delete_row = result[len(result)-1]
	else:
		print "This shouldn't happen"
		full_exit()
	query = "DELETE FROM `%s` WHERE `index` = %d" % (table, delete_row["index"])
	self.conn.execute(query)
	return delete_row

def delete_value_handler(self, table, column, value):
	if isinstance(value, basestring):
		query = text("SELECT * FROM `%s` WHERE `%s` = :value LIMIT 1" % (table, column))
	else:
		query = text("SELECT * FROM `%s` WHERE `%s` = :value LIMIT 1" % (table, column))
	res = result_to_dict(self.conn.execute(query, value=value))
	if res:
		if isinstance(value, basestring):
			query = text("DELETE FROM `%s` WHERE `%s` = :value LIMIT 1" % (table, column))
		else:
			query = text("DELETE FROM `%s` WHERE `%s` = :value LIMIT 1" % (table, column))
		self.conn.execute(query, value=value)
		return res[0]
	else:
		return False
		
def get_table(self, table):
	query = "SELECT * FROM `%s`" % table
	return result_to_dict(self.conn.execute(query))
	
def clear_table(self, table):
	query = "DELETE	FROM `%s`" % table
	self.conn.execute(query)

def database_exists(channel_parsed):
	query = text("SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :channel")
	engine = create_engine("mysql://root@localhost:3306/")
	res = result_to_dict(engine.execute(query, channel=channel_parsed))[0]["COUNT(*)"]
	if res > 0:
		return True
	else:
		return False
	
def create_database(channel_parsed):
	query = '''
CREATE DATABASE IF NOT EXISTS `%s`;
	USE `%s`;

	CREATE TABLE IF NOT EXISTS `8ball` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `responses` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;
	
	INSERT INTO `8ball` (`responses`) VALUES
		("It is certain"),
		("It is decidedly so"),
		("Without a doubt"),
		("Yes, definitely"),
		("You may rely on it"),
		("As I see it, yes"),
		("Most likely"),
		("Outlook good"),
		("Yes"),
		("Signs point to yes"),
		("Reply hazy try again"),
		("Ask again later"),
		("Better not tell you now"),
		("Cannot predict now"),
		("Concentrate and ask again"),
		("Don't count on it"),
		("My reply is no"),
		("My sources say no"),
		("Outlook not so good"),
		("Very doubtful");
		
	CREATE TABLE IF NOT EXISTS `autoreply` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `phrase` varchar(500) DEFAULT NULL,
	  `reply` varchar(500) DEFAULT NULL,
	  `level` TINYINT(1) UNSIGNED NULL DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `banphrase` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `banphrase` varchar(500) DEFAULT NULL,
	  `duration` double UNSIGNED NULL DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `banphrase_warn` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` double NOT NULL,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `caps_warn` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` double NOT NULL,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `chatters` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `command` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `command` varchar(500) DEFAULT NULL,
	  `reply` varchar(500) DEFAULT NULL,
	  `level` TINYINT(1) unsigned NULL DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	INSERT INTO `command` (`command`, `reply`, `level`) VALUES
		("!slap", "{*USER*} slaps {*TO_USER*} around a bit with a large trout.", 3),
		("!shoutout", "Check out twitch.tv/{*TO_USER*} and follow them!", 1),
		("!test", "Test successful.", 2);
		
	CREATE TABLE IF NOT EXISTS `countdown` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` DOUBLE unsigned NULL DEFAULT NULL,
	  `command` varchar(500) DEFAULT NULL,
	  `duration` DOUBLE unsigned NULL DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `default_commands` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `command` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;
	
	CREATE TABLE IF NOT EXISTS `editors` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;
	
	CREATE TABLE IF NOT EXISTS `emote_warn` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` double unsigned NOT NULL,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `fake_purge_warn` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` double unsigned NOT NULL,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `followers` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;
	
	CREATE TABLE IF NOT EXISTS `game` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `game` varchar(50) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;
	
	CREATE TABLE IF NOT EXISTS `ip_warn` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` double NOT NULL,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `link whitelist` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `link` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `link_whitelist_warn` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` double unsigned NOT NULL,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `long_msg_warn` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` double unsigned NOT NULL,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `long_word_warn` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` double unsigned NOT NULL,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `lottery` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `main` (
	  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `display_id` varchar(500) DEFAULT NULL,
	  `feature_status` bit(1) UNSIGNED DEFAULT NULL,
	  `feature_level` tinyint(1) UNSIGNED DEFAULT NULL,
	  PRIMARY KEY (`id`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;
	
	INSERT INTO `main` (`id`, `display_id`, `feature_status`, `feature_level`) VALUES
		(1, 'antispam', 1, 3),
		(2, 'link whitelist', 1, 2),
		(3, 'permit', 1, 3),
		(4, 'banphrase', 1, 2),
		(5, 'autoreply', 1, 2),
		(6, 'ban_emotes', 1, NULL),
		(7, 'command', 1, 2),
		(8, 'repeat', 1, 2),
		(9, 'countdown', 1, 2),
		(10, 'raffle', 0, 2),
		(11, 'lottery', 0, 2),
		(12, 'poll', 0, 2),
		(13, 'chatters', 1, 4),
		(14, 'followers', 1, 4),
		(15, 'viewers', 1, 4),
		(16, '8ball', 1, 2),
		(17, 'roulette', 1, 4),
		(18, 'roll', 1, 4),
		(19, 'math', 1, 4),
		(20, 'coin', 1, 4),
		(21, 'topic', 1, 1),
		(22, 'repeat antispam', 1, NULL),
		(23, 'emote antispam', 1, NULL),
		(24, 'caps antispam', 1, NULL),
		(25, 'long message antispam', 1, NULL),
		(26, 'long word antispam', 1, NULL),
		(27, 'fake purge antispam', 1, NULL),
		(28, 'skincode antispam', 1, NULL),
		(29, 'stats', 1, 4),
		(30, 'symbol antispam', 1, NULL),
		(31, 'link antispam', 1, NULL),
		(32, 'me antispam', 1, NULL),
		(33, 'ip antispam', 1, NULL),
		(34, 'purge', 1, 3),
		(35, 'points', 1, 4),
		(36, 'slots', 1, 4),
		(37, 'give', 1, 4),
		(38, 'views', 1, 4),
		(39, 'uptime', 1, 4),
		(40, 'editors', 1, 1),
		(41, 'set', 1, 2),
		(42, 'chanstats', 1, 4),
		(43, 'commercial', 1, 2),
		(44, 'title', 1, 4),
		(45, 'game', 1, 4),
		(46, 'topic', 1, 4),
		(47, 'moderators', 1, 4),
		(48, 'level', 1, 2),
		(49, 'loops', 0, 2);

	CREATE TABLE IF NOT EXISTS `me_warn` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` double unsigned NOT NULL,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `new_followers` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `new_viewers` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `permanent_chatters` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `permit` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` varchar(500) unsigned DEFAULT NULL,
	  `user` varchar(500) DEFAULT NULL,
	  `duration` double UNSIGNED DEFAULT NULL,
	  `type` ENUM('message', 'time', 'permanent') DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `point_users` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `user` varchar(500) DEFAULT NULL,
	  `points` double unsigned DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `raffle` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `repeat` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` double UNSIGNED DEFAULT NULL,
	  `phrase` varchar(500) DEFAULT NULL,
	  `interval` double UNSIGNED DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `reply_args` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `arg` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `skincode_warn` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` double UNSIGNED NOT NULL,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `spam_warn` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` double UNSIGNED NOT NULL,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `symbol_warn` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `set_time` double UNSIGNED NOT NULL,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `time_units` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `unit` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;
	
	CREATE TABLE IF NOT EXISTS `title` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `title` varchar(50) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `topic` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `topic` varchar(50) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;
	
	CREATE TABLE IF NOT EXISTS `viewers` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `user` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `poll` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `option` varchar(500) DEFAULT NULL,
	  `votes` bigint(20) UNSIGNED DEFAULT NULL,
	  `users` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	CREATE TABLE IF NOT EXISTS `vote_options` (
	  `index` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  `option` varchar(500) DEFAULT NULL,
	  PRIMARY KEY (`index`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;''' % (channel_parsed, channel_parsed)
	#print "Making new db if doesn't already exist for channel %s" % channel_parsed
	engine = create_engine("mysql://root@localhost:3306/")
	conn = engine.connect()
	conn.execute(query)
	
def update_chat_log(channel, time, message):
	message = message.decode("utf-8").encode("utf-8")
	#query = text("INSERT INTO main (channel, time, message) VALUES ('%s', %s, \"%s\")" % (channel, time, message))
	query = text("INSERT INTO main (channel, time, message) VALUES (:channel, :time, :message)")
	chat_log_conn.execute(query, channel=channel, time=time, message=message)

def clear_chat_log(channel):
	#remove all of a channel's chat messages, done when channel goes offline
	query = text("DELETE FROM main WHERE `channel` = :channel")
	chat_log_conn.execute(query, channel=channel)
	
def get_word_count_global(word):
	word = "%%%s%%" % word
	query = text("SELECT COUNT(*) FROM main WHERE message LIKE :word")
	res = result_to_dict(chat_log_conn.execute(query, word=word))
	return res[0]["COUNT(*)"]
	
def get_word_count(word, channel):
	word = "%%%s%%" % word
	query = text("SELECT COUNT(*) FROM main WHERE message LIKE :word and channel = :channel")
	res = result_to_dict(chat_log_conn.execute(query, word=word, channel=channel))
	return res[0]["COUNT(*)"]

def possessive_prettify(word):
	if word.endswith("s"):
		word += "'"
	else:
		word += "'s"
	return word
	
class TwitchBot(irc.IRCClient, object):

	def __init__(self, channel):
	
		#Initial stuff
		self.channel = channel
		self.nickname = nickname
		self.password = password
		self.channel_parsed = self.channel.replace("#", "")
		server = 'irc.twitch.tv'
		
		#Database
		#create database if it doesn't already exist
		if not database_exists(self.channel_parsed):
			create_database(self.channel_parsed)
		engine = create_engine("mysql://root@localhost:3306/%s" % self.channel_parsed)
		self.conn = engine.connect()
		
		#Display IDs
		self.link_whitelist_display_id = "link whitelist"
		self.antispam_display_id = "antispam"
		self.repeat_antispam_display_id = "repeat antispam"
		self.emote_antispam_display_id = "emote antispam"
		self.caps_antispam_display_id = "caps antispam"
		self.long_message_antispam_display_id = "long message antispam"
		self.long_word_antispam_display_id = "long word antispam"
		self.fake_purge_antispam_display_id = "fake purge antispam"
		self.skincode_antispam_display_id = "skincode antispam"
		self.symbol_antispam_display_id = "symbol antispam"
		self.link_antispam_display_id = "link antispam"
		self.me_antispam_display_id = "me antispam"
		self.ip_antispam_display_id = "ip antispam"
		self.permit_display_id = "permit"
		self.banphrase_display_id = "banphrase"
		self.autoreply_display_id = "autoreply"
		self.command_display_id = "command"
		self.repeat_display_id = "repeat"
		self.countdown_display_id = "countdown"
		self.raffle_display_id = "raffle"
		self.lottery_display_id = "lottery"
		self.poll_display_id = "poll"
		self.chatters_display_id = "chatters"
		self.followers_display_id = "followers"
		self.viewers_display_id = "viewers"
		self.ball_display_id = "8ball"
		self.roulette_display_id = "roulette"
		self.roll_display_id = "roll"
		self.math_display_id = "math"
		self.coin_display_id = "coin"
		self.topic_display_id = "topic"
		self.stats_display_id = "stats"
		self.purge_display_id = "purge"
		self.points_display_id = "points"
		self.slots_display_id = "slots"
		self.give_display_id = "give"
		self.views_display_id = "views"
		self.uptime_display_id = "uptime"
		self.editors_display_id = "editors"
		self.set_display_id = "set"
		self.chanstats_display_id = "chanstats"
		self.commercial_display_id = "commercial"
		self.title_display_id = "title"
		self.game_display_id = "game"
		self.subcribers_display_id = "subscribers"
		self.moderators_display_id = "moderators"
		self.level_display_id = "level"
		self.loops_display_id = "loops"

		#Raffle and Lottery Point values
		self.raffle_point_value = 0
		self.lottery_point_value = 0

		#Initial stream data values
		stream_data = get_json_stream(self.channel_parsed)["streams"]
		if stream_data:
			game = stream_data[0]["game"]
			insert_data(self, self.game_display_id, ["game"], game.encode("utf-8"))
			title = stream_data[0]["channel"]["status"]
			insert_data(self, self.title_display_id, ["title"], title.encode("utf-8"))
		insert_data(self, self.topic_display_id, ["topic"], "")
		
		#Roulette
		#we should put settings like this in an admin menu, along with the timeout durations and such
		self.rol_chance = .5
		self.rol_timeout = 5 #seconds
		
		#Timeout-related stuff
		self.purge_duration = 5
		self.last_timeout_time = 0
		self.timeout_interval = 3#time to wait before sending a timeout unsuccessful cannot time out mods message
		
		#Check intervals
		self.follower_check_interval = 300#5 min
		self.stream_status_check_interval = 300#5 min
		
		self.stream_status = False
		
		#Some defaults
		self.default_permit_time = 30#seconds
		self.default_permit_msg_count = 10#msgs
		self.default_point_value = 0
		self.default_banphrase_timeout = 30#seconds
		
		#For the bot
		self.time_unit_arr = ["sec", "secs", "second", "seconds", "min", "mins", "minute", "minutes", "hr", "hrs", "hour", "hours", "day", "days", "week", "weeks"]
		self.reply_args_arr = ["{*USER*}", "{*TO_USER*}", "{*GAME*}", "{*STATUS*}", "{*TOPIC*}", "{*VIEWERS*}", "{*CHATTERS*}", "{*VIEWS*}", "{*FOLLOWERS*}"]
		#perhaps we should make this vvv a table
		self.default_cmd_arr = ['!link whitelist', '!permit', '!banphrase', '!autoreply', '!set', '!vote', '!raffle', '!roulette', '!8ball', '!uptime', '!chatters', '!viewers', '!subs', '!subscribers', '!commercial', '!ban emote', '!repeat', '!title', '!topic', '!game', '!purge', '!math', '!roll', '!coin', '!countdown']
		self.mods_msg = ''
		self.whisper_mods_thread = False

		#For the channel stats
		self.follower_arr = []
		self.viewer_arr = []
		self.perm_chatter_arr = []#so that we say welcome back if they are in this, and welcome if it is first time
		self.follower_arr, new_follower_arr = get_new_followers(self.follower_arr, self.channel_parsed, self)
		self.viewer_arr, new_viewer_arr = get_new_viewers(self.viewer_arr, self.channel_parsed, self)
		self.perm_chatter_arr.extend(new_viewer_arr)
				
		#Regexes
		self.link_regex = re.compile(ur'^(?:https?:\/\/)?\w+(?:\.\w{2,})+(?:\/\S+)*$', re.MULTILINE)
		self.ip_regex= re.compile(ur'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$\b', re.MULTILINE)
				
		#Initiate check loops
		check_loop_repeats = LoopingCall(self.repeat_check)
		check_loop_repeats.start(0.003)
		
		check_loop_countdowns = LoopingCall(self.countdown_check)
		check_loop_countdowns.start(0.003)
		
		check_loop_followers= LoopingCall(self.follower_check)
		check_loop_followers.start(self.follower_check_interval)
		
		check_loop_stream_status = LoopingCall(self.stream_status_check)
		check_loop_stream_status.start(self.stream_status_check_interval)
		
	def link_whitelist_parse(self, user, msg, channel_parsed, user_type):
		link_whitelist_str = "!link whitelist"
		link_whitelist_add_str = "!link whitelist add"
		link_whitelist_del_str = "!link whitelist delete"
		link_whitelist_rem_str = "!link whitelist remove"
		link_whitelist_list_str = "!link whitelist list"
		link_whitelist_clr_str = "!link whitelist clear"

		if get_status(self, self.link_whitelist_display_id):
			if in_front(link_whitelist_str, msg):
				msg_arr = msg.split(" ")
				if in_front(link_whitelist_add_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.link_whitelist_display_id):
						if len(msg_arr) > 3:
							link_whitelist = msg_arr[3]
							if re.search(self.link_regex, link_whitelist):#if is link according to our regex
								#is a url
								if has_count(self, self.link_whitelist_display_id, "link", link_whitelist):
									send_str = "%s is already a whitelisted link." % (link_whitelist)
								else:
									insert_data(self, self.link_whitelist_display_id, ["link"], link_whitelist)
									send_str = "%s added to list of whitelisted links." % (link_whitelist)
							else:
								send_str = "%s is not a valid link." % (link_whitelist)
						else:
							send_str = "Usage: \"!link whitelist add <link>\""
							whisper(self, user, send_str)
							return
					else:
						send_str = "You don't have the correct permissions to use \"!link whitelist add\"." 
						whisper(self, user, send_str)
						return
				elif in_front(link_whitelist_del_str, msg) or in_front(link_whitelist_rem_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.link_whitelist_display_id):
						if len(msg_arr) > 3:
							link_whitelist = msg_arr[3]
							if is_num(link_whitelist):
								#we add on one to the actual index because users prefer to start with 1, rather than 0.
								link_whitelist = int(link_whitelist)
								delete_status = delete_index_handler(self, self.link_whitelist_display_id, link_whitelist)
								if delete_status:
									send_str = "Link %s removed at index %s." % (delete_status["link"], link_whitelist)
								else:
									send_str = "Invalid index for link removal."
							else:
								delete_status = delete_value_handler(self, self.link_whitelist_display_id, "link", link_whitelist)
								if delete_status:
									send_str = "Link %s removed." % (link_whitelist)									
								else:
									send_str = "Specified link does not exist." 
						else:
							send_str = "Usage: \"!link whitelist delete/remove <link/index>\"" 
							whisper(self, user, send_str)
							return
					else:
						send_str = "You don't have the correct permissions to use \"!link whitelist delete/remove\"." 
						whisper(self, user, send_str)
						return
				elif link_whitelist_list_str == msg:
					link_whitelist_table = get_table(self, self.link_whitelist_display_id)
					if len(link_whitelist_table) == 0:
						send_str = "No active links." 
					else:
						send_str = "Active links: " 
						for row_index, row in enumerate(link_whitelist_table):
							if (row_index != len(link_whitelist_table) -1):
								#every element but last one
								send_str += "(%s.) %s, " % (row_index+1, link_whitelist_table[row_index]["link"])
							else:
								#last element in arr
								send_str += "(%s.) %s." % (row_index+1, link_whitelist_table[row_index]["link"])
					if not has_level(self, user, channel_parsed, user_type, self.link_whitelist_display_id):
						whisper(self, user, send_str)		
						return		
				elif in_front(link_whitelist_clr_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.link_whitelist_display_id):
						clear_table(self, self.link_whitelist_display_id)
						send_str = "All links removed." 
					else:
						send_str = "You don't have the correct permissions to use \"!link whitelist clear\"." 
						whisper(self, user, send_str)
						return
				elif in_front(link_whitelist_str, msg):
					send_str = "Add or remove links to timeout users who say them. Syntax and more information can be found in the documentation." 
					whisper(self, user, send_str)
					return
				else:
					send_str = "Usage: \"!link whitelist add/delete/remove/list/clear\"" 
					whisper(self, user, send_str)
					return
				self.write(send_str)
			else:
				return False
		else:
			return False
	
	def spam_permit_parse(self, user, msg, channel_parsed, user_type):
		#spam permits
		#going to keep in the ability to give one user multiple permits, it can be useful
		permit_str = "!permit"
		permit_add_str = "!permit add"
		permit_del_str = "!permit delete"
		permit_rem_str = "!permit remove"
		permit_list_str = "!permit list"
		permit_clr_str = "!permit clear"
		unpermit_str = "!unpermit"
		#!permit add <user> message/time <message duration/time duration>
		#permit add user
		#permit add user time
		#permit add user type
		#!permit <user> default time duration
		#!permit <user> <time> default time
		#!permit <user> <type> default of either
		#if no user then dont do anything
		if get_status(self, self.permit_display_id):
			if in_front(permit_str, msg):
				if has_level(self, user, channel_parsed, user_type, self.permit_display_id):
					msg_arr = msg.split(" ")
					if in_front(permit_add_str, msg):#!permit add
						if len(msg_arr) >= 3:
							permit_user = msg_arr[2]
							if is_num(permit_user) == False and (permit_user != "time" or permit_user != "message" or permit_user != "permanent"):
								#!permit add <user>
								permit_user = permit_user.lower()
								if len(msg_arr) == 3:
									current_time = time.time()
									permit_time = self.default_permit_time
									permit_type = "time"
									permit_pair = [current_time, permit_user, permit_time, permit_type]
									if insert_permit(self, permit_pair):
										send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
									else:
										send_str = "This user already has a permit with a permanent or longer duration"
								elif len(msg_arr) == 4:
									if msg_arr[3] == "time":
										#!permit add <user> time
										current_time = time.time()
										permit_time = self.default_permit_time
										permit_type = "time"
										permit_pair = [current_time, permit_user, permit_time, permit_type]
										if insert_permit(self, permit_pair):
											send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
										else:
											send_str = "This user already has a permit with a permanent or longer duration"
									elif msg_arr[3] == "message":
										#!permit add <user> message
										msg_count = self.default_permit_msg_count
										permit_type = "message"
										permit_pair = [0, permit_user, msg_count, permit_type]#0 = current msg count
										if insert_permit(self, permit_pair):
											send_str = "%s's spam filter has been lifted for %s messages." % (permit_user, msg_count)
										else:
											send_str = "This user already has a permit with a permanent or longer duration"
									elif msg_arr[3] == "permanent":
										#!permit add <user> permanent
										permit_type = "permanent"
										permit_pair = [0, permit_user, 0, permit_type]#0 = current msg count
										if insert_permit(self, permit_pair):
											send_str = "%s's spam filter has been permanently lifted." % (permit_user)
										else:
											send_str = "This user already has a permit with a permanent or longer duration"
									elif is_num(msg_arr[3]):
										#!permit add <user> <time duration>
										current_time = time.time()
										permit_time = simplify_num(msg_arr[3])
										permit_type = "time"
										permit_pair = [current_time, permit_user, permit_time, permit_type]
										if insert_permit(self, permit_pair):
											send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
										else:
											send_str = "This user already has a permit with a permanent or longer duration"
									else:
										send_str = "Usage: !permit add <user> message/time/<time> <message count/time duration/time unit>/permanent" 
										whisper(self, user, send_str)
										return	
								elif len(msg_arr) == 5:
									if msg_arr[3] == "time":
										if is_num(msg_arr[4]):
											#!permit add <user> <type> <time duration>
											current_time = time.time()
											permit_time = simplify_num(msg_arr[4])
											permit_type = "time"
											permit_pair = [current_time, permit_user, permit_time, permit_type]
											if insert_permit(self, permit_pair):
												send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
											else:
												send_str = "This user already has a permit with a permanent or longer duration"
										else:
											send_str = "Usage: !permit add <user> message/time/<time> <message count/time duration/time unit>/permanent" 
											whisper(self, user, send_str)
											return
									elif msg_arr[3] == "message":
										if is_num(msg_arr[4]):
											#!permit add <user> <type> <message count>
											msg_count = simplify_num(msg_arr[4])
											permit_type = "message"
											permit_pair = [0, permit_user, msg_count, permit_type]#0 = current msg count
											if insert_permit(self, permit_pair):
												send_str = "%s's spam filter has been lifted for %s messages." % (permit_user, msg_count)
											else:
												send_str = "This user already has a permit with a permanent or longer duration"
										else:
											send_str = "Usage: !permit add <user> message/time/<time> <message count/time duration/time unit>/permanent" 
											whisper(self, user, send_str)
											return
									elif is_num(msg_arr[3]):
										if msg_arr[4] in self.time_unit_arr:
											#!permit add <user> <time> <time unit>
											current_time = time.time()
											permit_time = simplify_num(msg_arr[3])
											permit_time_unit = msg_arr[4]
											permit_time = convert_to_sec(permit_time, permit_time_unit, self)
											permit_type = "time"
											permit_pair = [current_time, permit_user, permit_time, permit_type]
											if insert_permit(self, permit_pair):
												send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
											else:
												send_str = "This user already has a permit with a permanent or longer duration"
										else:
											send_str = "Usage: !permit add <user> message/time/<time> <message count/time duration/time unit>/permanent" 
											whisper(self, user, send_str)
											return
								elif len(msg_arr) == 6:
									if msg_arr[3] == "time" and is_num(msg_arr[4]) and msg_arr[5] in self.time_unit_arr:
										#!permit add <user> time <time> <time unit>
										current_time = time.time()
										permit_time = simplify_num(msg_arr[4])
										permit_time_unit = msg_arr[5]
										permit_time = convert_to_sec(permit_time, permit_time_unit, self)
										permit_type = "time"
										if insert_permit(self, permit_pair):
											send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
										else:
											send_str = "This user already has a permit with a permanent or longer duration"
									else:
										send_str = "Usage: !permit add <user> message/time/<time> <message count/time duration/time unit>/permanent" 
										whisper(self, user, send_str)
										return
								else:
									send_str = "Usage: !permit add <user> message/time/<time> <message count/time duration/time unit>/permanent" 
									whisper(self, user, send_str)
									return
							else:
								send_str = "Usage: !permit add <user> message/time/<time> <message count/time duration/time unit>/permanent" 
								whisper(self, user, send_str)
								return
						else:
							send_str = "Usage: !permit add <user> message/time/<time> <message count/time duration/time unit>/permanent" 
							whisper(self, user, send_str)
							return
								
					#delete/remove
					elif in_front(permit_del_str, msg) or in_front(permit_rem_str, msg):
						if len(msg_arr) == 3:
							permit_user = msg_arr[2]
							if is_num(permit_user):
								permit_user = int(permit_user)
								delete_status = delete_index_handler(self, self.permit_display_id, permit_user)
								if delete_status:
									if delete_status["type"] == "permanent":
										send_str = "Permanent permit %s removed at index %s." % (delete_status["user"], permit_user)
									elif delete_status["type"] == "message":
										send_str = "Permit %s with duration %s messages removed at index %s." % (delete_status["user"], delete_status["duration"], permit_user)
									elif delete_status["type"] == "time":
										send_str = "Permit %s with duration %s removed at index %s." % (delete_status["user"], parse_sec_condensed(delete_status["duration"]), permit_user)
									else:
										send_str = "This shouldn't happen, contact my creator if it does"
								else:
									send_str = "Invalid index for permit removal." 
							else:
								delete_status = delete_value_handler(self, self.permit_display_id, "user", permit_user)
								if delete_status:
									send_str = "Permit \"%s\" removed." % delete_status["user"]		
								else:
									send_str = "Specified permit does not exist." 
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!permit delete/remove <user/index>\"." 
							whisper(self, user, send_str)
							return
					#list
					elif permit_list_str == msg:
						permits_table = get_table(self, self.permit_display_id)
						if len(permits_table) == 0:
							send_str = "No users with active permits." 
						else:
							send_str = "Users with active permits: " 
							for row_index, row in enumerate(permits_table):
								if (row_index != len(permits_table) -1):
									#every element but last one
									if row["type"] == "time":
										send_str += "(%s.) %s : %s, " % (row_index+1, row["user"], parse_sec_condensed(row["duration"]))
									elif row["type"] == "message":
										send_str += "(%s.) %s : %s messages, " % (row_index+1, row["user"], row["duration"])
									else:
										send_str += "(%s.) %s : permanent, " % (row_index+1, row["user"])
								else:
									#last element in arr
									if row["type"] == "time":
										send_str += "(%s.) %s : %s." % (row_index+1, row["user"], parse_sec_condensed(row["duration"]))
									elif row["type"] == "message":
										send_str += "(%s.) %s : %s messages." % (row_index+1, row["user"], row["duration"])
									else:
										send_str += "(%s.) %s : permanent." % (row_index+1, row["user"])
						if not has_level(self, user, channel_parsed, user_type, self.permit_display_id):
							whisper(self, user, send_str)		
							return		
					#clear
					elif in_front(permit_clr_str, msg):
						clear_table(self, self.permit_display_id)
						send_str = "All permits removed." 
					#normal
					elif permit_str == msg:
						if has_level(self, user, channel_parsed, user_type, self.permit_display_id):
							send_str = "Add or remove spam permits, allowing a user to message anything for a certain number of messages, or a length of time. Syntax and more information can be found in the documentation." 
						else:
							send_str = "You don't have the correct permissions to use !permit commands" 
						whisper(self, user, send_str)
						return
					#!permit <user>...
					elif len(msg_arr) >= 2:
						permit_user = msg_arr[1]
						if is_num(permit_user) == False and (permit_user != "time" or permit_user != "message"):
							#!permit <user>
							permit_user = permit_user.lower()
							if len(msg_arr) == 2:
								current_time = time.time()
								permit_time = self.default_permit_time
								permit_type = "time"
								permit_pair = [current_time, permit_user, permit_time, permit_type]
								if insert_permit(self, permit_pair):
									send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
								else:
									send_str = "This user already has a permit with a permanent or longer duration"
							elif len(msg_arr) == 3:
								if msg_arr[2] == "time":
									#!permit <user> time
									current_time = time.time()
									permit_time = self.default_permit_time
									permit_type = "time"
									permit_pair = [current_time, permit_user, permit_time, permit_type]
									if insert_permit(self, permit_pair):
										send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
									else:
										send_str = "This user already has a permit with a permanent or longer duration"
								elif msg_arr[2] == "message":
									#!permit <user> message
									msg_count = self.default_permit_msg_count
									permit_type = "message"
									permit_pair = [0, permit_user, msg_count, permit_type]#0 = current msg count
									if insert_permit(self, permit_pair):
										send_str = "%s's spam filter has been lifted for %s messages." % (permit_user, msg_count)
									else:
										send_str = "This user already has a permit with a permanent or longer duration"
								elif msg_arr[2] == "permanent":
									#!permit <user> permanent
									permit_type = "permanent"
									permit_pair = [0, permit_user, 0, permit_type]#0 = current msg count
									if insert_permit(self, permit_pair):
										send_str = "%s's spam filter has been permanently lifted." % (permit_user)
									else:
										send_str = "This user already has a permit with a permanent or longer duration"
								elif is_num(msg_arr[2]):
									#!permit <user> <time duration>
									current_time = time.time()
									permit_time = simplify_num(msg_arr[2])
									permit_type = "time"
									permit_pair = [current_time, permit_user, permit_time, permit_type]
									if insert_permit(self, permit_pair):
										send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
									else:
										send_str = "This user already has a permit with a permanent or longer duration"
								else:
									send_str = "Usage: !permit <user> message/time <message count/time duration>" 
									whisper(self, user, send_str)
									return
							elif len(msg_arr) == 4:
								if msg_arr[2] == "time":
									if is_num(msg_arr[3]):
										#!permit <user> <type> <time duration>
										current_time = time.time()
										permit_time = simplify_num(msg_arr[3])
										permit_type = "time"
										permit_pair = [current_time, permit_user, permit_time, permit_type]
										if insert_permit(self, permit_pair):
											send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
										else:
											send_str = "This user already has a permit with a permanent or longer duration"
									else:
										send_str = "Usage: !permit <user> message/time <message count/time duration>" 
										whisper(self, user, send_str)
										return
								elif msg_arr[2] == "message":
									if is_num(msg_arr[3]):
										#!permit <user> <type> <message count>
										msg_count = simplify_num(msg_arr[3])
										permit_type = "message"
										permit_pair = [0, permit_user, msg_count, permit_type]#0 = current msg count
										if insert_permit(self, permit_pair):
											send_str = "%s's spam filter has been lifted for %s messages." % (permit_user, msg_count)
										else:
											send_str = "This user already has a permit with a permanent or longer duration"
									else:
										send_str = "Usage: !permit <user> message/time <message count/time duration>/permanent" 
										whisper(self, user, send_str)
										return
								elif is_num(msg_arr[2]):
									if msg_arr[3] in self.time_unit_arr:
										#!permit <user> <time> <time unit>
										current_time = time.time()
										permit_time = simplify_num(msg_arr[2])
										permit_time_unit = msg_arr[3]
										permit_time = convert_to_sec(permit_time, permit_time_unit, self)
										permit_type = "time"
										permit_pair = [current_time, permit_user, permit_time, permit_type]
										if insert_permit(self, permit_pair):
											send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
										else:
											send_str = "This user already has a permit with a permanent or longer duration"
									else:
										send_str = "Usage: !permit <user> message/time/<time> <message count/time duration/time unit>/permanent" 
										whisper(self, user, send_str)
										return
								else:
									send_str = "Usage: !permit <user> message/time <message count/time duration>/permanent" 
									whisper(self, user, send_str)
									return
							elif len(msg_arr) == 5:
								if msg_arr[2] == "time" and is_num(msg_arr[3]) and msg_arr[4] in self.time_unit_arr:
									#!permit <user> time <time> <time unit>
									current_time = time.time()
									permit_time = simplify_num(msg_arr[3])
									permit_time_unit = msg_arr[4]
									permit_time = convert_to_sec(permit_time, permit_time_unit, self)
									permit_type = "time"
									permit_pair = [current_time, permit_user, permit_time, permit_type]
									if insert_permit(self, permit_pair):
										send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
									else:
										send_str = "This user already has a permit with a permanent or longer duration"
								else:
									send_str = "Usage: !permit <user> message/time/<time> <message count/time duration/time unit>/permanent" 
									whisper(self, user, send_str)
									return
							else:
								send_str = "Usage: !permit <user> message/time <message count/time duration>/permanent" 
								whisper(self, user, send_str)
								return
						else:
							send_str = "Usage: !permit <user> message/time <message count/time duration>/permanent" 
							whisper(self, user, send_str)
							return
					else:
						if has_level(self, user, channel_parsed, user_type, self.permit_display_id):
							send_str = "Add or remove spam permits, allowing a user to message anything for a certain number of messages, or a length of time. Syntax and more information can be found in the documentation." 
						else:
							send_str = "You don't have the correct permissions to use !permit commands" 
						whisper(self, user, send_str)
						return
					
									
				else:
					send_str = "You don't have the correct permissions to use !permit commands." 
					whisper(self, user, send_str)
					return
				self.write(send_str)
			
			
			if in_front(unpermit_str, msg):
				if has_level(self, user, channel_parsed, user_type, self.permit_display_id):
					msg_arr = msg.split(" ")
					if len(msg_arr) == 2:
						permit_user = msg_arr[1]
						delete_status = delete_value_handler(self, self.permit_display_id, "user", permit_user)
						if delete_status:
							send_str = "%s's spam permit has been removed." % permit_user.lower()
						else:
							send_str = "%s does not have a spam permit." % permit_user.lower()
					else:
						send_str = "Usage: \"!unpermit <user>\"" 
						whisper(self, user, send_str)
						return
				else:
					send_str = "You don't have the correct permissions to unpermit users." 
					whisper(self, user, send_str)
					return
				self.write(send_str)
				
			
			#if !permit or !unpermit were used then main_parse is over
			if in_front(permit_str, msg) or in_front(unpermit_str, msg):
				return True
			else:
				return False
		else:
			return False

	def antispam_parse(self, user, msg, channel_parsed, user_type):
		#antispam
		
		msg_info_arr = []
		long_word_limit = 80
		
		#timeout_msg = "No <timeout_msg> allowed"
		caps_warn_duration = 1
		caps_warn_cooldown = 30
		caps_timeout_msg = "excessive use of caps"
		caps_timeout_duration = 1
		
		emote_warn_duration = 1
		emote_warn_cooldown = 30
		emote_timeout_msg = "excessive use of emotes"
		emote_timeout_duration = 1
		
		ban_emote_warn_duration = 1
		ban_emote_warn_cooldown = 30
		ban_emote_timeout_msg = "banned emotes"
		ban_emote_timeout_duration = 1
			
		banphrase_warn_duration = 1
		banphrase_warn_cooldown = 30
		banphrase_timeout_msg = "banned phrases"
		banphrase_timeout_duration = 1
			
		fake_purge_warn_duration = 1
		fake_purge_warn_cooldown = 30
		fake_purge_timeout_msg = "fake purges"
		fake_purge_timeout_duration = 1
		fake_purge_arr = ["<message deleted>"] #need more of these?
		
		skincode_msg = "!skincode"
		skincode_warn_duration = 1
		skincode_warn_cooldown = 30
		skincode_timeout_msg = "skin code variations"
		skincode_timeout_duration = 1
		
		long_msg_warn_duration = 1
		long_msg_warn_cooldown = 30
		long_msg_timeout_msg = "excessively long messages"
		long_msg_timeout_duration = 1
		
		symbol_warn_duration = 1
		symbol_warn_cooldown = 30
		symbol_timeout_msg = "excessive use of symbols"
		symbol_timeout_duration = 1
		
		long_word_warn_duration = 1
		long_word_warn_cooldown = 30
		long_word_timeout_msg = "excessively long words"
		long_word_timeout_duration = 1
		
		link_whitelist_warn_duration = 1
		link_whitelist_warn_cooldown = 30
		link_whitelist_timeout_msg = "links"
		#######################################3
		link_whitelist_timeout_duration = 1
		######################################CHANGE THESE BACK TO REASONABLE, DEFAULT DURATIONS
		
		spam_warn_duration = 1
		spam_warn_cooldown = 30
		spam_timeout_msg = "spam"
		spam_timeout_duration = 1
		
		me_msg = "/me"
		me_warn_duration = 1
		me_warn_cooldown = 30
		me_timeout_msg = "usage of /me"
		me_timeout_duration = 1
		
		ip_warn_duration = 1
		ip_warn_cooldown = 30
		ip_timeout_msg = "IP Addresses"
		ip_timeout_duration = 1
		
		#add time, user, and message to array of 30second old messages
		if get_status(self, self.antispam_display_id):
			if user.rstrip() == self.nickname or is_streamer(user, self.channel_parsed) or has_level(self, user, channel_parsed, user_type, self.antispam_display_id):
				return False
			else:
				
				#links
				if get_status(self, self.link_antispam_display_id):
					for word in msg.split(" "):
						#we need to determine links for this sole reason
						if re.search(self.link_regex, word):#if is link according to our regex
							link_whitelist_table = get_table(self, self.link_whitelist_display_id)
							for row in link_whitelist_table:
								link_whitelist = row["link"]
								if "*" in link_whitelist:
									link_whitelist_wcard = link_whitelist.split("*")
									#this way if there is any part that is not in the word, it will move on
									#however if they are all in the word, it will do the else statement
									for link_wcard_part in link_whitelist_wcard:
										if link_wcard_part not in word:#time them out and return
											warn(user, msg, channel_parsed, self, "link_whitelist_warn", link_whitelist_warn_duration, link_whitelist_warn_cooldown, link_whitelist_timeout_msg, link_whitelist_timeout_duration)
											return True
									else:#the link was a pardoned one, let them free
										break
								else:
									if link_whitelist == word:
										break
							else:
								#link isn't whitelisted, time out user 
								warn(user, msg, channel_parsed, self, "link_whitelist_warn", link_whitelist_warn_duration, link_whitelist_warn_cooldown, link_whitelist_timeout_msg, link_whitelist_timeout_duration)
								return True
								
				'''#emote spam
				if get_status(self, "emote_antispam"):
					msg_emote_count = 0
					for emote in self.emote_arr:
						if word_count(msg, emote) != 0:
							msg_emote_count += msg.count(emote)
						if msg_emote_count >= emote_max:
							warn(user, msg, channel_parsed, self, "emote_warn", emote_warn_duration, emote_warn_cooldown, emote_timeout_msg, emote_timeout_duration)
							return True'''
				
				#banphrases
				if get_status(self, self.banphrase_display_id):
					banphrase_table = get_table(self, self.banphrase_display_id)
					for row_index, row in enumerate(banphrase_table):
						if row['banphrase'] in msg:
							banphrase_timeout_duration = simplify_num(row['duration'])
							warn(user, msg, channel_parsed, self, "banphrase_warn", banphrase_warn_duration, banphrase_warn_cooldown, banphrase_timeout_msg, banphrase_timeout_duration)
							return True
							
				#caps spam
				if get_status(self, self.caps_antispam_display_id):
					if len(msg) >= caps_perc_min_msg_len:
						if caps_perc(msg) >= 60:
							warn(user, msg, channel_parsed, self, "caps_warn", caps_warn_duration, caps_warn_cooldown, caps_timeout_msg, caps_timeout_duration)
							return True
				#fake purges
				if get_status(self, self.fake_purge_antispam_display_id):
					if msg in fake_purge_arr:
						warn(user, msg, channel_parsed, self, "fake_purge_warn", fake_purge_warn_duration, fake_purge_warn_cooldown, fake_purge_timeout_msg, fake_purge_timeout_duration)
						return True
				#!skincode
				if get_status(self, self.skincode_antispam_display_id):
					if in_front(skincode_msg, msg):
						warn(user, msg, channel_parsed, self, "skincode_warn", skincode_warn_duration, skincode_warn_cooldown, skincode_timeout_msg, skincode_timeout_duration)
						return True
				#long messages
				if get_status(self, self.long_message_antispam_display_id):
					if len(msg) > msg_length_max:
						warn(user, msg, channel_parsed, self, "long_msg_warn", long_msg_warn_duration, long_msg_warn_cooldown, long_msg_timeout_msg, long_msg_timeout_duration)
						return True
				
				#block symbols
				
				#dongers
				

				#excessive symbols
				#if there are more than min_symbol_chars in message, check the percentage and amount
				if get_status(self, self.symbol_antispam_display_id):
					if len(msg) > min_symbol_chars:
						symbol_num = symbol_count(msg)
						symbol_perc = float(symbol_num) / len(msg)
						#if the limits are exceeded for num or percentage
						if symbol_num > max_symbol_num or symbol_perc > max_symbol_perc:
							warn(user, msg, channel_parsed, self, "symbol_warn", symbol_warn_duration, symbol_warn_cooldown, symbol_timeout_msg, symbol_timeout_duration)
							return True
						
				#these need to be different types
				msg_arr = msg.split(" ")
				#long word spam
				if get_status(self, self.long_word_antispam_display_id):
					for word in msg_arr:
						if len(word) > long_word_limit and '\n' not in word:
							warn(user, msg, channel_parsed, self, "long_word_warn", long_word_warn_duration, long_word_warn_cooldown, long_word_timeout_msg, long_word_timeout_duration)
							return True
				#/me
				if get_status(self, self.me_antispam_display_id):
					if in_front(me_msg, msg):
						warn(user, msg, channel_parsed, self, "me_warn", me_warn_duration, me_warn_cooldown, me_timeout_msg, me_timeout_duration)
						return True
					
				#ip addresses
				if get_status(self, self.ip_antispam_display_id):
					for word in msg.split(" "):
						#we need to determine links for this sole reason
						if re.search(self.ip_regex, word):#if is ip address according to our regex
							warn(user, msg, channel_parsed, self, "ip_warn", ip_warn_duration, ip_warn_cooldown, ip_timeout_msg, ip_timeout_duration)
							return True
				'''the complicated general antispam that moobot offers
				if len(msg) > min_spam_chars:
					#idk how to go about making this without killing speed of program		
					pass'''
				return False
		else:
			return False
			
	def banphrase_parse(self, user, msg, channel_parsed, user_type):
		#banphrase
		#give option to ban people if phrase is said or after a warning
		banphrase_str = "!banphrase"
		banphrase_add_str = "!banphrase add"
		banphrase_del_str = "!banphrase delete"
		banphrase_rem_str = "!banphrase remove"
		banphrase_list_str = "!banphrase list"
		banphrase_clr_str = "!banphrase clear"
		
		if get_status(self, self.banphrase_display_id):
			msg_arr = msg.split(" ")
			if in_front(banphrase_str, msg):
				if in_front(banphrase_add_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.banphrase_display_id): 
						if len(msg_arr) > 2:#need to have this if statement more often
							del msg_arr[0:2]#remove command specifiers
							banphrase = ''
							for phrase_part in range(len(msg_arr)):
								if phrase_part == len(msg_arr)-2 and is_num(msg_arr[phrase_part]) and msg_arr[phrase_part+1] in self.time_unit_arr:#if unit of time specified
									banphrase = banphrase.rstrip()
									banphrase_timeout = simplify_num(msg_arr[phrase_part])
									interval_unit = msg_arr[phrase_part+1]
									banphrase_timeout = convert_to_sec(banphrase_timeout, interval_unit, self)
									break
								elif phrase_part == len(msg_arr)-1 and is_num(phrase_part):#if no unit of time specified, seconds
									banphrase = banphrase.rstrip()#get rid of trailing space
									banphrase_timeout = msg_arr[phrase_part]
								else:
									banphrase += msg_arr[phrase_part] + " "
							print banphrase_timeout
							if banphrase_timeout:
								if not is_num(banphrase_timeout):
									send_str = "Banphrase timeout duration must be a number." 
									whisper(self, user, send_str)
									return	
								else:
									#valid timeout input
									banphrase_timeout = simplify_num(banphrase_timeout)
									if banphrase_timeout < 0:
										send_str = "Banphrase timeout duration must be greater than 0." 
										whisper(self, user, send_str)
										return	
									if has_count(self, self.banphrase_display_id, "banphrase", banphrase):
										send_str = "%s is already a banphrase." % (banphrase)
									else:
										query = text("INSERT INTO `%s` (`banphrase`, `duration`) VALUES (:banphrase, %d)" % (self.banphrase_display_id, banphrase_timeout))
										self.conn.execute(query, banphrase=banphrase)
										send_str = "\"%s\" added to list of banphrases with timeout duration %d." % (banphrase, parse_sec_condensed(banphrase_timeout))
							else:
								if has_count(self, self.banphrase_display_id, "banphrase", banphrase):
									send_str = "%s is already a banphrase." % (banphrase)
								else:
									query = text("INSERT INTO `%s` (`banphrase`, `duration`) VALUES (:banphrase, %d)" % (self.banphrase_display_id, self.default_banphrase_timeout))
									self.conn.execute(query, banphrase=banphrase)
									send_str = "\"%s\" added to list of banphrases." % (banphrase)
						else:
							send_str = "Usage: \"!banphrase add <banphrase>\"" 
							whisper(self, user, send_str)
							return
					else:
						send_str = "You don't have the correct permissions to use \"!banphrase add\"." 
						whisper(self, user, send_str)
						return
				elif in_front(banphrase_del_str, msg) or in_front(banphrase_rem_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.banphrase_display_id):
						if len(msg_arr) > 2:
							banphrase = msg_arr[2]
							if is_num(banphrase):
								#we add on one to the actual index because users prefer to start with 1, rather than 0.
								banphrase = int(banphrase)
								delete_status = delete_index_handler(self, self.banphrase_display_id, banphrase)
								if delete_status:
									send_str = "Banphrase \"%s\" removed at index %s." % (delete_status["banphrase"], banphrase)
								else:
									send_str = "Invalid index for banphrase removal." 
							else:
								delete_status = delete_value_handler(self, self.banphrase_display_id, "banphrase", banphrase)
								if delete_status:
									send_str = "Banphrase \"%s\" removed." % (banphrase)									
								else:
									send_str = "Specified banphrase does not exist." 
						else:
							send_str = "Usage: \"!banphrase delete/remove <banphrase/index>\"" 
							whisper(self, user, send_str)
							return
					else:
						send_str = "You don't have the correct permissions to use \"!banphrase delete/remove\"." 
						whisper(self, user, send_str)
						return
				elif banphrase_list_str == msg:
					banphrase_table = get_table(self, self.banphrase_display_id)
					if len(banphrase_table) == 0:
						send_str = "No active banphrases." 
					else:
						send_str = "Active banphrases: " 
						for row_index, row in enumerate(banphrase_table):
							if (row_index != len(banphrase_table) -1):
								#every element but last one
								send_str += "(%s.) %s : %s, " % (row_index+1, row["banphrase"], parse_sec_condensed(row["duration"]))
							else:
								#last element in arr
								send_str += "(%s.) %s : %s." % (row_index+1, row["banphrase"], parse_sec_condensed(row["duration"]))
					if not has_level(self, user, channel_parsed, user_type, self.banphrase_display_id):
						whisper(self, user, send_str)		
						return		
				elif in_front(banphrase_clr_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.banphrase_display_id): 
						clear_table(self, self.banphrase_display_id)
						send_str = "All banphrases removed." 
					else:
						send_str = "You don't have the correct permissions to use \"!banphrase clear\"." 
						whisper(self, user, send_str)
						return
				elif in_front(banphrase_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.banphrase_display_id): 
						send_str = "Add or remove banphrases to timeout users who say them. Syntax and more information can be found in the documentation." 
					else:
						send_str = "You don't have the correct permissions to use !banphrase commands." 
						whisper(self, user, send_str)
						return
				self.write(send_str)
			else:
				return False
		else:
			return False
	
	def autoreply_parse(self, user, msg, channel_parsed, user_type):
		#autoreplies 
		autoreply_str = "!autoreply"
		autoreply_add_str = "!autoreply add"
		autoreply_del_str = "!autoreply delete"
		autoreply_rem_str = "!autoreply remove"
		autoreply_list_str = "!autoreply list"
		autoreply_clr_str = "!autoreply clear"
		
		autoreply_on = get_status(self, self.autoreply_display_id)
		if autoreply_on:
			if in_front(autoreply_str, msg):
				#add autoreplies
				if in_front(autoreply_add_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.autoreply_display_id): 
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) == 3:
							if ":" in msg_arr[2]:
								ar_msg_arr = msg_arr[2].split(":", 1)
								if len(ar_msg_arr) == 2:
									ar_phrase = ar_msg_arr[0].rstrip().lstrip()
									ar_reply = ar_msg_arr[1].rstrip().lstrip()
									if is_num(ar_reply[-1:]):
										ar_level = ar_reply[-1:]#get level
										ar_reply = ar_reply[:-1]#everything but last letter
									else:
										ar_level = False

									if ar_level:
										if not check_int(ar_level):
											send_str = "Level requirement must be an integer." 
											whisper(self, user, send_str)
											return	
										else:
											#valid level input
											ar_level = int(ar_level)
											if ar_level < 1 or ar_level > 4:
												send_str = "Level requirement must be between 1 and 4." 
												whisper(self, user, send_str)
												return	
											query = text("SELECT COUNT(*) FROM `%s` WHERE `phrase` = :phrase AND `reply` = :reply" % (self.autoreply_display_id))
											if result_to_dict(self.conn.execute(query, phrase=ar_phrase, reply=ar_reply))[0]["COUNT(*)"] > 0:
												send_str = "%s is already an autoreply phrase." % (ar_pair[0])
											else:
												if not disconnect_cmd(ar_reply):
													query = text("INSERT INTO `%s` (`phrase`, `reply`, `level`) VALUES (:phrase, :reply, %d)" % (self.autoreply_display_id, ar_level))
													self.conn.execute(query, phrase=ar_phrase, reply=ar_reply)
													send_str = "Phrase \"%s\" added, with reply \"%s\" and level %d." % (ar_phrase, ar_reply, ar_level	)
												else:
													send_str = "No \".disconnect\" or \"/disconnect\" variants allowed."
									else:
										query = text("SELECT COUNT(*) FROM `%s` WHERE `phrase` = :phrase AND `reply` = :reply" % (self.autoreply_display_id))
										if result_to_dict(self.conn.execute(query, phrase=ar_phrase, reply=ar_reply))[0]["COUNT(*)"] > 0:
											send_str = "%s is already an autoreply phrase." % (ar_pair[0])
										else:
											if not disconnect_cmd(ar_reply):
												query = text("INSERT INTO `%s` (`phrase`, `reply`, `level`) VALUES (:phrase, :reply, %d)" % (self.autoreply_display_id, 3))
												self.conn.execute(query, phrase=ar_phrase, reply=ar_reply)
												send_str = "Phrase \"%s\" added, with reply \"%s\"." % (ar_phrase, ar_reply)
											else:
												send_str = "No \".disconnect\" or \"/disconnect\" variants allowed."
								else:
									#incorrectly formatted, display usage
									send_str = "Usage: \"!autoreply add <phrase>:<reply>\"." 
									whisper(self, user, send_str)
									return
							else:
								#incorrectly formatted, display usage
								send_str = "Usage: \"!autoreply add <phrase>:<reply>\"." 
								whisper(self, user, send_str)
								return
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!autoreply add <phrase>:<reply>\"." 
							whisper(self, user, send_str)
							return
					else:
						send_str = "You don't have the correct permissions to use \"!autoreply add\"." 
						whisper(self, user, send_str)
						return
				#delete autoreplies
				elif in_front(autoreply_del_str, msg) or in_front(autoreply_rem_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.autoreply_display_id): 
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) == 3:
							ar_phrase = msg_arr[2]
							if is_num(ar_phrase):
								ar_phrase = int(ar_phrase)
								delete_status = delete_index_handler(self, self.autoreply_display_id, ar_phrase)
								if delete_status:
									send_str = "Autoreply %s:%s removed at index %s." % (delete_status["phrase"], delete_status["reply"], ar_phrase)
								else:
									send_str = "Invalid index for autoreply removal." 
							
							else:
								delete_status = delete_value_handler(self, self.autoreply_display_id, "phrase", ar_phrase)
								if delete_status:		
									send_str = "Autoreply %s:%s removed." % (delete_status["phrase"], delete_status["reply"])	
								else:
									send_str = "Specified autoreply does not exist." 
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!autoreply delete/remove <phrase/index>\"." 
							whisper(self, user, send_str)
							return
					else:
						send_str = "You don't have the correct permissions to use \"!autoreply delete/remove\"." 
						whisper(self, user, send_str)
						return
				#list autoreplies
				elif autoreply_list_str == msg:
					autoreply_table = get_table(self, self.autoreply_display_id)
					if len(autoreply_table) == 0:
						send_str = "No active autoreplies." 
					else:
						send_str = "Active autoreplies: " 
						for row_index, row in enumerate(autoreply_table):
							ar_phrase = row["phrase"]
							ar_reply = row["reply"]
							if (row_index != len(autoreply_table)-1):
								#every element but last one
								send_str += "(%s.) %s: %s, " % (row_index+1, row["phrase"], row["reply"])
							else:
								#last element in arr
								send_str += "(%s.) %s: %s." % (row_index+1, row["phrase"], row["reply"])
					if not has_level(self, user, channel_parsed, user_type, self.autoreply_display_id):
						whisper(self, user, send_str)		
						return			
				#clear autoreplies
				elif in_front(autoreply_clr_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.autoreply_display_id): 
						clear_table(self, self.autoreply_display_id)
						send_str = "All autoreplies removed." 
					else:
						send_str = "You don't have the correct permissions to use \"!autoreply clear\"." 
						whisper(self, user, send_str)
						return
				#just autoreply string, display usage
				elif in_front(autoreply_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.autoreply_display_id): 
						send_str = "Add or remove phrases that trigger automatic replies. Syntax and more information can be found in the documentation." 
					else:
						send_str = "You don't have the correct permissions to use !autoreply commands." 
					whisper(self, user, send_str)
					return
				else:
					if has_level(self, user, channel_parsed, user_type, self.autoreply_display_id): 
						send_str = "Usage: !autoreply add/delete/remove/list/clear" 
					else:
						send_str = "You don't have the correct permissions to use !autoreply commands." 
					whisper(self, user, send_str)
					return
				self.write(send_str)
			else:			
				if autoreply_on:
					autoreply_table = get_table(self, self.autoreply_display_id)
					for row in autoreply_table:
						try:
							phrase_index = msg.index(row["phrase"])
							#if msg did contain the autoreply phrase
							reply = row["reply"]
							level = row["level"]
							user_level = get_user_level(self, user, channel_parsed, user_type)
							if user_level <= level:
								for word in reply.split():
									if word in self.reply_args_arr:
										if word == "{*USER*}":
											reply = reply.replace("{*USER*}", user)
										elif word == "{*TO_USER*}":
											to_user_part = msg[phrase_index+len(ar_pair[0]):len(msg)]#all the elements after the autoreply
											reply_to_user = to_user_part.split()[0]#the first word after the autoreply, should be the to user
											reply = reply.replace("{*TO_USER*}", str(reply_to_user))
										elif word == "{*GAME*}":
											game = result_to_dict(self.conn.execute("SELECT `game` FROM game LIMIT 1"))
											reply = reply.replace("{*GAME*}", game)
										elif word == "{*STATUS*}":
											title = result_to_dict(self.conn.execute("SELECT `title` FROM title LIMIT 1"))
											reply = reply.replace("{*STATUS*}", title)
										elif word == "{*TOPIC*}":
											topic = result_to_dict(self.conn.execute("SELECT `topic` FROM topic LIMIT 1"))
											reply = reply.replace("{*TOPIC*}", topic)
										elif word == "{*VIEWERS*}":
											viewer_count = get_raw_general_stats(channel_parsed, 'viewers')
											reply = reply.replace("{*VIEWERS*}", str(viewer_count))
										elif word == "{*CHATTERS*}":
											chatter_count = get_raw_general_stats(channel_parsed, 'chatters')
											reply = reply.replace("{*CHATTERS*}", str(chatter_count))
										elif word == "{*VIEWS*}":
											view_count = get_raw_general_stats(channel_parsed, 'views')
											reply = reply.replace("{*VIEWS*}", str(view_count))
										elif word == "{*FOLLOWERS*}":
											follower_count = get_raw_general_stats(channel_parsed, 'followers')
											reply = reply.replace("{*FOLLOWERS*}", str(follower_count))
								if in_front("/w", reply) or in_front(".w", reply):
									whisper_response(reply)
								else:
									self.write(reply)
								return False
							'''else:
								send_str = "You don't have the correct permissions to use this autoreply." 
								whisper(self, user, send_str)
								return'''
						except:
							#msg did not contain the autoreply
							pass
				return False
		else:
			return False
	
	def set_parse(self, user, msg, channel_parsed, user_type):
		#sets			
		
		set_str = "!set"
		set_roulette_str = "!set roulette"
		set_ball_str = "!set 8ball"
		set_banphrase_str = "!set banphrase"
		set_autoreply_str = "!set autoreply"
		set_repeat_str = "!set repeat"
		set_roll_str = "!set roll"
		set_math_str = "!set math"
		set_coin_str = "!set coin"
		set_countdown_str = "!set countdown"
		set_topic_str = "!set topic"
		set_stats_str = "!set stats"
		set_views_str = "!set views"
		set_viewers_str = "!set viewers"
		set_chatters_str = "!set chatters"
		set_followers_str = "!set followers"
		set_loops_str = "!set loops"
		set_set_str = "!set set"
		
		set_antispam_str = "!set antispam"
		set_repeat_antispam_str = "!set repeat antispam"
		set_emote_antispam_str = "!set emote antispam"
		set_caps_antispam_str = "!set caps antispam"
		set_fake_purge_antispam_str = "!set fake purge antispam"
		set_skincode_antispam_str = "!set skincode antispam"
		set_long_msg_antispam_str = "!set long message antispam"
		set_symbol_antispam_str = "!set symbol antispam"
		set_link_antispam_str = "!set link antispam"
		set_long_word_antispam_str = "!set long word antispam"
		set_me_antispam_str = "!set me antispam"
		set_ip_antispam_str = "!set ip antispam"
		
		set_ban_emotes_str = "!set ban emotes"
		set_spam_permits_str = "!set spam permits"
		
		set_rol_cmd_str = "!roulette"
		set_rol_chance_str = "!roulette chance"
		
		if in_front(set_str, msg):
			if has_level(self, user, channel_parsed, user_type, self.set_display_id):
				msg_arr = msg.split(" ")
				if len(msg_arr) == 3:
					
					#turn roulette on or off
					if in_front(set_roulette_str, msg):
						set_value(self, self.roulette_display_id, msg_arr)
						
					#turn 8ball on or off
					elif in_front(set_ball_str, msg):
						set_value(self, self.ball_display_id, msg_arr)
						
					#banphrases
					elif in_front(set_banphrase_str, msg):
						set_value(self, self.banphrase_display_id, msg_arr)
					
					#autoreplies
					elif in_front(set_autoreply_str, msg):
						set_value(self, self.autoreply_display_id, msg_arr)
						
					#antispam
					elif in_front(set_antispam_str, msg):
						set_value(self, self.antispam_display_id, msg_arr)
						
					#repeat
					elif in_front(set_repeat_str, msg):
						set_value(self, self.repeat_display_id, msg_arr)
					
					#roll
					elif in_front(set_roll_str, msg):
						set_value(self, self.roll_display_id, msg_arr)
					
					#math
					elif in_front(set_math_str, msg):
						set_value(self, self.math_display_id, msg_arr)
						
					#coin
					elif in_front(set_coin_str, msg):
						set_value(self, self.coin_display_id, msg_arr)
					
					#countdown
					elif in_front(set_countdown_str, msg):
						set_value(self, self.countdown_display_id, msg_arr)
						
					#topic
					elif in_front(set_topic_str, msg):
						set_value(self, self.topic_display_id, msg_arr)
					
					#views
					elif in_front(set_views_str, msg):
						set_value(self, self.views_display_id, msg_arr)	
					
					#viewers
					elif in_front(set_viewers_str, msg):
						set_value(self, self.viewers_display_id, msg_arr)
					
					#chatters
					elif in_front(set_chatters_str, msg):
						set_value(self, self.chatters_display_id, msg_arr)
					
					#followers
					elif in_front(set_followers_str, msg):
						set_value(self, self.followers_display_id, msg_arr)
					
					#stats
					elif in_front(set_stats_str, msg):
						set_value(self, self.stats_display_id, msg_arr)
					
					#loops
					elif in_front(set_loops_str, msg):
						set_value(self, self.loops_display_id, msg_arr)

					#set
					elif in_front(set_set_str, msg):
						set_value(self, self.set_display_id, msg_arr)	

					else:
						send_str = "Usage: \"!set <feature> on/off \"." 
						whisper(self, user, send_str)
						return
				elif len(msg_arr) == 4:
					#repeat antispam
					if in_front(set_repeat_antispam_str, msg):
						set_value(self, self.repeat_antispam_display_id, msg_arr)
						
					#emote antispam
					elif in_front(set_emote_antispam_str, msg):
						set_value(self, self.emote_antispam_display_id, msg_arr)
						
					#caps antispam
					elif in_front(set_caps_antispam_str, msg):
						set_value(self, self.caps_antispam_display_id, msg_arr)
					
					#skincode antispam
					elif in_front(set_skincode_antispam_str, msg):
						set_value(self, self.skincode_antispam_display_id, msg_arr)
					
					#symbol antispam
					elif in_front(set_symbol_antispam_str, msg):
						set_value(self, self.symbol_antispam_display_id, msg_arr)
					
					#link antispam
					elif in_front(set_link_antispam_str, msg):
						set_value(self, self.link_antispam_display_id, msg_arr)
					
					#me antispam
					elif in_front(set_me_antispam_str, msg):
						set_value(self, self.me_antispam_display_id, msg_arr)
					
					#spam permits
					elif in_front(set_spam_permits_str, msg):
						set_value(self, self.permit_display_id, msg_arr)
						
					#ip antispam
					elif in_front(set_ip_antispam_str, msg):
						set_value(self, self.ip_antispam_display_id, msg_arr)
					
					else:
						send_str = "Usage: \"!set <feature> on/off \"." 
						whisper(self, user, send_str)
						return		
					#ban emotes
					'''elif in_front(set_ban_emotes_str, msg):
						self.ban_emotes_on = set_value(self, self.ban_emotes_on, "ban emotes", msg_arr)
					
					'''	
					
				elif len(msg_arr) == 5:
					#fake purge antispam
					if in_front(set_fake_purge_antispam_str, msg):
						set_value(self, self.fake_purge_antispam_display_id, msg_arr)
					
					#long message antispam
					elif in_front(set_long_msg_antispam_str, msg):
						set_value(self, self.long_message_antispam_display_id, msg_arr)
					
					#long word antispam
					elif in_front(set_long_word_antispam_str, msg):
						set_value(self, self.long_word_antispam_display_id, msg_arr)
					
					else:
						send_str = "Usage: \"!set <feature> on/off \"." 
						whisper(self, user, send_str)
						return	
				else:
					#usage
					send_str = "Usage: \"!set <feature> on/off \"." 
					whisper(self, user, send_str)
					return
				#just set_str, explain usage.
				if set_str == msg:
					send_str = "Turn features on or off. Usage: \"!set <feature> on/off \"." 
					whisper(self, user, send_str)
					return
			else:
				#not mod
				send_str = "You don't have the correct permissions to use !set commands." 
				whisper(self, user, send_str)
				return
			
		else:
			return False
	
	def vote_parse(self, user, msg, channel_parsed, user_type):
		#voting - all mod commands are !poll, all non-mod are !vote
		vote_str = "!vote"
		poll_str = "!poll"
		poll_start_str = "!poll start"
		poll_options_str = "!poll options"
		poll_reset_str = "!poll reset"
		poll_stats_str = "!poll stats"
		vote_remove_str = "!vote remove"
		poll_end_str = "!poll end"
		poll_close_str = "!poll close"
		
		vote_cmd_arr = ["start", "options", "reset", "stats", "remove", "end", "close"]
		msg_arr = msg.split(" ", 2)

		#save us from going into the loop if the vote is off and the command is not !vote start, done by a mod
		vote_on = get_status(self, self.poll_display_id)
		if in_front(vote_str, msg) and has_level(self, user, channel_parsed, user_type, self.poll_display_id) and not vote_on:
			if not in_front(poll_start_str, msg):
				send_str = "There are no ongoing votes." 
				self.write(send_str)
				return
			
		if in_front(vote_str, msg) or in_front(poll_str, msg):
			if len(msg_arr) >= 2:
				if in_front(poll_start_str, msg):
					if len(msg_arr) >= 3:
						if has_level(self, user, channel_parsed, user_type, self.poll_display_id):
							#reset vote stuffs
							if vote_on:#if already ongoing poll
								send_str = "There is already an ongoing poll." 
							else:
								clear_table(self, self.poll_display_id)
								vote_option_arr = msg_arr[2].split(",")
								for vote_option in vote_option_arr:
									if vote_option in vote_cmd_arr:
										send_str = "You cannot use default vote commands as poll options"
										break
								else:
									if len(vote_option_arr) > 1:
										set_status(self, self.poll_display_id, True)
										send_str = "Poll opened! To vote use !vote <option/index>." 
										for vote_option_index, vote_option in enumerate(vote_option_arr): 
											query = text("INSERT INTO `%s` (`option`, `votes`, `users`) VALUES (:option, 0, '[]')" % self.poll_display_id)
											self.conn.execute(query, option=vote_option.strip())
										self.write(send_str)
										
										vote_table = get_table(self, self.poll_display_id)
										send_str = "Current poll options are: "
										for row_index, row in enumerate(vote_table):
											if row_index != len(vote_table) -1:
												send_str += "(%s.) %s, " % (row_index + 1, row["option"])
											else:
												send_str += "(%s.) %s." % (row_index + 1, row["option"])	
										self.write(send_str)
										return 
									else:
										send_str = "You must specify more than one option for a poll."
						else:
							send_str = "You don't have the correct permissions to start a poll." 
							whisper(self, user, send_str)
							return
					else:
						send_str = "Usage: !poll start <option1, option2, ...>" 
						whisper(self, user, send_str)
						return
				elif in_front(poll_options_str, msg):
					if len(msg_arr) == 2:
						if vote_on:
							send_str = "Current poll options are: "
							for vote_option_index, vote_option in enumerate(vote_option_table):
								if vote_option_index != len(vote_option_table) -1:
									send_str += "(%s.) %s, " % (vote_option_index + 1, vote_option)
								else:
									send_str += "(%s.) %s." % (vote_option_index + 1, vote_option)
						else:
							send_str = "No votes to display."
					else:
						send_str = "Usage !poll options"
						whisper(self, user, send_str)
						return
					if not has_level(self, user, channel_parsed, user_type, self.poll_display_id):
						whisper(self, user, send_str)		
						return
				elif in_front(poll_reset_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.poll_display_id):
						query = text("UPDATE `%s` SET votes = 0, users = '[]'" % self.poll_display_id)
						self.conn.execute(query)
						send_str = "Votes reset."
						self.write(send_str)
						return 
					else:
						send_str = "You don't have the correct permissions to reset the poll votes." 
						whisper(self, user, send_str)
						return
				elif in_front(poll_stats_str, msg):
					if vote_on:
						votes_table = get_table(self, self.poll_display_id)
						vote_total = get_sum(self, self.poll_display_id, "votes")
						print vote_total
						if vote_total != 0:
							send_str = "Current poll stats: "
							for row in votes_table:
								key = row["option"]
								value = row["votes"]
								vote_perc = round((float(value) / vote_total) * 100, 2)
								vote_perc = simplify_num(vote_perc)
								send_str += "%s: %s%% " % (key, vote_perc)
							send_str += "Total votes: %s" % vote_total
							self.write(send_str)
							poll_winner = [['', 0]]
							for row in votes_table:
								key = row["option"]
								value = row["votes"]
								option_perc = (float(poll_winner[0][1])/vote_total * 100)
								option_perc = simplify_num(option_perc)
								if value == poll_winner[0][1]:
									poll_winner.append([key, value])
								elif value > poll_winner[0][1]:
									poll_winner = [[key, value]]
							winner_perc = round(float(poll_winner[0][1])/vote_total * 100, 2)
							winner_perc = simplify_num(winner_perc)
							if len(poll_winner) == 1:
								#1 winner
								if poll_winner[0][1] == 1:
									send_str = "Current poll winner: %s with %s%% majority and %s total vote." % (poll_winner[0][0], winner_perc, poll_winner[0][1])
								else:
									send_str = "Current poll winner: %s with %s%% majority and %s total votes." % (poll_winner[0][0], winner_perc, poll_winner[0][1])
							elif len(poll_winner) >= 2:
								send_str = "Poll is a draw between: " 
								for vote_option in range(len(poll_winner)):
									if vote_option < len(poll_winner)-1:
										send_str += "%s, " % (poll_winner[vote_option][0])
									else:
										#last option in the arr
										if poll_winner[0][1] == 1:
											send_str += " and %s. They each have %s%% of the total vote and %s vote." % (poll_winner[vote_option][0], winner_perc, poll_winner[0][1])
										else:	
											send_str += " and %s. They each have %s%% of the total vote and %s votes." % (poll_winner[vote_option][0], winner_perc, poll_winner[0][1])
								#display current stats
							else:
								#prevent divide by 0 error.
								send_str = "No votes to display." 

						else:
							#prevent divide by 0 error.
							send_str = "No votes to display." 
					else:
						send_str = "There are no ongoing polls." 
						
					if not has_level(self, user, channel_parsed, user_type, self.poll_display_id):
						whisper(self, user, send_str)		
						return
				elif in_front(vote_remove_str, msg):
					votes_table = get_table(self, self.poll_display_id)
					vote_total = get_sum(self, self.poll_display_id, "votes")
					for row_index, row in enumerate(votes_table):
						if user in row["users"]:
							vote_users = json.loads(row["users"])
							vote_users.remove(user)
							vote_users = json.dumps(vote_users)
							#vote_users = votes_table[row_index]["users"].replace(user, '')
							query = text("UPDATE `%s` SET users = :users WHERE `index` = :index" % self.poll_display_id)
							self.conn.execute(query, users=vote_users, index=row["index"])
							query = text("UPDATE `%s` SET votes = votes-1 WHERE `index` = :index" % self.poll_display_id)
							self.conn.execute(query, index=row["index"])
							vote_total -=1
							send_str = "Vote removed."
							whisper(self, user, send_str)
							break
					else:
						send_str = "You have not yet voted for an option."
						whisper(self, user, send_str)
					return						
				elif in_front(poll_end_str, msg) or in_front(poll_close_str, msg):
					#close the vote
					if has_level(self, user, channel_parsed, user_type, self.poll_display_id):
						if vote_on:
							set_status(self, self.poll_display_id, False)
							send_str = "Poll stats: " 
							votes_table = get_table(self, self.poll_display_id)
							vote_total = get_sum(self, self.poll_display_id, "votes")
							if vote_total != 0:
								poll_winner = [['', 0]]
								for row in enumerate(votes_table):
									key = row[1]["option"]
									value = row[1]["votes"]
									option_perc = round(float(value)/vote_total * 100, 2)
									option_perc = simplify_num(option_perc)
									if value == poll_winner[0][1]:
										poll_winner.append([key, value])
									elif value > poll_winner[0][1]:
										poll_winner = [[key, value]]
									send_str += "%s: %s%% " % (key, option_perc)
								send_str += "Total votes: %s" % vote_total
								self.write(send_str)
								winner_perc = round(float(poll_winner[0][1])/vote_total * 100, 2)
								winner_perc = simplify_num(winner_perc)
								if len(poll_winner) == 1:
									#1 winner
									if poll_winner[0][1] == 1:
										send_str = "Poll winner: %s with %s%% majority and %s total vote." % (poll_winner[0][0], winner_perc, poll_winner[0][1])
									else:
										send_str = "Poll winner: %s with %s%% majority and %s total votes." % (poll_winner[0][0], winner_perc, poll_winner[0][1])
								elif len(poll_winner) >= 2:
									send_str = "Poll is a draw between: " 
									for vote_option in range(len(poll_winner)):
										if vote_option < len(poll_winner)-1:
											send_str += "%s, " % (poll_winner[vote_option][0])
										else:
											#last option in the arr
											if poll_winner[0][1] == 1:
												send_str += " and %s. They each had %s%% of the total vote and %s vote." % (poll_winner[vote_option][0], winner_perc, poll_winner[0][1])
											else:	
												send_str += " and %s. They each had %s%% of the total vote and %s votes." % (poll_winner[vote_option][0], winner_perc, poll_winner[0][1])
								else:
									send_str = "No poll winner, this shouldn't happen. Contact me if it does. value_dict: %s, poll_winners: %s" % (value_dict, poll_winner)
							else:
								send_str = "Poll closed with no votes." 
							clear_table(self, self.poll_display_id)	
						else:
							send_str = "There are no ongoing polls."
					else:
						send_str = "You don't have the correct permissions to end a poll." 
						whisper(self, user, send_str)
						return
				else:
					if has_count(self, self.poll_display_id, "option", msg_arr[1].strip()):
						votes_table = get_table(self, self.poll_display_id)
						vote_total = get_sum(self, self.poll_display_id, "votes")
						#msg_arr[1] is a vote option
						#input vote if user hasnt already voted
						for row_index, row in enumerate(votes_table):
							if msg_arr[1] == row["option"]:
								#do nothing if they are already in it, if not then find add them and remove them from the one they used to be in
								#convert row["users"] to list here again
								if user not in row["users"]:
									query = text("UPDATE `%s` SET votes = votes+1 WHERE `index` = :index" % self.poll_display_id)
									self.conn.execute(query, index=row["index"])
									vote_users = json.loads(row["users"])
									vote_users.append(user)
									vote_users = json.dumps(vote_users)
									query = text("UPDATE `%s` SET users = :users WHERE `index` = :index" % self.poll_display_id)
									self.conn.execute(query, users=vote_users, index=votes_table[row_index]["index"])
									vote_total+=1
									#if it's not the option they want and they are in it then remove them
									for old_row_index, old_row in enumerate(votes_table):
										#convert the users to list
										if old_row["option"] != msg_arr[1] and user in old_row["users"]:
											query = text("UPDATE `%s` SET votes = votes-1 WHERE `index` = :index" % self.poll_display_id)
											self.conn.execute(query, index=old_row["index"])
											vote_total-=1
											vote_users = json.loads(votes_table[old_row_index]["users"])
											vote_users.remove(user)
											vote_users = json.dumps(vote_users)
											query = text("UPDATE `%s` SET users = :users WHERE `index` = :index" % self.poll_display_id)
											self.conn.execute(query, users=vote_users, index=votes_table[old_row_index]["index"])
											send_str = "Vote changed."
											whisper(self, user, send_str)
											break
									else:
										send_str = "Vote added."
										whisper(self, user, send_str)
									return
								elif user in row["users"]:
									send_str = "You have already voted for that option"
									whisper(self, user, send_str)
									return#save some time, end this loop if they are already in the option they selected
								break#this actually shouldn't be possible
						else:
							send_str = "Invalid vote option"
							whisper(self, user, send_str)
						return 
							
					elif is_num(msg_arr[1].strip()):
						vote_choice_index = int(msg_arr[1])
						votes_table = get_table(self, self.poll_display_id)
						vote_total = get_sum(self, self.poll_display_id, "votes")
						if vote_choice_index > 0 and vote_choice_index <= len(votes_table):
							for row_index, row in enumerate(votes_table):
								#do nothing if they are already in it, if not then find add them and remove them from the one they used to be in
								if vote_choice_index == row_index+1:
									#convert to list
									if user not in row["users"]:
										query = text("UPDATE `%s` SET votes = votes+1 WHERE `index` = :index" % self.poll_display_id)
										self.conn.execute(query, index=row["index"])
										vote_users = json.loads(votes_table[row_index]["users"])
										vote_users.append(user)
										vote_users = repr(json.dumps(vote_users))
										query = text("UPDATE `%s` SET users = :users WHERE `index` = :index" % self.poll_display_id)
										self.conn.execute(query, users=vote_users, index=votes_table[row_index]["index"])
										vote_total+=1
										#if it's not the option they want and they are in it then remove them
										for old_row_index, old_row in enumerate(votes_table):
											#convert to list(maybe not necessary?)
											if old_row_index != vote_choice_index-1 and user in old_row["users"]:
												vote_users = json.loads(votes_table[row_index]["users"])
												vote_users.remove(user)
												vote_users = repr(json.dumps(vote_users))
												query = text("UPDATE `%s` SET users = :users WHERE `index` = :index" % self.poll_display_id)
												self.conn.execute(query, users=vote_users, index=votes_table[old_row_index]["index"])
												query = text("UPDATE `%s` SET votes = votes-1 WHERE `index` = :index" % self.poll_display_id)
												self.conn.execute(query, index=row["index"])
												send_str = "Vote changed."
												vote_total-=1
												whisper(self, user, send_str)
												break
										else:
											send_str = "Vote added."
											whisper(self, user, send_str)
										return
									elif user in row["users"]:
										send_str = "You have already voted for that option"
										whisper(self, user, send_str)
										return#save some time, end this loop if they are already in the option they selected
									break#also shouldnt be possible
							return 
						else:
							send_str = "Invalid index for vote choice."
							whisper(self, user, send_str)
							return
					else:
						if has_level(self, user, channel_parsed, user_type, self.poll_display_id):
							if in_front(vote_str, msg):
								send_str = "Usage: !vote <option/index>"
							else:
								send_str = "Usage: !poll start/reset/stats/end/close" 
						else:
							send_str = "Usage: !vote <option/index>"
						whisper(self, user, send_str)
						return
				self.write(send_str)
			else:
				if has_level(self, user, channel_parsed, user_type, self.poll_display_id):
					if in_front(vote_str, msg):
						send_str = "Usage: !vote <option/index>"
					else:
						send_str = "Usage: !poll start/reset/stats/end/close" 
				else:
					send_str = "Usage: !vote <option/index>"
				whisper(self, user, send_str)
				return
		elif vote_str == msg:
			send_str = "Usage: !vote <option/index>"
			whisper(self, user, send_str)
			return
		else:
			return False
			
	def raffle_parse(self, user, msg, channel_parsed, user_type):
		#raffle
		raffle_str = "!raffle"
		start_raffle_str = "!raffle start"
		end_raffle_str = "!raffle end"
		
		if in_front(raffle_str, msg):
			if get_status(self, self.raffle_display_id):
				#avoid duplicates
				if raffle_str == msg:
					if not has_count(self, self.raffle_display_id, "user", user):
						insert_data(self, self.raffle_display_id, ["user"], user)
						send_str = "You have been added to the raffle."
					else:
						send_str = "You are already in the raffle."
					whisper(self, user, send_str)
					return
				elif in_front(start_raffle_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.raffle_display_id):
						send_str = "There is already an ongoing raffle." 
					else:
						send_str = "Only mods can start raffles." 
						whisper(self, user, send_str)
						return
					
				elif in_front(end_raffle_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.raffle_display_id):
						raffle_table = get_table(self, self.raffle_display_id)
						if len(raffle_table) > 0:
							winner = raffle_table[random.randint(0, (len(raffle_table) - 1))]["user"]
							point_change(self, winner, self.raffle_point_value)
							if self.lottery_point_value != 1:
								send_str = "%s has won the raffle and obtained %s points!" % (winner, self.raffle_point_value)
							else:
								send_str = "%s has won the raffle and obtained %s point!" % (winner, self.raffle_point_value)
							whisper_str = "You now have %s points in this channel." % point_balance(self, winner)
							whisper(self, winner, whisper_str)
						else:
							send_str = "No one joined the raffle, there is no winner." 
						set_status(self, self.raffle_display_id, False)
						clear_table(self, self.raffle_display_id)
						
					else:
						send_str = "Only mods can end raffles." 
						whisper(self, user, send_str)
						return
				else:
					if has_level(self, user, channel_parsed, user_type, self.raffle_display_id):
						send_str = "Usage: !raffle start/end <point value>"
					else:
						send_str = "Only mods can use !raffle commands"
					whisper(self, user, send_str)
					return
			else:
				if in_front(start_raffle_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.raffle_display_id):
						set_status(self, self.raffle_display_id, True)
						msg_arr = msg.split()
						if len(msg_arr) > 2:
							if is_num(msg_arr[2]):
								self.raffle_point_value = simplify_num(msg_arr[2])
								send_str = "Raffle started with a %s point prize. Join the raffle with \"!raffle\"." % self.raffle_point_value
							else:
								self.raffle_point_value = 0
								send_str = "Invalid raffle prize input, raffle started with prize of 0 points. Join the raffle with \"!raffle\"." 
						else:
							self.raffle_point_value = 0
							send_str = "No raffle prize input, raffle started with prize of 0 points. Join the raffle with \"!raffle\"." 
					else:
						send_str = "Only mods can start raffles." 
						whisper(self, user, send_str)
						return
				elif raffle_str == msg and has_level(self, user, channel_parsed, user_type, self.raffle_display_id):
					send_str = "Usage: !raffle start/end <point value>" 
					whisper(self, user, send_str)
					return
				elif in_front(end_raffle_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.raffle_display_id):
						send_str = "No ongoing raffles."
						self.write(send_str)	
					else:
						send_str = "Only mods can end raffles." 
						whisper(self, user, send_str)
						return
				else:
					send_str = "Usage: !raffle start/end <point value>" 
					whisper(self, user, send_str)
					return
			self.write(send_str)
		else:
			return False
	
	def lottery_parse(self, user, msg, channel_parsed, user_type):
		#lottery
		lottery_str = "!lottery"
		start_lottery_str = "!lottery start"
		end_lottery_str = "!lottery end"
		
		if in_front(lottery_str, msg):
			if get_status(self, self.lottery_display_id):
				if in_front(start_lottery_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.lottery_display_id):
						send_str = "There is already an ongoing lottery." 
					else:
						send_str = "Only mods can start lotteries." 
						whisper(self, user, send_str)
						return
				elif in_front(end_lottery_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.lottery_display_id):
						chatters_json = get_json_chatters(channel_parsed)
						#if chatters_json[self.chatters_display_id]["viewers"]:#should be run in an existing channel so this should always be true
						extend_data(self, self.lottery_display_id, "user", chatters_json["chatters"]["viewers"])
						extend_data(self, self.lottery_display_id, "user", chatters_json["chatters"]["moderators"])
						lottery_table = get_table(self, self.lottery_display_id)
						if len(lottery_table) > 0:
							winner = lottery_table[random.randint(0, (len(lottery_table) - 1))]["user"].encode("utf-8")
							point_change(self, winner, self.lottery_point_value)
							if self.lottery_point_value != 1:
								send_str = "%s has won the lottery and obtained %s points!" % (winner, self.lottery_point_value)
							else:
								send_str = "%s has won the lottery and obtained %s point!" % (winner, self.lottery_point_value)
							whisper_str = "You now have %s points in this channel." % point_balance(self, winner)
							whisper(self, winner, whisper_str)
						else:
							send_str = "No one joined the lottery, there is no winner." 
						set_status(self, self.lottery_display_id, False)
						clear_table(self, self.lottery_display_id)
						
					else:
						send_str = "Only mods can end lotteries." 
						whisper(self, user, send_str)
						return
				else:
					if has_level(self, user, channel_parsed, user_type, self.lottery_display_id):
						send_str = "Usage: !lottery start/end <point value>"
					else:
						send_str = "Only mods can use !lottery commands"
					whisper(self, user, send_str)
					return
				self.write(send_str)
			else:
				if in_front(start_lottery_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.lottery_display_id):
						set_status(self, self.lottery_display_id, True)
						msg_arr = msg.split()
						if len(msg_arr) > 2:
							if is_num(msg_arr[2]):
								self.lottery_point_value = simplify_num(msg_arr[2])
								send_str = "Lottery started with a %s point prize." % self.lottery_point_value
							else:
								self.lottery_point_value = 0
								send_str = "Invalid lottery prize input, lottery started with prize of 0 points." 
						else:
							self.lottery_point_value = 0
							send_str = "No lottery prize input, lottery started with prize of 0 points." 
					else:
						send_str = "Only mods can start lotteries." 
						whisper(self, user, send_str)
						return
					self.write(send_str)
				elif lottery_str == msg and has_level(self, user, channel_parsed, user_type, self.lottery_display_id):
					send_str = "Usage: !lottery start/end <point value>" 
					whisper(self, user, send_str)
					return
				elif in_front(end_lottery_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.lottery_display_id):
						send_str = "No ongoing lotteries."
						self.write(send_str)	
					else:
						send_str = "Only mods can end lotteries." 
						whisper(self, user, send_str)
						return
				else:
					send_str = "Usage: !lottery start/end <point value>" 
					whisper(self, user, send_str)
					return
		else:
			return False
			
	def roulette_parse(self, user, msg, channel_parsed, user_type):
		#roulette
		#if user is mod then say it doesnt kill you or something
		#should absolutely just make the chance input in the GUI rather than text based.
		rol_str = "!roulette"
		rol_chance_str = "!roulette chance"
		
		if get_status(self, self.roulette_display_id):
			if in_front(rol_str, msg):
				if rol_str == msg:
					#trigger roulette - allow custom messages for win/loss to replace default ones
					possessive_user = possessive_prettify(user)
					send_str = "/me places the revolver to %s head" % (possessive_user)
					self.write(send_str)
					time.sleep(1)
					if random.random() < self.rol_chance:
						#time out the user(ban from chat) for rol_timeout amount of seconds
						if has_level(self, user, channel_parsed, user_type, self.raffle_display_id) == False:
							timeout(user, self, self.rol_timeout)
							send_str = "The trigger is pulled, and the revolver fires! %s lies dead in chat" % (user)
						else:
							send_str = "The gun jams thanks to %s super mod powers. %s lives!" % (possessive_user, user)
					else:
						#do nothing, notify of victory
						send_str = "The trigger is pulled, and the revolver clicks. %s has lived to survive roulette!" % (user)
					self.write(send_str)
				elif in_front(rol_chance_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.raffle_display_id):
						#get the new chance for ban in roulette
						msg_arr = msg.split(" ")
						if len(msg_arr) > 2:
							#percentage is input as chance, *.01 to change to decimal
							input_perc = msg_arr[2]
							if is_num(input_perc) == True:
								input_perc = simplify_num(input_perc)
							if input_perc > 100 or input_perc < 0 or is_num(input_perc) == False:
								send_str = "Please input a percentage chance for roulette to be triggered, i.e. \"!roulette chance 50\". Chance must be between 0 and 100." 
							else:
								self.rol_chance = input_perc * .01
								input_perc = check_int(input_perc)
								send_str = "Roulette chance successfully changed to %s%%" % (input_perc)
						else:
							send_str = "Usage: !roulette chance <percent chance>" 
							whisper(self, user, send_str)
							return
					else:
						send_str = "Only mods can change the chance of the roulette." 
						whisper(self, user, send_str)
						return
					self.write(send_str)
				else:
					if has_level(self, user, channel_parsed, user_type, self.raffle_display_id):
						send_str = "Usage: !roulette chance <percent chance>" 
					else:
						send_str = "You don't have the correct permissions to use \"!lottery\" commands."
					whisper(self, user, send_str)
					return
			else:
				return False
	
	def ball_parse(self, user, msg, channel_parsed, user_type):
		#8ball
		#adding in deleting/adding/clearing of values
		ball_str = "!8ball"
		ball_add_str = "!8ball add"
		ball_del_str = "!8ball delete"
		ball_rem_str = "!8ball remove"
		ball_list_str = "!8ball list"
		ball_clr_str = "!8ball clear"
		
		#move this up a level when we allow editing of these values		
		if get_status(self, self.ball_display_id):
			if in_front(ball_str, msg):
				msg_arr = msg.split(" ", 2)
				if in_front(ball_add_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.ball_display_id):
						if len(msg_arr) > 2:#need to have this if statement more often
							ball_response = msg_arr[2]
							if not has_count(self, self.ball_display_id, "responses", ball_response):
								insert_data(self, self.ball_display_id, ["responses"], ball_response)
								send_str = "\"%s\" added to list of 8ball responses." % (ball_response)
							else:
								send_str = "%s is already an 8ball response." % (ball_response)
						else:
							send_str = "Usage: \"!8ball add <8ball response>\"" 
						self.write(send_str)
					else:
						send_str = "You don't have the correct permissions to use \"!8ball add\"."
						whisper(self, user, send_str)
					return
				elif in_front(ball_del_str, msg) or in_front(ball_rem_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.ball_display_id):
						if len(msg_arr) > 2:
							ball_response = msg_arr[2]
							if is_num(ball_response):
								#we add on one to the actual index because users prefer to start with 1, rather than 0.
								ball_response = int(ball_response)
								delete_status = delete_index_handler(self, self.ball_display_id, ball_response)
								if delete_status:
									send_str = "8Ball response \"%s\" removed at index %s." % (delete_status["responses"], ball_response)
								else:
									send_str = "Invalid index for 8ball response removal." 
							else:
								delete_status = delete_value_handler(self, self.ball_display_id, "responses", ball_response)
								if delete_status:
									send_str = "8Ball response \"%s\" removed." % (delete_status["responses"])									
								else:
									send_str = "Specified 8ball response does not exist." 
						else:
							send_str = "Usage: \"!8ball delete/remove <8ball response/index>\"" 
						self.write(send_str)
					else:
						send_str = "You don't have the correct permissions to use \"!8ball delete/remove\"."
						whisper(self, user, send_str)
					return
				elif in_front(ball_list_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.ball_display_id):
						ball_table = get_table(self, self.ball_display_id)
						if len(ball_table) > 0:
							send_str = "Current 8ball responses: " 
							for row_index, row in enumerate(ball_table):
								if (row_index != len(ball_table) -1):
									#if not last response in arr
									send_str += "(%s.) %s, " % (row_index+1, row["responses"])
								else:
									send_str += "(%s.) %s." % (row_index+1, row["responses"])
								#this accounts for any messages longer than the character cap
								
							self.write(send_str)
						else:
							send_str = "There are currently no 8ball responses." 
							whisper(self, user, send_str)
							return
					else:
						send_str = "You don't have the correct permissions to use \"!8ball clear\"."
						whisper(self, user, send_str)
					return
				elif ball_clr_str == msg:
					if has_level(self, user, channel_parsed, user_type, self.ball_display_id): 
						clear_table(self, self.ball_display_id)
						send_str = "All 8ball responses removed." 
						self.write(send_str)
					else:
						send_str = "You don't have the correct permissions to use \"!8ball clear\"."
						whisper(self, user, send_str)
						return
					return
				elif ball_str == msg:
					if has_level(self, user, channel_parsed, user_type, self.ball_display_id):
						send_str = "Usage: \"!8ball add/delete/remove/list/clear/<question>\"" 
						whisper(self, user, send_str)
					else:
						send_str = "You don't have the correct permissions to use \"!8ball clear\"."
						whisper(self, user, send_str)
					return
						
				else:#so we don't respond when using the 8ball commands
					if "?" in msg: #and msg.rstrip().endswith("?") <-- is this better?
						msg_arr = msg.split(" ", 1)
						if len(msg_arr) == 2:
							ball_table = get_table(self, self.ball_display_id)
							if len(ball_table) > 0:
								response_index = random.randint(0, len(ball_table)-1)
								response = ball_table[response_index]["responses"]
								send_str = "Magic 8 ball says... %s" % (response)
							else:
								send_str = "There are currently no 8ball responses." 
								whisper(self, user, send_str)
								return
						elif ball_str == msg:
							send_str = "Get the Magic 8 Ball to answer your question. Usage: \"!8ball <question> \"."
							whisper(self, user, send_str)
							return
						else:
							send_str = "Usage: \"!8ball <question>? \"." 
							whisper(self, user, send_str)
							return
					else:
						send_str = "Usage: \"!8ball <question>? \"." 
						whisper(self, user, send_str)
						return
					self.write(send_str)
			else:
				return False
		else:
			return False
	
	def uptime_parse(self, user, msg, channel_parsed, user_type):
		#uptime - leaving this to print to everyone for now
		uptime_str = "!uptime"
		if in_front(uptime_str, msg):
			msg_arr = msg.split(" ")
			if len(msg_arr) == 1:
				uptime = get_uptime_str(self.channel_parsed)
				if uptime:
					send_str = "@%s has been live for: %s" % (self.channel_parsed, uptime)
				else:
					send_str = "@%s is currently offline." % self.channel_parsed

			elif len(msg_arr) > 1:
				uptime = get_uptime_str(msg_arr[1])
				if uptime:
					send_str = "%s has been live for: %s" % (msg_arr[1], get_uptime_str(msg_arr[1]))
				else:
					send_str = "%s is not an active channel." % msg_arr[1]
			if get_status(self, self.uptime_display_id) and has_level(self, user, channel_parsed, user_type, self.uptime_display_id):
				self.write(send_str)
			else:
				whisper(self, user, send_str)
		else:
			return False
	
	def general_channel_stats_parse(self, user, msg, channel_parsed, user_type, stat_str):
		find_stat_str = "!" + stat_str
		if in_front(find_stat_str, msg):
			msg_arr = msg.split()
			if len(msg_arr) == 1:
				if stat_str == self.chatters_display_id:
					stat_data = get_json_chatters(channel_parsed.lower().strip())
					stat_count = stat_data["chatter_count"]
					send_str = "There are currently %s accounts in chat." % (stat_count)
				elif stat_str == self.viewers_display_id:
					stat_data = get_json_stream(channel_parsed.lower().strip())
					stat_count = stat_data["streams"]
					if stat_count:
						stat_count = stat_count[0]["viewers"]
						send_str = "There are currently %s viewers in the channel." % (stat_count)
					else:
						send_str = "This channel is currently offline."
				elif stat_str == self.views_display_id:
					stat_data = get_json_views_follows(channel_parsed.lower().strip())
					stat_count = stat_data["views"]
					send_str = "This channel has %s views." % (stat_count)
				elif stat_str == self.followers_display_id:
					stat_data = get_json_views_follows(channel_parsed.lower().strip())
					stat_count = stat_data["followers"]
					send_str = "This channel has %s followers." % (stat_count)
			elif len(msg_arr) > 1:
				stat_channel = msg_arr[1]
				
				if stat_str == self.chatters_display_id:
					stat_data = get_json_chatters(stat_channel.lower().strip())
					stat_count = stat_data["chatter_count"]
				elif stat_str == self.viewers_display_id:
					stat_data = get_json_stream(stat_channel.lower().strip())
					stat_count = stat_data["streams"]
				elif stat_str == self.views_display_id:
					stat_data = get_json_views_follows(stat_channel.lower().strip())
					stat_count = stat_data["views"]
				elif stat_str == self.followers_display_id:
					stat_data = get_json_views_follows(stat_channel.lower().strip())
					stat_count = stat_data["followers"]
					
				if stat_count:
					if stat_str == self.viewers_display_id:
						stat_count = stat_data[0]["viewers"]
						
					stat_count = prettify_num(stat_count)
					if stat_channel.rstrip().endswith("s"):
						stat_channel = stat_channel + "'"
					else:	
						stat_channel = stat_channel + "'s"
				
					if stat_str == self.chatters_display_id:
						send_str = "There are currently %s accounts in %s chat." % (stat_count, stat_channel)
					elif stat_str == self.viewers_display_id:
						send_str = "There are currently %s viewers in %s channel." % (stat_count, stat_channel)
					elif stat_str == self.views_display_id:
						send_str = "There are currently %s views in %s channel." % (stat_count, stat_channel)
					elif stat_str == self.followers_display_id:
						send_str = "%s channel has %s followers." % (stat_channel.capitalize(), stat_count)
				else:
					send_str = "%s is not an active channel." % msg_arr[1]
			else:
				send_str = "Usage: \"%s <channel>\"" % find_stat_str
				
			if get_status(self, stat_str) and has_level(self, user, channel_parsed, user_type, stat_str):
				self.write(send_str)
			else:	
				whisper(self, user, send_str)
		else:
			return False
	
	def channel_stats_parse(self, user, msg, channel_parsed, user_type):
		chan_stats_str = "!chanstats"
		if get_status(self, self.ball_display_id):
			if in_front(chan_stats_str, msg):
				msg_arr = msg.split(" ")
				if len(msg_arr) == 1:
					stat_data = get_json_stream(channel_parsed.lower().strip())
					stat_data= stat_data["streams"]
					if stat_data:
						game = result_to_dict(self.conn.execute("SELECT `game` FROM game LIMIT 1"))
						if game != '':
							send_str = "%s is playing %s for %s viewers." % (channel_parsed.capitalize(), game, stat_data[0]["viewers"])
						else:
							send_str = "%s is not playing a game, however there are %s viewers" % (channel_parsed.capitalize(), stat_data[0]["viewers"])
					else:
						send_str = "%s is currently offline." % channel_parsed.capitalize()
					if not has_level(self, user, channel_parsed, user_type, self.chanstats_display_id):
						whisper(self, user, send_str)
						return
						
				elif len(msg_arr) > 1:
					stat_data = get_json_stream(msg_arr[1].lower().strip())
					stat_data = stat_data["streams"]
					if stat_data:
						channel_game = stat_data[0]["game"]
						if channel_game:
							send_str = "%s is playing %s for %s viewers." % (msg_arr[1].capitalize(), channel_game, stat_data[0]["viewers"])
						else:
							send_str = "%s is not playing a game, however there are %s viewers" % (msg_arr[1].capitalize(), stat_data[0]["viewers"])
					else:
						send_str = "%s is not an active channel." % msg_arr[1].capitalize()
				else:
					send_str = "Usage: !chanstats <channel>"
					whisper(self, user, send_str)
					return
				if get_status(self, self.chanstats_display_id) and has_level(self, user, channel_parsed, user_type, self.chanstats_display_id):
					self.write(send_str)
				else:
					whisper(self, user, send_str)
			else:
				return False
		else:
			return False
			
	def subs_parse(self, user, msg, channel_parsed, user_type):
		#subscribers
		subscribers_str = "!subscribers"
		subs_str = "!subs"	
		if in_front(subs_str, msg) or in_front(subscribers_str, msg):
			msg_arr = msg.split()
			if len(msg_arr) == 1:
				sub_data = get_json_subs(channel_parsed.lower())
				sub_count = sub_data["_total"]
				send_str = "This channel has %s subs." % (sub_count)
			elif len(msg_arr) > 1:
				sub_channel = msg_arr[1]
				sub_data = get_json_subs(sub_channel.lower())
				sub_count = sub_data["_total"]
				if sub_count:
					sub_count = prettify_num(sub_count)
					if sub_channel.rstrip().endswith("s"):
						send_str = "%s' channel has %s subs." % (sub_channel, sub_count)
					else:
						send_str = "%s's channel has %s subs." % (sub_channel, sub_count)
				else:
					send_str = "%s does not currently allow tecsbot access." % sub_channel
			else:
				send_str = "Usage: \"!subs/!subscribers <channel>\""
				
			if get_status(self, self.subcribers_display_id) and has_level(self, user, channel_parsed, user_type, self.subcribers_display_id):
				self.write(send_str)
			else:	
				whisper(self, user, send_str)
		else:
			return False
			
	def commercial_parse(self, user, msg, channel_parsed, user_type):
		#commercials
		comm_str = "!commercial"
		if comm_str == msg:
			if get_status(self, self.commercial_display_id):
				if has_level(self, user, channel_parsed, user_type, self.commercial_display_id):
					msg_arr = msg.split(" ")
					if len(msg_arr) == 1:
						#start default length commercial
						comm_len = 30
						start_commercial(comm_len, self.channel_parsed)
						send_str = "%s commercial started." % (parse_sec_condensed(comm_len))
					elif len(msg_arr) == 2:
						comm_len = msg_arr[1]
						if is_num(comm_len):
							if comm_len in comm_len_arr:
								start_commercial(comm_len, self.channel_parsed)
								send_str = "%s commercial started." % (parse_sec_condensed(comm_len))
						else:
							#display usage
							send_str = "Usage: !commercial <length of commercial>"
							whisper(self, user, send_str)
							return
					else:
						#display usage
						send_str = "Usage: !commercial <length of commercial>"
						whisper(self, user, send_str)
						return
				else:
					#not mod
					send_str = "You don't have the correct permissions to start commercials." 
					whisper(self, user, send_str)
					return
				self.write(send_str)
			else:
				return False
		else:
			return False

	def repeat_parse(self, user, msg, channel_parsed, user_type):
		#repeat commands
		#can easily be mod commands by just inputting /ban, /timeout, etc
		#need to put all commands in an array so that we can do !random command 
		#!repeat add <command> interval
		#concatenate all commands after [1] and before [len(arr)-1]
		repeat_str = "!repeat"
		repeat_add_str = "!repeat add"
		repeat_del_str = "!repeat delete"
		repeat_rem_str = "!repeat remove"
		repeat_list_str = "!repeat list"
		repeat_clr_str = "!repeat clear"
		
		if get_status(self, self.repeat_display_id):
			if in_front(repeat_str, msg):
				if in_front(repeat_add_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.repeat_display_id):
						msg_arr = msg.split(" ")
						if len(msg_arr) > 3:
							del msg_arr[0:2]#remove command specifiers
							repeat_cmd = ''
							for cmd_part in range(len(msg_arr)):
								if cmd_part == len(msg_arr)-2 and is_num(msg_arr[cmd_part]) and msg_arr[cmd_part+1] in self.time_unit_arr:#if unit of time specified
									repeat_cmd = repeat_cmd.rstrip()
									repeat_interval = simplify_num(msg_arr[cmd_part])
									interval_unit = msg_arr[cmd_part+1]
									repeat_interval = convert_to_sec(repeat_interval, interval_unit, self)
									break
								elif cmd_part == len(msg_arr)-1:#if no unit of time specified, seconds
									repeat_cmd = repeat_cmd.rstrip()#get rid of trailing space
									repeat_interval = msg_arr[cmd_part]
								else:
									repeat_cmd += msg_arr[cmd_part] + " "
							if not disconnect_cmd(repeat_cmd):
								current_time = time.time()
								#repeat_set = [current_time, repeat_cmd, repeat_interval]
								#add the new set to the database
								query = text("INSERT INTO `%s` (`set_time`, `phrase`, `interval`) VALUES (:time, :command, :interval)" % self.repeat_display_id)
								self.conn.execute(query, time=current_time, command=repeat_cmd, interval=repeat_interval)
								send_str = "Repeat command \"%s\" added with interval %s." % (repeat_cmd, parse_sec_condensed(repeat_interval))
							else:
								send_str = "No \".disconnect\" or \"/disconnect\" variants allowed."
						else:
							send_str = "Usage: !repeat add <command> <interval>" 
							whisper(self, user, send_str)
							return
					else:
						send_str = "You don't have the correct permissions to use \"!repeat add\"." 
						whisper(self, user, send_str)
						return
				elif in_front(repeat_del_str, msg) or in_front(repeat_rem_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.repeat_display_id):
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) > 2:
							repeat_cmd = msg_arr[2]
							if is_num(repeat_cmd):
								repeat_cmd = int(repeat_cmd)
								delete_status = delete_index_handler(self, self.repeat_display_id, repeat_cmd)
								if delete_status:
									send_str = "Repeat command \"%s\" with interval %s removed at index %s." % (delete_status["phrase"], parse_sec_condensed(delete_status["interval"]), repeat_cmd)
									#return the row that was deleted if 
								else:
									send_str = "Invalid index for repeat command removal." 
							else:
								delete_status = delete_value_handler(self, self.repeat_display_id, "phrase", repeat_cmd)
								if delete_status:
									send_str = "Repeat command \"%s\" with interval %s removed." % (repeat_cmd, parse_sec_condensed(delete_status["interval"]))		
								else:
									send_str = "Specified repeat command does not exist." 
						else:
							send_str = "Usage: !repeat delete/remove <command/index>" 
							whisper(self, user, send_str)
							return
					else:
						send_str = "You don't have the correct permissions to use \"!repeat delete/remove\"." 
						whisper(self, user, send_str)
						return
				elif repeat_list_str == msg:
					repeats_table = get_table(self, self.repeat_display_id)
					if len(repeats_table) == 0:
						send_str = "No active repeat commands." 
					else:
						send_str = "Active repeat commands: " 
						for row_index, row in enumerate(repeats_table):
							if (row_index != len(repeats_table)-1):
								#every element but last one
								send_str += "(%s.) %s: %s, " % (row_index+1, row["phrase"], parse_sec_condensed(row["interval"]))
							else:
								#last element in arr
								send_str += "(%s.) %s: %s." % (row_index+1, row["phrase"], parse_sec_condensed(row["interval"]))
					if not has_level(self, user, channel_parsed, user_type, self.repeat_display_id):
						whisper(self, user, send_str)		
						return			
				elif repeat_clr_str == msg:
					if has_level(self, user, channel_parsed, user_type, self.repeat_display_id): 
						clear_table(self, self.repeat_display_id)
						send_str = "All repeat commands removed." 
					else:
						send_str = "You don't have the correct permissions to use \"!repeat clear\"." 
						whisper(self, user, send_str)
						return
				elif repeat_str == msg:
					send_str = "Add or remove commands to be repeated every specified interval. Syntax and more information can be found in the documentation." 
					whisper(self, user, send_str)
					return
				else:
					if has_level(self, user, channel_parsed, user_type, self.repeat_display_id):
						send_str = "Usage: !repeat add/delete/remove/list/clear <command> <interval>" 
					else:
						send_str = "Usage: !repeat list" 
					whisper(self, user, send_str)
					return
				self.write(send_str)
				return
			else:
				return False
	
	def custom_command_parse(self, user, msg, channel_parsed, user_type):
		#custom commands
		cmd_str = "!command"
		cmd_add_str = "!command add"
		cmd_del_str = "!command delete"
		cmd_rem_str = "!command remove"
		cmd_list_str = "!command list"
		cmd_clr_str = "!command clear"
		cmd_on = get_status(self, self.command_display_id)
		if cmd_on:
			if in_front(cmd_str, msg):
				#add commands
				if in_front(cmd_add_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.command_display_id):
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) >= 3:
							if ":" in msg_arr[2] and in_front("!", msg_arr[2]):
								cmd_msg_arr = msg_arr[2].split(":", 1)
								if len(cmd_msg_arr) == 2:
									cmd_phrase = cmd_msg_arr[0].rstrip().lstrip()
									cmd_reply = cmd_msg_arr[1].rstrip().lstrip()
									if is_num(cmd_reply[-1:]):
										cmd_level = cmd_reply[-1:]#get level
										cmd_reply = cmd_reply[:-1]#everything but last letter
									else:
										cmd_level = False

									if cmd_level:
										if not check_int(cmd_level):
											send_str = "Level requirement must be an integer." 
											whisper(self, user, send_str)
											return	
										else:
											#valid level input
											cmd_level = int(cmd_level)
											if cmd_level < 1 or cmd_level > 4:
												send_str = "Level requirement must be between 1 and 4." 
												whisper(self, user, send_str)
												return	
											if cmd_phrase in self.default_cmd_arr:#dont add something that is already a default command
												send_str = "%s is already a default command." % (cmd_phrase)
											else:
												query = text("SELECT COUNT(*) FROM `%s` WHERE `command` = :command AND `reply` = :reply" % (self.command_display_id))
												if result_to_dict(self.conn.execute(query, command=cmd_phrase, reply=cmd_reply))[0]["COUNT(*)"] > 0:
													send_str = "%s is already a custom command." % (cmd_phrase)
												else:
													if not disconnect_cmd(cmd_reply):
														query = text("INSERT INTO `%s` (`command`, `reply`, `level`) VALUES (:phrase, :reply, %d)" % (self.command_display_id, cmd_level))
														self.conn.execute(query, phrase=cmd_phrase, reply=cmd_reply)
														send_str = "Command \"%s\" added, with reply \"%s\" and level requirement %d." % (cmd_phrase, cmd_reply, cmd_level)
													else:
														send_str = "No \".disconnect\" or \"/disconnect\" variants allowed."
									else:
										if cmd_phrase in self.default_cmd_arr:#dont add something that is already a default command
											send_str = "%s is already a default command." % (cmd_phrase)
										else:
											query = text("SELECT COUNT(*) FROM `%s` WHERE `command` = :command AND `reply` = :reply" % (self.command_display_id))
											if result_to_dict(self.conn.execute(query, command=cmd_phrase, reply=cmd_reply))[0]["COUNT(*)"] > 0:
												send_str = "%s is already a custom command." % (cmd_phrase)
											else:
												if not disconnect_cmd(cmd_reply):
													query = text("INSERT INTO `%s` (`command`, `reply`, `level`) VALUES (:phrase, :reply, %d)" % (self.command_display_id, 3))#default to mods 
													self.conn.execute(query, phrase=cmd_phrase, reply=cmd_reply)
													send_str = "Command \"%s\" added, with reply \"%s\"." % (cmd_phrase, cmd_reply)
												else:
													send_str = "No \".disconnect\" or \"/disconnect\" variants allowed."
								else:
									#incorrectly formatted, display usage
									send_str = "Usage: \"!command add !<command>:<reply> <level>\"." 
									whisper(self, user, send_str)
									return	
							else:
								#incorrectly formatted, display usage
								send_str = "Usage: \"!command add !<command>:<reply> <level>\"." 
								whisper(self, user, send_str)
								return
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!command add !<command>:<reply> <level>\"."
							whisper(self, user, send_str)
							return
					else:
						send_str = "You don't have the correct permissions to use \"!command add\"." 
						whisper(self, user, send_str)
						return
				#delete commands
				elif in_front(cmd_del_str, msg) or in_front(cmd_rem_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.command_display_id):
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) == 3:
							cmd_phrase = msg_arr[2]
							if is_num(cmd_phrase):
								cmd_phrase = int(cmd_phrase)
								delete_status = delete_index_handler(self, self.command_display_id, cmd_phrase)
								if delete_status:
									send_str = "Command %s:%s removed at index %s." % (delete_status["command"], delete_status["reply"], cmd_phrase)
								else:
									send_str = "Invalid index for command removal." 
							
							else:
								delete_status = delete_value_handler(self, self.command_display_id, "command", cmd_phrase)
								if delete_status:
									send_str = "Command %s:%s removed." % (delete_status["command"], delete_status["reply"])	
								else:
									send_str = "Specified command does not exist." 
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!command delete/remove <command/index>\"." 
					else:
						send_str = "You don't have the correct permissions to use \"!command delete/remove\"." 
						whisper(self, user, send_str)
						return
				#list commands
				elif cmd_list_str == msg:
					#check to make sure there are commands to list
					cmd_table = get_table(self, self.command_display_id)
					if len(cmd_table) == 0:
						send_str = "No active commands." 
					else:
						send_str = "Active commands: " 
						for row_index, row in enumerate(cmd_table):
							if (row_index != len(cmd_table)-1):
								#every element but last one
								send_str += "(%s.) %s: %s, " % (row_index+1, row["command"], row["reply"])
							else:
								#last element in arr
								send_str += "(%s.) %s: %s." % (row_index+1, row["command"], row["reply"])
							
					if not has_level(self, user, channel_parsed, user_type, self.command_display_id):
						whisper(self, user, send_str)		
						return
				#clear commands
				elif cmd_clr_str == msg:
					if has_level(self, user, channel_parsed, user_type, self.command_display_id):
						clear_table(self, self.command_display_id)
						send_str = "All custom commands removed." 
					else:
						send_str = "You don't have the correct permissions to use \"!command clear\"." 
						whisper(self, user, send_str)
						return
				#just cmd string, display usage
				elif cmd_str == msg:
					send_str = "Add or remove custom commands. Syntax and more information can be found in the documentation." 
					whisper(self, user, send_str)
					return
				else:
					if has_level(self, user, channel_parsed, user_type, self.command_display_id):
						send_str = "Usage: !command add/delete/remove/list/clear" 
					else:
						send_str = "Usage: !command list." 
					whisper(self, user, send_str)
					return
				self.write(send_str)
			else:	
				################################################################################
				####THIS NEEDS TO NOT BE IS MOD BUT DEPEND ON THE LEVEL PARAMETER OF THE COMMAND
				################################################################################
				if cmd_on:
					cmd_table = get_table(self, self.command_display_id)
					for row in cmd_table:
						try:
							cmd_index = msg.index(row["command"])
							#if msg did contain the custom command
							reply = row["reply"]
							level = row["level"]
							user_level = get_user_level(self, user, channel_parsed, user_type)
							if user_level <= level:
								for word in reply.split():
									if word in self.reply_args_arr:
										if word == "{*USER*}":
											reply = reply.replace("{*USER*}", user)
										elif word == "{*TO_USER*}":
											to_user_part = msg[cmd_index+len(row["command"]):len(msg)]#all the elements after the autoreply
											reply_to_user = to_user_part.split()[0]#the first word after the autoreply, should be the to user
											reply = reply.replace("{*TO_USER*}", str(reply_to_user))
										elif word == "{*GAME*}":
											game = result_to_dict(self.conn.execute("SELECT `game` FROM game LIMIT 1"))
											reply = reply.replace("{*GAME*}", game)
										elif word == "{*STATUS*}":
											title = result_to_dict(self.conn.execute("SELECT `title` FROM title LIMIT 1"))
											reply = reply.replace("{*STATUS*}", title)
										elif word == "{*TOPIC*}":
											topic = result_to_dict(self.conn.execute("SELECT `topic` FROM topic LIMIT 1"))
											reply = reply.replace("{*TOPIC*}", topic)
										elif word == "{*VIEWERS*}":
											viewer_count = get_raw_general_stats(channel_parsed, 'viewers')
											reply = reply.replace("{*VIEWERS*}", str(viewer_count))
										elif word == "{*CHATTERS*}":
											chatter_count = get_raw_general_stats(channel_parsed, 'chatters')
											reply = reply.replace("{*CHATTERS*}", str(chatter_count))
										elif word == "{*VIEWS*}":
											view_count = get_raw_general_stats(channel_parsed, 'views')
											reply = reply.replace("{*VIEWS*}", str(view_count))
										elif word == "{*FOLLOWERS*}":
											follower_count = get_raw_general_stats(channel_parsed, 'followers')
											reply = reply.replace("{*FOLLOWERS*}", str(follower_count))
								'''else:
									send_str = "You don't have the correct permissions to use this custom command." 
									whisper(self, user, send_str)
									return'''
								if in_front("/w", reply) or in_front(".w", reply):
									whisper_response(reply)
								else:
									self.write(reply)
								return False
						except:
							#msg did not contain the autoreply
							pass
				return False
		else:
			return False
	
	def stats_parse(self, user, msg, channel_parsed, user_type):
		stats_str = "!stats"
		
		if in_front(stats_str, msg):
			msg_arr = msg.split(" ", 2)
			if len(msg_arr) == 2:
				#!stats <word/phrase>
				if self.stream_status:
					word = msg_arr[1]
					word_count = get_word_count(word, channel_parsed)
					minute = get_uptime_min(stats_channel)
					word_per_min = round((word_count / minute), 2)
					stats_channel = possessive_prettify(stats_channel)
					send_str = "Total times %s has been sent in this channel: %s. Per minute: %s." % (word, stats_channel, prettify_num(word_count), simplify_num(word_per_min))
				else:
					send_str = "This channel is currently offline."
					whisper(self, user, send_str)
					return
				
			elif len(msg_arr) > 2:
				#!stats <channel>/global <word>
				stats_channel = msg_arr[1].strip()
				word = msg_arr[2]
				if stats_channel != "global":
					if stats_channel == channel_parsed:
						if self.stream_status:
							word_count = get_word_count(word, channel_parsed)
							minute = get_uptime_min(stats_channel)
							word_per_min = round((word_count / minute), 2)
							stats_channel = possessive_prettify(stats_channel)
							send_str = "Total times %s has been sent in this channel: %s. Per minute: %s." % (word, stats_channel, prettify_num(word_count), simplify_num(word_per_min))
						else:
							send_str = "This channel is currently offline."
							whisper(self, user, send_str)
							return
					else:
						channel_data = get_json_stream(stats_channel)["streams"]
						if channel_data:
							word_count = get_word_count(word, stats_channel)
							minute = get_uptime_min(stats_channel)
							word_per_min = round((word_count / minute), 2)
							stats_channel = possessive_prettify(stats_channel)
							send_str = "Total times %s has been sent in %s channel: %s. Per minute: %s." % (word, stats_channel, prettify_num(word_count), simplify_num(word_per_min))
						else:
							send_str = "That channel is currently offline."
							whisper(self, user, send_str)
							return
				else:
					word_count_global = get_word_count_global(word)
					send_str = "Total times %s has been sent in all channels: %s." % (word, prettify_num(word_count_global))
			else:
				send_str = "Usage: !stats <channel>/global <word/phrase>" 
				whisper(self, user, send_str)
				return
			if get_status(self, self.stats_display_id) and has_level(self, user, channel_parsed, user_type, self.stats_display_id):
				self.write(send_str)
			else:
				whisper(self, user, send_str)
			return
		else:
			return False
	
	def mods_parse(self, user, msg, channel_parsed, user_type):
		mods_str = "!mods" 
		moderators_str = "!moderators"
		
		if in_front(mods_str, msg) or in_front(moderators_str, msg):
			if get_status(self, self.moderators_display_id) and has_level(self, user, channel_parsed, user_type, self.moderators_display_id):
				self.write("/mods")
			else:
				whisper(self, user, "/mods")
			return
			
		else:
			return False
	
	def repeat_check(self):
		#perhaps this would be better: https://twistedmatrix.com/documents/10.1.0/core/howto/time.html, for now using LoopingCalls
		
		if get_status(self, self.repeat_display_id):
			current_time = time.time()
			query = "SELECT * FROM `repeat` WHERE (%d - set_time > `interval`)" % current_time
			result = self.conn.execute(query)
			for repeat_row in result:
				query = "UPDATE `repeat` SET set_time=%d WHERE `index`=%s" % (current_time, repeat_row[0])
				self.conn.execute(query)
				#have to ahve this for some reason idk whhy it breaks without it
				try:
					self.write(repeat_row[2])
				except:
					pass
	
	def countdown_check(self):
		if get_status(self, self.countdown_display_id):
			current_time = time.time()
			query = "SELECT * FROM countdown WHERE (%d - set_time > `duration` )" % current_time
			result = self.conn.execute(query)
			for countdown_row in result:
				#have to ahve this for some reason idk whhy it breaks without it
				query = text("DELETE FROM countdown WHERE `index` = :index")
				self.conn.execute(query, index=countdown_row["index"])
				try:
					self.write(countdown_row["command"])
				except:
					pass
									
	def follower_check(self):
		self.follower_arr, new_follower_arr = get_new_followers(self.follower_arr, self.channel_parsed, self)
		if len(new_follower_arr) > 0:
			send_str = "Thanks for following "
			if len(new_follower_arr) == 1:
				send_str += "%s!" % new_follower_arr[0]
			elif len(new_follower_arr) == 2:
				send_str += "%s and %s!" % (new_follower_arr[0], new_follower_arr[1])
			else:
				for new_follower_index, new_follower in enumerate(new_follower_arr):
					if new_follower_index != len(new_follower_arr)-1:
						send_str += "%s, " % new_follower
					else:
						send_str += "and %s!" % new_follower
			try:
				self.write(send_str.encode("utf-8"))
			except:
				pass
	
	def stream_status_check(self):
		channel_json = get_json_stream(self.channel_parsed)
		while True:
			try:
				stream_status = channel_json["streams"]
				if stream_status == []:
					self.viewer_arr = []
					self.lurker_arr = []
					self.stream_status = False
					clear_chat_log(self.channel_parsed)
					return
				else:
					self.stream_status = True
					return
			except:
				pass
				
	def title_parse(self, user, msg, channel_parsed, user_type):
		title_str = "!title"
		status_str = "!status"
		
		msg_arr = msg.split(" ", 1)
		if in_front(title_str, msg) or in_front(status_str, msg):
			if len(msg_arr) > 1:
				if is_streamer(user, channel_parsed):
					title = msg_arr[1]
					update_data(self, self.title_display_id, ["title"], title)
					send_str = "Title changed to \"%s\"" % title
					self.write(send_str)
					url = "https://api.twitch.tv/kraken/channels/%s?oauth_token=%s" % (channel_parsed, access_token)
					data = json.dumps({'channel': {'status': title}})
					headers = {'content-type': 'application/json', 'Accept': 'application/vnd.twitchtv.v3+json'}
					r = requests.put(url, data=data, headers=headers)
				else:
					send_str = "You have to be the streamer to change the channel title."
					whisper(self, user, send_str)
			else:
				title = result_to_dict(self.conn.execute("SELECT `title` FROM title LIMIT 1"))
				if title:
					title = title[0]["title"]
					send_str = "The current title is: \"%s\"" % title.encode("utf-8")
					if has_level(self, user, channel_parsed, user_type, display_id):
						self.write(send_str)
					else:
						whisper(self, user, send_str)
				else:	
					channel_data = get_json_stream(channel_parsed)["streams"]
					if channel_data:
						title = channel_data[0]["channel"]["status"]
						send_str = "The current title is: \"%s\"" % title.encode("utf-8")
					else:
						send_str = "%s, %s is currently offline." % (user, self.channel_parsed)
			if get_status(self, self.title_display_id) and has_level(self, user, channel_parsed, user_type, display_id):
				self.write(send_str)
			else:
				whisper(self, user, send_str)
				return
		else:
			return False
			
	def game_parse(self, user, msg, channel_parsed, user_type):
		game_str = "!game"
		msg_arr = msg.split(" ", 1)
		if in_front(game_str, msg):
			if len(msg_arr) > 1:
				if is_streamer(user, channel_parsed):
					game = msg_arr[1]
					update_data(self, self.game_display_id, ["game"], game)
					send_str = "Game changed to \"%s\"" % game
					self.write(send_str)
					url = "https://api.twitch.tv/kraken/channels/%s?oauth_token=%s" % (channel_parsed, access_token)
					data = json.dumps({'channel': {'game': game}})
					headers = {'content-type': 'application/json', 'Accept': 'application/vnd.twitchtv.v3+json'}
					r = requests.put(url, data=data, headers=headers)
				else:
					send_str = "You have to be the streamer to change the channel game"
					whisper(self, user, send_str)
			else:
				#gonna need to see what the output is from this and edit accordingly
				game = result_to_dict(self.conn.execute("SELECT `game` FROM game LIMIT 1"))
				#if they want game and it's equal to "", then get the game and check accordingly
				if game != []:
					if game == False:
						send_str = "%s is not playing a game." % channel_parsed.capitalize()
					else:
						send_str = "The current game is: \"%s\"" % game.encode("utf-8")
					if has_level(self, user, channel_parsed, user_type, self.game_display_id):
						self.write(send_str)
						return
					else:
						whisper(self, user, send_str)
						return
				else:	
					#get the new game and then print accordingly
					channel_data = get_json_stream(channel_parsed)["streams"]
					if channel_data:
						game = channel_data[0]["game"]
						send_str = "The current game is: \"%s\"" % game.encode("utf-8")
					else:
						send_str = "%s is not playing a game." % channel_parsed.capitalize()
						
			if get_status(self, self.game_display_id) and has_level(self, user, channel_parsed, user_type, self.game_display_id):
				self.write(send_str)
				return
			else:
				whisper(self, user, send_str)
				return
		else:
			return False
			
	def topic_parse(self, user, msg, channel_parsed, user_type):
		topic_str = "!topic"
		
		if get_status(self, self.topic_display_id):
			msg_arr = msg.split(" ", 1)
			if in_front(topic_str, msg):
				if len(msg_arr) > 1:
					if has_level(self, user, channel_parsed, user_type, self.topic_display_id):
						update_data(self, self.topic_display_id, ["topic"], msg_arr[1])
						send_str = "Topic changed to \"%s\"" % msg_arr[1]
						self.write(send_str)
					else:
						send_str = "You don't have the correct permissions to change the channel topic"
						whisper(self, user, send_str)
				else:
					topic = result_to_dict(self.conn.execute("SELECT `topic` FROM topic LIMIT 1"))
					send_str = "The current topic is: \"%s\"" % topic
				if has_level(self, user, channel_parsed, user_type, self.topic_display_id):
					self.write(send_str)
				else:
					whisper(self, user, send_str)
			else:
				return False
		else:
			return False
	
	def purge_parse(self, user, msg, channel_parsed, user_type):
		purge_str = "!purge"
		if get_status(self, self.purge_display_id):
			if in_front(purge_str, msg):
				if has_level(self, user, channel_parsed, user_type, self.purge_display_id):
					msg_arr = msg.split()
					if len(msg_arr) > 1:
						purge_user = msg_arr[1]
						if is_streamer(purge_user, channel_parsed):
							send_str = "I cannot purge the streamer."
						else:
							timeout(purge_user, self, self.purge_duration)
							return
					elif len(msg_arr) == 1:
						send_str = "Time the user out for a short duration, deleting their messages. Syntax and more information can be found in the documentation."
						whisper(self, user, send_str)
						return
					else:
						send_str = "Usage: !purge <user>"
						whisper(self, user, send_str)
						return
				else:
					send_str = "Only mods can use \"!purge\"."
					whisper(self, user, send_str)
					return	
				self.write(send_str)
			else:
				return False
		else:
			return False
			
	def math_parse(self, user, msg, channel_parsed, user_type):
		#math - print if mod whisper if not
		math_str = "!math"
		if get_status(self, self.math_display_id):
			if in_front(math_str, msg):
				msg_arr = msg.split(" ")
				if len(msg_arr) == 1:
					send_str = "Usage: !math <equation>" 
					whisper(self, user, send_str)
				elif len(msg_arr) > 1:
					equation = msg_arr[1]
					try:
						send_str = str(eval(equation))
					except:
						send_str = "Unable to solve equation."
						whisper(self, user, send_str)
						return
				self.write(send_str)
			else:
				return False
		else:
			return False
			
	def roll_parse(self, user, msg, channel_parsed, user_type):
		#roll - return a random number in the given range
		roll_str = "!roll"
		
		if get_status(self, self.roll_display_id):
			if in_front(roll_str, msg):
				msg_arr = msg.split(" ", 1)
				if len(msg_arr) == 1:
					send_str = "Usage: !roll <lower limit(default: 0)>, <upper limit>" 
					whisper(self, user, send_str)
					return
				elif len(msg_arr) > 1:
					range_lims = msg_arr[1].split(",")
					if len(range_lims) > 1:
						roll_lower_lim = range_lims[0]
						roll_upper_lim = range_lims[1]
						if not is_num(roll_lower_lim) or not is_num(roll_upper_lim):
							send_str = "!Usage: !roll <lower limit(default: 0)>, <upper limit>"
							whisper(self, user, send_str)
							return
					else:
						if not is_num(msg_arr[1]):
							send_str = "!Usage: !roll <lower limit(default: 0)>, <upper limit>"
							whisper(self, user, send_str)
							return
						if int(float(msg_arr[1])) < 0:
							roll_lower_lim = msg_arr[1]
							roll_upper_lim = 0
						else:
							roll_lower_lim = 0
							roll_upper_lim = msg_arr[1]
					#get the random number
					roll_lower_lim = int(float(roll_lower_lim))
					roll_upper_lim = int(float(roll_upper_lim))
					roll_num = random.randint(roll_lower_lim, roll_upper_lim)
					send_str = "%s: %s" % (user, prettify_num(roll_num))
					if not has_level(self, user, channel_parsed, user_type, self.roll_display_id):
						whisper(self, user, send_str)
						return
				self.write(send_str)
			else:
				return False
		else:
			return False
			
	def coin_parse(self, user, msg, channel_parsed, user_type):
		#coin - return heads or tails
		coin_str = "!coin"
		if get_status(self, self.coin_display_id):
			if in_front(coin_str, msg):
				if random.randint(0, 1) == 0:
					send_str = "%s: Heads" % user
				else:
					send_str = "%s: Tails" % user
				if not has_level(self, user, channel_parsed, user_type, self.coin_display_id):
					whisper(self, user, send_str)
					return
				self.write(send_str)
			else:
				return False
		else:
			return False
	
	def countdown_parse(self, user, msg, channel_parsed, user_type):
		#add in expiration date/time til expiration for command
		#!countdown add asdf: 5 seconds
		#!countdown add asdf: <date>
		#how can we do the second's date, formatting wise?
		
		countdown_str = "!countdown"
		countdown_add_str = "!countdown add"
		countdown_del_str = "!countdown delete"
		countdown_rem_str = "!countdown remove"
		countdown_list_str = "!countdown list"
		countdown_clr_str = "!countdown clear"

		if get_status(self, self.countdown_display_id):
			if in_front(countdown_str, msg):
				if in_front(countdown_add_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.countdown_display_id):
						msg_arr = msg.split(" ")
						if len(msg_arr) > 3:
							del msg_arr[0:2]#remove command specifiers
							countdown_cmd = ''
							for cmd_part in range(len(msg_arr)):
								if cmd_part == len(msg_arr)-2 and msg_arr[cmd_part+1] in self.time_unit_arr:#if unit of time specified
									countdown_cmd = countdown_cmd.rstrip()
									countdown_time = simplify_num(msg_arr[cmd_part])
									time_unit = msg_arr[cmd_part+1]
									countdown_time = convert_to_sec(countdown_time, time_unit, self)
									break
								elif cmd_part == len(msg_arr)-1:#if no unit of time specified, seconds OR date of expiration
									countdown_cmd = countdown_cmd.rstrip()#get rid of trailing space
									countdown_time = msg_arr[cmd_part]
								else:
									countdown_cmd += msg_arr[cmd_part] + " "
							if not disconnect_cmd(countdown_cmd):
								current_time = time.time()
								#countdown_set = [current_time, countdown_cmd, countdown_time]
								query = text("INSERT INTO `%s` (`set_time`, `command`, `duration`) VALUES (:time, :command, :expiration)" % self.countdown_display_id)
								self.conn.execute(query, time=current_time, command=countdown_cmd, expiration=countdown_time)
								send_str = "Countdown command \"%s\" added with expiration time %s." % (countdown_cmd, parse_sec_condensed(countdown_time))
							else:
								send_str = "No \".disconnect\" or \"/disconnect\" variants allowed."
						else:
							send_str = "Usage: !countdown add <command> <expiration time/date>" 
							whisper(self, user, send_str)
							return
					else:
						send_str = "You don't have the correct permissions to use \"!countdown add\"." 
						whisper(self, user, send_str)
						return
				elif in_front(countdown_del_str, msg) or in_front(countdown_rem_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.countdown_display_id):
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) > 2:
							countdown_cmd = msg_arr[2]
							if is_num(countdown_cmd):
								countdown_cmd = int(countdown_cmd)
								delete_status = delete_index_handler(self, self.countdown_display_id, countdown_cmd)
								if delete_status:
									send_str = "Countdown command \"%s\" with expiration time %s removed at index %s." % (delete_status["command"], parse_sec_condensed(delete_status["duration"]), countdown_cmd)
								else:
									send_str = "Invalid index for countdown command removal." 
							else:
								delete_status = delete_value_handler(self, self.countdown_display_id, "command", countdown_cmd)
								if delete_status: 
									send_str = "Countdown command \"%s\" with expiration time %s removed." % (countdown_cmd, parse_sec_condensed(delete_status["duration"]))		
								else:
									send_str = "Specified countdown command does not exist." 
						else:
							send_str = "Usage: !countdown delete/remove <command/index>" 
							whisper(self, user, send_str)
							return
					else:
						send_str = "You don't have the correct permissions to use \"!countdown delete/remove\"." 
						whisper(self, user, send_str)
						return
				elif countdown_list_str == msg:
					countdown_table = get_table(self, self.countdown_display_id)
					if len(countdown_table) == 0:
						send_str = "No active countdown commands." 
					else:
						send_str = "Active countdown commands: " 
						for row_index, row in enumerate(countdown_table):
							if (row_index != len(countdown_table)-1):
								#every element but last one
								send_str += "(%s.) %s: %s, " % (row_index+1, row["command"], parse_sec_condensed(row["duration"]))
							else:
								#last element in arr
								send_str += "(%s.) %s: %s." % (row_index+1, row["command"], parse_sec_condensed(row["duration"]))
								
					if not has_level(self, user, channel_parsed, user_type, self.countdown_display_id):
						whisper(self, user, send_str)		
						return			
				elif countdown_clr_str == msg:
					if has_level(self, user, channel_parsed, user_type, self.countdown_display_id): 
						clear_table(self, self.countdown_display_id)
						send_str = "All countdown commands removed." 
					else:
						send_str = "You don't have the correct permissions to use \"!countdown clear\"." 
						whisper(self, user, send_str)
						return
				elif countdown_str == msg:
					send_str = "Add or remove commands to be executed at the end of a specified time. Syntax and more information can be found in the documentation." 
					whisper(self, user, send_str)
					return
				else:
					if has_level(self, user, channel_parsed, user_type, self.countdown_display_id):
						send_str = "Usage: !countdown add/delete/remove/list/clear <command> <expiration time>" 
					else:
						send_str = "Usage: !countdown list" 
					whisper(self, user, send_str)
					return
				self.write(send_str)
				return
			else:
				return False
	
	def points_parse(self, user, msg, channel_parsed, user_type):
		#!points - return number of points for the current user, allow mods to get the points of any user
		points_str = "!points"
		if get_status(self, self.points_display_id):
			if in_front(points_str, msg):
				if has_level(self, user, channel_parsed, user_type, self.points_display_id):
					msg_arr = msg.split()
					if len(msg_arr) > 1:
						if has_level(self, user, channel_parsed, user_type, self.points_display_id):
							point_user = msg_arr[1]
							points_num = point_balance(self, point_user)
							if point_user == user:
								if points_num:
									if points_num != 1:
										send_str = "%s, you have %s points in this channel" % (user, points_num)
									else:
										send_str = "%s, you have %s point in this channel" % (user, points_num)
								else:
									send_str = "%s, you do not have any points in this channel" % user
							else:
								if points_num:
									if points_num != 1:
										send_str = "%s has %s points in this channel." % (point_user, points_num)
									else:
										send_str = "%s has %s point in this channel." % (point_user, points_num)
								else:
									send_str = "%s has no points in this channel." % point_user
						else:
							send_str = "You don't have the correct permissions to get the points of other users"
					elif len(msg_arr) == 1:
						points_num = point_balance(self, user)
						if points_num:
							if points_num != 1:
								send_str = "%s, you have %s points in this channel" % (user, points_num)
							else:
								send_str = "%s, you have %s point in this channel" % (user, points_num)
						else:
							send_str = "%s, you do not have any points in this channel" % user
					else:
						send_str = "!Usage: !points <user>"
						whisper(self, user, send_str)
						return
						
					self.write(send_str)
				else:
					send_str = "You don't have the correct permissions to use \"!points\"."
					whisper(self, user, send_str)
					return
			else:
				return False
		else:
			return False
	
	def slots_parse(self, user, msg, channel_parsed, user_type):
		'''
		Randomly chooses emoticon three times and gives points, default stats are below
		They have to pay a default fee of 5 points to play
		Will whisper them back their new total of points after they play
		Will print the slot roll and points gained
		
		1 PraiseIt = 10 points
		2 PraiseIts = 60 Points
		3 PraiseIts = 300 Points / Jackpot
		
		3 Kappas = 20
		3 KappaPrides = 30
		3 KappaRoss = 40
		3 PeteZaRoll = 50
		3 bleedPurple = 60
		3 deIlluminati = 70
		
		Kappa			35%
		KappaPride		30%
		KappaRoss		20%
		PeteZaroll		08%
		bleedPurple		04%
		deIlluminati	02%
		PraiseIt		01%
		'''
		slots_str = "!slots"
		if get_status(self, self.slots_display_id):
			if in_front(slots_str, msg):
				if has_level(self, user, channel_parsed, user_type, self.slots_display_id):
					default_slots_cost = -1
					point_change(self, user, default_slots_cost)
					slot_rand_arr = [random.random(), random.random(), random.random()]
					slot_emote_arr = ['','','']
					for slot_index, slot in enumerate(slot_rand_arr):
						if slot <= .35:
							slot_emote_arr[slot_index] = "Kappa"
						elif slot <= .65:
							slot_emote_arr[slot_index] = "KappaPride"
						elif slot <= .85:
							slot_emote_arr[slot_index] = "KappaRoss"
						elif slot <= .93:
							slot_emote_arr[slot_index] = "PeteZaroll"
						elif slot <= .97:
							slot_emote_arr[slot_index] = "bleedPurple"
						elif slot <= .99:
							slot_emote_arr[slot_index] = "deIlluminati"
						elif slot <= 1.00:
							slot_emote_arr[slot_index] = "PraiseIt"
						else:
							slot_emote_arr[slot_index] = "Invalid"
					if slot_emote_arr.count("Kappa") == 3:
						slot_point_value = 20
					elif slot_emote_arr.count("KappaPride") == 3:
						slot_point_value = 30
					elif slot_emote_arr.count("KappaRoss") == 3:
						slot_point_value = 40
					elif slot_emote_arr.count("PeteZaroll") == 3:
						slot_point_value = 50
					elif slot_emote_arr.count("bleedPurple") == 3:
						slot_point_value = 60
					elif slot_emote_arr.count("deIlluminati") == 3:
						slot_point_value = 70
					elif slot_emote_arr.count("PraiseIt") >= 1:
						if slot_emote_arr.count("PraiseIt") == 1:
							slot_point_value = 10
						elif slot_emote_arr.count("PraiseIt") == 2:
							slot_point_value = 60
						elif slot_emote_arr.count("PraiseIt") == 3:
							slot_point_value = 300
						#else shouldnt happen
					else:
						slot_point_value = 0
					
					send_str = "%s has rolled %s %s %s , which is worth %s points." % (user, slot_emote_arr[0], slot_emote_arr[1], slot_emote_arr[2], slot_point_value)
					if slot_emote_arr.count("PraiseIt") == 3:#perhaps this will change when time comes for advanced settings, need this condition to be the one that determines the jackpot
						send_str += " Congratulations on rolling a jackpot!"
					elif slot_point_value <= 0:
						send_str += " Better luck next time!"
					point_change(self, user, slot_point_value)
					self.write(send_str)
					send_str = "You now have %s points in this channel." % point_balance(self, user)
					whisper(self, user, send_str)
				else:
					send_str = "You don't have the correct permissions to use \"!slots\"."
					whisper(self, user, send_str)
					return
			else:
				return False
		else:
			return False
	
	def give_parse(self, user, msg, channel_parsed, user_type):
		#!give - give user specified amount of coins, 
		give_str = "!give"
		if get_status(self, self.give_display_id):
			if in_front(give_str, msg):
				msg_arr = msg.split()
				if len(msg_arr) == 3:
					give_user = msg_arr[1]
					give_amount = msg_arr[2]
					if is_num(give_amount):
						give_amount = simplify_num(give_amount)
						user_point_bal = point_balance(self, user)
						if user_point_bal >= 0:
							if give_amount >= 0:
								if user_point_bal - give_amount >= 0:
									point_change(self, user, give_amount*-1)
									point_change(self, give_user, give_amount)
									if has_level(self, user, channel_parsed, user_type, self.give_display_id):
										if give_amount != 1:
											send_str = "%s has given %s %s points." % (user, give_user, give_amount)
										else:
											send_str = "%s has given %s %s point." % (user, give_user, give_amount)
									else:
										if give_amount != 1:
											send_str = "You have given %s %s points." % (give_user, give_amount)
											whisper(self, user, send_str)
											send_str = "%s has given you %s points." % (user, give_amount)
											whisper(self, give_user, send_str)
										else:
											send_str = "You have given %s %s point." % (give_user, give_amount)
											whisper(self, user, send_str)
											send_str = "%s has given you %s point." % (user, give_amount)
											whisper(self, give_user, send_str)
										return
								else:
									send_str = "You cannot give more points than you have." 
									whisper(self, user, send_str)
									return
							else:
								send_str = "You cannot give negative points." 
								whisper(self, user, send_str)
								return
						else:
							send_str = "You cannot give more points than you currently have." 
							whisper(self, user, send_str)
							return
					else:
						send_str = "Usage: !give <user> <point amount> "
						whisper(self, user, send_str)
						return
				else:
					send_str = "Usage: !give <user> <point amount>"
					whisper(self, user, send_str)
					return
				self.write(send_str)
			else:
				return False
		else:
			return False
	
	def editors_parse(self, user, msg, channel_parsed, user_type):
		#editors 
		editors_str = "!editors"
		editors_add_str = "!editors add"
		editors_del_str = "!editors delete"
		editors_rem_str = "!editors remove"
		editors_list_str = "!editors list"
		editors_clr_str = "!editors clear"
		
		editors_on = get_status(self, self.editors_display_id)
		if editors_on:
			if in_front(editors_str, msg):
				#add editors
				if in_front(editors_add_str, msg):
					if has_level(self, user, self.channel_parsed, user_type, self.editors_display_id): 
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) == 3:
							editor = msg_arr[2].strip()
							if has_count(self, self.editors_display_id, "user", editor):
								send_str = "%s is already an editor." % (editor)
							else:
								query = text("INSERT INTO `editors` (`user`) VALUES (:editor)")
								self.conn.execute(query, editor=editor)
								send_str = "Editor \"%s\" added." % (editor)
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!editors add <editor>\"." 
							whisper(self, user, send_str)
							return
					else:
						send_str = "You don't have the correct permissions to use \"!editors add\"." 
						whisper(self, user, send_str)
						return
				#delete editors
				elif in_front(editors_del_str, msg) or in_front(editors_rem_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.editors_display_id): 
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) == 3:
							editor = msg_arr[2]
							if is_num(editor):
								editor = int(editor)
								delete_status = delete_index_handler(self, self.editors_display_id, editor)
								if delete_status:
									send_str = "Editor %s removed at index %s." % (delete_status["user"], editor)
								else:
									send_str = "Invalid index for editor removal." 
							
							else:
								delete_status = delete_value_handler(self, self.editors_display_id, "user", editor)
								if delete_status:		
									send_str = "Editor %s removed." % (delete_status["user"])	
								else:
									send_str = "Specified user is not an editor." 
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!editors delete/remove <editor>\"." 
							whisper(self, user, send_str)
							return
					else:
						send_str = "You don't have the correct permissions to use \"!editors delete/remove\"." 
						whisper(self, user, send_str)
						return
				#list editor
				elif editors_list_str == msg:
					editor_table = get_table(self, self.editors_display_id)
					if len(editor_table) == 0:
						send_str = "There are currently no editors." 
					else:
						send_str = "Editors: " 
						for row_index, row in enumerate(editor_table):
							editor = row["user"]
							if (row_index != len(editor_table)-1):
								#every element but last one
								send_str += "(%s.) %s, " % (row_index+1, row["user"])
							else:
								#last element in arr
								send_str += "(%s.) %s." % (row_index+1, row["user"])
					if not has_level(self, user, channel_parsed, user_type, self.editors_display_id):
						whisper(self, user, send_str)		
						return			
				#clear editors
				elif in_front(editors_clr_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.editors_display_id): 
						clear_table(self, self.editors_display_id)
						send_str = "All editors removed." 
					else:
						send_str = "You don't have the correct permissions to use \"!editors clear\"." 
						whisper(self, user, send_str)
						return
				#just editor string, display usage
				elif in_front(editors_str, msg):
					if has_level(self, user, channel_parsed, user_type, self.editors_display_id): 
						send_str = "Promote or demote users to and from the editor level. Syntax and more information can be found in the documentation." 
					else:
						send_str = "You don't have the correct permissions to use !editors commands." 
					whisper(self, user, send_str)
					return
				else:
					if has_level(self, user, channel_parsed, user_type, self.editors_display_id): 
						send_str = "Usage: !editors add/delete/remove/list/clear" 
					else:
						send_str = "You don't have the correct permissions to use !editors commands." 
					whisper(self, user, send_str)
					return
				self.write(send_str)
			else:
				return False
		else:
			return False
	
	def level_parse(self, user, msg, channel_parsed, user_type):
		#!level - set level requirement of different features
		level_str = "!level"
		if get_status(self, "level"):
			if in_front(level_str, msg):
				if has_level(self, user, channel_parsed, user_type, self.level_display_id):
					msg_arr = msg.split(" ", 1)
					if len(msg_arr) > 1:
						feature_arr = msg_arr[1:][0]
						if is_num(feature_arr[-1]):#if last element in the array is a number then assign the feature to everything before it and assign the level to the number
							feature = feature_arr[:-1].strip()
							level = int(feature_arr[-1])
							if level < 1 or level > 4:
								send_str = "Level requirement must be between 1 and 4." 
								whisper(user, send_str)
								return 
							if "!" in feature[:1]:
								feature = feature[1:]
							if feature == "subs":
								feature = self.subcribers_display_id#this way we don't have to make a new row and stuff just for this.
							elif feature == "mods":
								feature = self.moderators_display_id#same ^^^
							if has_count(self, "main", "display_id", feature):
								query = text("SELECT COUNT(*) FROM main WHERE display_id = :feature AND feature_level = %d" % level)
								if result_to_dict(self.conn.execute(query, feature=feature))[0]["COUNT(*)"] > 0:
									feature = possessive_prettify(feature)
									send_str = "%s level requirement is already set to %d." % (feature.capitalize(), level)
								else:
									query = text("UPDATE main SET feature_level = %d WHERE display_id = :feature" % level)
									self.conn.execute(query, feature=feature)
									feature = possessive_prettify(feature)
									send_str = "%s level requirement set to %d." % (feature.capitalize(), level)
									self.write(send_str)
									return
							else:
								send_str = "%s is not a feature." % feature
								whisper(self, user, send_str)
								return
						else:
							send_str = "Usage: !level <feature> <level>"
					else:
						send_str = "Usage: !level <feature> <level>"
				else:
					send_str = "You don't have the correct permissions to use \"!level\"."
				whisper(self, user, send_str)
				return
			else:
				return False
		else:
			return False
			
	def main_parse(self, user, msg, user_type):
		comm_len_arr = [30, 60, 90, 120, 150, 180]
		#need to make this off, until mod turns it on with a command
		#then it turns off again after elapsed voting time or mod ends raffle time with !winner or something so that a winner can be chosen
		#none of these declarations should be in here
		
		#start_log(log_file_path)
		#remove from the permit_dict once they have been there more than the permit_time
		#do we need to put this outside the loop?
		current_time = time.time()
		#[current_msg_count, user, msg_count, type]
		#[current_time, user, permit_time, type]
		#Take the message and add to chat log
		update_chat_log(self.channel_parsed, current_time, msg)
		
		###new viewers/chatters
		#needs to be reassigned every time so that we keep the topic up to date
		topic = result_to_dict(self.conn.execute("SELECT `topic` FROM topic LIMIT 1"))
		self.welcome_msg = "Welcome to the channel! The current topic is \"%s\""  % topic
		self.welcome_back_msg = "Welcome back! The current topic is \"%s\""  % topic
		
		###start of debugging functions
		#holy shit wish i thought of this earlier
		#only for debugging and development, will immediately stop execution of program
		#also because i am fucking tired of goldmine ads
		if 'goldmine' in msg or 'BTC' in msg or 'bitcoin' in msg or "rektmine" in msg:
			send_str = "/ban %s" % (user)
			self.write(send_str)
		if "e" == msg and (user == "darkelement75" or user == "dark_element_slave1"):
			full_exit()
		
		if in_front("!say", msg):
			self.write(msg.split(" ", 1)[1])
		###end of debugging functions
		#link whitelists
		#has to be before anti spam so that adding/removing a link will not trigger and time out the user doing so			
		if self.link_whitelist_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.antispam_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		if self.spam_permit_parse(user, msg, self.channel_parsed, user_type) != False:
			return

		if self.banphrase_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.autoreply_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.set_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.vote_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.raffle_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.lottery_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.roulette_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.ball_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.uptime_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.general_channel_stats_parse(user, msg, self.channel_parsed, user_type, "chatters") != False:
			return
			
		if self.general_channel_stats_parse(user, msg, self.channel_parsed, user_type, "viewers") != False:
			return
			
		if self.general_channel_stats_parse(user, msg, self.channel_parsed, user_type, "views") != False:
			return
			
		if self.general_channel_stats_parse(user, msg, self.channel_parsed, user_type, "followers") != False:
			return	
			
		if self.channel_stats_parse(user, msg, self.channel_parsed, user_type) != False:
			return	
			
		if self.subs_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.commercial_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		#if self.ban_emote_parse(user, msg, self.channel_parsed, user_type, display_id) != False:
			#return
			
		if self.repeat_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.custom_command_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.stats_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.mods_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.topic_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.game_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.title_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.purge_parse(user, msg, self.channel_parsed, user_type) != False:
			return

		#Until we find a more dependable solution
		#if self.math_parse(user, msg, self.channel_parsed, user_type) != False:
			#return
			
		if self.roll_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.coin_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.countdown_parse(user, msg, self.channel_parsed, user_type) != False:
			return	
		
		if self.points_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.slots_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.give_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.editors_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.level_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
	def signedOn(self):
		logging.warning("Signed on as {}".format(self.nickname))

		# Set IRC caps for Twitch and join channel
		self.sendLine("CAP REQ :twitch.tv/membership")
		self.sendLine("CAP REQ :twitch.tv/commands")
		self.sendLine("CAP REQ :twitch.tv/tags")
		self.join(self.channel)

	def joined(self, channel):
		logging.warning("Joined %s" % channel)

	def privmsg(self, user, channel, msg):
		# Extract twitch name
		name = user.split('!', 1)[0].lower()
	
		# Log the message
		logging.info("{}: {}".format(name, msg))
		self.main_parse(name, msg, self.user_type)
	
	def parsemsg(self, s):
		"""Breaks raw IRC message into tags, prefix, command, and arguments."""
		tags, prefix, trailing = {}, '', []
		if s[0] == '@':
			tags_str, s = s[1:].split(' ', 1)
			tag_list = tags_str.split(';')
			tags = dict(t.split('=') for t in tag_list)
		if s[0] == ':':
			prefix, s = s[1:].split(' ', 1)
		if s.find(' :') != -1:
			s, trailing = s.split(' :', 1)
			args = s.split()
			args.append(trailing)
		else:
			args = s.split()
		command = args.pop(0).lower()
		return tags, prefix, command, args
	
	def action(self, user, channel, msg):
		#Only gets called when there is an action in the message, the only action being "/me"
		name = user.split('!', 1)[0].lower()
		msg = "/me " + msg
		
		#Log the message
		logging.info("{}: {}".format(name, msg))
		
		self.main_parse(name, msg, self.user_type)
		
	def lineReceived(self, line):
		'''Handle IRC line'''
		# First, we check for any custom twitch commands
		tags, prefix, cmd, args = self.parsemsg(line)
		
		if cmd == "hosttarget":
			self.hostTarget(*args)
		elif cmd == "clearchat":
			self.clearChat(*args)
		elif cmd == "notice":
			self.notice(tags, args)
		elif cmd == "privmsg":
			name = prefix.split("!")[0]
			self.user_type = tags.get('user-type')
		# Remove IRCv3 tag information
		if line[0] == "@":
			line = line.split(' ', 1)[1]
			
		'''if len(args) == 2:
			if "\x01ACTION" in args[1]:
				args[1] = args[1].replace("\x01ACTION", "/me").replace("\x01", "")
		print args'''
		# Then we let IRCClient handle the rest
		super(TwitchBot, self).lineReceived(line)

	def hostTarget(self, channel, target):
		'''Track Twitch hosting status'''
		target = target.split(' ')[0]
		if target == "-":
			logging.warning("Exited host mode")
		else:
			logging.warning("Now hosting {}".format(target))

	def clearChat(self, channel, target=None):
		'''Track chat clear notices'''
		if target:
			logging.warning("{} was timed out".format(target))
		else:
			logging.warning("chat was cleared")

	def notice(self, tags, args):
		'''Track all other Twitch notices'''
		if "msg-id" not in tags:
			return
		logging.warning(tags['msg-id'])
		current_time = time.time()
		if tags['msg-id'] == "bad_timeout_mod":
			if current_time - self.last_timeout_time > self.timeout_interval:
				self.last_timeout_time = current_time
				self.write("Timeout unsuccessful, I cannot time out moderators without being the streamer.")
		'''elif tags['msg-id'] == "timeout_success":
			if current_time - self.last_timeout_time > self.timeout_interval:
				self.last_timeout_time = current_time
				self.write("Timeout successful.")'''#disabled because too many messages
		#for /mods response
		if args[0] == self.channel and "The moderators of this room are:" in args[1]:
			args[1] += ", and %s." % self.channel.replace("#", "")
			#self.write(args[1])
			self.mods_msg = args[1]
		elif args[0] == self.channel and "There are no moderators of this room." in args[1]:
			#self.write(args[1])
			self.mods_msg = args[1]

	def write(self, msg):
		'''Send message to channel and log it'''
		if "/mods" in msg:
			original_msg = msg
			msg = "/mods"
			self.msg(self.channel, msg)
			if not self.whisper_mods_thread:#if we aren't looking for the msg for the get whisper mods msg function
				thread.start_new_thread(get_mods_msg, (self, original_msg))

		else:	
			self.msg(self.channel, msg.encode("utf-8"))
			logging.info("{}: {}".format(self.nickname, msg))

		if get_status(self, "loops"):
			self.main_parse(nickname, msg, '')#parse our own if that feature is on
		
class BotFactory(protocol.ClientFactory, object):
	wait_time = 1

	def __init__(self, channel):
		self.channel = channel

	def buildProtocol(self, addr):
		return TwitchBot(self.channel)

	def clientConnectionLost(self, connector, reason):
		# Reconnect when disconnected
		logging.error("Lost connection, reconnecting")
		self.protocol = TwitchBot
		connector.connect()

	def clientConnectionFailed(self, connector, reason):
		# Keep retrying when connection fails
		msg = "Could not connect, retrying in {}s"
		logging.warning(msg.format(self.wait_time))
		time.sleep(self.wait_time)
		self.wait_time = min(512, self.wait_time * 2)
		connector.connect()

class TwitchWhisperBot(irc.IRCClient, object):

	def __init__(self, channel):#for now only channel
		self.channel = channel
		self.nickname = nickname
		self.password = password
		self.channel_parsed = self.channel.replace("#", "")
		reactor.whisper_bot = self
		#Database
		#create database here with the .sql file if it doesn't already exist
		if not database_exists(self.nickname):	
			create_database(self.nickname)
		engine = create_engine("mysql://root@localhost:3306/%s" % self.nickname)
		self.conn = engine.connect()
		self.mods_msg = ''
		
		#check_loop = LoopingCall(self.whisper_check)
		#check_loop.start(0.003)
	
	def test_parse(self, user, msg):
		#test
		test_str = "!test"
		test_reply = "Test successful."
		
		if msg == "!test":
			whisper(self, user, test_reply)
		else:
			return False
	
	def ball_parse(self, user, msg, channel_parsed):
		#8ball
		#adding in deleting/adding/clearing of values
		ball_str = "!8ball"
		
		if in_front(ball_str, msg):
			if "?" in msg: #and msg.rstrip().endswith("?") <-- is this better?
				msg_arr = msg.split(" ", 1)
				if len(msg_arr) == 2:
					ball_table = get_table(self, self.ball_display_id)
					if len(ball_table) > 0:
						response_index = random.randint(0, len(ball_table)-1)
						response = ball_table[response_index]["responses"]
						send_str = "Magic 8 ball says... %s" % (response)
					else:
						send_str = "There are currently no 8ball responses." 
				elif ball_str == msg:
					send_str = "Get the Magic 8 Ball to answer your question. Usage: \"!8ball <question> \"." 
				else:
					send_str = "Usage: \"!8ball <question>? \"." 
			else:
				send_str = "Usage: \"!8ball <question>? \"." 
			whisper(self, user, send_str)
		else:
			return False

	def uptime_parse(self, user, msg, channel_parsed):
		#uptime
		uptime_str = "!uptime"
		if in_front(uptime_str, msg):
			msg_arr = msg.split(" ")
			if len(msg_arr) > 1:
				uptime = get_uptime_str(msg_arr[1])
				if uptime:
					send_str = "%s has been live for: %s" % (msg_arr[1], get_uptime_str(msg_arr[1]))
				else:
					send_str = "%s is not an active channel." % msg_arr[1]
			else:
				send_str = "Usage: \"!uptime <channel>\""
			whisper(self, user, send_str)
		else:
			return False
	
	def general_channel_stats_parse(self, user, msg, channel_parsed, stat_str):
		find_stat_str = "!" + stat_str
		if in_front(find_stat_str, msg):
			msg_arr = msg.split()
			if len(msg_arr) > 1:
				stat_channel = msg_arr[1]
				
				if stat_str == self.chatters_display_id:
					stat_data = get_json_chatters(stat_channel.lower().strip())
					stat_count = stat_data["chatter_count"]
				elif stat_str == self.viewers_display_id:
					stat_data = get_json_stream(stat_channel.lower().strip())
					stat_count = stat_data["streams"]
				elif stat_str == self.views_display_id:
					stat_data = get_json_views_follows(stat_channel.lower().strip())
					stat_count = stat_data["views"]
				elif stat_str == self.followers_display_id:
					stat_data = get_json_views_follows(stat_channel.lower().strip())
					stat_count = stat_data["followers"]
					
				if stat_count:
					if stat_str == self.viewers_display_id:
						stat_count = stat_count[0]["viewers"]
						
					stat_count = prettify_num(stat_count)
					if stat_channel.rstrip().endswith("s"):
						stat_channel = stat_channel + "'"
					else:	
						stat_channel = stat_channel + "'s"
				
					if stat_str == self.chatters_display_id:
						send_str = "There are currently %s accounts in %s chat." % (stat_count, stat_channel)
					elif stat_str == self.viewers_display_id:
						send_str = "There are currently %s viewers in %s channel." % (stat_count, stat_channel)
					elif stat_str == self.views_display_id:
						send_str = "There are currently %s views in %s channel." % (stat_count, stat_channel)
					elif stat_str == self.followers_display_id:
						send_str = "%s channel has %s followers." % (stat_channel.capitalize(), stat_count)
				else:
					send_str = "%s is not an active channel." % msg_arr[1]
			else:
				send_str = "Usage: \"%s <channel>\"" % find_stat_str
				
			whisper(self, user, send_str)
		else:
			return False
		
	def channel_stats_parse(self, user, msg, channel_parsed):
		chan_stats_str = "!chanstats"
		if in_front(chan_stats_str, msg):
			msg_arr = msg.split(" ")
			if len(msg_arr) > 1:
				stat_data = get_json_stream(msg_arr[1].lower().strip())
				stat_data = stat_data["streams"]
				if stat_data:
					channel_game = stat_data[0]["game"]
					if channel_game:
						send_str = "%s is playing %s for %s viewers." % (msg_arr[1].capitalize(), channel_game, stat_data[0]["viewers"])
					else:
						send_str = "%s is not playing a game, however there are %s viewers" % (msg_arr[1].capitalize(), stat_data[0]["viewers"])
				else:
					send_str = "%s is not an active channel." % msg_arr[1].capitalize()
			else:
				send_str = "Usage: !chanstats <channel>"
			whisper(self, user, send_str)
		else:
			return False
		
	def subs_parse(self, user, msg, channel_parsed):
		#subscribers
		subscribers_str = "!subscribers"
		subs_str = "!subs"	
		if in_front(subs_str, msg) or in_front(subscribers_str, msg):
			msg_arr = msg.split()
			if len(msg_arr) > 1:
				sub_channel = msg_arr[1]
				sub_data = get_json_subs(sub_channel.lower())
				sub_count = sub_data["_total"]
				if sub_count:
					sub_count = prettify_num(sub_count)
					if sub_channel.rstrip().endswith("s"):
						send_str = "%s' channel has %s subs." % (sub_channel, sub_count)
					else:
						send_str = "%s's channel has %s subs." % (sub_channel, sub_count)
				else:
					send_str = "%s does not currently allow tecsbot access." % sub_channel
			else:
				send_str = "Usage: \"!subs/!subscribers <channel>\""
				
			if has_level(self, user, channel_parsed, user_type, self.subcribers_display_id):
				self.write(send_str)
			else:	
				whisper(self, user, send_str)
		else:
			return False
	
	def stats_parse(self, user, msg, channel_parsed):
		stats_str = "!stats"
		if in_front(stats_str, msg):
			msg_arr = msg.split(" ", 2)
			if len(msg_arr) > 2:
				#!stats <channel> <word>
				stats_channel = msg_arr[1]
				word = msg_arr[2]
				if stats_channel != "global":
					word_count = get_word_count(word, stats_channel)
					channel_data = get_json_stream(stats_channel)["streams"]
					if channel_data:
						minute = get_uptime_min(stats_channel)
						word_per_min = round((word_count / minute), 2)
						stats_channel = possessive_prettify(stats_channel)
						send_str = "Total times %s has been sent in %s channel: %s. Per minute: %s." % (word, stats_channel, prettify_num(word_count), simplify_num(word_per_min))
					else:
						send_str = "That channel is currently offline."
				else:
					word_count_global = get_word_count_global(word)
					send_str = "Total times %s has been sent in all channels: %s." % (word, prettify_num(word_count_global))
			else:
				send_str = "Usage: !stats <channel> <word>" 
				whisper(self, user, send_str)
				return
			whisper(self, user, send_str)
			return
		else:
			return False
			
	'''def mods_parse(self, user, msg, channel_parsed):
		mods_str = "!mods" 
		moderators_str = "!moderators"
		
		if in_front(mods_str, msg) or in_front(moderators_str, msg):
			self.write("/mods")
		else:
			return False
	'''
	def main_parse(self, user, msg):
	
		if self.test_parse(user, msg) != False:
			return
			
		if self.ball_parse(user, msg, self.channel_parsed) != False:
			return
			
		if self.uptime_parse(user, msg, self.channel_parsed) != False:
			return
			
		if self.general_channel_stats_parse(user, msg, self.channel_parsed, self.chatters_display_id) != False:
			return
			
		if self.general_channel_stats_parse(user, msg, self.channel_parsed, self.viewers_display_id) != False:
			return
			
		if self.general_channel_stats_parse(user, msg, self.channel_parsed, self.views_display_id) != False:
			return
			
		if self.general_channel_stats_parse(user, msg, self.channel_parsed, self.followers_display_id) != False:
			return	
		
		if self.channel_stats_parse(user, msg, self.channel_parsed) != False:
			return	
			
		if self.stats_parse(user, msg, self.channel_parsed) != False:
			return
		
	def whisper_check(self):
		#print whisper_msg, whisper_user
		
		global whisper_msg, whisper_user
		#when any of the threads change both values whisper the message and reset the values
		if whisper_msg != "" and whisper_user != "":
			whisper_str = "/w %s %s" % (whisper_user, whisper_msg)
			self.write(whisper_str)
		whisper_msg = ""
		whisper_user = ""
			
	def signedOn(self):
		#for the whisper function
		reactor.whisper_bot = self

		logging.warning("Signed on as {}".format(self.nickname))

		# Set IRC caps for Twitch and join channel
		self.sendLine("CAP REQ :twitch.tv/membership")
		self.sendLine("CAP REQ :twitch.tv/commands")
		self.sendLine("CAP REQ :twitch.tv/tags")
		self.join(self.channel)

	def joined(self, channel):
		logging.warning("Joined %s" % channel)

	def privmsg(self, user, channel, msg):
		# Extract twitch name
		name = user.split('!', 1)[0].lower()
	
		# Log the message
		logging.info("{}: {}".format(name, msg))	
	
	def parsemsg(self, s):
		"""Breaks raw IRC message into tags, prefix, command, and arguments."""
		tags, prefix, trailing = {}, '', []
		if s[0] == '@':
			tags_str, s = s[1:].split(' ', 1)
			tag_list = tags_str.split(';')
			tags = dict(t.split('=') for t in tag_list)
		if s[0] == ':':
			prefix, s = s[1:].split(' ', 1)
		if s.find(' :') != -1:
			s, trailing = s.split(' :', 1)
			args = s.split()
			args.append(trailing)
		else:
			args = s.split()
		command = args.pop(0).lower()
		return tags, prefix, command, args
	
	def action(self, user, channel, msg):
		#Only gets called when there is an action in the message, the only action being "/me"
		name = user.split('!', 1)[0].lower()
		msg = "/me " + msg
		
		#Log the message
		logging.info("{}: {}".format(name, msg))
		
		self.main_parse(name, msg, self.user_type)
		
	def lineReceived(self, line):
		'''Handle IRC line'''
		# First, we check for any custom twitch commands
		tags, prefix, cmd, args = self.parsemsg(line)
		
		if cmd == "hosttarget":
			self.hostTarget(*args)
		elif cmd == "clearchat":
			self.clearChat(*args)
		elif cmd == "notice":
			self.notice(tags, args)
		# Remove IRCv3 tag information
		elif cmd == "whisper":
			user = tags.get("display-name")
			msg = args[1]
			self.main_parse(user, msg)
		if line[0] == "@":
			line = line.split(' ', 1)[1]

		# Then we let IRCClient handle the rest
		super(TwitchWhisperBot, self).lineReceived(line)

	def hostTarget(self, channel, target):
		'''Track Twitch hosting status'''
		target = target.split(' ')[0]
		if target == "-":
			logging.warning("Exited host mode")
		else:
			logging.warning("Now hosting {}".format(target))

	def clearChat(self, channel, target=None):
		'''Track chat clear notices'''
		if target:
			logging.warning("{} was timed out".format(target))
		else:
			logging.warning("chat was cleared")

	def notice(self, tags, args):
		'''Track all other Twitch notices'''
		if "msg-id" not in tags:
			return
		logging.warning(tags['msg-id'])
		'''Send message to channel and log it'''
		
		self.msg(self.channel, msg.encode("utf-8"))
		logging.info("{}: {}".format(self.nickname, msg))
		
	def write(self, msg):
		self.msg(self.channel, msg.encode("utf-8"))
		logging.info("{}: {}".format(self.nickname, msg))

class WhisperBotFactory(protocol.ClientFactory, object):
	wait_time = 1

	def __init__(self, channel):
		global whisper_bot

		self.channel = channel

	def buildProtocol(self, addr):
		return TwitchWhisperBot(self.channel)

	def clientConnectionLost(self, connector, reason):
		# Reconnect when disconnected
		logging.error("Lost connection, reconnecting")
		self.protocol = TwitchWhisperBot
		connector.connect()

	def clientConnectionFailed(self, connector, reason):
		# Keep retrying when connection fails
		msg = "Could not connect, retrying in {}s"
		logging.warning(msg.format(self.wait_time))
		time.sleep(self.wait_time)
		self.wait_time = min(512, self.wait_time * 2)
		connector.connect()
			
#main whisper bot where other threads with processes will be started
#sets variables for connection to twitch chat

whisper_channel = '#_tecsbot_1444071429976'
whisper_channel_parsed = whisper_channel.replace("#", "")

server_json = get_json_servers()
server_arr = (server_json["servers"][0]).split(":")
server = server_arr[0]
port = int(server_arr[1])

#try:
# we are using this to make more connections, better than threading
# Make logging format prettier
logging.basicConfig(format="[%(asctime)s] %(message)s",
					datefmt="%H:%M:%S",
					level=logging.INFO)

# Connect to Twitch IRC server, make more instances for more connections
#Whisper connection
reactor.connectTCP(server, port, WhisperBotFactory(whisper_channel))

#Channel connections
reactor.connectTCP('irc.twitch.tv', 6667, BotFactory("#darkelement75"))

#MOAR DATA!!!!!!!!
#Note: if we disconnect ourselves (like I did earlier with forsenlol), then it won't be connected to the stream to check if the stream is online,
	#and subsequently will never delete the logs of that stream. We can just have it delete them when told to leave
'''reactor.connectTCP('irc.twitch.tv', 6667, BotFactory("#sodapoppin"))
reactor.connectTCP('irc.twitch.tv', 6667, BotFactory("#nl_kripp"))
reactor.connectTCP('irc.twitch.tv', 6667, BotFactory("#c9sneaky"))
reactor.connectTCP('irc.twitch.tv', 6667, BotFactory("#lirik"))
reactor.connectTCP('irc.twitch.tv', 6667, BotFactory("#forsenlol"))
reactor.connectTCP('irc.twitch.tv', 6667, BotFactory("#bestrivenna"))
reactor.connectTCP('irc.twitch.tv', 6667, BotFactory("#trumpsc"))
reactor.connectTCP('irc.twitch.tv', 6667, BotFactory("#admiralbulldog"))'''

reactor.run()
	
#except Exception as errtxt:
	#print errtxt



