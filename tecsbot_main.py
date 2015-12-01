# -*- coding: utf-8 -*-
#^^this makes it so we can actually parse unicode
#TODO:
#TECSBot, Twitch Emote Chat Statistics Bot
#Made by DarkElement75, AKA Blake Edwards
"""
SEPERATE IDEAS
20 bot network controlled by one main bot
	could be used to paste 1/20th of a copypasta at a time
	ascii art line by line
	have a small channel come alive with bots
	
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

SERVER:
how to keep permanently on, desktop is best current option, other than some form of cloud hosting/streamer hosting<-- see stackoverflow response
still cant track emotes it's not seeing, can't see them if it's not online. Permanent online is necessary for accurate emote stats.<-- ^

multi channel processing for comparison stats?
famous person has joined chat
donations <-if this isnt already done very well
hours til next strim? <--countdown command
score of current game/tourney/bo3/etc
song functionality
sub notifications
raffle -  expiration timer? <-- we could let the countdowns do this
social media info
allow users to program question responses like ALICE? <-- interesting idea for a solo channel
overall and per day -time user has watched stream
	other user tracking stuff
overrall and per day -messages of user, high score, etc
check to make sure x!= '' is present in all the things
log/dict/array of recent commands? <-doubt this would actually help with an undo command
	do similar thing to moobot, have a chatbox of the commands said and run, without other misc messages
different levels of authority? 
tecsbot moderator group?
more advanced !test results?
figure out what to do with the other spamerino things
excludes for "regulars" and subs
offtime - time stream has been offline
the minimum number of symbols should be disabled by default
link our access_token html file and this file 
	this is going to be completely different most likely when we do this on a server, so for now we are just doing a text file edit
need to make friends with a twitch partner
need to have command to check if user is subscribed to channel 
	!subscribed /!subbed <user>
just a note: better to try and open file and catch exception than to check if isfile
the bad file descriptor is apparently related to the self. variables<--so you know why it's happening if it does happen again
make it so capitalization doesnt matter on several things(i.e. autoreply) option?
make an option to let bot respond to it's own replies to autoreplies? Would this be for all of them? i.e. countdown, repeat, autoreply as well, etrc
use round() wherever needed
use enumerate wherever needed
point system for watching stream/chatting/etc
	more points -> greater chance to win prizes/raffles/etcidk
	when points added or subtracted then do point_change(self, point_num, user)
		add user to self.user_points_arr if not in it already
	we should do this as a dictionary actually
	
!x delete 21, 1, 5 <--- multiple deleting possibility <--- can we make a function for deleting?
allow streamer to choose what to let mods do?<--- could work with level system
analytic for messages and emotes and shiznizzle
when adding/removing ban emotes for the special emotes(o_O, O_o, etc), it currently will bulk remove/add them. 
	In the GUI, we want to have a checkbox for "remove all variants of <input emote text>(emote picture)?" that if checked will do as did normally, if unchecked then will do one at a time.
1 second between requests is recommended
replace as many api requests as possible
time for level system:
	streamer has all control, GUI settings as well as everything else
	editor level = all settings other than gui
	moderator = can they start things but not edit, or can they do neither?
	
!clever <user> to troll user
add !leave and !join commands (and !rejoin)
make stats for all words instead of just emotes
https://apis.rtainc.co/twitchbot/status?user=Darkelement75 custom api link
	http://deepbot.tv/wiki/Custom+Commands
should we deprecate ban emotes if we won't be distincting between emotes and words in the stats future?
argument for mod requirement custom commands autoreplies
	allow it for already existing commands, maybe edit in GUI
	allow it to be input for custom and autoreply commands
execute commands with streamer capabilities
http://deepbot.deep.sg/wiki/Bot+Commands
@customapi@[api link] where customapi is a variable that represents the data on the api link, ie how nightbot has uptime api link
	use more try except/catch 
oauth_on variable
!time to print current time
need to either figure out a way to whisper the /mods response or implement this when there is a new way to get the mods of a room
dont let it time out mods unless it can send messages on behalf of streamer
make link whitelist also look for false positives? i.e. dot com
remember to update the default command list, the README, and the sets
should we allow setting on/off of stuff like uptime and topic?
whisper mods list or whispers argument where mods can choose to have bot's responses whispered to them instead of printed
default starting amount of points, make changeable just like all the others
4 main things:
	1. Song requests - website for streamer to use that bot is hooked up to, use the gui
	2. Database setting storage
	3. website and gui for the bot 
		a. Allows settings input
		b. Has connect with twitch button first
input time out duration for banphrases?
current_time = time.time() will not get fractions of a second, it will only get whole seconds
	for now I don't want to implement this because why would you care so much about those fractions of a second
	maybe we will make it loop every second in the future instead of 0.003, i dont fucking know i just know i dont want to 
	do it right now
for the lists - individualize em'
check if link antispam first
get_status instead of if self.status_on
pretty sure it used to be resetting the votes when someone did !poll start if there was already a poll going on. should be fixed now
need to make finish the vote database implementation
once all the db backend is complete remember to delete all the sets and arrays and no longer used variables
need uptime_on, topic, viewers etc
is get_status fast enough for the checks? oh maybe we could only check when about to send them??
"""
'''misc
 function loadEmotes() { $.getJSON("https://api.betterttv.net/emotes").done(function(data) { $emotes.text(''); parseEmotes(data.emotes); }).fail(function() { $('#emote').text("Error loading emotes.."); }); }
1:42 TimeoutBan Clearflare: https://api.betterttv.net/emotes/ will give you json
'''
'''
errors:

Traceback (most recent call last):
  File "C:\Python27\Scripts\tecsbot\tecsbot_main.py", line 2842, in <module>
	data = irc.recv(1204) #gets output from IRC server
  File "C:\Python27\lib\socket.py", line 170, in _dummy
	raise error(EBADF, 'Bad file descriptor')
socket.error: [Errno 9] Bad file descriptor
Unhandled exception in thread started by
sys.excepthook is missing
lost sys.stderr

Unhandled exception in thread started by <bound method channel_bot_start.main of <__main__.channel_bot_start object at 0x0000000002D3DDD8>>
Traceback (most recent call last):
  File "C:\Python27\Scripts\tecsbot\tecsbot_main.py", line 2331, in main
	irc.connect((server, 6667)) #connects to the server
  File "C:\Python27\lib\socket.py", line 222, in meth
	return getattr(self._sock,name)(*args)
socket.gaierror: [Errno 11004] getaddrinfo failed

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
	self.connect()
  File "C:\Python27\lib\httplib.py", line 736, in connect
	self.timeout, self.source_address)
  File "C:\Python27\lib\socket.py", line 551, in create_connection
	for res in getaddrinfo(host, port, 0, SOCK_STREAM):
IOError: [Errno socket error] [Errno 11004] getaddrinfo failed
'''
import socket #imports module allowing connection to IRC
import thread, threading #imports module allowing timing functions
import sys, operator, time, urllib, json, math, os, random, unicodedata, requests, select
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


f = open("C:\\Python27\\Scripts\\bot_oauth.log", "r")
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

link_whitelist_arr = []


#This determines whether to do search_str == msg, or search_str in message when looking for commands
cmd_match_full = True

#initial connect
f = open("C:\\Python27\\Scripts\\bot_oauth.log", "r")
access_token = f.readlines()[1]
client_id = "jpf2a90oon0wqdnno5ygircwgomt9rz"

whisper_msg = ""
whisper_user = ""

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

def create_count_dict(emote_arr):
	dict = {}
	for emote in emote_arr:
		dict[emote] = []
		dict[emote].append(0)
	return dict
	
def update_count_dict(count_dict, emote_arr):#can we deprecate this?
	#remove emotes that were removed, add new ones
	for emote in emote_arr:
		if emote not in count_dict:#if emote is not yet added
			count_dict[emote] = []
			count_dict[emote].append(0)
	for emote in count_dict:
		if emote not in emote_arr:#remove if not an emote
			del count_dict[emote]
	return count_dict

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

def find_per_min(emote, count_dict, channel_parsed):
	emote_count = count_dict[emote][0]
	#this number is from the start of the program to the current time of the query, 
	#giving the amount of minutes from the start of the program.
	minute = get_uptime_min(channel_parsed)
	emote_per_min = emote_count / minute
	return emote_per_min

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
		print x
		return False
		
def set_value(self, display_id, msg_arr):
	status = get_status(self, display_id)
	if msg_arr[2] == "on":
		if status:
			send_str = "%s is already on." % (set_feature.capitalize())
		else:
			set_status(self, feature, True)
			send_str = "%s turned on. You can do \"!set %s off\" to turn it off again." % (set_feature.capitalize(), set_feature)
	elif msg_arr[2] == "off":
		if not status:
			send_str = "%s is already off." % (set_feature.capitalize())
		else:
			set_status(self, feature, False)
			send_str = "%s turned off. You can do \"!set %s on\" to turn it on again." % (set_feature.capitalize(), set_feature)
	else:
		#usage
		send_str = "Usage: \"!set %s on/off \"." % (set_feature)
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
	
def warn(user, msg, channel_parsed, self, warn_table, warn_duration, warn_cooldown, timeout_msg, timeout_duration):
	#function to warn if they havent already been warned, and time them out if they have.
	query = "SELECT COUNT(*) FROM %s WHERE user = '%s'" % (warn_table, user)
	res = result_to_dict(self.conn.execute(query))
	
	if res[0]["COUNT(*)"] > 0:
		current_time = time.time()
		#check if current time is longer than the warning duration from the last time name was entered
		query = "SELECT * FROM %s WHERE user = '%s' and (%s - set_time <= %s) LIMIT 1" % (warn_table, user, current_time, warn_cooldown)
		row = result_to_dict(self.conn.execute(query))
		if row != []:
			#they did a bad thing in a time less than the cooldown, time out for long duration
			#timeout user for long duration and remove from array
			timeout(user, self, timeout_duration)
			
			delete_value_handler(self, warn_table, "index", row[0]["index"])
			send_str = "No %s allowed (%s)" % (timeout_msg, user.capitalize())
			self.write(send_str)
			whisper_msg = "You were timed out for %s in %s (%s)" % (timeout_msg, channel_parsed, parse_sec(timeout_duration))
			whisper(user, whisper_msg)
		else:
			#they did a bad thing in a time more than the cooldown, time out for long duration
			#replace old entry with new one and send warning as well as timeout for warn_duration
			#short duration
			query = "SELECT * FROM %s WHERE user = '%s' and (%s - set_time > %s) LIMIT 1" % (warn_table, user, current_time, warn_cooldown)
			row = result_to_dict(self.conn.execute(query))
			timeout(user, self, warn_duration)
			print row
			delete_value_handler(self, warn_table, "index", row[0]["index"])
			pair = [current_time, user]
			insert_data(self, warn_table, ["set_time", "user"], pair)
			send_str = "No %s allowed (%s)(warning)" % (timeout_msg, user.capitalize())
			self.write(send_str)
			whisper_msg = "You were timed out for %s in %s (%s, warning)" % (timeout_msg, channel_parsed, parse_sec(warn_duration))		
			whisper(user, whisper_msg)
	else:
		#add new entry and send warning, with timeout for warn_duration
		#short duration
		timeout(user, self, warn_duration)
		current_time = time.time()
		pair = [current_time, user]
		insert_data(self, warn_table, ["set_time", "user"], pair)
		send_str = "No %s allowed (%s)(warning)" % (timeout_msg, user.capitalize())
		self.write(send_str)
		whisper_msg = "You were timed out for %s in %s (%s, warning)" % (timeout_msg, channel_parsed, parse_sec(warn_duration))
		whisper(user, whisper_msg)
		
def symbol_count(msg):
	reg_chars = [',','.',' ','\'','\"','?', ';']
	reg_chars.extend(list(string.letters))
	reg_chars.extend(list(string.digits))
	msg_symbol_count = 0
	for char in msg:
		if char not in reg_chars:
			msg_symbol_count += 1
	return msg_symbol_count		

def in_front(str, msg):
	if str in msg[:len(str)+1]:
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

def whisper(user, msg):
	global whisper_user, whisper_msg
	whisper_user = user
	whisper_msg = msg
	
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

def get_emote_list(channel_parsed):
	url = "https://api.twitch.tv/kraken/chat/%s/emoticons" % channel_parsed
	emote_json = requests.get(url).json()
	emote_arr = ['O_O', 'o_O', 'O_o', 'o_o',':o', ':O', ':\\', ':/',':p', ':P', ';p', ';P', ':)', ':(', ':D', '>(', ':|', 'B)', '<3', ';)', 'R)']
	#these first 16 are the specials/duplicates, made into one array b/c it was being bitchy about .extending
	while True:
		try:
			for emote in emote_json["emoticons"]:
				if "\\" not in emote["regex"]:
					emote_arr.append(str(emote["regex"]))
			return emote_arr
		except:
			pass
	
def is_emote(emote, emote_arr):
	#returns T/F depending on if it's emote or no.
	#not worrying about dupes anymore
	'''if emote in emote_arr[:16]:#it's a dupe
		if emote == 'O_O' or emote == 'o_o' or emote == 'o_O' or emote == 'O_o':
			return 'O_O'
		elif emote == ':o' or emote == ':O':
			return ':O'
		elif emote == ':\\' or emote == ':/':
			return ':/'
		elif emote == ':p' or emote == ':P':
			return ':P'
		elif emote == ';p' or emote == ';P':
			return ';P'		'''
	if emote in emote_arr:#is emote
		return True
	else:#not an emote
		return False	

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
	permit_high_user = permit_pair[1]
	permit_high_type = permit_pair[3]
	permit_high_duration = permit_pair[2]
	
	if permit_high_type == "permanent":
		query = "DELETE FROM spam_permits WHERE user = '%s'" % permit_high_user
		self.conn.execute(query)
		insert_data(self, "spam_permits", ["set_time", "user", "duration", "type"], permit_pair)
		return True
	else:
		query = "SELECT COUNT(*) FROM spam_permits WHERE user = '%s' and type = 'permanent'" % permit_high_user
		res = result_to_dict(self.conn.execute(query))
		if res[0]["COUNT(*)"] <= 0:
			#this user does not have a permanent permit, check with the others
			query = "DELETE FROM spam_permits WHERE type = '%s' and duration < %d" % (permit_high_type, permit_high_duration)
			self.conn.execute(query)
			query = "SELECT COUNT(*) FROM spam_permits WHERE type = '%s' and duration > %d" % (permit_high_type, permit_high_duration)
			res = result_to_dict(self.conn.execute(query))
			if res[0]["COUNT(*)"] <= 0:
				#as long as there are none that are greater than ours(which means there are now no others of this type in the db), add it
				insert_data(self, "spam_permits", ["set_time", "user", "duration", "type"], permit_pair)
				return True
	return False

def get_raw_general_stats(channel_parsed, stat_str):
	if stat_str == "chatters":
		stat_data = get_json_chatters(channel_parsed.lower().strip())
		stat_count = stat_data["chatter_count"]
	elif stat_str == "viewers":
		stat_data = get_json_stream(channel_parsed.lower().strip())
		stat_count = stat_data["streams"]
	elif stat_str == "views":
		stat_data = get_json_views_follows(channel_parsed.lower().strip())
		stat_count = stat_data["views"]
	elif stat_str == "followers":
		stat_data = get_json_views_follows(channel_parsed.lower().strip())
		stat_count = stat_data["followers"]
		
	if stat_count:
		if stat_str == "viewers":
			stat_count = stat_count[0]["viewers"]
		return stat_count
	else:
		return '0'

def point_change(self, user, points):
	#if points != 0:#don't waste our time if it's 0 points#we actually remove this so that we tell them their new total of points and this may interfere with a custom setting
	if get_status(self, "points"):
		query = "SELECT COUNT(*) FROM point_users WHERE user = %s" % user
		res = result_to_dict(self.conn.execute(query))
		if len(res) <= 0:
			insert_data(self, "point_users", ["user", "points"], [user, 0])
		query = "UPDATE point_users SET points = points+%d WHERE user = %s" % (points, user)
		self.conn.execute(query)

def point_balance(self, user):
	query = "SELECT points FROM point_users WHERE user = %s" % user
	res = result_to_dict(self.conn.execute(query))
	return res
	
def result_to_dict(res):
	return [dict(row) for row in res]

#ONLY USE THIS FOR DEBUGGING
def is_empty(self, table):
	if get_len_table(self, table) > 0:
		return False
	else:
		return True
		
def get_len_table(self, table):
	query = "SELECT COUNT(*) FROM %s" % table
	res = result_to_dict(self.conn.execute(query))
	len_table = res[0]["COUNT(*)"]
	return len_table

def check_duplicate(self, table, columns, values):
	columns = "(" + ','.join(x for x in columns) + ")"
	values = '(' + repr(values)[1:-1] + ')'
	query = text("SELECT COUNT(*) FROM %s WHERE %s = %s" % (table, columns, values))
	if result_to_dict(self.conn.execute(query))[0]["COUNT(*)"] > 0:
		return True
	else:
		return False
		
def get_status(self, display_id):
	query = "SELECT feature_status FROM main WHERE display_id = '%s'" % display_id
	status = result_to_dict(self.conn.execute(query))
	if status[0]["feature_status"] == 1:
		return True
	else:
		return False
		
def set_status(self, feature, status):
	if status:
		query = "UPDATE main SET feature_status = 1 where display_id = '%s'" % feature
	else:
		query = "UPDATE main SET feature_status = 0 where display_id = '%s'" % feature
	self.conn.execute(query)
		
def insert_data(self, table, columns, values):
	columns = "(" + ','.join(x for x in columns) + ")"
	if not isinstance(values, list):
		values = [values]
	values = '(' + repr(values)[1:-1] + ')'
	query = text("INSERT INTO %s %s VALUES %s" % (table, columns, values)) 
	self.conn.execute(query)
	
def insert_row_data(self, table, columns, values):
	columns = "(" + ','.join(x for x in columns) + ")"
	row_values = ''
	for value in values:
		row_values += "(\"" + repr(value)[1:-1] + "\"),"
	row_values = row_values[:-1] + ";"
	query = text("INSERT INTO %s %s VALUES %s" % (table, columns, row_values)) 
	self.conn.execute(query)
	
def update_data(self, table, columns, values):
	if len(columns) > 1:
		columns = "(`" + ','.join(x for x in columns) + "`)"
	else:
		columns = columns[0]
	values = '("' + repr(values)[1:-1] + '")'
	query = text("UPDATE %s SET %s = %s" % (table, columns, values)) 
	self.conn.execute(query)

def get_data(self, table, columns):
	#Simple way to get data, will likely only be used for the game, title, and topic functions
	columns = "(" + ','.join(x for x in columns) + ")"
	query = text("SELECT %s FROM %s" % (table, columns))
	return result_to_dict(self.conn.execute(query))
	
def extend_data(self, table, column, values):
	columns = "(" + ','.join(x for x in columns) + ")"
	values = repr(values)[1:-1]
	query = text("INSERT INTO %s %s VALUES %s" % (table, columns, values)) 
	self.conn.execute(query)
##def update_8ball_table(self, type, 

def delete_index_handler(self, table, index):
	len_table = get_len_table(self, table)
	if not index > 0 or not index <= len_table:
		return False
	query = "SELECT * FROM %s LIMIT %s" % (table, index)
	result = result_to_dict(self.conn.execute(query))
	if len(result) == index: #could be len -1 = delete_index -1 to be more readable but ehh
		delete_row = result[len(result)-1]
	else:
		print "This shouldn't happen"
		full_exit()
	query = "DELETE FROM %s WHERE `index` = %s" % (table, delete_row["index"])
	self.conn.execute(query)
	return delete_row

def delete_value_handler(self, table, column, value):
	query = text("SELECT * FROM %s WHERE %s = '%s' LIMIT 1" % (table, column, value))
	res = result_to_dict(self.conn.execute(query))
	if res:
		query = text("DELETE FROM %s WHERE %s = '%s' LIMIT 1" % (table, column, value))
		self.conn.execute(query)
		return res[0]
	else:
		return False
	
	
def get_table(self, table):
	query = "SELECT * FROM %s" % table
	return result_to_dict(self.conn.execute(query))
	
def clear_table(self, table):
	query = "DELETE FROM %s" % table
	self.conn.execute(query)
	
class TwitchBot(irc.IRCClient, object):

	def __init__(self, channel):#for now only channel
		self.channel = channel
		self.nickname = nickname
		self.password = password
		self.channel_parsed = self.channel.replace("#", "")
		server = 'irc.twitch.tv'
		
		#Database
		#create database here with the .sql file
		engine = create_engine("mysql://root@localhost:3306/%s" % self.channel_parsed)
		self.conn = engine.connect()
		
		#self.ban_emote_on = True
		#self.emote_stats_on = True
		
		self.repeat_on = True
		self.countdown_on = True
		
		self.raffle_users = []
		self.lottery_users = []
		self.raffle_point_value = 0
		self.lottery_point_value = 0
		
		#self.vote_on = False
		self.link_whitelist_arr = []
		self.permit_arr = []
		self.banphrase_arr = []
		self.ar_arr = []
		self.ban_emote_arr = []
		self.emote_arr = []
		self.cmd_arr = []
		self.countdown_arr = []

		
		self.vote_total = 0
		
		#self.topic = 'Any ideas and questions welcome!'

		stream_data = get_json_stream(self.channel_parsed)["streams"]
		if stream_data:
			game = stream_data[0]["game"]
			if is_empty(self, "game"):
				insert_data(self, "game", ["game"], game)
			title = stream_data[0]["channel"]["status"]
			if is_empty(self, "title"):
				insert_data(self, "title", ["title"], title)
			topic = ""
			if is_empty(self, "topic"):
				insert_data(self, "topic", ["topic"], topic)
			
		#we should put settings like this in an admin menu, along with the timeout durations and such
		self.rol_chance = .5
		self.rol_timeout = 5 #seconds
		
		self.purge_duration = 5
		self.last_timeout_time = 0
		self.timeout_interval = 3#time to wait before sending a timeout unsuccessful cannot time out mods message
		
		self.follower_check_interval = 300#5 min
		self.stream_status_check_interval = 300#5 min
		
		self.chatter_arr = []
		self.stream_status = False
		
		self.default_permit_time = 30#seconds
		self.default_permit_msg_count = 10#msgs
		#######NOTE: ONLY USE THIS FOR DEBUGGING! AFTER THIS IT SHOULD ALWAYS BE EMPTY AND THIS WILL ONLY BE RUN ONCE!
		##########
		if is_empty(self, "8ball_responses"):
			insert_row_data(self, "8ball_responses", ["responses"], ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Reply hazy try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again", "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"])
		
		self.time_unit_arr = ["sec", "secs", "second", "seconds", "min", "mins", "minute", "minutes", "hr", "hrs", "hour", "hours", "day", "days", "week", "weeks"]
		#self.emote_arr = get_emote_list(self.channel_parsed)
		#self.special_emote_arr = ['o_O', 'O_o', 'o_o', 'O_O', ':o', ':O', ':\\', ':/', ':p', ':P', ';p', ';P']
		#self.emote_arr.extend(self.special_emote_arr)
		#self.count_dict = create_count_dict(self.emote_arr)
		
		self.reply_args_arr = ["{*USER*}", "{*TO_USER*}", "{*GAME*}", "{*STATUS*}", "{*TOPIC*}", "{*VIEWERS*}", "{*CHATTERS*}", "{*VIEWS*}", "{*FOLLOWERS*}"]
		#perhaps we should make this vvv a table
		self.default_cmd_arr = ['!link whitelist', '!permit', '!banphrase', '!autoreply', '!set', '!vote', '!raffle', '!roulette', '!8ball', '!uptime', '!chatters', '!viewers', '!subs', '!subscribers', '!commercial', '!ban emote', '!repeat', '!title', '!topic', '!game', '!purge', '!math', '!roll', '!coin', '!countdown']
		
		self.follower_arr = []
		self.viewer_arr = []
		self.perm_chatter_arr = []#so that we say welcome back if they are in this, and welcome if it is first time
		self.follower_arr, new_follower_arr = get_new_followers(self.follower_arr, self.channel_parsed, self)
		self.viewer_arr, new_viewer_arr = get_new_viewers(self.viewer_arr, self.channel_parsed, self)
		self.perm_chatter_arr.extend(new_viewer_arr)
				
		#Regexes
		self.link_regex = re.compile(ur'^(?:https?:\/\/)?\w+(?:\.\w{2,})+(?:\/\S+)*$', re.MULTILINE)
		self.ip_regex= re.compile(ur'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$\b', re.MULTILINE)
		
		#Default additions to autoreply and command arrays	
		if is_empty(self, "commands"):
			insert_data(self, "commands", ["command", "reply"], ["!slap", "{*USER*} slaps {*TO_USER*} around a bit with a large trout."])
			insert_data(self, "commands", ["command", "reply"], ["!shoutout", "Check out twitch.tv/{*TO_USER*} and follow them!"])
			
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

		if get_status(self, "link_whitelists"):
			if in_front(link_whitelist_str, msg):
				msg_arr = msg.split(" ")
				if in_front(link_whitelist_add_str, msg):
					if is_mod(user, channel_parsed, user_type):
						if len(msg_arr) > 3:
							link_whitelist = msg_arr[3]
							if re.search(self.link_regex, link_whitelist):#if is link according to our regex
								#is a url
								if check_duplicate(self, "link_whitelists", ["link"], [link_whitelist]):
									send_str = "%s is already a whitelisted link." % (link_whitelist)
								else:
									insert_data(self, "link_whitelists", ["link"], link_whitelist)
									send_str = "%s added to list of whitelisted links." % (link_whitelist)
							else:
								send_str = "%s is not a valid link." % (link_whitelist)
						else:
							send_str = "Usage: \"!link whitelist add <link>\""
							whisper(user, send_str)
							return
					else:
						send_str = "You have to be a mod to use \"!link whitelist add\"." 
						whisper(user, send_str)
						return
				elif in_front(link_whitelist_del_str, msg) or in_front(link_whitelist_rem_str, msg):
					if is_mod(user, channel_parsed, user_type):
						if len(msg_arr) > 3:
							link_whitelist = msg_arr[3]
							if is_num(link_whitelist):
								#we add on one to the actual index because users prefer to start with 1, rather than 0.
								link_whitelist = int(link_whitelist)
								delete_status = delete_index_handler(self, "link_whitelists", link_whitelist)
								if delete_status:
									send_str = "Link %s removed at index %s." % (delete_status["link"], link_whitelist)
								else:
									send_str = "Invalid index for link removal."
							else:
								delete_status = delete_value_handler(self, "link_whitelists", "link", link_whitelist)
								if delete_status:
									send_str = "Link %s removed." % (link_whitelist)									
								else:
									send_str = "Specified link does not exist." 
						else:
							send_str = "Usage: \"!link whitelist delete/remove <link/index>\"" 
							whisper(user, send_str)
							return
					else:
						send_str = "You have to be a mod to use \"!link whitelist delete/remove\"." 
						whisper(user, send_str)
						return
				elif link_whitelist_list_str == msg:
					link_whitelist_table = get_table(self, "link_whitelists")
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
					if not is_mod(user, self.channel_parsed, user_type):
						whisper(user, send_str)		
						return
						
				elif in_front(link_whitelist_clr_str, msg):
					if is_mod(user, channel_parsed, user_type):
						clear_table(self, "link_whitelists")
						send_str = "All links removed." 
					else:
						send_str = "You have to be a mod to use \"!link whitelist clear\"." 
						whisper(user, send_str)
						return
				elif in_front(link_whitelist_str, msg):
					send_str = "Add or remove links to timeout users who say them. Syntax and more information can be found in the documentation." 
					whisper(user, send_str)
					return
				else:
					send_str = "Usage: \"!link whitelist add/delete/remove/list/clear\"" 
					whisper(user, send_str)
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
		if get_status(self, "spam_permits"):
			if in_front(permit_str, msg):
				if is_mod(user, self.channel_parsed, user_type):
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
										whisper(user, send_str)
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
											whisper(user, send_str)
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
											whisper(user, send_str)
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
											whisper(user, send_str)
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
										whisper(user, send_str)
										return
								else:
									send_str = "Usage: !permit add <user> message/time/<time> <message count/time duration/time unit>/permanent" 
									whisper(user, send_str)
									return
							else:
								send_str = "Usage: !permit add <user> message/time/<time> <message count/time duration/time unit>/permanent" 
								whisper(user, send_str)
								return
						else:
							send_str = "Usage: !permit add <user> message/time/<time> <message count/time duration/time unit>/permanent" 
							whisper(user, send_str)
							return
								
					#delete/remove
					elif in_front(permit_del_str, msg) or in_front(permit_rem_str, msg):
						if len(msg_arr) == 3:
							permit_user = msg_arr[2]
							if is_num(permit_user):
								delete_status = delete_index_handler(self, "spam_permits", permit_user)
								if delete_status:
									if delete_status["type"] == "permanent":
										send_str = "Permanent permit %s removed at index %s." % (delete_status["user"], permit_user)
									elif delete_status["type"] == "message":
										send_str = "Permit %s with duration %s messages removed at index %s." % (delete_status["user"], delete_status["duration"], permit_user)
									elif delete_status["type"] == "time":
										send_str = "Permit %s with duration %s removed at index %s." % (delete_status["user"], parse_sec_condensed(delete_status["duration"]), permit_user)
									else:
										send_str = "This shouldn't happen, contact my creator if it does"
									#Should be the same index as the pair, after all.
									del self.permit_arr[int(permit_user)-1]
								else:
									send_str = "Invalid index for permit removal." 
							else:
								delete_status = delete_value_handler(self, "spam_permits", "user", permit_user)
								if delete_status:
									send_str = "Permit \"%s\" removed." % delete_status["user"]		
								else:
									send_str = "Specified permit does not exist." 
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!permit delete/remove <user/index>\"." 
							whisper(user, send_str)
							return
					#list
					elif permit_list_str == msg:
						permits_table = get_table(self, "spam_permits")
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
						if not is_mod(user, self.channel_parsed, user_type):
							whisper(user, send_str)		
							return		
					#clear
					elif in_front(permit_clr_str, msg):
						clear_table(self, "spam_permits")
						send_str = "All permits removed." 
					#normal
					elif permit_str == msg:
						if is_mod(user, self.channel_parsed, user_type):
							send_str = "Add or remove spam permits, allowing a user to message anything for a certain number of messages, or a length of time. Syntax and more information can be found in the documentation." 
						else:
							send_str = "You have to be a mod to use !permit commands" 
						whisper(user, send_str)
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
									whisper(user, send_str)
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
										whisper(user, send_str)
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
										whisper(user, send_str)
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
										whisper(user, send_str)
										return
								else:
									send_str = "Usage: !permit <user> message/time <message count/time duration>/permanent" 
									whisper(user, send_str)
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
									whisper(user, send_str)
									return
							else:
								send_str = "Usage: !permit <user> message/time <message count/time duration>/permanent" 
								whisper(user, send_str)
								return
						else:
							send_str = "Usage: !permit <user> message/time <message count/time duration>/permanent" 
							whisper(user, send_str)
							return
					else:
						if is_mod(user, self.channel_parsed, user_type):
							send_str = "Add or remove spam permits, allowing a user to message anything for a certain number of messages, or a length of time. Syntax and more information can be found in the documentation." 
						else:
							send_str = "You have to be a mod to use !permit commands" 
						whisper(user, send_str)
						return
					
									
				else:
					send_str = "You have to be a mod to use !permit commands." 
					whisper(user, send_str)
					return
				self.write(send_str)
			
			
			if in_front(unpermit_str, msg):
				if is_mod(user, self.channel_parsed, user_type):
					msg_arr = msg.split(" ")
					if len(msg_arr) == 2:
						permit_user = msg_arr[1]
						delete_status = delete_value_handler(self, "spam_permits", "user", permit_user)
						if delete_status:
							send_str = "%s's spam permit has been removed." % permit_user.lower()
						else:
							send_str = "%s does not have a spam permit." % permit_user.lower()
					else:
						send_str = "Usage: \"!unpermit <user>\"" 
						whisper(user, send_str)
						return
				else:
					send_str = "You have to be a mod to unpermit users." 
					whisper(user, send_str)
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
		if get_status(self, "antispam"):
			for permit_pair in self.permit_arr:
				if user.capitalize().rstrip() in permit_pair:
					return False
			else:
				if user.rstrip() == self.nickname or is_streamer(user, self.channel_parsed) or is_mod(user, self.channel_parsed, user_type):
					return False
				else:
					#if it's not tecsbot
					#if user does not have a permit then start the checks
					#need to update this
					'''if self.repeat_antispam_on:
						#general spam - need to improve this, for now adding in the set
						#needs to be in similar format to others for easy integration
						current_time = time.time() #unix time of message sent
						msg_data_arr = [current_time, user, msg]
						for msg_data in msg_info_arr:
							if msg_data_arr[0] - msg_data[0] < spam_cooldown: #only see messages that are within 30 seconds of newest messages
								if msg_data_arr[1] == msg_data[1] and msg_data_arr[2] == msg_data[2]: #if new message has the same user and same message as a previous message
									#if identical new message was sent within spam cooldown, then timeout user and stop looking through messages
									for permit_pair in self.permit_arr:
										if permit_pair[1] == user: 
											#if user is permitted to spam, don't time him out
											break
									else:
										timeout(user, irc, spam_timeout)
										return True
									break
							else:
								#pop the element out, since it no longer is within 30 seconds of the first message.
								msg_info_arr.remove(msg_data)
						msg_info_arr.insert(0, msg_data_arr)#add in the new message to the beginning of the list'''
						
					#emote spam
					if get_status(self, "emote_antispam"):
						msg_emote_count = 0
						for emote in self.emote_arr:
							if word_count(msg, emote) != 0:
								msg_emote_count += msg.count(emote)
							if msg_emote_count >= emote_max:
								warn(user, msg, channel_parsed, self, "emote_warn", emote_warn_duration, emote_warn_cooldown, emote_timeout_msg, emote_timeout_duration)
								return True
					'''#ban emotes
					if get_status(self, ":
						for ban_emote in self.ban_emote_arr:
							if word_count(msg, ban_emote) != 0:
								self.ban_emote_warn_arr = warn(user, msg, channel_parsed, self, self.ban_emote_warn_arr, ban_emote_warn_duration, ban_emote_warn_cooldown, ban_emote_timeout_msg, ban_emote_timeout_duration)
								return True'''
					
					#banphrases
					if get_status(self, "banphrases"):
						for banphrase in self.banphrase_arr:
							if banphrase in msg:
								warn(user, msg, channel_parsed, self, "banphrase_warn", banphrase_warn_duration, banphrase_warn_cooldown, banphrase_timeout_msg, banphrase_timeout_duration)
								return True
								
					#caps spam
					if get_status(self, "caps_antispam"):
						if len(msg) >= caps_perc_min_msg_len:
							if caps_perc(msg) >= 60:
								warn(user, msg, channel_parsed, self, "caps_warn", caps_warn_duration, caps_warn_cooldown, caps_timeout_msg, caps_timeout_duration)
								return True
					#fake purges
					if get_status(self, "fake_purge_antispam"):
						if msg in fake_purge_arr:
							warn(user, msg, channel_parsed, self, "fake_purge_warn", fake_purge_warn_duration, fake_purge_warn_cooldown, fake_purge_timeout_msg, fake_purge_timeout_duration)
							return True
					#!skincode
					if get_status(self, "skincode_antispam"):
						if in_front(skincode_msg, msg):
							warn(user, msg, channel_parsed, self, "skincode_warn", skincode_warn_duration, skincode_warn_cooldown, skincode_timeout_msg, skincode_timeout_duration)
							return True
					#long messages
					if get_status(self, "long_message_antispam"):
						if len(msg) > msg_length_max:
							warn(user, msg, channel_parsed, self, "long_msg_warn", long_msg_warn_duration, long_msg_warn_cooldown, long_msg_timeout_msg, long_msg_timeout_duration)
							return True
					
					#block symbols
					
					#dongers
					

					#excessive symbols
					#if there are more than min_symbol_chars in message, check the percentage and amount
					if get_status(self, "symbol_antispam"):
						if len(msg) > min_symbol_chars:
							symbol_num = symbol_count(msg)
							symbol_perc = float(symbol_num) / len(msg)
							#if the limits are exceeded for num or percentage
							if symbol_num > max_symbol_num or symbol_perc > max_symbol_perc:
								warn(user, msg, channel_parsed, self, "symbol_warn", symbol_warn_duration, symbol_warn_cooldown, symbol_timeout_msg, symbol_timeout_duration)
								return True
					#links
					#need a way to parse out the link exactly, instead of just checking if ours is in the link
					#we can split by spaces, look at each one and see if it contains any of these, thus making it a link and allowing us to parse and do tthe things
					#how to do the *path things? for now it's exact match
					if get_status(self, "link_whitelist_antispam"):
						for word in msg.split(" "):
							#we need to determine links for this sole reason
							if re.search(self.link_regex, word):#if is link according to our regex
								for link_whitelist in self.link_whitelist_arr:
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
							
					#these need to be different types
					msg_arr = msg.split(" ")
					#long word spam
					if get_status(self, "long_word_antispam"):
						for word in msg_arr:
							if len(word) > long_word_limit and '\n' not in word:
								warn(user, msg, channel_parsed, self, "long_word_warn", long_word_warn_duration, long_word_warn_cooldown, long_word_timeout_msg, long_word_timeout_duration)
								return True
					#/me
					if get_status(self, "me_antispam"):
						if in_front(me_msg, msg):
							warn(user, msg, channel_parsed, self, "me_warn", me_warn_duration, me_warn_cooldown, me_timeout_msg, me_timeout_duration)
							return True
						
					#ip addresses
					if get_status(self, "ip_antispam"):
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
		
		if get_status(self, "banphrases"):
			msg_arr = msg.split(" ", 2)
			if in_front(banphrase_str, msg):
				if in_front(banphrase_add_str, msg):
					if is_mod(user, self.channel_parsed, user_type): 
						if len(msg_arr) > 2:#need to have this if statement more often
							banphrase = msg_arr[2]
							if check_duplicate(self, "banphrases", "banphrase", banphrase):
								send_str = "%s is already a banphrase." % (banphrase)
							else:
								insert_data(self, "banphrases", ["banphrase"], banphrase)
								send_str = "\"%s\" added to list of banphrases." % (banphrase)
						else:
							send_str = "Usage: \"!banphrase add <banphrase>\"" 
							whisper(user, send_str)
							return
					else:
						send_str = "You have to be a mod to use \"!banphrase add\"." 
						whisper(user, send_str)
						return
					return
				elif in_front(banphrase_del_str, msg) or in_front(banphrase_rem_str, msg):
					if is_mod(user, self.channel_parsed, user_type):
						if len(msg_arr) > 2:
							banphrase = msg_arr[2]
							if is_num(banphrase):
								#we add on one to the actual index because users prefer to start with 1, rather than 0.
								banphrase = int(banphrase)
								delete_status = delete_index_handler(self, "banphrases", banphrase)
								if delete_status:
									send_str = "Banphrase \"%s\" removed at index %s." % (delete_status["banphrase"], banphrase)
								else:
									send_str = "Invalid index for banphrase removal." 
							else:
								delete_status = delete_value_handler(self, "banphrases", "banphrase", banphrase)
								if delete_status:
									send_str = "Banphrase \"%s\" removed." % (banphrase)									
								else:
									send_str = "Specified banphrase does not exist." 
						else:
							send_str = "Usage: \"!banphrase delete/remove <banphrase/index>\"" 
							whisper(user, send_str)
							return
					else:
						send_str = "You have to be a mod to use \"!banphrase delete/remove\"." 
						whisper(user, send_str)
						return
				elif banphrase_list_str == msg:
					banphrase_table = get_table(self, "banphrases")
					if len(banphrase_table) == 0:
						send_str = "No active banphrases." 
					else:
						send_str = "Active banphrases: " 
						for row_index, row in enumerate(banphrase_table):
							if (row_index != len(banphrase_table) -1):
								#every element but last one
								send_str += "(%s.) %s, " % (row_index+1, row["banphrase"])
							else:
								#last element in arr
								send_str += "(%s.) %s." % (row_index+1, row["banphrase"])
					if not is_mod(user, self.channel_parsed, user_type):
						whisper(user, send_str)		
						return		
				elif in_front(banphrase_clr_str, msg):
					if is_mod(user, self.channel_parsed, user_type): 
						clear_table(self, "banphrases")
						send_str = "All banphrases removed." 
					else:
						send_str = "You have to be a mod to use \"!banphrase clear\"." 
						whisper(user, send_str)
						return
				elif in_front(banphrase_str, msg):
					if is_mod(user, self.channel_parsed, user_type): 
						send_str = "Add or remove banphrases to timeout users who say them. Syntax and more information can be found in the documentation." 
					else:
						send_str = "You have to be a mod to use !banphrase commands." 
						whisper(user, send_str)
						return
				self.write(send_str)
			else:
				return False
		else:
			return False
	
	def test_parse(self, user, msg, channel_parsed, user_type):
		#test
		test_str = "!test"
		test_reply = "Test successful."
		
		if msg == "!test":
			send_str = "%s" % (test_reply)
			self.write(send_str)
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
		
		autoreply_on = get_status(self, "autoreplies")
		if autoreply_on:
			if in_front(autoreply_str, msg):
				#add autoreplies
				if in_front(autoreply_add_str, msg):
					if is_mod(user, self.channel_parsed, user_type): 
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) == 3:
							if ":" in msg_arr[2]:
								ar_msg_arr = msg_arr[2].split(":", 1)
								if len(ar_msg_arr) == 2:
									ar_phrase = ar_msg_arr[0].rstrip().lstrip()
									ar_reply = ar_msg_arr[1].rstrip().lstrip()
									ar_pair = [ar_phrase, ar_reply]
									if check_duplicate(self, "autoreplies", ["phrase", "reply"], ar_pair):
										send_str = "%s is already an autoreply phrase." % (ar_pair[0])
									else:
										if not disconnect_cmd(ar_reply):
											insert_data(self, "autoreplies", ["phrase", "reply"], ar_pair)
											send_str = "Phrase \"%s\" added, with reply \"%s\"." % (ar_phrase, ar_reply)
										else:
											send_str = "No \".disconnect\" or \"/disconnect\" variants allowed."
								else:
									#incorrectly formatted, display usage
									send_str = "Usage: \"!autoreply add <phrase>:<reply>\"." 
									whisper(user, send_str)
									return
							else:
								#incorrectly formatted, display usage
								send_str = "Usage: \"!autoreply add <phrase>:<reply>\"." 
								whisper(user, send_str)
								return
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!autoreply add <phrase>:<reply>\"." 
							whisper(user, send_str)
							return
					else:
						send_str = "You have to be a mod to use \"!autoreply add\"." 
						whisper(user, send_str)
						return
				#delete autoreplies
				elif in_front(autoreply_del_str, msg) or in_front(autoreply_rem_str, msg):
					if is_mod(user, self.channel_parsed, user_type): 
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) == 3:
							ar_phrase = msg_arr[2]
							if is_num(ar_phrase):
								ar_phrase = int(ar_phrase)
								delete_status = delete_index_handler(self, "autoreplies", ar_phrase)
								if delete_status:
									send_str = "Autoreply %s:%s removed at index %s." % (delete_status["phrase"], delete_status["reply"], ar_phrase)
								else:
									send_str = "Invalid index for autoreply removal." 
							
							else:
								delete_status = delete_value_handler(self, "autoreplies", "phrase", ar_phrase)
								if delete_status:		
									send_str = "Autoreply %s:%s removed." % (delete_status["phrase"], delete_status["reply"])	
								else:
									send_str = "Specified autoreply does not exist." 
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!autoreply delete/remove <phrase/index>\"." 
							whisper(user, send_str)
							return
					else:
						send_str = "You have to be a mod to use \"!autoreply delete/remove\"." 
						whisper(user, send_str)
						return
				#list autoreplies
				elif autoreply_list_str == msg:
					autoreply_table = get_table(self, "autoreplies")
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
					if not is_mod(user, self.channel_parsed, user_type):
						whisper(user, send_str)		
						return			
				#clear autoreplies
				elif in_front(autoreply_clr_str, msg):
					if is_mod(user, self.channel_parsed, user_type): 
						clear_table(self, "autoreplies")
						send_str = "All autoreplies removed." 
					else:
						send_str = "You have to be a mod to use \"!autoreply clear\"." 
						whisper(user, send_str)
						return
				#just autoreply string, display usage
				elif in_front(autoreply_str, msg):
					if is_mod(user, self.channel_parsed, user_type): 
						send_str = "Add or remove phrases that trigger automatic replies. Syntax and more information can be found in the documentation." 
					else:
						send_str = "You have to be a mod to use !autoreply commands." 
					whisper(user, send_str)
					return
				else:
					if is_mod(user, self.channel_parsed, user_type): 
						send_str = "Usage: !autoreply add/delete/remove/list/clear" 
					else:
						send_str = "You have to be a mod to use !autoreply commands." 
					whisper(user, send_str)
					return
				self.write(send_str)
			else:			
				if autoreply_on:
					autoreply_table = get_table(self, "autoreplies")
					for row in autoreply_table:
						try:
							phrase_index = msg.index(row["phrase"])
							#if msg did contain the autoreply phrase
							reply = row["reply"]
							for word in reply.split():
								if word in self.reply_args_arr:
									if word == "{*USER*}":
										reply = reply.replace("{*USER*}", user)
									elif word == "{*TO_USER*}":
										to_user_part = msg[phrase_index+len(ar_pair[0]):len(msg)]#all the elements after the autoreply
										reply_to_user = to_user_part.split()[0]#the first word after the autoreply, should be the to user
										reply = reply.replace("{*TO_USER*}", str(reply_to_user))
									elif word == "{*GAME*}":
										reply = reply.replace("{*GAME*}", get_data(self, "game", ["game"]))
									elif word == "{*STATUS*}":
										reply = reply.replace("{*STATUS*}", get_data(self, "title", ["title"]))
									elif word == "{*TOPIC*}":
										reply = reply.replace("{*TOPIC*}", get_data(self, "topic", ["topic"]))
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
		
		set_ban_emotes_str = "!set ban emotes"
		set_emote_stats_str = "!set emote stats"
		set_spam_permits_str = "!set spam permits"
		
		set_rol_cmd_str = "!roulette"
		set_rol_chance_str = "!roulette chance"
		
		if in_front(set_str, msg):
			if is_mod(user, self.channel_parsed, user_type):
				msg_arr = msg.split(" ")
				if len(msg_arr) == 3:
					
					#turn roulette on or off
					if in_front(set_roulette_str, msg):
						set_value(self, "roulette", "roulette", msg_arr)
						
					#turn 8ball on or off
					elif in_front(set_ball_str, msg):
						set_value(self, "8ball_responses", "8ball", msg_arr)
						
					#banphrases
					elif in_front(set_banphrase_str, msg):
						set_value(self, "banphrases", "banphrase", msg_arr)
					
					#autoreplies
					elif in_front(set_autoreply_str, msg):
						set_value(self, "autoreplies", "autoreply", msg_arr)
						
					#antispam
					elif in_front(set_antispam_str, msg):
						set_value(self, "antispam", "antispam", msg_arr)
						
					#repeat
					elif in_front(set_repeat_str, msg):
						set_value(self, "repeats", "repeat", msg_arr)
					
					#roll
					elif in_front(set_roll_str, msg):
						set_value(self, "roll", "roll", msg_arr)
					
					#math
					elif in_front(set_math_str, msg):
						set_value(self, "math", "math", msg_arr)
						
					#coin
					elif in_front(set_coin_str, msg):
						set_value(self, "coin", "coin", msg_arr)
					
					#countdown
					elif in_front(set_countdown_str, msg):
						set_value(self, "countdowns", "countdown", msg_arr)
						
					#topic
					elif in_front(set_topic_str, msg):
						set_value(self, "topic", "topic", msg_arr)
						
					else:
						send_str = "Usage: \"!set <feature> on/off \"." 
						whisper(user, send_str)
						return
				elif len(msg_arr) == 4:
					#repeat antispam
					if in_front(set_repeat_antispam_str, msg):
						set_value(self, "repeat_antispam", "repeat antispam", msg_arr)
						
					#emote antispam
					elif in_front(set_emote_antispam_str, msg):
						set_value(self, "emote_antispam", "emote antispam", msg_arr)
						
					#caps antispam
					elif in_front(set_caps_antispam_str, msg):
						set_value(self, "caps_antispam", "caps antispam", msg_arr)
					
					#skincode antispam
					elif in_front(set_skincode_antispam_str, msg):
						set_value(self, "skincode_antispam", "skincode antispam", msg_arr)
					
					#symbol antispam
					elif in_front(set_symbol_antispam_str, msg):
						set_value(self, "symbol_antispam", "symbol antispam", msg_arr)
					
					#link antispam
					elif in_front(set_link_antispam_str, msg):
						set_value(self, "link_antispam", "link antispam", msg_arr)
					
					#me antispam
					elif in_front(set_me_antispam_str, msg):
						set_value(self, "me_antispam", "me antispam", msg_arr)
					
					#spam permits
					elif in_front(set_spam_permits_str, msg):
						set_value(self, "spam_permits", "spam permits", msg_arr)
						
					else:
						send_str = "Usage: \"!set <feature> on/off \"." 
						whisper(user, send_str)
						return		
					#ban emotes
					'''elif in_front(set_ban_emotes_str, msg):
						self.ban_emotes_on = set_value(self, self.ban_emotes_on, "ban emotes", msg_arr)
					
					#emote stats
					elif in_front(set_emote_stats_str, msg):
						self.emote_stats_on = set_value(self, self.emote_stats_on, "emote stats", msg_arr)
					'''	
					
				elif len(msg_arr) == 5:
					#fake purge antispam
					if in_front(set_fake_purge_antispam_str, msg):
						set_value(self, "fake_purge_antispam", "fake purge antispam", msg_arr)
					
					#long message antispam
					elif in_front(set_long_msg_antispam_str, msg):
						set_value(self, "long_message_antispam", "long message antispam", msg_arr)
					
					#long word antispam
					elif in_front(set_long_word_antispam_str, msg):
						set_value(self, "long_word_antispam", "long word antispam", msg_arr)
					
					else:
						send_str = "Usage: \"!set <feature> on/off \"." 
						whisper(user, send_str)
						return	
				else:
					#usage
					send_str = "Usage: \"!set <feature> on/off \"." 
					whisper(user, send_str)
					return
				#just set_str, explain usage.
				if set_str == msg:
					send_str = "Turn features on or off. Usage: \"!set <feature> on/off \"." 
					whisper(user, send_str)
					return
			else:
				#not mod
				send_str = "You have to be a mod to use !set commands." 
				whisper(user, send_str)
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
		vote_on = get_status(self, "vote_dict")
		if in_front(vote_str, msg) and is_mod(user, self.channel_parsed, user_type) and vote_on:
			if not in_front(poll_start_str, msg):
				send_str = "There are no ongoing votes." 
				self.write(send_str)
				return
			
		if in_front(vote_str, msg) or in_front(poll_str, msg):
			if len(msg_arr) >= 2:
				if in_front(poll_start_str, msg):
					if len(msg_arr) >= 3:
						if is_mod(user, self.channel_parsed, user_type):
							#reset vote stuffs
							if vote_on:#if already ongoing poll
								send_str = "There is already an ongoing poll." 
							else:
								clear_table(self, "votes")
								vote_option_arr = msg_arr[2].split(",")
								for vote_option in vote_option_arr:
									if vote_option in vote_cmd_arr:
										send_str = "You cannot use default vote commands as poll options"
										break
								else:
									vote_option_table = get_table(self, "vote_options")
									if len(vote_option_table) > 1:
										set_status(self, "vote_dict", True)
										send_str = "Poll opened! To vote use !vote <option/index>." 
										for vote_option_index, vote_option in enumerate(vote_option_table): 
											insert_data(self, "votes", ["option", "votes", "users"], [vote_option.strip(), 0, []])
										self.write(send_str)
										
										send_str = "Current poll options are: "
										for vote_option_index, vote_option in enumerate(vote_option_table):
											if vote_option_index != len(vote_option_table) -1:
												send_str += "(%s.) %s, " % (vote_option_index + 1, vote_option)
											else:
												send_str += "(%s.) %s." % (vote_option_index + 1, vote_option)	
										self.write(send_str)
										return 
									else:
										send_str = "You must specify more than one option for a poll."
						else:
							send_str = "You have to be a mod to start a poll." 
							whisper(user, send_str)
							return
					else:
						send_str = "Usage: !poll start <option1, option2, ...>" 
						whisper(user, send_str)
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
						whisper(user, send_str)
						return
					if not is_mod(user, self.channel_parsed, user_type):
						whisper(user, send_str)		
						return
				elif in_front(poll_reset_str, msg):
					if is_mod(user, self.channel_parsed, user_type):
						query = "UPDATE votes SET votes = 0, users = []"
						self.conn.execute(query)
						send_str = "Votes reset."
						self.write(send_str)
						return 
					else:
						send_str = "You have to be a mod to reset the poll votes." 
						whisper(user, send_str)
						return
				elif in_front(poll_stats_str, msg):
					if ote_on:
						if self.vote_total != 0:
							send_str = "Current poll stats: "
							votes_table = get_table(self, "votes")
							for pair in votes_table:
								key = pair[0]
								value = pair[1]
								vote_perc = round((float(value) / self.vote_total) * 100, 2)
								vote_perc = simplify_num(vote_perc)
								send_str += "%s: %s%% " % (key, vote_perc)
							send_str += "Total votes: %s" % self.vote_total
							self.write(send_str)
							poll_winner = [['', 0]]
							for pair in votes_table:
								key = pair[0]
								value = pair[1]
								option_perc = (float(poll_winner[0][1])/self.vote_total * 100)
								option_perc = simplify_num(option_perc)
								if value == poll_winner[0][1]:
									poll_winner.append([key, value])
								elif value > poll_winner[0][1]:
									poll_winner = [[key, value]]
							winner_perc = round(float(poll_winner[0][1])/self.vote_total * 100, 2)
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
						send_str = "There are no ongoing polls." 
						
					if not is_mod(user, self.channel_parsed, user_type):
						whisper(user, send_str)		
						return
				elif in_front(vote_remove_str, msg):
					votes_table = get_table(self, "votes")
					for row_index, row in enumerate(votes_table):
						if user in row["users"]:
							print row
							###########3
							#need to convert to list, remove, then update set the new array once we start da debugs
							###########
							row["users"].remove(user)
							query = "UPDATE votes SET votes = votes-1 WHERE `index` = %s" % row["index"]
							self.conn.execute(query)
							self.vote_total -=1
							send_str = "Vote removed."
							whisper(user, send_str)
							break
					else:
						send_str = "You have not yet voted for an option."
						whisper(user, send_str)
					return						
				elif in_front(poll_end_str, msg) or in_front(poll_close_str, msg):
					#close the vote
					if is_mod(user, self.channel_parsed, user_type):
						if vote_on:
							set_status(self, "vote_dict", False)
							send_str = "Poll stats: " 
							if self.vote_total != 0:
								votes_table = get_table(self, "votes")
								poll_winner = [['', 0]]
								for pair in self.vote_arr:
									key = pair[0]
									value = pair[1]
									option_perc = round(float(value)/self.vote_total * 100, 2)
									option_perc = simplify_num(option_perc)
									if value == poll_winner[0][1]:
										poll_winner.append([key, value])
									elif value > poll_winner[0][1]:
										poll_winner = [[key, value]]
									send_str += "%s: %s%% " % (key, option_perc)
								send_str += "Total votes: %s" % self.vote_total
								self.write(send_str)
								winner_perc = round(float(poll_winner[0][1])/self.vote_total * 100, 2)
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
						else:
							send_str = "There are no ongoing polls."
					else:
						send_str = "You have to be a mod to end a poll." 
						whisper(user, send_str)
						return
				else:
					vote_options_table = get_table(self, "vote_options")
					if msg_arr[1].strip() in vote_options_table: 		
						votes_table = get_table(self, "votes")
						#msg_arr[1] is a vote option
						#input vote if user hasnt already voted
						for row_index, row in enumerate(votes_table):
							if msg_arr[1] == row["option"]:
								#do nothing if they are already in it, if not then find add them and remove them from the one they used to be in
								#convert row["users"] to list here again
								if user not in row["users"]:
									query = "UPDATE votes SET votes = votes+1 WHERE `index` = %s" % row["index"]
									self.conn.execute(query)
									#convert to list and add then update
									votes_table[vote_option_index]["users"].append(user)
									self.vote_total+=1
									#if it's not the option they want and they are in it then remove them
									for old_row_index, old_row in enumerate(votes_table):
										#convert the users to list
										if old_row["option"] != msg_arr[1] and user in old_row["users"]:
											old_row[old_row_index]["users"].remove(user)
											query = "UPDATE votes SET votes = votes-1 WHERE `index` = %s" % old_row["index"]
											self.conn.execute(query)
											self.vote_total-=1
											send_str = "Vote changed."
											whisper(user, send_str)
											break
									else:
										send_str = "Vote added."
										whisper(user, send_str)
									return
								elif user in vote_option[2]:
									send_str = "You have already voted for that option"
									whisper(user, send_str)
									return#save some time, end this loop if they are already in the option they selected
								break#this actually shouldn't be possible
						else:
							send_str = "Invalid vote option"
							whisper(user, send_str)
						return 
							
					elif is_num(msg_arr[1].strip()):
						vote_choice_index = int(msg_arr[1])
						votes_table = get_table(self, "votes")
						if vote_choice_index > 0 and vote_choice_index <= len(votes_table):
							for row_index, row in enumerate(votes_table):
								#do nothing if they are already in it, if not then find add them and remove them from the one they used to be in
								if vote_choice_index == row_index+1:
									#convert to list
									if user not in row["users"]:
										query = "UPDATE votes SET votes = votes+1 WHERE `index` = %s" % row["index"]
										self.conn.execute(query)
										#add to list then update set
										self.vote_arr[vote_option_index][2].append(user)
										self.vote_total+=1
										#if it's not the option they want and they are in it then remove them
										for old_row_index, old_row in enumerate(votes_table):
											#convert to list(maybe not necessary?)
											if old_row_index != vote_choice_index-1 and user in old_row["users"]:
												self.vote_arr[old_vote_option_index][2].remove(user)
												query = "UPDATE votes SET votes = votes-1 WHERE `index` = %s" % old_row["index"]
												self.conn.execute(query)
												self.vote_total-=1
												send_str = "Vote changed."
												whisper(user, send_str)
												break
										else:
											send_str = "Vote added."
											whisper(user, send_str)
										return
									elif user in row["users"]:
										send_str = "You have already voted for that option"
										whisper(user, send_str)
										return#save some time, end this loop if they are already in the option they selected
									break#also shouldnt be kimpossible		
							return 
						else:
							send_str = "Invalid index for vote choice."
							whisper(user, send_str)
							return
					else:
						if is_mod(user, self.channel_parsed, user_type):
							send_str = "Usage: !poll start/stats/reset/end/close" 
							
						else:
							send_str = "Usage: !vote <option/index>"
						whisper(user, send_str)
						return
			else:
				if is_mod(user, self.channel_parsed, user_type):
					send_str = "Usage: !poll start/reset/stats/end/close" 
				else:
					send_str = "Usage: !vote <option/index>"
				whisper(user, send_str)
				return
		elif vote_str == msg:
			send_str = "Usage: !vote <option/index>"
			whisper(user, send_str)
			return
		else:
			return False
		self.write(send_str)
		
	def raffle_parse(self, user, msg, channel_parsed, user_type):
		#raffle
		raffle_str = "!raffle"
		start_raffle_str = "!raffle start"
		end_raffle_str = "!raffle end"
		
		if in_front(raffle_str, msg):
			if get_status(self, "raffle"):
				#avoid duplicates
				if raffle_str == msg and not check_duplicate(self, "lottery", ["user"], [user]):
					insert_data(self, "raffle", ["user"], [user])
					send_str = "You have been added to the raffle."
					whisper(user, send_str)
					return
				elif start_raffle_str == msg:
					if is_mod(user, self.channel_parsed, user_type):
						send_str = "There is already an ongoing raffle." 
					else:
						send_str = "Only mods can start raffles." 
						whisper(user, send_str)
						return
					
				elif end_raffle_str == msg:
					if is_mod(user, self.channel_parsed, user_type):
						raffle_table = get_table(self, "raffle")
						if len(raffle_table) > 0:
							winner = raffle_table[random.randint(0, (len(raffle_table) - 1))]["user"]
							point_change(self, winner, self.raffle_point_value)
							if self.lottery_point_value != 1:
								send_str = "%s has won the raffle and obtained %s points!" % (winner, self.raffle_point_value)
							else:
								send_str = "%s has won the raffle and obtained %s point!" % (winner, self.raffle_point_value)
							whisper_str = "You now have %s points in this channel." % point_balance(self, winner)
							whisper(winner, whisper_str)
						else:
							send_str = "No one joined the raffle, there is no winner." 
						set_status(self, "raffle", False)
						clear_table(self, "raffle")
						
					else:
						send_str = "Only mods can end raffles." 
						whisper(user, send_str)
						return
				else:
					if is_mod(user, channel_parsed, user_type):
						send_str = "Usage: !raffle start/end <point value>"
					else:
						send_str = "Only mods can use !raffle commands"
					whisper(user, send_str)
					return
			else:
				if in_front(start_raffle_str, msg):
					if is_mod(user, self.channel_parsed, user_type):
						set_status(self, "raffle", True)
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
						whisper(user, send_str)
						return
				elif raffle_str == msg and is_mod(user, self.channel_parsed, user_type):
					send_str = "Usage: !raffle start/end" 
					whisper(user, send_str)
					return
				elif in_front(end_raffle_str, msg):
					if is_mod(user, self.channel_parsed, user_type):
						send_str = "No ongoing raffles."
						self.write(send_str)	
					else:
						send_str = "Only mods can end raffles." 
						whisper(user, send_str)
						return
				else:
					send_str = "Usage: !raffle start/end" 
					whisper(user, send_str)
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
			if get_status(self, "lottery"):
				if start_lottery_str == msg:
					if is_mod(user, self.channel_parsed, user_type):
						send_str = "There is already an ongoing lottery." 
					else:
						send_str = "Only mods can start lotteries." 
						whisper(user, send_str)
						return
				elif end_lottery_str == msg:
					if is_mod(user, self.channel_parsed, user_type):
						chatters_json = get_json_chatters(channel_parsed)
						#if chatters_json["chatters"]["viewers"]:#should be run in an existing channel so this should always be true
						extend_data(self, "lottery", ["user"], chatters_json["chatters"]["viewers"])
						extend_data(self, "lottery", ["user"], chatters_json["chatters"]["moderators"])
						lottery_table = get_table(self, "lottery")
						if len(lottery_table) > 0:
							winner = lottery_table[random.randint(0, (len(lottery_table) - 1))]["user"].encode("utf-8")
							point_change(self, winner, self.lottery_point_value)
							if self.lottery_point_value != 1:
								send_str = "%s has won the lottery and obtained %s points!" % (winner, self.lottery_point_value)
							else:
								send_str = "%s has won the lottery and obtained %s point!" % (winner, self.lottery_point_value)
							whisper_str = "You now have %s points in this channel." % point_balance(self, winner)
							whisper(winner, whisper_str)
						else:
							send_str = "No one joined the lottery, there is no winner." 
						set_status(self, "lottery", False)
						clear_table(self, "lottery")
						
					else:
						send_str = "Only mods can end lotteries." 
						whisper(user, send_str)
						return
				else:
					if is_mod(user, channel_parsed, user_type):
						send_str = "Usage: !lottery start/end <point value>"
					else:
						send_str = "Only mods can use !lottery commands"
					whisper(user, send_str)
					return
				self.write(send_str)
			else:
				if in_front(start_lottery_str, msg):
					if is_mod(user, self.channel_parsed, user_type):
						set_status(self, "lottery", True)
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
						whisper(user, send_str)
						return
					self.write(send_str)
				elif lottery_str == msg and is_mod(user, self.channel_parsed, user_type):
					send_str = "Usage: !lottery start/end" 
					whisper(user, send_str)
					return
				elif in_front(end_lottery_str, msg):
					if is_mod(user, self.channel_parsed, user_type):
						send_str = "No ongoing lotteries."
						self.write(send_str)	
					else:
						send_str = "Only mods can end lotteries." 
						whisper(user, send_str)
						return
				else:
					send_str = "Usage: !lottery start/end" 
					whisper(user, send_str)
					return
		else:
			return False
			
	def roulette_parse(self, user, msg, channel_parsed, user_type):
		#roulette
		#if user is mod then say it doesnt kill you or something
		#should absolutely just make the chance input in the GUI rather than text based.
		rol_str = "!roulette"
		rol_chance_str = "!roulette chance"
		
		if get_status(self, "roulette"):
			if in_front(rol_str, msg):
				if rol_str == msg:
					#trigger roulette - allow custom messages for win/loss to replace default ones
					send_str = "/me places the revolver to %s's head" % (user)
					self.write(send_str)
					time.sleep(1)
					if random.random() < self.rol_chance:
						#time out the user(ban from chat) for rol_timeout amount of seconds
						if is_mod(user, self.channel_parsed, user_type) == False:
							timeout(user, self, self.rol_timeout)
							send_str = "The trigger is pulled, and the revolver fires! %s lies dead in chat" % (user)
						else:
							send_str = "The gun jams thanks to your super mod powers. %s lives!" % (user)
					else:
						#do nothing, notify of victory
						send_str = "The trigger is pulled, and the revolver clicks. %s has lived to survive roulette!" % (user)
					self.write(send_str)
				elif in_front(rol_chance_str, msg):
					if is_mod(user, self.channel_parsed, user_type):
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
							whisper(user, send_str)
							return
					else:
						send_str = "Only mods can change the chance of the roulette." 
						whisper(user, send_str)
						return
					self.write(send_str)
				else:
					if is_mod(user, self.channel_parsed, user_type):
						send_str = "Usage: !roulette chance <percent chance>" 
						whisper(user, send_str)
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
		if get_status(self, "8ball_responses"):
			if in_front(ball_str, msg):
				msg_arr = msg.split(" ", 2)
				if in_front(ball_add_str, msg):
					if is_mod(user, self.channel_parsed, user_type):
						if len(msg_arr) > 2:#need to have this if statement more often
							ball_response = msg_arr[2]
							if ball_response not in self.ball_arr:
								self.ball_arr.append(ball_response)
								send_str = "\"%s\" added to list of 8ball responses." % (ball_response)
							else:
								send_str = "%s is already an 8ball response." % (ball_response)
						else:
							send_str = "Usage: \"!8ball add <8ball response>\"" 
						self.write(send_str)
					else:
						send_str = "You have to be a mod to use \"!8ball add\"."
						whisper(user, send_str)
					return
				elif in_front(ball_del_str, msg) or in_front(ball_rem_str, msg):
					if is_mod(user, channel_parsed, user_type):
						if len(msg_arr) > 2:
							ball_response = msg_arr[2]
							if is_num(ball_response):
								#we add on one to the actual index because users prefer to start with 1, rather than 0.
								ball_response = int(ball_response)
								if ball_response > 0 and ball_response <= len(self.ball_arr):
									send_str = "8Ball response \"%s\" removed at index %s." % (self.ball_arr[ball_response-1], ball_response)
									del self.ball_arr[ball_response-1]
								else:
									send_str = "Invalid index for 8ball response removal." 
							else:
								if ball_response in self.ball_arr:
									self.ball_arr.remove(ball_response)
									send_str = "8Ball response \"%s\" removed." % (ball_response)									
								else:
									send_str = "Specified 8ball response does not exist." 
						else:
							send_str = "Usage: \"!8ball delete/remove <8ball response/index>\"" 
						self.write(send_str)
					else:
						send_str = "You have to be a mod to use \"!8ball delete/remove\"."
						whisper(user, send_str)
					return
				elif in_front(ball_list_str, msg):
					if is_mod(user, channel_parsed, user_type):
						if len(self.ball_arr) > 0:
							send_str = "Current 8ball responses: " 
							for ball_response in range(len(self.ball_arr)):
								if (ball_response != len(self.ball_arr) -1):
									#if not last response in arr
									send_str += "(%s.) %s, " % (ball_response+1, self.ball_arr[ball_response])
								else:
									send_str += "(%s.) %s." % (ball_response+1, self.ball_arr[ball_response])
								#this accounts for any messages longer than the character cap
								
							self.write(send_str)
						else:
							send_str = "There are currently no 8ball responses." 
							self.write(send_str)
					else:
						send_str = "You have to be a mod to use \"!8ball clear\"."
						whisper(user, send_str)
					return
				elif ball_clr_str == msg:
					if is_mod(user, self.channel_parsed, user_type): 
						if len(self.ball_arr) > 0:
							clear_table(self, "8ball_responses")
							send_str = "All 8ball responses removed." 
						else:	
							send_str = "There are currently no 8ball responses." 
						self.write(send_str)
					else:
						send_str = "You have to be a mod to use \"!8ball clear\"."
						whisper(user, send_str)
						return
					return
				elif ball_str == msg:
					if is_mod(user, self.channel_parsed, user_type):
						send_str = "Usage: \"!8ball add/delete/remove/list/clear/<question>\"" 
						whisper(user, send_str)
					else:
						send_str = "You have to be a mod to use \"!8ball clear\"."
						whisper(user, send_str)
					return
						
				else:#so we don't respond when using the 8ball commands
					if "?" in msg: #and msg.rstrip().endswith("?") <-- is this better?
						msg_arr = msg.split(" ", 1)
						if len(msg_arr) == 2:
							if len(self.ball_arr) > 0:
								ball_response_index = random.randint(0, len(self.ball_arr)-1)
								ball_response = self.ball_arr[ball_response_index]
								send_str = "Magic 8 ball says... %s" % (ball_response)
							else:
								send_str = "There are currently no 8ball responses." 
								whisper(user, send_str)
								return
						elif ball_str == msg:
							send_str = "Get the Magic 8 Ball to answer your question. Usage: \"!8ball <question> \"."
							whisper(user, send_str)
							return
						else:
							send_str = "Usage: \"!8ball <question>? \"." 
							whisper(user, send_str)
							return
					else:
						send_str = "Usage: \"!8ball <question>? \"." 
						whisper(user, send_str)
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
				send_str = "@%s has been live for: %s" % (self.channel_parsed, get_uptime_str(self.channel_parsed))
			elif len(msg_arr) > 1:
				uptime = get_uptime_str(msg_arr[1])
				if uptime:
					send_str = "%s has been live for: %s" % (msg_arr[1], get_uptime_str(msg_arr[1]))
				else:
					send_str = "%s is not an active channel." % msg_arr[1]
			self.write(send_str)
		else:
			return False
	
	def general_channel_stats_parse(self, user, msg, channel_parsed, user_type, stat_str):
		find_stat_str = "!" + stat_str
		if in_front(find_stat_str, msg):
			msg_arr = msg.split()
			if len(msg_arr) == 1:
				if stat_str == "chatters":
					stat_data = get_json_chatters(channel_parsed.lower().strip())
					stat_count = stat_data["chatter_count"]
					send_str = "There are currently %s accounts in chat." % (stat_count)
				elif stat_str == "viewers":
					stat_data = get_json_stream(channel_parsed.lower().strip())
					stat_count = stat_data["streams"][0]["viewers"]
					send_str = "There are currently %s viewers in the channel." % (stat_count)
				elif stat_str == "views":
					stat_data = get_json_views_follows(channel_parsed.lower().strip())
					stat_count = stat_data["views"]
					send_str = "This channel has %s views." % (stat_count)
				elif stat_str == "followers":
					stat_data = get_json_views_follows(channel_parsed.lower().strip())
					stat_count = stat_data["followers"]
					send_str = "This channel has %s followers." % (stat_count)
			elif len(msg_arr) > 1:
				stat_channel = msg_arr[1]
				
				if stat_str == "chatters":
					stat_data = get_json_chatters(stat_channel.lower().strip())
					stat_count = stat_data["chatter_count"]
				elif stat_str == "viewers":
					stat_data = get_json_stream(stat_channel.lower().strip())
					stat_count = stat_data["streams"]
				elif stat_str == "views":
					stat_data = get_json_views_follows(stat_channel.lower().strip())
					stat_count = stat_data["views"]
				elif stat_str == "followers":
					stat_data = get_json_views_follows(stat_channel.lower().strip())
					stat_count = stat_data["followers"]
					
				if stat_count:
					if stat_str == "viewers":
						stat_count = stat_data[0]["viewers"]
						
					stat_count = prettify_num(stat_count)
					if stat_channel.rstrip().endswith("s"):
						stat_channel = stat_channel + "'"
					else:	
						stat_channel = stat_channel + "'s"
				
					if stat_str == "chatters":
						send_str = "There are currently %s accounts in %s chat." % (stat_count, stat_channel)
					elif stat_str == "viewers":
						send_str = "There are currently %s viewers in %s channel." % (stat_count, stat_channel)
					elif stat_str == "views":
						send_str = "There are currently %s views in %s channel." % (stat_count, stat_channel)
					elif stat_str == "followers":
						send_str = "%s channel has %s followers." % (stat_channel.capitalize(), stat_count)
				else:
					send_str = "%s is not an active channel." % msg_arr[1]
			else:
				send_str = "Usage: \"%s <channel>\"" % find_stat_str
				
			if is_mod(user, channel_parsed, user_type):
				self.write(send_str)
			else:	
				whisper(user, send_str)
		else:
			return False
	
	def channel_stats_parse(self, user, msg, channel_parsed, user_type):
		chan_stats_str = "!chanstats"
		if in_front(chan_stats_str, msg):
			msg_arr = msg.split(" ")
			if len(msg_arr) == 1:
				stat_data = get_json_stream(channel_parsed.lower().strip())
				stat_data= stat_data["streams"]
				if stat_data:
					game = get_data(self, "game", ["game"])
					if game != '':
						send_str = "%s is playing %s for %s viewers." % (channel_parsed.capitalize(), game, stat_data[0]["viewers"])
					else:
						send_str = "%s is not playing a game, however there are %s viewers" % (channel_parsed.capitalize(), stat_data[0]["viewers"])
				else:
					send_str = "%s is currently offline." % channel_parsed.capitalize()
				if not is_mod(user, channel_parsed, user_type):
					whisper(user, send_str)
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
				if not is_mod(user, channel_parsed, user_type):
					whisper(user, send_str)
					return
			else:
				send_str = "Usage: !chanstats <channel>"
				whisper(user, send_str)
				return
			self.write(send_str)
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
				
			if is_mod(user, channel_parsed, user_type):
				self.write(send_str)
			else:	
				whisper(user, send_str)
		else:
			return False
			
	def commercial_parse(self, user, msg, channel_parsed, user_type):
		#commercials
		comm_str = "!commercial"
		if comm_str == msg:
			if is_streamer(user, self.channel_parsed):
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
						whisper(user, send_str)
						return
				else:
					#display usage
					send_str = "Usage: !commercial <length of commercial>"
					whisper(user, send_str)
					return
			else:
				#not mod
				send_str = "You have to be the current streamer in order to start commercials." 
				whisper(user, send_str)
				return
			self.write(send_str)
		else:
			return False
	
	def ban_emote_parse(self, user, msg, channel_parsed, user_type):
		#ban emotes
		#gonna make it bulk remove special emotes if one is selected for banning/unbanning, will allow disabling of this feature in GUI.
		#should add a regex option, as well as the bulk and individual
		ban_emote_str = "!ban emote"
		ban_emote_add_str = "!ban emote add"
		ban_emote_del_str = "!ban emote delete"
		ban_emote_rem_str = "!ban emote remove"
		ban_emote_list_str = "!ban emote list"
		ban_emote_clr_str = "!ban emote clear"
		
		if self.ban_emote_on:
			msg_arr = msg.split(" ")
			if in_front(ban_emote_str, msg):
				if in_front(ban_emote_add_str, msg):
					if is_mod(user, channel_parsed, user_type):
						if len(msg_arr) > 3:
							ban_emote = msg_arr[3]
							if is_emote(ban_emote, self.emote_arr):
								if ban_emote in self.special_emote_arr:#bulk adding of specials	#['o_O', 'O_o', 'o_o', 'O_O', ':o', ':O', ':\\', ':/', ':p', ':P', ';p', ';P']
									for ban_emote_variant in self.ban_emote_arr:#special dupes, will need to change this when the bulk/individual checkbox is enabled.
										if isinstance(ban_emote_variant, list):
											if ban_emote in ban_emote_variant:
												send_str = "%s variants are already banned." % (ban_emote)
												break
									else:
										if ban_emote in ['o_O', 'O_o', 'o_o', 'O_O']:
											self.ban_emote_arr.append(['o_O', 'O_o', 'o_o', 'O_O'])
										elif ban_emote in [':o', ':O']:
											self.ban_emote_arr.append([':o', ':O'])
										elif ban_emote in [':\\', ':/']:
											self.ban_emote_arr.append([':\\', ':/'])
										elif ban_emote in [':p', ':P']:
											self.ban_emote_arr.append([':p', ':P'])
										elif ban_emote in [';p', ';P']:
											self.ban_emote_arr.append([';p', ';P'])
										#else shouldnt occur										
										#self.ban_emote_arr.append(ban_emote)
										send_str = "%s variants added to list of banned emotes." % (ban_emote)
								else:
									if ban_emote not in self.ban_emote_arr:#dupes
										self.ban_emote_arr.append(ban_emote)
										send_str = "%s added to list of banned emotes." % (ban_emote)
									else:
										send_str = "%s is already a banned emote." % (ban_emote)
							else:
								send_str = "%s is not a valid emote." % (ban_emote)
						else:
							send_str = "Usage: \"!ban emote add <emote>\"" 
							whisper(user, send_str)
							return
					else:
						send_str = "You have to be a mod to use \"!ban emote add\"."
						whisper(user, send_str)
						return
				elif in_front(ban_emote_del_str, msg) or in_front(ban_emote_rem_str, msg):
					if is_mod(user, channel_parsed, user_type):
						if len(msg_arr) > 3:
							ban_emote = msg_arr[3]
							if is_num(ban_emote):
								#we add on one to the actual index because users prefer to start with 1, rather than 0.
								ban_emote = int(ban_emote)
								if ban_emote > 0 and ban_emote <= len(self.ban_emote_arr):
									if isinstance(self.ban_emote_arr[ban_emote-1], list):
										send_str = "Ban emote %s variants removed." % (self.ban_emote_arr[ban_emote-1][0])
										'''for ban_emote_variant_index, ban_emote_variant in enumerate(self.ban_emote_arr[ban_emote-1]):
											if ban_emote_variant_index == len(self.ban_emote_arr[ban_emote-1])-1:
												#last element
												send_str += "and \"%s\" removed at index %s." % (ban_emote_variant, ban_emote_variant_index)
											else:
												send_str += "\"%s\", " % ban_emote_variant'''
									else:
										send_str = "Ban emote %s removed at index %s." % (self.ban_emote_arr[ban_emote-1], ban_emote)
									del self.ban_emote_arr[ban_emote-1]									
								else:
									send_str = "Invalid index for emote removal." 
							else:
								if ban_emote in self.ban_emote_arr:
									send_str = "Ban emote %s removed." % (ban_emote)									
									self.ban_emote_arr.remove(ban_emote)
								elif ban_emote in self.special_emote_arr:
									for ban_emote_variant in self.ban_emote_arr:
										if isinstance(ban_emote_variant, list) and ban_emote in ban_emote_variant:
											send_str = "Ban emote %s variants removed." % (ban_emote)
											self.ban_emote_arr.remove(ban_emote_variant)
											break
								else:
									send_str = "Specified ban emote does not exist." 
						else:
							send_str = "Usage: \"!ban emote delete/remove <emote/index>\"" 
							whisper(user, send_str)
							return
					else:
						send_str = "You have to be a mod to use \"!ban emote delete/remove\"."
						whisper(user, send_str)
						return	
				elif in_front(ban_emote_list_str, msg):
					if len(self.ban_emote_arr) == 0:
						send_str = "No active ban emotes." 
					else:
						send_str = "Active ban emotes: " 
						for ban_emote in range(len(self.ban_emote_arr)):
							if (ban_emote != len(self.ban_emote_arr) -1):
								#every element but last one
								if isinstance(self.ban_emote_arr[ban_emote], list):
									send_str += "(%s.) %s variants, " % (ban_emote+1, self.ban_emote_arr[ban_emote][0])
								else:
									send_str += "(%s.) %s, " % (ban_emote+1, self.ban_emote_arr[ban_emote])
							else:
								#last element in arr
								if isinstance(self.ban_emote_arr[ban_emote], list):
									send_str += "(%s.) %s variants." % (ban_emote+1, self.ban_emote_arr[ban_emote][0])
								else:
									send_str += "(%s.) %s ." % (ban_emote+1, self.ban_emote_arr[ban_emote])
					if not is_mod(user, self.channel_parsed, user_type):
						whisper(user, send_str)		
						return
				elif in_front(ban_emote_clr_str, msg):
					if is_mod(user, self.channel_parsed, user_type): 
						self.ban_emote_arr = []
						send_str = "All ban emotes removed." 
					else:
						send_str = "You have to be a mod to use \"!ban emote clear\"."
						whisper(user, send_str)
						return	
				elif ban_emote_str == msg:
					if is_mod(user, self.channel_parsed, user_type): 
						send_str = "Add or remove ban emotes to timeout users who say them. Syntax and more information can be found in the documentation." 
					else:
						send_str = "You have to be a mod to use \"!ban emote delete/remove\"."
						whisper(user, send_str)
						return	
				else:
					if is_mod(user, channel_parsed, user_type):
						send_str = "Usage: \"!ban emote add/delete/remove/list/clear\"" 
					else:
						send_str = "Usage: \"!ban emote list\"" 
					whisper(user, send_str)
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
		
		if get_status(self, "repeats"):
			if in_front(repeat_str, msg):
				if in_front(repeat_add_str, msg):
					if is_mod(user, channel_parsed, user_type):
						msg_arr = msg.split(" ")
						if len(msg_arr) > 3:
							del msg_arr[0:2]#remove command specifiers
							repeat_cmd = ''
							for cmd_part in range(len(msg_arr)):
								if cmd_part == len(msg_arr)-2 and msg_arr[cmd_part+1] in self.time_unit_arr:#if unit of time specified
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
								repeat_set = [current_time, repeat_cmd, repeat_interval]
								#add the new set to the database
								insert_data(self, "repeats", ["set_time", "phrase", "`interval`"], repeat_set)
								send_str = "Repeat command \"%s\" added with interval %s." % (repeat_cmd, parse_sec_condensed(repeat_interval))
							else:
								send_str = "No \".disconnect\" or \"/disconnect\" variants allowed."
						else:
							send_str = "Usage: !repeat add <command> <interval>" 
							whisper(user, send_str)
							return
					else:
						send_str = "You have to be a mod to use \"!repeat add\"." 
						whisper(user, send_str)
						return
				elif in_front(repeat_del_str, msg) or in_front(repeat_rem_str, msg):
					if is_mod(user, channel_parsed, user_type):
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) > 2:
							repeat_cmd = msg_arr[2]
							if is_num(repeat_cmd):
								repeat_cmd = int(repeat_cmd)
								delete_status = delete_index_handler(self, "repeats", repeat_cmd)
								if delete_status:
									send_str = "Repeat command \"%s\" with interval %s removed at index %s." % (delete_status["phrase"], parse_sec_condensed(delete_status["interval"]), repeat_cmd)
									#return the row that was deleted if 
								else:
									send_str = "Invalid index for repeat command removal." 
							else:
								delete_status = delete_value_handler(self, "repeats", "phrase", repeat_cmd)
								if delete_status:
									send_str = "Repeat command \"%s\" with interval %s removed." % (repeat_cmd, parse_sec_condensed(delete_status["interval"]))		
								else:
									send_str = "Specified repeat command does not exist." 
						else:
							send_str = "Usage: !repeat delete/remove <command/index>" 
							whisper(user, send_str)
							return
					else:
						send_str = "You have to be a mod to use \"!repeat delete/remove\"." 
						whisper(user, send_str)
						return
				elif repeat_list_str == msg:
					repeats_table = get_table(self, "repeats")
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
					if not is_mod(user, self.channel_parsed, user_type):
						whisper(user, send_str)		
						return			
				elif repeat_clr_str == msg:
					if is_mod(user, self.channel_parsed, user_type): 
						clear_table(self, "repeats")
						send_str = "All repeat commands removed." 
					else:
						send_str = "You have to be a mod to use \"!repeat clear\"." 
						whisper(user, send_str)
						return
				elif repeat_str == msg:
					send_str = "Add or remove commands to be repeated every specified interval. Syntax and more information can be found in the documentation." 
					whisper(user, send_str)
					return
				else:
					if is_mod(user, channel_parsed, user_type):
						send_str = "Usage: !repeat add/delete/remove/list/clear <command> <interval>" 
					else:
						send_str = "Usage: !repeat list" 
					whisper(user, send_str)
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
		cmd_on = get_status(self, "commands")
		if cmd_on:
			if in_front(cmd_str, msg):
				#add commands
				if in_front(cmd_add_str, msg):
					if is_mod(user, channel_parsed, user_type):
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) == 3:
							if ":" in msg_arr[2] and in_front("!", msg_arr[2]):
								cmd_msg_arr = msg_arr[2].split(":", 1)
								if len(cmd_msg_arr) == 2:
									cmd_phrase = cmd_msg_arr[0].rstrip().lstrip()
									cmd_reply = cmd_msg_arr[1].rstrip().lstrip()
									if cmd_phrase in self.default_cmd_arr:#dont add something that is already a default command
										send_str = "%s is already a default command." % (cmd_phrase)
									else:
										cmd_pair = [cmd_phrase, cmd_reply]
										if check_duplicate(self, table, ["command", "reply"], cmd_pair):
											send_str = "%s is already a custom command." % (cmd_phrase)
										else:
											if not disconnect_cmd(cmd_reply):
												insert_data(self, "commands", ["command", "reply"], cmd_pair)
												send_str = "Command \"%s\" added, with reply \"%s\"." % (cmd_phrase, cmd_reply)
											else:
												send_str = "No \".disconnect\" or \"/disconnect\" variants allowed."
								else:
									#incorrectly formatted, display usage
									send_str = "Usage: \"!command add !<command>:<reply>\"." 
									whisper(user, send_str)
									return	
							else:
								#incorrectly formatted, display usage
								send_str = "Usage: \"!command add !<command>:<reply>\"." 
								whisper(user, send_str)
								return
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!command add !<command>:<reply>\"."
							whisper(user, send_str)
							return
					else:
						send_str = "You have to be a mod to use \"!command add\"." 
						whisper(user, send_str)
						return
				#delete commands
				elif in_front(cmd_del_str, msg) or in_front(cmd_rem_str, msg):
					if is_mod(user, channel_parsed, user_type):
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) == 3:
							cmd_phrase = msg_arr[2]
							if is_num(cmd_phrase):
								cmd_phrase = int(cmd_phrase)
								delete_status = delete_index_handler(self, "commands", cmd_phrase)
								if delete_status:
									send_str = "Command %s:%s removed at index %s." % (delete_status["command"], delete_status["reply"], cmd_phrase)
								else:
									send_str = "Invalid index for command removal." 
							
							else:
								delete_status = delete_value_handler(self, "repeats", "phrase", repeat_cmd)
								if delete_status:
									send_str = "Command %s:%s removed." % (delete_status["command"], delete_status["reply"])	
								else:
									send_str = "Specified command does not exist." 
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!command delete/remove <command/index>\"." 
					else:
						send_str = "You have to be a mod to use \"!command delete/remove\"." 
						whisper(user, send_str)
						return
				#list commands
				elif cmd_list_str == msg:
					#check to make sure there are commands to list
					cmd_table = get_table(self, "commands")
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
							
					if not is_mod(user, self.channel_parsed, user_type):
						whisper(user, send_str)		
						return
				#clear commands
				elif cmd_clr_str == msg:
					if is_mod(user, channel_parsed, user_type):
						clear_table(self, "commands")
						send_str = "All custom commands removed." 
					else:
						send_str = "You have to be a mod to use \"!command clear\"." 
						whisper(user, send_str)
						return
				#just cmd string, display usage
				elif cmd_str == msg:
					send_str = "Add or remove custom commands. Syntax and more information can be found in the documentation." 
					whisper(user, send_str)
					return
				else:
					if is_mod(user, channel_parsed, user_type):
						send_str = "Usage: !command add/delete/remove/list/clear" 
					else:
						send_str = "Usage: !command list." 
					whisper(user, send_str)
					return
				self.write(send_str)
			else:	
				################################################################################
				####THIS NEEDS TO NOT BE IS MOD BUT DEPEND ON THE LEVEL PARAMETER OF THE COMMAND
				################################################################################
				if cmd_on:
					for cmd_pair in self.cmd_arr:
						try:
							cmd_index = msg.index(cmd_pair[0])
							#if msg did contain the custom command
							if is_mod(user, channel_parsed, user_type):
								reply = cmd_pair[1]
								for word in reply.split():
									if word in self.reply_args_arr:
										if word == "{*USER*}":
											reply = reply.replace("{*USER*}", user)
										elif word == "{*TO_USER*}":
											to_user_part = msg[cmd_index+len(cmd_pair[0]):len(msg)]#all the elements after the autoreply
											reply_to_user = to_user_part.split()[0]#the first word after the autoreply, should be the to user
											reply = reply.replace("{*TO_USER*}", str(reply_to_user))
										elif word == "{*GAME*}":
											reply = reply.replace("{*GAME*}", get_data(self, "game", ["game"]))
										elif word == "{*STATUS*}":
											reply = reply.replace("{*STATUS*}", get_data(self, "title", ["title"]))
										elif word == "{*TOPIC*}":
											reply = reply.replace("{*TOPIC*}", get_data(self, "topic", ["topic"]))
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
							else:
								send_str = "You have to be a mod to use custom commands." 
								whisper(user, send_str)
								return
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
	
	def emote_stats_parse(self, user, msg, channel_parsed, user_type):
		#going to be deprecated RIP
		emote_stats_str = "!stats"
		if self.emote_stats_on:
			if in_front(emote_stats_str, msg):
				#if is_mod(user, self.channel_parsed, self.user_type): <-- one of those gui make it require mod status things
				msg_arr = msg.split(" ", 1)
				if len(msg_arr) == 2:
					emote = msg_arr[1]
					if is_emote(emote, self.emote_arr):
						#don't count when getting stats
						#emote_count = word_count(msg, emote)
						#self.count_dict[emote][0] += emote_count
						emote_per_min = round(find_per_min(emote, self.count_dict, self.channel_parsed), 2)
						send_str = "Total times %s has been sent: %s. %s per minute: %s." % (emote, prettify_num(self.count_dict[emote][0]), emote, prettify_num(simplify_num(emote_per_min)))
					else:
						send_str = "Invalid emote for emote stats." 
				else:
					send_str = "Usage: !stats <emote>" 
				self.write(send_str)
				return
			#dont count emotes sent by us, or when getting stats
			else:
				if user != self.nickname:
					for emote in self.emote_arr:
						if word_count(msg, emote) != 0:
							emote_count = word_count(msg, emote)
							self.count_dict[emote][0] += emote_count
			return False
	
	def mods_parse(self, user, msg, channel_parsed, user_type):
		mods_str = "!mods" 
		moderators_str = "!moderators"
		
		if in_front(mods_str, msg) or in_front(moderators_str, msg):
			self.write("/mods")
		else:
			return False
	
	def repeat_check(self):
		#perhaps this would be better: https://twistedmatrix.com/documents/10.1.0/core/howto/time.html, for now using LoopingCalls
		
		if self.repeat_on:
			current_time = time.time()
			query = "SELECT * FROM repeats WHERE (%d - set_time > `interval` )" % current_time
			result = self.conn.execute(query)
			for repeat_set in result:
				query = "UPDATE repeats SET set_time=%d WHERE `index`=%s" % (current_time, repeat_set[0])
				self.conn.execute(query)
				#have to ahve this for some reason idk whhy it breaks without it
				try:
					self.write(repeat_set[2])
				except:
					pass
				self.main_parse(self.nickname, repeat_set[2], 'mod')
	
	def countdown_check(self):
		if self.countdown_on:
			current_time = time.time()
			for countdown_set in self.countdown_arr:
				countdown_set_time = countdown_set[0]
				countdown_cmd = countdown_set[1] 
				countdown_time = simplify_num(countdown_set[2])
				if (current_time - countdown_set_time >= countdown_time):
					self.write(countdown_cmd)
					self.main_parse(self.nickname, countdown_cmd, 'mod')
					#write and parse the command, then remove it
					self.countdown_arr.remove(countdown_set)
					
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
					self.chatter_arr = []
					self.lurker_arr = []
					self.stream_status = False
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
					update_data(self, "title", ["title"], title)
					send_str = "Title changed to \"%s\"" % title
					self.write(send_str)
					url = "https://api.twitch.tv/kraken/channels/%s?oauth_token=%s" % (channel_parsed, access_token)
					data = json.dumps({'channel': {'status': title}})
					headers = {'content-type': 'application/json', 'Accept': 'application/vnd.twitchtv.v3+json'}
					r = requests.put(url, data=data, headers=headers)
				else:
					send_str = "You have to be the streamer to change the channel title."
					whisper(user, send_str)
			else:
				title = get_data(self, "title", ["title"])
				if title:
					title = title[0]["title"]
					send_str = "The current title is: \"%s\"" % title.encode("utf-8")
					if is_mod(user, channel_parsed, user_type):
						self.write(send_str)
					else:
						whisper(user, send_str)
				else:	
					channel_data = get_json_stream(channel_parsed)
					title = channel_data["streams"][0]["channel"]["status"]
					send_str = "The current title is: \"%s\"" % title.encode("utf-8")
					if is_mod(user, channel_parsed, user_type):
						self.write(send_str)
					else:
						whisper(user, send_str)
		else:
			return False
			
	def game_parse(self, user, msg, channel_parsed, user_type):
		game_str = "!game"
		msg_arr = msg.split(" ", 1)
		if in_front(game_str, msg):
			if len(msg_arr) > 1:
				if is_streamer(user, channel_parsed):
					game = msg_arr[1]
					update_data(self, "game", ["game"], game)
					send_str = "Game changed to \"%s\"" % game
					self.write(send_str)
					url = "https://api.twitch.tv/kraken/channels/%s?oauth_token=%s" % (channel_parsed, access_token)
					data = json.dumps({'channel': {'game': game}})
					headers = {'content-type': 'application/json', 'Accept': 'application/vnd.twitchtv.v3+json'}
					r = requests.put(url, data=data, headers=headers)
				else:
					send_str = "You have to be the streamer to change the channel game"
					whisper(user, send_str)
			else:
				#gonna need to see what the output is from this and edit accordingly
				game = get_data(self, "game", ["game"])[0]["game"]
				#if they want game and it's equal to "", then get the game and check accordingly
				if game != "":
					if game == False:
						send_str = "%s is not playing a game." % channel_parsed.capitalize()
					else:
						send_str = "The current game is: \"%s\"" % game.encode("utf-8")
					if is_mod(user, channel_parsed, user_type):
						self.write(send_str)
						return
					else:
						whisper(user, send_str)
						return
				else:	
					#get the new game and then print accordingly
					channel_data = get_json_stream(channel_parsed)
					game = channel_data["streams"][0]["game"]
					if not game:
						game = False
						
					if game == False:
						send_str = "%s is not playing a game." % channel_parsed.capitalize()
					else:
						send_str = "The current game is: \"%s\"" % game.encode("utf-8")
					if is_mod(user, channel_parsed, user_type):
						self.write(send_str)
						return
					else:
						whisper(user, send_str)
						return
		else:
			return False
			
	def topic_parse(self, user, msg, channel_parsed, user_type):
		topic_str = "!topic"
		
		if get_status(self, "topic"):
			msg_arr = msg.split(" ", 1)
			if in_front(topic_str, msg):
				if len(msg_arr) > 1:
					if is_mod(user, channel_parsed, user_type):
						update_data(self, "topic", ["topic"], msg_arr[1])
						send_str = "Topic changed to \"%s\"" % msg_arr[1]
						self.write(send_str)
					else:
						send_str = "You have to be a mod to change the channel topic"
						whisper(user, send_str)
				else:
					topic = get_data(self, "topic", ["topic"])[0]["topic"]
					send_str = "The current topic is: \"%s\"" % topic
					if is_mod(user, channel_parsed, user_type):
						self.write(send_str)
					else:
						whisper(user, send_str)
			else:
				return False
		else:
			return False
	
	def purge_parse(self, user, msg, channel_parsed, user_type):
		purge_str = "!purge"
		if get_status(self, "purges"):
			if in_front(purge_str, msg):
				if is_mod(user, channel_parsed, user_type):
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
						whisper(user, send_str)
						return
					else:
						send_str = "Usage: !purge <user>"
						whisper(user, send_str)
						return
				else:
					send_str = "Only mods can use \"!purge\"."
					whisper(user, send_str)
					return	
				self.write(send_str)
			else:
				return False
		else:
			return False
			
	def math_parse(self, user, msg, channel_parsed, user_type):
		#math - print if mod whisper if not
		math_str = "!math"
		if get_status(self, "math"):
			if in_front(math_str, msg):
				msg_arr = msg.split(" ")
				if len(msg_arr) == 1:
					send_str = "Usage: !math <equation>" 
					whisper(user, send_str)
				elif len(msg_arr) > 1:
					equation = msg_arr[1]
					try:
						send_str = str(eval(equation))
					except:
						send_str = "Unable to solve equation."
						whisper(user, send_str)
						return
				self.write(send_str)
			else:
				return False
		else:
			return False
			
	def roll_parse(self, user, msg, channel_parsed, user_type):
		#roll - return a random number in the given range
		roll_str = "!roll"
		
		if get_status(self, "roll"):
			if in_front(roll_str, msg):
				msg_arr = msg.split(" ", 1)
				if len(msg_arr) == 1:
					send_str = "Usage: !roll <lower limit(default: 0)>, <upper limit>" 
					whisper(user, send_str)
					return
				elif len(msg_arr) > 1:
					range_lims = msg_arr[1].split(",")
					if len(range_lims) > 1:
						roll_lower_lim = range_lims[0]
						roll_upper_lim = range_lims[1]
						if not is_num(roll_lower_lim) or not is_num(roll_upper_lim):
							send_str = "!Usage: !roll <lower limit(default: 0)>, <upper limit>"
							whisper(user, send_str)
							return
					else:
						if not is_num(msg_arr[1]):
							send_str = "!Usage: !roll <lower limit(default: 0)>, <upper limit>"
							whisper(user, send_str)
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
					if not is_mod(user, channel_parsed, user_type):
						whisper(user, send_str)
						return
				self.write(send_str)
			else:
				return False
		else:
			return False
			
	def coin_parse(self, user, msg, channel_parsed, user_type):
		#coin - return heads or tails
		coin_str = "!coin"
		if get_status(self, "coin"):
			if in_front(coin_str, msg):
				if random.randint(0, 1) == 0:
					send_str = "%s: Heads" % user
				else:
					send_str = "%s: Tails" % user
				if not is_mod(user, channel_parsed, user_type):
					whisper(user, send_str)
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

		if get_status(self, "countdowns"):
			if in_front(countdown_str, msg):
				if in_front(countdown_add_str, msg):
					if is_mod(user, channel_parsed, user_type):
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
								countdown_set = [current_time, countdown_cmd, countdown_time]
								insert_data(self, "countdowns", ["set_time", "command", "duration"], countdown_set)
								send_str = "Countdown command \"%s\" added with expiration time %s." % (countdown_cmd, parse_sec_condensed(countdown_time))
							else:
								send_str = "No \".disconnect\" or \"/disconnect\" variants allowed."
						else:
							send_str = "Usage: !countdown add <command> <expiration time/date>" 
							whisper(user, send_str)
							return
					else:
						send_str = "You have to be a mod to use \"!countdown add\"." 
						whisper(user, send_str)
						return
				elif in_front(countdown_del_str, msg) or in_front(countdown_rem_str, msg):
					if is_mod(user, channel_parsed, user_type):
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) > 2:
							countdown_cmd = msg_arr[2]
							if is_num(countdown_cmd):
								countdown_cmd = int(countdown_cmd)
								delete_status = delete_index_handler(self, "countdowns", countdown_cmd)
								if delete_status:
									send_str = "Countdown command \"%s\" with expiration time %s removed at index %s." % (delete_status["command"], parse_sec_condensed(delete_status["duration"]), countdown_cmd)
								else:
									send_str = "Invalid index for countdown command removal." 
							else:
								delete_status = delete_value_handler(self, "countdowns", "command", countdown_cmd)
								if delete_status: 
									send_str = "Countdown command \"%s\" with expiration time %s removed." % (countdown_cmd, parse_sec_condensed(delete_status["duration"]))		
								else:
									send_str = "Specified countdown command does not exist." 
						else:
							send_str = "Usage: !countdown delete/remove <command/index>" 
							whisper(user, send_str)
							return
					else:
						send_str = "You have to be a mod to use \"!countdown delete/remove\"." 
						whisper(user, send_str)
						return
				elif countdown_list_str == msg:
					countdown_table = get_table(self, "countdowns")
					if len(countdown_table) == 0:
						send_str = "No active countdown commands." 
					else:
						send_str = "Active countdown commands: " 
						for row_index, row in enmuerate(countdown_table):
							if (countdown_set != len(self.countdown_arr)-1):
								#every element but last one
								send_str += "(%s.) %s: %s, " % (row_index+1, row["command"], row["duration"])
							else:
								#last element in arr
								send_str += "(%s.) %s: %s." % (row_index+1, row["command"], row["duration"])
								
					if not is_mod(user, self.channel_parsed, user_type):
						whisper(user, send_str)		
						return			
				elif countdown_clr_str == msg:
					if is_mod(user, self.channel_parsed, user_type): 
						clear_table(self, "countdowns")
						send_str = "All countdown commands removed." 
					else:
						send_str = "You have to be a mod to use \"!countdown clear\"." 
						whisper(user, send_str)
						return
				elif countdown_str == msg:
					send_str = "Add or remove commands to be executed at the end of a specified time. Syntax and more information can be found in the documentation." 
					whisper(user, send_str)
					return
				else:
					if is_mod(user, channel_parsed, user_type):
						send_str = "Usage: !countdown add/delete/remove/list/clear <command> <expiration time>" 
					else:
						send_str = "Usage: !countdown list" 
					whisper(user, send_str)
					return
				self.write(send_str)
				return
			else:
				return False
	
	def points_parse(self, user, msg, channel_parsed, user_type):
		#!points - return number of points for the current user, allow mods to get the points of any user
		points_str = "!points"
		if get_status(self, "points"):
			if in_front(points_str, msg):
				msg_arr = msg.split()
				if len(msg_arr) > 1:
					if is_mod(user, channel_parsed, user_type):
						point_user = msg_arr[1]
						points_num = point_balance(self, point_user)
						if points_num:
							if points_num != 1:
								send_str = "%s has %s points in this channel." % (point_user, points_num)
							else:
								send_str = "%s has %s point in this channel." % (point_user, points_num)
						else:
							send_str = "%s has no points in this channel." % point_user
							whisper(user, send_str)
							return
					else:
						send_str = "You have to be a mod to get the points of other users"
				elif len(msg_arr) == 1:
					points_num = point_balance(self, point_user)
					if points_num:
						if points_num != 1:
							send_str = "%s, you have %s points in this channel" % (user, points_num)
						else:
							send_str = "%s, you have %s point in this channel" % (user, points_num)
					else:
						send_str = "%s, you do not have any points in this channel" % user
				else:
					send_str = "!Usage: !points <user>"
					whisper(user, send_str)
					return
					
				if is_mod(user, channel_parsed, user_type):
					self.write(send_str)
				else:				
					whisper(user, send_str)
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
		if get_status(self, "slots"):
			if in_front(slots_str, msg):
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
				whisper(user, send_str)
			else:
				return False
		else:
			return False
	
	def give_parse(self, user, msg, channel_parsed, user_type):
		#!give - give user specified amount of coins, 
		give_str = "!give"
		if get_status(self, "give"):
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
									if is_mod(user, channel_parsed, user_type):
										if give_amount != 1:
											send_str = "%s has given %s %s points." % (user, give_user, give_amount)
										else:
											send_str = "%s has given %s %s point." % (user, give_user, give_amount)
									else:
										if give_amount != 1:
											send_str = "You have given %s %s points." % (give_user, give_amount)
											whisper(user, send_str)
											send_str = "%s has given you %s points." % (user, give_amount)
											whisper(give_user, send_str)
										else:
											send_str = "You have given %s %s point." % (give_user, give_amount)
											whisper(user, send_str)
											send_str = "%s has given you %s point." % (user, give_amount)
											whisper(give_user, send_str)
										return
								else:
									send_str = "You cannot give more points than you have." 
									whisper(user, send_str)
									return
							else:
								send_str = "You cannot give negative points." 
								whisper(user, send_str)
								return
						else:
							send_str = "You cannot give more points than you currently have." 
							whisper(user, send_str)
							return
					else:
						send_str = "Usage: !give <point amount> <user>"
						whisper(user, send_str)
						return
				else:
					send_str = "Usage: !give <point amount> <user>"
					whisper(user, send_str)
					return
				self.write(send_str)
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
		#Take the message and add each word to the word frequency database
		
		###new viewers/chatters
		#needs to be reassigned every time so that we keep the topic up to date
		topic = get_data(self, "topic", ["topic"])
		self.welcome_msg = "Welcome to the channel! The current topic is \"%s\""  % topic
		self.welcome_back_msg = "Welcome back! The current topic is \"%s\""  % topic
		'''if user not in self.chatter_arr:#so that we don't say "Welcome!" until we know they aren't a lurker
			self.chatter_arr.append(user)
			if not is_streamer(user, self.channel_parsed):
				if user in self.perm_chatter_arr:
					whisper(user, self.welcome_back_msg)
				else:
					whisper(user, self.welcome_msg)
					self.perm_chatter_arr.extend(user)'''
					
		for permit_pair in self.permit_arr:
			if permit_pair[3] == "message":
				if user == permit_pair[1]:
					current_msg_count = permit_pair[0]
					max_msg_count = permit_pair[2]
					if current_msg_count >= max_msg_count:
						#remove
						self.permit_arr.remove(permit_pair)
					else:
						#add to the message count
						permit_pair[0] += 1
					
			elif permit_pair[3] == "time":
				user_time = permit_pair[0]
				permit_time = permit_pair[2]
				if permit_pair[1] != self.nickname:
					#don't remove tecsbot
					if ((current_time - user_time) >= permit_time):
						self.permit_arr.remove(permit_pair)#should be fine since only one permit can be added at a time
			#do nothing if permanent permit
		
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
		
		#test command if bot is in chat, should also give connection stats in the response
		if self.test_parse(user, msg, self.channel_parsed, user_type) != False:
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
			
		if self.general_channel_stats_parse(user, msg, self.channel_parsed, user_type, "stats") != False:
			return	
			
		if self.channel_stats_parse(user, msg, self.channel_parsed, user_type) != False:
			return	
			
		if self.subs_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.commercial_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		#if self.ban_emote_parse(user, msg, self.channel_parsed, user_type) != False:
			#return
			
		if self.repeat_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.custom_command_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		#if self.emote_stats_parse(user, msg, self.channel_parsed, user_type) != False:
			#return
		
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
			self.write(args[1])

	def write(self, msg):
		'''Send message to channel and log it'''
		self.msg(self.channel, msg.encode("utf-8"))
		logging.info("{}: {}".format(self.nickname, msg))
		
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
		
		self.ball_arr = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Reply hazy try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again", "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]
		
		
		check_loop = LoopingCall(self.whisper_check)
		check_loop.start(0.003)
	
	def test_parse(self, user, msg):
		#test
		test_str = "!test"
		test_reply = "Test successful."
		
		if msg == "!test":
			whisper(user, test_reply)
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
					if len(self.ball_arr) > 0:
						ball_response_index = random.randint(0, len(self.ball_arr)-1)
						ball_response = self.ball_arr[ball_response_index]
						send_str = "Magic 8 ball says... %s" % (ball_response)
					else:
						send_str = "There are currently no 8ball responses." 
				elif ball_str == msg:
					send_str = "Get the Magic 8 Ball to answer your question. Usage: \"!8ball <question> \"." 
				else:
					send_str = "Usage: \"!8ball <question>? \"." 
			else:
				send_str = "Usage: \"!8ball <question>? \"." 
			whisper(user, send_str)
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
			whisper(user, send_str)
		else:
			return False
	
	def general_channel_stats_parse(self, user, msg, channel_parsed, stat_str):
		find_stat_str = "!" + stat_str
		if in_front(find_stat_str, msg):
			msg_arr = msg.split()
			if len(msg_arr) > 1:
				stat_channel = msg_arr[1]
				
				if stat_str == "chatters":
					stat_data = get_json_chatters(stat_channel.lower().strip())
					stat_count = stat_data["chatter_count"]
				elif stat_str == "viewers":
					stat_data = get_json_stream(stat_channel.lower().strip())
					stat_count = stat_data["streams"]
				elif stat_str == "views":
					stat_data = get_json_views_follows(stat_channel.lower().strip())
					stat_count = stat_data["views"]
				elif stat_str == "followers":
					stat_data = get_json_views_follows(stat_channel.lower().strip())
					stat_count = stat_data["followers"]
					
				if stat_count:
					if stat_str == "viewers":
						stat_count = stat_count[0]["viewers"]
						
					stat_count = prettify_num(stat_count)
					if stat_channel.rstrip().endswith("s"):
						stat_channel = stat_channel + "'"
					else:	
						stat_channel = stat_channel + "'s"
				
					if stat_str == "chatters":
						send_str = "There are currently %s accounts in %s chat." % (stat_count, stat_channel)
					elif stat_str == "viewers":
						send_str = "There are currently %s viewers in %s channel." % (stat_count, stat_channel)
					elif stat_str == "views":
						send_str = "There are currently %s views in %s channel." % (stat_count, stat_channel)
					elif stat_str == "followers":
						send_str = "%s channel has %s followers." % (stat_channel.capitalize(), stat_count)
				else:
					send_str = "%s is not an active channel." % msg_arr[1]
			else:
				send_str = "Usage: \"%s <channel>\"" % find_stat_str
				
			whisper(user, send_str)
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
			whisper(user, send_str)
		else:
			return False
		
	def subs_parse(self, user, msg, channel_parsed, user_type):
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
				
			if is_mod(user, channel_parsed, user_type):
				self.write(send_str)
			else:	
				whisper(user, send_str)
		else:
			return False
	'''def emote_stats_parse(self, user, msg, channel_parsed):
		emote_stats_str = "!stats"
		if self.emote_stats_on:
			if in_front(emote_stats_str, msg):
				#if is_mod(user, self.channel_parsed, self.user_type): <-- one of those gui make it require mod status things
				msg_arr = msg.split(" ", 1)
				if len(msg_arr) == 2:
					emote = msg_arr[1]
					if is_emote(emote, self.emote_arr):
						#don't count when getting stats
						#emote_count = word_count(msg, emote)
						#self.count_dict[emote][0] += emote_count
						emote_per_min = round(find_per_min(emote, self.count_dict, self.channel_parsed), 2)
						send_str = "Total times %s has been sent: %s. %s per minute: %s." % (emote, self.count_dict[emote][0], emote, simplify_num(emote_per_min))
					else:
						send_str = "Invalid emote for emote stats." 
				else:
					send_str = "Usage: !stats <emote>" 
				self.write(send_str)
				return
			#dont count emotes sent by us, or when getting stats
			else:
				if user != self.nickname:
					for emote in self.emote_arr:
						if word_count(msg, emote) != 0:
							emote_count = word_count(msg, emote)
							self.count_dict[emote][0] += emote_count
			return False
	'''
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
			
		if self.general_channel_stats_parse(user, msg, self.channel_parsed, "chatters") != False:
			return
			
		if self.general_channel_stats_parse(user, msg, self.channel_parsed, "viewers") != False:
			return
			
		if self.general_channel_stats_parse(user, msg, self.channel_parsed, "views") != False:
			return
			
		if self.general_channel_stats_parse(user, msg, self.channel_parsed, "followers") != False:
			return	
		
		if self.channel_stats_parse(user, msg, self.channel_parsed) != False:
			return	
		'''if self.emote_stats_parse(user, msg, self.channel_parsed) != False:
			return'''
		
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

	def write(self, msg):
		'''Send message to channel and log it'''
		self.msg(self.channel, msg.encode("utf-8"))
		logging.info("{}: {}".format(self.nickname, msg))
		
class WhisperBotFactory(protocol.ClientFactory, object):
	wait_time = 1

	def __init__(self, channel):
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

reactor.run()
	
#except Exception as errtxt:
	#print errtxt


