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
hours til next strim?
score of current game/tourney/bo3/etc
song functionality
welcome newcomers
	custom message
	need to auth before getting subs
sub notifications
raffle -  expiration timer?
commercials? 
commands for mods to change game or title or other(commercials?)
social media info
repeat info, like social media info
allow users to program question responses like ALICE? <-- interesting idea for a solo channel
overall and per day -time user has watched stream
	other user tracking stuff
overrall and per day -messages of user, high score, etc
dont disable bot, only change some responses when offline stream
remember to only allow some commands to work if user is mod/owner
	different responses for mods/owners
check to make sure x!= '' is present in all the things
log/dict/array of recent commands? <-doubt this would actually help with an undo command
	do similar thing to moobot, have a chatbox of the commands said and run, without other misc messages
different levels of authority?
tecsbot moderator group?
when put online it will greet the first(?) viewer and followr on the list
more advanced !test results
how to find zalgo symbols?
figure out what to do with the other spamerino things
break out of if statement chain when there is a command found <-- may already be fixed, may bring up 2 errors on very rare occurences
excludes for "regulars" and subs
change autoreplies to commands, add variables for responses
all of spam control set on/off?
offtime - time stream has been offline
the minimum number of symbols should be disabled by default
may still be some lurking bugs from the multithreading
need to make sure it breaks out of the spam checks if it finds one so as not to do a double warning/timeout
link our access_token html file and this file 
need to make friends with a twitch partner
need to have command to check if user is subscribed to channel 
	!subscribed /!subbed <user>
just a note: better to try and open file and catch exception than to check if isfile
needs to not add if already exists for many of the functions
is it quitting because there is no data being sent? need it to be infinitely patient
the bad file descriptor is apparently related to the self. variables<--so you know why it's happening if it does happen again
do we need to get timezones working for the get_uptime_str?
add the end check loops for emotes and shit to their respective parsers
make it so capitalization doesnt matter on several things(i.e. autoreply)
need to find better solution to KappaPride problem
for the chat integration of autoreplies, we can stop the user from inputting ":" into either the phrase or the reply,
	or we can allow it but only allow them to delete by using the phrase of the pair, since we cannot have both in this situation
	however this can be fine in the GUI
make an option to let bot respond to it's own replies to autoreplies? Would be funny
if permits on, voting on,
have user checked for mod status either at beginning of main_parse and have that as a is_mod BOOL, or just only check when they have issued a command
make !vote results also show the current winner?
use round() wherever needed
use enumerate wherever needed
point system for watching stream/chatting/etc
	more points -> greater chance to win prizes/raffles/etcidk
!x delete 21, 1, 5 <--- multiple deleting possibility <--- can we make a function for deleting?
allow streamer to choose what to let mods do?<--- could work with level system
!followers
analytic for messages and emotes and shiznizzle
when adding/removing ban emotes for the special emotes(o_O, O_o, etc), it currently will bulk remove/add them. 
	In the GUI, we want to have a checkbox for "remove all variants of <input emote text>(emote picture)?" that if checked will do as did normally, if unchecked then will do one at a time.
need to add in turbo and other emotes
1 second between requests is recommended
replace as many api requests as possible
use sets instead of arrays?
add in !roll like in dota 3 
add in slot machine, make it emoticons  http://www.phantombot.net/threads/slot-machine-beta.537/
add in lottery
!clever <user> to troll user
!math command and all the others here: https://github.com/memanlolz/Twitch_Bot/blob/master/src/com/yofungate/ircBot/Main.java
add possibility to have !maddcom !heyo %broadcaster% wants %user% to tell %touser% that they are an idiot. so that they can refer to other users
add !leave and !join commands (and !rejoin)
emote stats doesn't work with sub emotes for other channels atm, could do this by querying for their channels then getting the emotes, or it would probably be a lot easier to store every word in a dbase/dictionary and it's corresponding 
	occurences, idk, figure it out future self
can we make LoopingCall's interval 0? <-- do we want to
if you add tags for commands you can receive whispers - respond with whispers when whispered to
allow a lot of commands to be done by users just only through whispers
and those that only through whispers for users can be either or for mods
vote options/list to give current vote options, vote index
permits:
	if permanent replace all others for that user
	if longer message or time replace the respective one
add in default autoreplies and commands for examples	
argument for mod requirement custom commands autoreplies
	allow it for already existing commands, maybe edit in GUI
	allow it to be input for custom and autoreply commands
allow custom commands and autoreplies to be set off and on
when voting for an option, keep it as "vote", otherwise make it poll, specify this in the usage
allow changing of votes and removing of votes
link regex #2 - inches...DansGame is not a link god dammit

	use more try except/catch 
just use [str(v) for v in list_thing] to remove unicode from strings<--what code was he referring to
apparently there are a few specific characters that zalgo text needs
add in functions for parsing each of the things in main_parse, ie if link-whitelist_on: link_whitelist_parse(msg, etd) <--do we do this with the antispam? if we do we will have to have a way to stop going through when a value is returned
we can put the large num of variables in another file and import if necessary

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
import socket #imports module allowing connection to IRCBRB
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

'''
#this is already in channel settings
blacklist_timeout = 10 #seconds
blacklist_arr = ["belgium"]
'''
#This determines whether to do search_str == msg, or search_str in message when looking for commands
cmd_match_full = True

#initial connect
f = open("C:\\Python27\\Scripts\\bot_oauth.log", "r")
access_token = f.readlines()[1]

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
	
def update_count_dict(count_dict, emote_arr):
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

'''dont think we will ever use this again
def update_dict():
	print "Checking Logs..."
	
	log_file = open(log_file_path, 'r')
	for msg in log_file:
		emotes_file = open(emote_file_path, 'r')
		for emote in emotes_file:
			#parsing stuff
			emote = emote.rstrip()
			if msg.count(emote) != 0:
				emote_count = msg.count(emote)
				#count_dict[emote] = emote
				#needs to add to existing count
				count_dict[emote][0] += emote_count'''

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
		except ValueError:
			time.sleep(3)
			pass
	
def get_json_chatters(channel_parsed):
	url = "https://tmi.twitch.tv/group/user/%s/chatters" % channel_parsed
	return requests.get(url).json()

def get_json_follows(channel_parsed):
	url = "https://api.twitch.tv/kraken/channels/%s/follows/" % channel_parsed
	return requests.get(url).json()
	
def get_json_subs(channel_parsed):	
	url = "https://api.twitch.tv/kraken/channels/%s/subscriptions" % channel_parsed
	data = requests.get(url, params={'oauth_token': access_token})
	print data.json()
	return data.json()

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
	
def stream_online(channel_parsed):
	#we use this return value to trigger the loop of everything.
	channel_json = get_json_stream(channel_parsed)
	while True:
		try:
			stream_status = channel_json["streams"]
			if stream_status == None:
				return False
			else:
				return True
		except:
			pass
	
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

def get_time_return_str(time_type, time_str):
	return_str = ""
	if time_type > 0:
		return_str += " %s %s" % (time_type, time_str)
		if time_type > 1:
			return_str += "s"
		return_str += ", "
	else:
		return_str = ""
	return return_str
	
def parse_sec(sec):
	#assumes that parameter is not 0
	sec = float(sec)#just in case str is input
	hour = int(math.floor(sec/3600))
	minute = int(math.floor((sec - hour *3600) / 60))
	sec = prettify_num((sec - hour *3600 - minute*60))
	
	return_str = get_time_return_str(hour, "hour")
	return_str += get_time_return_str(minute, "minute")
	return_str += get_time_return_str(sec, "second")
	if return_str.endswith(", "):
		return_str = return_str[:-2]
	return return_str

def parse_sec_condensed(sec):
	sec = float(sec)
	hour = int(math.floor(sec/3600))
	minute = int(math.floor((sec - hour *3600) / 60))
	sec = prettify_num((sec - hour *3600 - minute*60))
	if hour == 0 and minute == 0:
		return_str = "%ss" % (sec)
	elif hour == 0:
		return_str = "%sm %ss" % (minute, sec)
	else:
		return_str = "%sh %sm %ss" % (hour, minute, sec)	
	#return the string for sending
	return return_str
	
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
	admin_types = ["admin", "global_mod", "staff"]
	if user == channel_parsed or user_type != '' or user_type in admin_types:
		return True
	else:
		return False

def is_streamer(user, channel_parsed):
	if user == channel_parsed:
		return True
	else:
		return False
	
def create_viewer_arr(channel_parsed):
	channel_json = get_json_chatters(channel_parsed)
	viewer_arr = []
	viewers = channel_json["chatters"]["viewers"]
	viewer_arr.extend(viewers)
	return viewer_arr
	
def new_follower(follower_arr, channel_parsed, self):
	follows_json = get_json_follows(channel_parsed)
	#need to return follower if there are any, and false if not
	if len(follows_json["follows"]) > 0:
		if follows_json["follows"][0]["user"]["display_name"] not in follower_arr:
			#if the first is not already recorded, then new follower
			follower_arr.append(follows_json["follows"][0]["user"]["display_name"])
			send_str = "Hello %s! Thank you for following %s's channel!" % (follows_json["follows"][0]["user"]["display_name"], channel_parsed)
			self.write(send_str)
		for follower in follows_json["follows"]:
			#add all that arent already recorded
			if follower["user"]["display_name"] not in follower_arr:
				follower_arr.append(follower["user"]["display_name"])
		return follower_arr
	else:
		return False

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
		
def set_value(set_on, set_feature, msg_arr, self):
	if msg_arr[2] == "on":
		if set_on == True:
			send_str = "%s is already on." % (set_feature.capitalize())
		else:
			set_on = True
			send_str = "%s turned on. You can do \"!set %s off\" to turn it off again." % (set_feature.capitalize(), set_feature)
	elif msg_arr[2] == "off":
		if set_on == False:
			send_str = "%s is already off." % (set_feature.capitalize())
		else:
			set_on = False
			send_str = "%s turned off. You can do \"!set %s on\" to turn it on again." % (set_feature.capitalize(), set_feature)
	else:
		#usage
		send_str = "Usage: \"!set %s on/off \"." % (set_feature)
	self.write(send_str)
	return set_on

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
	
def warn(user, msg, channel_parsed, self, warn_arr, warn_duration, warn_cooldown, timeout_msg, timeout_duration):
	#function to warn if they havent already been warned, and time them out if they have.
	global whisper_msg, whisper_user
	
	for warn_pair in warn_arr:
		if user == warn_pair[1]:
			#check if current time is longer than the warning duration from the last time name was entered
			current_time = time.time()
			if (current_time - warn_pair[0] <= warn_cooldown):
				#timeout user for long duration and remove from array
				timeout(user, self, timeout_duration)
				warn_arr.remove(warn_pair)
				send_str = "No %s allowed (%s)" % (timeout_msg, user.capitalize())
				self.write(send_str)
				whisper_msg = "You were timed out for %s in %s (%s)" % (timeout_msg, channel_parsed, parse_sec(timeout_duration))
				whisper_user = user
				return warn_arr
			else:
				#replace old entry with new one and send warning as well as timeout for warn_duration
				#short duration
				timeout(user, self, warn_duration)
				warn_arr.remove(warn_pair)
				pair = [current_time, user]
				warn_arr.append(pair)
				send_str = "No %s allowed (%s)(warning)" % (timeout_msg, user.capitalize())
				self.write(send_str)
				whisper_msg = "You were timed out for %s in %s (%s, warning)" % (timeout_msg, channel_parsed, parse_sec(warn_duration))		
				whisper_user = user
				return warn_arr
	else:
		#add new entry and send warning, with timeout for warn_duration
		#short duration
		timeout(user, self, warn_duration)
		current_time = time.time()
		pair = [current_time, user]
		warn_arr.append(pair)
		send_str = "No %s allowed (%s)(warning)" % (timeout_msg, user.capitalize())
		self.write(send_str)
		whisper_msg = "You were timed out for %s in %s (%s, warning)" % (timeout_msg, channel_parsed, parse_sec(warn_duration))
		whisper_user = user
	return warn_arr
		
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

def prettify_num(num):
	return check_int(float(num))
	
class TwitchBot(irc.IRCClient, object):

	def __init__(self, channel):#for now only channel
		self.channel = channel
		self.nickname = nickname
		self.password = password
		self.channel_parsed = self.channel.replace("#", "")
		server = 'irc.twitch.tv'
		
		'''irc = socket.socket()
		irc.connect((server, 6667)) #connects to the server
		#sends variables for connection to twitch chat
		irc.send("CAP REQ :twitch.tv/tags")
		irc.send('PASS ' + password + "")
		irc.send('USER ' + nick + ' 0 * :' + bot_owner + "")
		irc.send('NICK ' + nick + "")
		irc.send('JOIN ' + self.channel + "")'''
		
		self.rol_on = True
		self.ball_on = True
		self.banphrase_on = True
		self.autoreply_on = True
		self.link_whitelist_on = True
		self.antispam_on = True
		self.repeat_antispam_on = True
		self.emote_antispam_on = True
		self.caps_antispam_on = True
		self.fake_purge_antispam_on = True
		self.skincode_antispam_on = True
		self.long_msg_antispam_on = True
		self.zalgo_antispam_on = True
		self.symbol_antispam_on = True
		self.link_antispam_on = True
		self.long_word_antispam_on = True
		self.me_antispam_on = True
		self.ban_emote_on = True
		self.emote_stats_on = True
		self.repeat_on = True
		
		self.raffle_on = False
		
		self.vote_on = False
		self.cmd_on = True
		#emotes_file = open(emote_file_path, 'r')
		#log_file = open(log_file_path, 'r')	
		
		#should delete dictionary of values when/if stream goes offline.
		
		#update_dict()
		#print_dict_by_value(count_dict)
		
		#start with empty array of followers
		self.follower_arr = []
		#add current viewers to viewer_arr so we dont welcome everyone
		self.viewer_arr = create_viewer_arr(self.channel_parsed)
		self.raffle_users = []
		
		#self.vote_on = False
		self.link_whitelist_arr = []
		self.permit_arr = []
		self.banphrase_arr = []
		self.ar_arr = []
		self.ban_emote_arr = []
		self.cmd_dict = {}
		self.emote_arr = []
		self.cmd_arr = []
		self.repeat_arr = []
		
		self.caps_warn_arr = []
		self.emote_warn_arr = []
		self.fake_purge_warn_arr = []
		self.skincode_warn_arr = []
		self.long_msg_warn_arr = []
		self.zalgo_warn_arr = []
		#block_warn_arr = []
		self.symbol_warn_arr = []
		self.link_warn_arr = []
		self.spam_warn_arr = []
		self.long_word_warn_arr = []
		self.me_warn_arr = []
		
		self.ban_emote_warn_arr = []
		self.banphrase_warn_arr = []
		self.link_whitelist_warn_arr = []
		
		self.vote_option_arr = []
		self.vote_dict = {}
		self.vote_users = []
		self.vote_total = 0
		
		self.rol_chance = .5
		self.rol_timeout = 5 #seconds

		self.default_permit_time = 30#seconds
		self.default_permit_msg_count = 10#msgs
		self.ball_arr = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Reply hazy try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again", "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]
		
		self.emote_arr = get_emote_list(self.channel_parsed)
		self.special_emote_arr = ['o_O', 'O_o', 'o_o', 'O_O', ':o', ':O', ':\\', ':/', ':p', ':P', ';p', ';P']
		#self.emote_arr.extend(self.special_emote_arr)
		self.count_dict = create_count_dict(self.emote_arr)
		
		self.default_cmd_arr = ['!link whitelist', '!permit', '!banphrase', '!autoreply', '!set', '!vote', '!raffle', '!roulette', '!8ball', '!uptime', '!chatters', '!viewers', '!subs', '!subscribers', '!commercial', '!ban emote', '!repeat']
		'''if self.permit_arr == []:
			current_time = time.time()
			permit_pair = [current_time, nick, 420, "time"]
			self.permit_arr.append(permit_pair)
			permit_nick = "Tmi.twitch.tv 001 %s" % nick
			permit_pair = [current_time, permit_nick, 322, "time"]#number irrelevant
			self.permit_arr.append(permit_pair)'''
		
		#old regex = '\S+\.\w{2,6}\b(?!\.)'
		#less old regex = \S+[^\d]\.\w{2,6}\b(?!\.)
		self.link_regex = re.compile(ur'(?![\d\.]\b)(\S+\.[^\d]{2,6})\b', re.MULTILINE)
		#registers "a[].remove()" as a link
		#if this one fails, try this one, i'm pretty sure it's actually better 
		#(?![\d\.]\b)(\S+\.[^\d]{2,6})\b
		check_loop = LoopingCall(self.repeat_check)
		check_loop.start(0.003)
	
	def link_whitelist_parse(self, user, msg, channel_parsed, user_type):
		link_whitelist_str = "!link whitelist"
		link_whitelist_add_str = "!link whitelist add"
		link_whitelist_del_str = "!link whitelist delete"
		link_whitelist_rem_str = "!link whitelist remove"
		link_whitelist_list_str = "!link whitelist list"
		link_whitelist_clr_str = "!link whitelist clear"

		if self.link_whitelist_on:
			if in_front(link_whitelist_str, msg):
				if is_mod(user, self.channel_parsed, user_type):
					msg_arr = msg.split(" ")
					if in_front(link_whitelist_add_str, msg):
						if len(msg_arr) > 3:
							link_whitelist = msg_arr[3]
							if re.search(self.link_regex, link_whitelist):#if is link according to our regex
								#is a url
								if link_whitelist in self.link_whitelist_arr:#if already whitelisted
									send_str = "%s is already a whitelisted link." % (link_whitelist)
								else:
									self.link_whitelist_arr.append(link_whitelist)
									send_str = "%s added to list of whitelisted links." % (link_whitelist)
							else:
								send_str = "%s is not a valid link." % (link_whitelist)
						else:
							send_str = "Usage: \"!link whitelist add <link>\""
					elif in_front(link_whitelist_del_str, msg) or in_front(link_whitelist_rem_str, msg):
						if len(msg_arr) > 3:
							link_whitelist = msg_arr[3]
							if is_num(link_whitelist):
								#we add on one to the actual index because users prefer to start with 1, rather than 0.
								link_whitelist = int(link_whitelist)
								if link_whitelist > 0 and link_whitelist <= len(self.link_whitelist_arr):
									send_str = "Link %s removed at index %s." % (self.link_whitelist_arr[link_whitelist-1], link_whitelist)
									del self.link_whitelist_arr[link_whitelist-1]
								else:
									send_str = "Invalid index for link removal."
							else:
								if link_whitelist in self.link_whitelist_arr:
									self.link_whitelist_arr.remove(link_whitelist)
									send_str = "Link %s removed." % (link_whitelist)									
								else:
									send_str = "Specified link does not exist." 
						else:
							send_str = "Usage: \"!link whitelist delete/remove <link/index>\"" 
					elif link_whitelist_list_str == msg:
							if len(self.link_whitelist_arr) == 0:
								send_str = "No active links." 
							else:
								send_str = "Active links: " 
								for link_whitelist in range(len(self.link_whitelist_arr)):
									if (link_whitelist != len(self.link_whitelist_arr) -1):
										#every element but last one
										send_str += "(%s.) %s, " % (link_whitelist+1, self.link_whitelist_arr[link_whitelist])
									else:
										#last element in arr
										send_str += "(%s.) %s." % (link_whitelist+1, self.link_whitelist_arr[link_whitelist])
									
					elif link_whitelist_clr_str == msg:
						self.link_whitelist_arr = []
						send_str = "All links removed." 
					elif link_whitelist_str == msg:
						send_str = "Add or remove links to timeout users who say them. Syntax and more information can be found in the documentation." 
					else:
						send_str = "Usage: \"!link whitelist add/delete/remove/list/clear\"" 
				else:
					send_str = "You have to be a mod to use !list whitelist commands." 
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
								self.permit_arr.append(permit_pair)
								send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
							elif len(msg_arr) == 4:
								if msg_arr[3] == "time":
									#!permit add <user> time
									current_time = time.time()
									permit_time = self.default_permit_time
									permit_type = "time"
									permit_pair = [current_time, permit_user, permit_time, permit_type]
									self.permit_arr.append(permit_pair)
									send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
								elif msg_arr[3] == "message":
									#!permit add <user> message
									msg_count = self.default_permit_msg_count
									permit_type = "message"
									permit_pair = [0, permit_user, msg_count, permit_type]#0 = current msg count
									self.permit_arr.append(permit_pair)
									send_str = "%s's spam filter has been lifted for %s messages." % (permit_user, msg_count)
								elif msg_arr[3] == "permanent":
									#!permit add <user> permanent
									permit_type = "permanent"
									permit_pair = [0, permit_user, 0, permit_type]#0 = current msg count
									self.permit_arr.append(permit_pair)
									send_str = "%s's spam filter has been permanently lifted." % (permit_user)
								elif is_num(msg_arr[3]):
									#!permit add <user> <time duration>
									current_time = time.time()
									permit_time = prettify_num(msg_arr[3])
									permit_type = "time"
									permit_pair = [current_time, permit_user, permit_time, permit_type]
									self.permit_arr.append(permit_pair)
									send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
								else:
									send_str = "Usage: !permit add <user> message/time <message count/time duration>/permanent" 
							elif len(msg_arr) == 5:
								if msg_arr[3] == "time":
									if is_num(msg_arr[4]):
										#!permit add <user> <type> <time duration>
										current_time = time.time()
										permit_time = prettify_num(msg_arr[4])
										permit_type = "time"
										permit_pair = [current_time, permit_user, permit_time, permit_type]
										self.permit_arr.append(permit_pair)
										send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
									else:
										send_str = "Usage: !permit add <user> message/time <message count/time duration>/permanent" 
								elif msg_arr[3] == "message":
									if is_num(msg_arr[4]):
										#!permit add <user> <type> <message count>
										msg_count = prettify_num(msg_arr[4])
										permit_type = "message"
										permit_pair = [0, permit_user, msg_count, permit_type]#0 = current msg count
										self.permit_arr.append(permit_pair)
										send_str = "%s's spam filter has been lifted for %s messages." % (permit_user, msg_count)
									else:
										send_str = "Usage: !permit add <user> message/time <message count/time duration>/permanent" 
								else:
									send_str = "Usage: !permit add <user> message/time <message count/time duration>/permanent" 
							else:
								send_str = "Usage: !permit add <user> message/time <message count/time duration>/permanent" 
						else:
							send_str = "Usage: !permit add <user> message/time <message count/time duration>/permanent" 
					else:
						send_str = "Usage: !permit add <user> message/time <message count/time duration>/permanent" 
							
				#delete/remove
				elif in_front(permit_del_str, msg) or in_front(permit_rem_str, msg):
					if len(msg_arr) == 3:
						permit_user = msg_arr[2]
						if is_num(permit_user):
							if permit_user > 0 and permit_user <= len(self.permit_arr):
								if self.permit_arr[int(permit_user)-1][3] == "permanent":
									send_str = "Permanent permit %s removed at index %s." % (self.permit_arr[int(permit_user)-1][1], permit_user.lower())
								elif self.permit_arr[int(permit_user)-1][3] == "message":
									send_str = "Permit %s with duration %s messages removed at index %s." % (self.permit_arr[int(permit_user)-1][1], self.permit_arr[int(permit_user)-1][2], permit_user.lower())
								elif self.permit_arr[int(permit_user)-1][3] == "time":
									send_str = "Permit %s with duration %s removed at index %s." % (self.permit_arr[int(permit_user)-1][1], parse_sec_condensed(self.permit_arr[int(permit_user)-1][2]), permit_user.lower())
								else:
									send_str = "This shouldn't happen, contact my creator if it does"
								#Should be the same index as the pair, after all.
								del self.permit_arr[int(permit_user)-1]
							else:
								send_str = "Invalid index for permit removal." 
						else:
							for permit_pair in self.permit_arr:
								if permit_user.lower() == permit_pair[1] or permit_user.capitalize() == permit_pair[1]:
									self.permit_arr.remove(permit_pair)
									send_str = "Permit \"%s\" removed." % (permit_user.lower())		
									break
							else:
								send_str = "Specified permit does not exist." 
					else:
						#incorrectly formatted, display usage
						send_str = "Usage: \"!permit delete/remove <user/index>\"." 
				#list
				elif permit_list_str == msg:
					if len(self.permit_arr) == 0:
						send_str = "No users with active permits." 
					else:
						send_str = "Users with active permits: " 
						for permit_pair in range(len(self.permit_arr)):
							if (permit_pair != len(self.permit_arr) -1):
								#every element but last one
								if self.permit_arr[permit_pair][3] == "time":
									send_str += "(%s.) %s : %s, " % (permit_pair+1, self.permit_arr[permit_pair][1], parse_sec_condensed(self.permit_arr[permit_pair][2]))
								elif self.permit_arr[permit_pair][3] == "message":
									send_str += "(%s.) %s : %s messages, " % (permit_pair+1, self.permit_arr[permit_pair][1], self.permit_arr[permit_pair][2])
								else:
									send_str += "(%s.) %s : permanent, " % (permit_pair+1, self.permit_arr[permit_pair][1])
							else:
								#last element in arr
								if self.permit_arr[permit_pair][3] == "time":
									send_str += "(%s.) %s : %s." % (permit_pair+1, self.permit_arr[permit_pair][1], parse_sec_condensed(self.permit_arr[permit_pair][2]))
								elif self.permit_arr[permit_pair][3] == "message":
									send_str += "(%s.) %s : %s messages." % (permit_pair+1, self.permit_arr[permit_pair][1], self.permit_arr[permit_pair][2])
								else:
									send_str += "(%s.) %s : permanent." % (permit_pair+1, self.permit_arr[permit_pair][1])
							
				#clear
				elif permit_clr_str == msg:
					self.permit_arr = []
					send_str = "All permits removed." 
				#normal
				elif permit_str == msg:
					if is_mod(user, self.channel_parsed, user_type):
						send_str = "Add or remove spam permits, allowing a user to message anything for a certain number of messages, or a length of time. Syntax and more information can be found in the documentation." 
					else:
						send_str = "You have to be a mod to use !permit commands" 
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
							self.permit_arr.append(permit_pair)
							send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
						elif len(msg_arr) == 3:
							if msg_arr[2] == "time":
								#!permit <user> time
								current_time = time.time()
								permit_time = self.default_permit_time
								permit_type = "time"
								permit_pair = [current_time, permit_user, permit_time, permit_type]
								self.permit_arr.append(permit_pair)
								send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
							elif msg_arr[2] == "message":
								#!permit <user> message
								msg_count = self.default_permit_msg_count
								permit_type = "message"
								permit_pair = [0, permit_user, msg_count, permit_type]#0 = current msg count
								self.permit_arr.append(permit_pair)
								send_str = "%s's spam filter has been lifted for %s messages." % (permit_user, msg_count)
							elif msg_arr[2] == "permanent":
								#!permit <user> permanent
								permit_type = "permanent"
								permit_pair = [0, permit_user, 0, permit_type]#0 = current msg count
								self.permit_arr.append(permit_pair)
								send_str = "%s's spam filter has been permanently lifted." % (permit_user)
							elif is_num(msg_arr[2]):
								#!permit <user> <time duration>
								current_time = time.time()
								permit_time = prettify_num(msg_arr[2])
								permit_type = "time"
								permit_pair = [current_time, permit_user, permit_time, permit_type]
								self.permit_arr.append(permit_pair)
								send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
							else:
								send_str = "Usage: !permit <user> message/time <message count/time duration>" 
						elif len(msg_arr) == 4:
							if msg_arr[2] == "time":
								if is_num(msg_arr[3]):
									#!permit add <user> <type> <time duration>
									current_time = time.time()
									permit_time = prettify_num(msg_arr[3])
									permit_type = "time"
									permit_pair = [current_time, permit_user, permit_time, permit_type]
									self.permit_arr.append(permit_pair)
									send_str = "%s's spam filter has been lifted for %s." % (permit_user, parse_sec_condensed(permit_time))
								else:
									send_str = "Usage: !permit <user> message/time <message count/time duration>" 
							elif msg_arr[2] == "message":
								if is_num(msg_arr[3]):
									#!permit add <user> <type> <message count>
									
									msg_count = prettify_num(msg_arr[3])
									permit_type = "message"
									permit_pair = [0, permit_user, msg_count, permit_type]#0 = current msg count
									self.permit_arr.append(permit_pair)
									send_str = "%s's spam filter has been lifted for %s messages." % (permit_user, msg_count)
								else:
									send_str = "Usage: !permit <user> message/time <message count/time duration>/permanent" 
							else:
								send_str = "Usage: !permit <user> message/time <message count/time duration>/permanent" 
						else:
							send_str = "Usage: !permit <user> message/time <message count/time duration>/permanent" 
					else:
						send_str = "Usage: !permit <user> message/time <message count/time duration>/permanent" 
				else:
					if is_mod(user, self.channel_parsed, user_type):
						send_str = "Add or remove spam permits, allowing a user to message anything for a certain number of messages, or a length of time. Syntax and more information can be found in the documentation." 
					else:
						send_str = "You have to be a mod to use !permit commands" 
			
			else:
				send_str = "You have to be a mod to use !permit commands." 
			self.write(send_str)
		
		
		if in_front(unpermit_str, msg):
			if is_mod(user, self.channel_parsed, user_type):
				msg_arr = msg.split(" ")
				if len(msg_arr) == 2:
					permit_user = msg_arr[1]
					for permit_pair in self.permit_arr:
						if permit_pair[1] == permit_user:
							send_str = "%s's spam permit has been removed." % (permit_user.lower())
							self.permit_arr.remove(permit_pair)
							break
				else:
					send_str = "Usage: \"!unpermit <user>\"" 
			else:
				send_str = "You have to be a mod to unpermit users." 
			self.write(send_str)
			
		
		#if !permit or !unpermit were used then main_parse is over
		if in_front(permit_str, msg) or in_front(unpermit_str, msg):
			return True
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
		
		zalgo_warn_duration = 1
		zalgo_warn_cooldown = 30
		zalgo_timeout_msg = "zalgo symbols"
		zalgo_timeout_duration = 1
		
		symbol_warn_duration = 1
		symbol_warn_cooldown = 30
		symbol_timeout_msg = "excessive use of symbols"
		symbol_timeout_duration = 1
		
		me_msg = "/me"
		me_warn_duration = 1
		me_warn_cooldown = 30
		me_timeout_msg = "usage of /me"
		me_timeout_duration = 1
		
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
		
		
		#add time, user, and message to array of 30second old messages
		'''perma permit for tecsbot avoids this
		if len(self.permit_arr) != 0:
			for permit_pair in self.permit_arr:
				if user not in '''
		if self.antispam_on:
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
					if self.emote_antispam_on:
						msg_emote_count = 0
						for emote in self.emote_arr:
							if word_count(msg, emote) != 0:
								msg_emote_count += msg.count(emote)
							if msg_emote_count >= emote_max:
								self.emote_warn_arr = warn(user, msg, channel_parsed, self, self.emote_warn_arr, emote_warn_duration, emote_warn_cooldown, emote_timeout_msg, emote_timeout_duration)
								return True
					#ban emotes
					if self.ban_emote_on:
						for ban_emote in self.ban_emote_arr:
							if word_count(msg, ban_emote) != 0:
								self.ban_emote_warn_arr = warn(user, msg, channel_parsed, self, self.ban_emote_warn_arr, ban_emote_warn_duration, ban_emote_warn_cooldown, ban_emote_timeout_msg, ban_emote_timeout_duration)
								return True
					
					#banphrases
					if self.banphrase_on:
						for banphrase in self.banphrase_arr:
							if banphrase in msg:
								self.banphrase_warn_arr = warn(user, msg, channel_parsed, self, self.banphrase_warn_arr, banphrase_warn_duration, banphrase_warn_cooldown, banphrase_timeout_msg, banphrase_timeout_duration)
								return True
								
					#caps spam
					if self.caps_antispam_on:
						if len(msg) >= caps_perc_min_msg_len:
							if caps_perc(msg) >= 60:
								self.caps_warn_arr = warn(user, msg, channel_parsed, self, self.caps_warn_arr, caps_warn_duration, caps_warn_cooldown, caps_timeout_msg, caps_timeout_duration)
								return True
					#fake purges
					if self.fake_purge_antispam_on:
						if msg in fake_purge_arr:
							self.fake_purge_warn_arr = warn(user, msg, channel_parsed, self, self.fake_purge_warn_arr, fake_purge_warn_duration, fake_purge_warn_cooldown, fake_purge_timeout_msg, fake_purge_timeout_duration)
							return True
					#!skincode
					if self.skincode_antispam_on:
						if in_front(skincode_msg, msg):
							self.skincode_warn_arr = warn(user, msg, channel_parsed, self, self.skincode_warn_arr, skincode_warn_duration, skincode_warn_cooldown, skincode_timeout_msg, skincode_timeout_duration)
							return True
					#long messages
					if self.long_msg_antispam_on:
						if len(msg) > msg_length_max:
							self.long_msg_warn_arr = warn(user, msg, channel_parsed, self, self.long_msg_warn_arr, long_msg_warn_duration, long_msg_warn_cooldown, long_msg_timeout_msg, long_msg_timeout_duration)
							return True
					#zalgo symbols
					#Very likely this will take a lot of time, find more efficient method if so
					if self.zalgo_antispam_on:
						for char in msg:
							if isinstance(char, unicode):
								print char
								print "HOLY SHIT A ZALGO HAPPENED"
								full_exit()
								if unicodedata.combining(char) != 0:
									#obviously will remove this when the damn thing works
									sys.exit("zalgo detected")
									self.zalgo_warn_arr = warn(user, msg, channel_parsed, self, self.zalgo_warn_arr, zalgo_warn_duration, zalgo_warn_cooldown, zalgo_timeout_msg, zalgo_timeout_duration)
									return True
					#block symbols
					
					#dongers
					

					#excessive symbols
					#if there are more than min_symbol_chars in message, check the percentage and amount
					if self.symbol_antispam_on:
						if len(msg) > min_symbol_chars:
							symbol_num = symbol_count(msg)
							symbol_perc = float(symbol_num) / len(msg)
							#if the limits are exceeded for num or percentage
							if symbol_num > max_symbol_num or symbol_perc > max_symbol_perc:
								self.symbol_warn_arr = warn(user, msg, channel_parsed, self, self.symbol_warn_arr, symbol_warn_duration, symbol_warn_cooldown, symbol_timeout_msg, symbol_timeout_duration)
								return True
					#links
					#need a way to parse out the link exactly, instead of just checking if ours is in the link
					#we can split by spaces, look at each one and see if it contains any of these, thus making it a link and allowing us to parse and do tthe things
					#how to do the *path things? for now it's exact match
					if self.link_antispam_on:
						for word in msg.split(" "):
							#we need to determine links for this sole reason
							if re.search(self.link_regex, word):#if is link according to our regex
								for link_whitelist in self.link_whitelist_arr:
									if "*" in link_whitelist:
										link_whitelist_wcard = link_whitelist_wcard.split("*")
										#this way if there is any part that is not in the word, it will move on
										#however if they are all in the word, it will do the else statement
										for link_wcard_part in link_whitelist_wcard:
											if link_wcard_part not in word:#time them out and return
												self.link_whitelist_warn_arr = warn(user, msg, channel_parsed, self, self.link_whitelist_warn_arr, link_whitelist_warn_duration, link_whitelist_warn_cooldown, link_whitelist_timeout_msg, link_whitelist_timeout_duration)
												return True
										else:#the link was a pardoned one, let them free
											break
									else:
										if link_whitelist == word:
											break
								else:
									#link isn't whitelisted, time out user 
									self.link_whitelist_warn_arr = warn(user, msg, channel_parsed, self, self.link_whitelist_warn_arr, link_whitelist_warn_duration, link_whitelist_warn_cooldown, link_whitelist_timeout_msg, link_whitelist_timeout_duration)
									return True
							
					#these need to be different types
					msg_arr = msg.split(" ")
					#long word spam
					if self.long_word_antispam_on:
						for word in msg_arr:
							if len(word) > long_word_limit and '\n' not in word:
								self.long_word_warn_arr = warn(user, msg, channel_parsed, self, self.long_word_warn_arr, long_word_warn_duration, long_word_warn_cooldown, long_word_timeout_msg, long_word_timeout_duration)
								return True
					#/me
					if self.me_antispam_on:
						if in_front(me_msg, msg):
							self.me_warn_arr = warn(user, msg, channel_parsed, self, self.me_warn_arr, me_warn_duration, me_warn_cooldown, me_timeout_msg, me_timeout_duration)
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
		
		if self.banphrase_on:
			msg_arr = msg.split(" ", 2)
			if in_front(banphrase_str, msg):
				if is_mod(user, self.channel_parsed, user_type): 
					if in_front(banphrase_add_str, msg):
						#if is_mod(user, self.channel_parsed, user_type):
						if len(msg_arr) > 2:#need to have this if statement more often
							banphrase = msg_arr[2]
							self.banphrase_arr.append(banphrase)
							send_str = "\"%s\" added to list of banphrases." % (banphrase)
						else:
							send_str = "Usage: \"!banphrase add <banphrase>\"" 
						#else:
							#send_str = "You have to be a mod to add banphrases." 
						#self.write(send_str)
				
					elif in_front(banphrase_del_str, msg) or in_front(banphrase_rem_str, msg):
						#if is_mod(user, self.channel_parsed, user_type):
						if len(msg_arr) > 2:
							banphrase = msg_arr[2]
							if is_num(banphrase):
								#we add on one to the actual index because users prefer to start with 1, rather than 0.
								banphrase = int(banphrase)
								if banphrase > 0 and banphrase <= len(self.banphrase_arr):
									send_str = "Banphrase \"%s\" removed at index %s." % (self.banphrase_arr[banphrase-1], banphrase)
									del self.banphrase_arr[banphrase-1]
								else:
									send_str = "Invalid index for banphrase removal." 
							else:
								if banphrase in self.banphrase_arr:
									self.banphrase_arr.remove(banphrase)
									send_str = "Banphrase \"%s\" removed." % (banphrase)									
								else:
									send_str = "Specified banphrase does not exist." 
						else:
							send_str = "Usage: \"!banphrase delete/remove <banphrase/index>\"" 
						#else:
							#send_str = "You have to be a mod to remove banphrases." %	
						#self.write(send_str)
					elif banphrase_list_str == msg:
						if len(self.banphrase_arr) == 0:
							send_str = "No active banphrases." 
						else:
							send_str = "Active banphrases: " 
							for banphrase in range(len(self.banphrase_arr)):
								if (banphrase != len(self.banphrase_arr) -1):
									#every element but last one
									send_str += "(%s.) %s, " % (banphrase+1, self.banphrase_arr[banphrase])
								else:
									#last element in arr
									send_str += "(%s.) %s." % (banphrase+1, self.banphrase_arr[banphrase])
								
					elif banphrase_clr_str == msg:
						self.banphrase_arr = []
						send_str = "All banphrases removed." 
					elif banphrase_str == msg:
						send_str = "Add or remove banphrases to timeout users who say them. Syntax and more information can be found in the documentation." 
					self.write(send_str)
				else:
					send_str = "You have to be a mod to use !banphrase commands." 
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
		
		if self.autoreply_on:
			if in_front(autoreply_str, msg):
				if is_mod(user, self.channel_parsed, user_type):
					#add autoreplies
					if in_front(autoreply_add_str, msg):
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) == 3:
							if ":" in msg_arr[2]:
								ar_msg_arr = msg_arr[2].split(":")
								if len(ar_msg_arr) == 2:
									ar_phrase = ar_msg_arr[0].rstrip().lstrip()
									ar_reply = ar_msg_arr[1].rstrip().lstrip()
									
									for ar_pair in self.ar_arr:
										if ar_phrase == ar_pair[0]:
											#dont add duplicates
											send_str = "%s is already an autoreply phrase." % (ar_pair[0])
											break
									else:
										if not disconnect_cmd(ar_reply):
											ar_pair = [ar_phrase, ar_reply]
											self.ar_arr.append(ar_pair)
											#[phrase[reply],phrase[reply]]hopefully
											send_str = "Phrase \"%s\" added, with reply \"%s\"." % (ar_phrase, ar_reply)
										else:
											send_str = "No \".disconnect\" or \"/disconnect\" variants allowed."
								else:
									#incorrectly formatted, display usage
									send_str = "Usage: \"!autoreply add <phrase>:<reply>\"." 
							else:
								#incorrectly formatted, display usage
								send_str = "Usage: \"!autoreply add <phrase>:<reply>\"." 
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!autoreply add <phrase>:<reply>\"." 
					#delete autoreplies
					elif in_front(autoreply_del_str, msg) or in_front(autoreply_rem_str, msg):
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) == 3:
							ar_phrase = msg_arr[2]
							if is_num(ar_phrase):
								if ar_phrase > 0 and ar_phrase <= len(self.ar_arr):
									send_str = "Autoreply %s:%s removed at index %s." % (self.ar_arr[int(ar_phrase)-1][0], self.ar_arr[int(ar_phrase)-1][1], ar_phrase)
									#should be the same index as the pair, after all.
									del self.ar_arr[int(ar_phrase)-1]
								else:
									send_str = "Invalid index for autoreply removal." 
							
							else:
								for ar_pair in self.ar_arr:
									if ar_phrase == ar_pair[0]:
										send_str = "Autoreply %s:%s removed." % (ar_pair[0], ar_pair[1])	
										self.ar_arr.remove(ar_pair)
										break
								else:
									send_str = "Specified autoreply does not exist." 
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!autoreply delete/remove <phrase/index>\"." 
					#list autoreplies
					elif autoreply_list_str == msg:
						#check to make sure there are autoreplies to list
						if len(self.ar_arr) == 0:
							send_str = "No active autoreplies." 
						else:
							send_str = "Active autoreplies: " 
							for ar_pair in range(len(self.ar_arr)):
								ar_phrase = self.ar_arr[ar_pair][0]
								ar_reply = self.ar_arr[ar_pair][1]
								if (ar_pair != len(self.ar_arr)-1):
									#every element but last one
									send_str += "(%s.) %s: %s, " % (ar_pair+1, ar_phrase, ar_reply)
								else:
									#last element in arr
									send_str += "(%s.) %s: %s." % (ar_pair+1, ar_phrase, ar_reply)
									
					#clear autoreplies
					elif autoreply_clr_str == msg:
						self.ar_arr = []
						send_str = "All autoreplies removed." 
					#just autoreply string, display usage
					elif autoreply_str == msg:
						send_str = "Add or remove phrases that trigger automatic replies. Syntax and more information can be found in the documentation." 
					else:
						send_str = "Usage: !autoreply add/delete/remove/list/clear" 
				else:
					send_str = "You have to be a mod to use !autoreply commands." 
				self.write(send_str)
			else:			
				if self.autoreply_on:
					for ar_pair in self.ar_arr:
						if ar_pair[0] == msg:
							reply = ar_pair[1]
							if in_front("/w", reply) or in_front(".w", reply):
								whisper_response(reply)
							else:
								self.write(reply)
							return False
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
		
		set_antispam_str = "!set antispam"
		set_repeat_antispam_str = "!set repeat antispam"
		set_emote_antispam_str = "!set emote antispam"
		set_caps_antispam_str = "!set caps antispam"
		set_fake_purge_antispam_str = "!set fake purge antispam"
		set_skincode_antispam_str = "!set skincode antispam"
		set_long_msg_antispam_str = "!set long message antispam"
		set_zalgo_antispam_str = "!set zalgo antispam"
		set_symbol_antispam_str = "!set symbol antispam"
		set_link_antispam_str = "!set link antispam"
		set_long_word_antispam_str = "!set long word antispam"
		set_me_antispam_str = "!set me antispam"
		
		set_ban_emotes_str = "!set ban emotes"
		set_emote_stats_str = "!set emote stats"
		
		set_rol_cmd_str = "!roulette"
		set_rol_chance_str = "!roulette chance"
		if in_front(set_str, msg):
			if is_mod(user, self.channel_parsed, user_type):
				msg_arr = msg.split(" ")
				if len(msg_arr) == 3:
					
					#turn roulette on or off
					if in_front(set_roulette_str, msg):
						self.rol_on = set_value(self.rol_on, "roulette", msg_arr, irc)
						
					#turn 8ball on or off
					elif in_front(set_ball_str, msg):
						self.ball_on - set_value(self.ball_on, "8ball", msg_arr, irc)
						
					#banphrases
					elif in_front(set_banphrase_str, msg):
						self.banphrase_on = set_value(self.banphrase_on, "banphrase", msg_arr, irc)
					
					#autoreplies
					elif in_front(set_autoreply_str, msg):
						self.autoreply_on = set_value(self.autoreply_on, "autoreply", msg_arr, irc)
						
					#antispam
					elif in_front(set_antispam_str, msg):
						self.antispam_on = set_value(self.antispam_on, "antispam", msg_arr, irc)
						
					#repeat
					elif in_front(set_repeat_str, msg):
						self.repeat_on = set_value(self.repeat_on, "repeat", msg_arr, irc)
				
				elif len(msg_arr) == 4:
					#repeat antispam
					if in_front(set_repeat_antispam_str, msg):
						self.repeat_antispam_on = set_value(self.repeat_antispam_on, "repeat antispam", msg_arr, irc)
						
					#emote antispam
					elif in_front(set_emote_antispam_str, msg):
						self.emote_antispam_on = set_value(self.emote_antispam_on, "emote antispam", msg_arr, irc)
						
					#caps antispam
					elif in_front(set_caps_antispam_str, msg):
						self.caps_antispam_on = set_value(self.caps_antispam_on, "caps antispam", msg_arr, irc)
					
					#skincode antispam
					elif in_front(set_skincode_antispam_str, msg):
						self.skincode_antispam_on = set_value(self.skincode_antispam_on, "skincode antispam", msg_arr, irc)
					
					#zalgo antispam
					elif in_front(set_zalgo_antispam_str, msg):
						self.zalgo_antispam_on = set_value(self.zalgo_antispam_on, "zalgo antispam", msg_arr, irc)
					
					#symbol antispam
					elif in_front(set_symbol_antispam_str, msg):
						self.symbol_antispam_on = set_value(self.symbol_antispam_on, "symbol antispam", msg_arr, irc)
					
					#link antispam
					elif in_front(set_link_antispam_str, msg):
						self.link_antispam_on = set_value(self.link_antispam_on, "link antispam", msg_arr, irc)
					
					#me antispam
					elif in_front(set_me_antispam_str, msg):
						self.me_antispam_on = set_value(self.me_antispam_on, "me antispam", msg_arr, irc)
						
					#ban emotes
					elif in_front(set_ban_emotes_str, msg):
						self.ban_emotes_on = set_value(self.ban_emotes_on, "ban emotes", msg_arr, irc)
					
					#emote stats
					elif in_front(set_emote_stats_str, msg):
						self.emote_stats_on = set_value(self.emote_stats_on, "emote stats", msg_arr, irc)
						
				elif len(msg_arr) == 5:
					#fake purge antispam
					if in_front(set_fake_purge_antispam_str, msg):
						self.fake_purge_antispam_on = set_value(self.fake_purge_antispam_on, "fake purge antispam", msg_arr, irc)
					
					#long message antispam
					elif in_front(set_long_msg_antispam_str, msg):
						self.long_msg_antispam_on = set_value(self.long_msg_antispam_on, "long message antispam", msg_arr, irc)
					
					#long word antispam
					elif in_front(set_long_word_antispam_str, msg):
						self.long_word_antispam_on = set_value(self.long_word_antispam_on, "long word antispam", msg_arr, irc)
				else:
					#usage
					send_str = "Usage: \"!set <feature> on/off \"." 
					self.write(send_str)
				#just set_str, explain usage.
				if set_str == msg:
					send_str = "Turn features on or off. Usage: \"!set <feature> on/off \"." 
					self.write(send_str)
			else:
				#not mod
				send_str = "You have to be a mod to use !set commands." 
				self.write(send_str)
		else:
			return False
	
	def vote_parse(self, user, msg, channel_parsed, user_type):
		#voting
		vote_str = "!vote"
		vote_start_str = "!vote start"
		vote_options_str = "!vote options"
		vote_reset_str = "!vote reset"
		vote_stats_str = "!vote stats"
		vote_end_str = "!vote end"
		vote_close_str = "!vote close"
		
		msg_arr = msg.split(" ", 2)
		#save us from going into the loop if the vote is off and the command is not !vote start, done by a mod
		if in_front(vote_str, msg) and is_mod(user, self.channel_parsed, user_type) and self.vote_on == False:
			if in_front(vote_start_str, msg):
				pass
			else:
				send_str = "There are no ongoing votes." 
				self.write(send_str)
				return
			
		if in_front(vote_str, msg):
			if len(msg_arr) >= 2:
				if in_front(vote_start_str, msg):
					if len(msg_arr) >= 3:
						if is_mod(user, self.channel_parsed, user_type):
							#reset vote stuffs
							self.vote_arr = []
							self.vote_users = []
							if self.vote_on:#if already ongoing poll
								send_str = "There is already an ongoing poll." 
							else:
								
								self.vote_option_arr = msg_arr[2].split(",")
								if len(self.vote_option_arr) > 1:
									self.vote_on = True
									send_str = "Poll opened! To vote use !vote <option/index>." 
									for vote_option_index, vote_option in enumerate(self.vote_option_arr): 
										self.vote_option_arr[vote_option_index] = self.vote_option_arr[vote_option_index].rstrip().lstrip()
										self.vote_arr.append([vote_option.strip(), 0])
									self.write(send_str)
									
									send_str = "Current vote options are: "
									for vote_option_index, vote_option in enumerate(self.vote_option_arr):
										if vote_option_index != len(self.vote_option_arr) -1:
											send_str += "(%s.) %s, " % (vote_option_index + 1, vote_option)
										else:
											send_str += "(%s.) %s." % (vote_option_index + 1, vote_option)	
									self.write(send_str)
									return [self.vote_option_arr, self.vote_arr, [], 0]
								else:
									send_str = "You must specify more than one option for a poll."
						else:
							send_str = "You have to be a mod to start a poll." 
					else:
						send_str = "Usage: !vote start <option1, option2, ...>" 
				elif in_front(vote_options_str, msg):
					if len(msg_arr) == 2:
						if is_mod(user, self.channel_parsed, user_type):
							if self.vote_on:
								send_str = "Current vote options are: "
								for vote_option_index, vote_option in enumerate(self.vote_option_arr):
									if vote_option_index != len(self.vote_option_arr) -1:
										send_str += "(%s.) %s, " % (vote_option_index + 1, vote_option)
									else:
										send_str += "(%s.) %s." % (vote_option_index + 1, vote_option)
							else:
								send_str = "No votes to display."
						else:	
							send_str = "You have to be whispering or a mod to view vote options"
					else:
						send_str = "Usage !vote options"
						
				elif in_front(vote_reset_str, msg):
					if is_mod(user, self.channel_parsed, user_type):
						for pair in self.vote_arr:
							pair[1] = 0
						send_str = "Votes reset." 
						self.write(send_str)
						return [self.vote_option_arr, self.vote_dict, [], 0]
					else:
						send_str = "You have to be a mod to reset the poll votes." 
				elif in_front(vote_stats_str, msg):
					if self.vote_on:
						if is_mod(user, self.channel_parsed, user_type):
							if self.vote_total != 0:
								send_str = "Current poll stats: "
								for pair in self.vote_arr:
									key = pair[0]
									value = pair[1]
									vote_perc = round((float(value) / self.vote_total) * 100, 2)
									vote_perc = prettify_num(vote_perc)
									send_str += "%s: %s%% " % (key, vote_perc)
								send_str += "Total votes: %s" % self.vote_total
								self.write(send_str)
								poll_winner = [['', 0]]
								for pair in self.vote_arr:
									key = pair[0]
									value = pair[1]
									option_perc = (float(poll_winner[0][1])/self.vote_total * 100)
									option_perc = prettify_num(option_perc)
									if value == poll_winner[0][1]:
										poll_winner.append([key, value])
									elif value > poll_winner[0][1]:
										poll_winner = [[key, value]]
								winner_perc = round(float(poll_winner[0][1])/self.vote_total * 100, 2)
								winner_perc = prettify_num(winner_perc)
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
							send_str = "You have to be a mod to display the current poll stats." 
					else:
						send_str = "There are no ongoing votes." 
				elif in_front(vote_end_str, msg) or in_front(vote_close_str, msg):
					#close the vote
					if self.vote_on:
						if is_mod(user, self.channel_parsed, user_type):
							self.vote_on = False
							send_str = "Poll stats: " 
							if self.vote_total != 0:
								poll_winner = [['', 0]]
								for pair in self.vote_arr:
									key = pair[0]
									value = pair[1]
									option_perc = round(float(value)/self.vote_total * 100, 2)
									option_perc = prettify_num(option_perc)
									if value == poll_winner[0][1]:
										poll_winner.append([key, value])
									elif value > poll_winner[0][1]:
										poll_winner = [[key, value]]
									send_str += "%s: %s%% " % (key, option_perc)
								send_str += "Total votes: %s" % self.vote_total
								self.write(send_str)
								winner_perc = round(float(poll_winner[0][1])/self.vote_total * 100, 2)
								winner_perc = prettify_num(winner_perc)
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
									send_str = "No vote winner, this shouldn't happen. Contact me if it does. value_dict: %s, poll_winners: %s" % (value_dict, poll_winner)
									
							else:
								send_str = "No votes to display." 
						else:
							send_str = "You have to be a mod to end a poll." 
					else:
						send_str = "There are no ongoing votes." 
						
				#elif user not in self.vote_users:
				#if user is in option
					#do nothing
				#if it's a different one, remove them
				#then add them to the other one
				#simple enough
				#deprecate vote users arr
				#check if new option is actually an option before removing them
				##################33
				#first bit should be fine need to add in a remove option for votes and make the numbers work like the manualoptions do
				#####################gl future self and hello strim
				else:
					if msg_arr[1].strip() in self.vote_option_arr: 
						
							#msg_arr[1] is a vote option
							#input vote if user hasnt already voted
							for vote_option_index, vote_option in enumerate(self.vote_arr):
								if msg_arr[1] == vote_option[0]:
									#do nothing if they are already in it, if not then find add them and remove them from the one they used to be in
									if user not in vote_option:
										self.vote_arr[vote_option_index][1] += 1
										self.vote_arr[vote_option_index].append(user)
										#if it's not the option they want and they are in it then remove them
										for old_vote_option_index, old_vote_option in enumerate(self.vote_arr):
											if old_vote_option != msg_arr[1] and user in old_vote_option[1:]:
												self.vote_arr[old_vote_option_index].remove(user)
												self.vote_total-=1
												break
									elif user in vote_option[1:]
										break#save some time, end this loop if they are already in the option they selected
									
							
							#self.vote_users.append(user)
							return [self.vote_option_arr, self.vote_arr, self.vote_users, self.vote_total]
					elif is_num(msg_arr[1].strip()) and msg_arr[1].strip() > 0 and msg_arr[1].strip() <= len(self.vote_arr):
						if user not in self.vote_users:
							self.vote_arr[int(msg_arr[1])-1][1] += 1
							self.vote_users.append(user)
							self.vote_total+=1
							return [self.vote_option_arr, self.vote_arr, self.vote_users, self.vote_total]
					else:
						if is_mod(user, self.channel_parsed, user_type):
							send_str = "Usage: !vote start/stats/reset/end/close" 
						else:
							send_str = "Usage: !vote <option/index>"
				
				'''else:
					if is_mod(user, self.channel_parsed, user_type):
						send_str = "Usage: !vote start/stats/reset/end/close" 
					else:
						return'''
			else:
				if is_mod(user, self.channel_parsed, user_type):
					send_str = "Usage: !vote start/reset/stats/end/close" 
				else:
					send_str = "Usage: !vote <option/index>"
		elif vote_str == msg:
			send_str = "Usage: !vote <option/index>"
		else:
			return False
		self.write(send_str)
		
	def raffle_parse(self, user, msg, channel_parsed, user_type):
		#raffle
		
		raffle_str = "!raffle"
		start_raffle_str = "!raffle start"
		end_raffle_str = "!raffle end"
		
		if in_front(raffle_str, msg):
			if self.raffle_on:
				#avoid duplicates
				if raffle_str == msg and user not in self.raffle_users:
					self.raffle_users.append(user)
				
				elif start_raffle_str == msg:
					if is_mod(user, self.channel_parsed, user_type):
						send_str = "There is already an ongoing raffle." 
					else:
						send_str = "Only mods can start raffles." 
					self.write(send_str)
					
				elif end_raffle_str == msg:
					if is_mod(user, self.channel_parsed, user_type):
						if len(self.raffle_users) > 0:
							winner = self.raffle_users[random.randint(0, (len(self.raffle_users) - 1))]
							#need to have prize of some sorts?
							send_str = "%s has won the raffle!" % (winner)
						else:
							send_str = "No one joined the raffle, there is no winner." 
						self.raffle_on = False
						self.raffle_users = []
						
					else:
						send_str = "Only mods can end raffles." 
					self.write(send_str)
			else:
				if start_raffle_str == msg:
					if is_mod(user, self.channel_parsed, user_type):
						self.raffle_on = True
						send_str = "Raffle started. Join the raffle with \"!raffle\"." % ()
					else:
						send_str = "Only mods can start raffles." 
					self.write(send_str)
				elif raffle_str == msg and is_mod(user, self.channel_parsed, user_type):
					send_str = "Usage: !raffle start/end" 
					self.write(send_str)
				elif end_raffle_str == msg:
					if is_mod(user, self.channel_parsed, user_type):
						send_str = "No ongoing raffles." 
					else:
						send_str = "Only mods can end raffles." 
					self.write(send_str)	
					
		else:
			return False
	
	def roulette_parse(self, user, msg, channel_parsed, user_type):
		#roulette
		#if user is mod then say it doesnt kill you or something
		#should absolutely just make the chance input in the GUI rather than text based.
		rol_str = "!roulette"
		rol_chance_str = "!roulette chance"
		
		if self.rol_on:
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
								input_perc = prettify_num(input_perc)
							if input_perc > 100 or input_perc < 0 or is_num(input_perc) == False:
								send_str = "Please input a percentage chance for roulette to be triggered, i.e. \"!roulette chance 50\". Chance must be between 0 and 100." 
							else:
								self.rol_chance = input_perc * .01
								input_perc = check_int(input_perc)
								send_str = "Roulette chance successfully changed to %s%%" % (input_perc)
						else:
							send_str = "Usage: !roulette chance <percent chance>" 
					else:
						send_str = "Only mods can change the chance of the roulette." 
					self.write(send_str)
				else:
					if is_mod(user, self.channel_parsed, user_type):
						send_str = "Usage: !roulette chance <percent chance>" 
						self.write(send_str)
			else:
				return False
	
	def ball_parse(self, user, msg, channel_parsed, user_type):
		#8ball
		#adding in deleting/adding/clearing of values
		ball_str = "!8ball"
		ball_list_str = "!8ball list"
		ball_add_str = "!8ball add"
		ball_del_str = "!8ball delete"
		ball_rem_str = "!8ball remove"
		ball_clr_str = "!8ball clear"
		#move this up a level when we allow editing of these values		
		
		if in_front(ball_str, msg):
			if self.ball_on:
				if is_mod(user, self.channel_parsed, user_type):
					msg_arr = msg.split(" ", 2)
					if in_front(ball_add_str, msg):
						#if is_mod(user, self.channel_parsed, user_type):
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
						return
					elif in_front(ball_del_str, msg) or in_front(ball_rem_str, msg):
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
						return
					elif in_front(ball_list_str, msg):
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
						return
					elif ball_clr_str == msg:
						if len(self.ball_arr) > 0:
							self.ball_arr = []
							send_str = "All 8ball responses removed." 
						else:	
							send_str = "There are currently no 8ball responses." 
						self.write(send_str)
						return
					elif ball_str == msg and is_mod(user, self.channel_parsed, user_type):
						send_str = "Usage: \"!8ball add/delete/remove/list/clear/<question>\"" 
						self.write(send_str)
						return

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
					self.write(send_str)
		else:
			return False
	
	def uptime_parse(self, user, msg, channel_parsed, user_type):
		#uptime
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
			
	def chatters_parse(self, user, msg, channel_parsed, user_type):
		chatters_str = "!chatters"
		#chatters
		if chatters_str == msg:
			chatter_data = get_json_chatters(self.channel_parsed)
			chatter_count = int(chatter_data["chatter_count"]) - 1 #don't count ourselves
			send_str = "There are currently %s accounts in chat." % (chatter_count)
			self.write(send_str)
		else:
			return False
			
	def viewers_parse(self, user, msg, channel_parsed, user_type):
		#viewers
		viewers_str = "!viewers"
		if viewers_str == msg:
			viewer_data = get_json_stream(self.channel_parsed)
			viewer_count = viewer_data["streams"][0]["viewers"]
			if viewer_count != '1':
				send_str = "There are currently %s viewers in the channel." % (viewer_count)
			else:
				send_str = "There is currently %s viewer in the channel." % (viewer_count)
			self.write(send_str)
		else:
			return False
			
	def subs_parse(self, user, msg, channel_parsed, user_type):
		#subscribers
		subscribers_str = "!subscribers"
		subs_str = "!subs"	
		if subs_str == msg or subscribers_str == msg:
			sub_data = get_json_subs(self.channel_parsed)
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
				else:
					#display usage
					send_str = "Usage: !commercial <length of commercial>"
			else:
				#not mod
				send_str = "You have to be the current streamer in order to start commercials." 
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
				if is_mod(user, self.channel_parsed, user_type): 
					if in_front(ban_emote_add_str, msg):
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
				
					elif in_front(ban_emote_del_str, msg) or in_front(ban_emote_rem_str, msg):
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
					elif in_front(ban_emote_clr_str, msg):
						self.ban_emote_arr = []
						send_str = "All ban emotes removed." 
					elif ban_emote_str == msg:
						send_str = "Add or remove ban emotes to timeout users who say them. Syntax and more information can be found in the documentation." 
					else:
						send_str = "Usage: \"!ban emote add/delete/remove/list/clear\"" 
					self.write(send_str)
				else:
					send_str = "You have to be a mod to use !ban emote commands." 
					self.write(send_str)
			else:
				return False
		else:
			return False
		'''ban_emote_str = "!ban emote"
		unban_emote_str = "!unban emote"
		#ban emotes
		if self.ban_emote_on:
			if in_front(ban_emote_str, msg):
				if is_mod(user, self.channel_parsed, user_type):
					msg_arr = msg.split(" ")
					if msg_arr == 3:
						ban_emote = msg_arr[2]
						self.ban_emote_arr.append(ban_emote)
						send_str = "Emote \"%s\" banned." % (ban_emote)
					else:
						send_str = "Usage: \"!ban emote <emote>\"" 
				else:
					send_str = "Only mods can ban emotes." 
				self.write(send_str)
				return
			if in_front(unban_emote_str, msg):
				if is_mod(user, self.channel_parsed, user_type):
					msg_arr = msg.split(" ")
					if msg_arr == 3:
						ban_emote = msg_arr[2]
						self.ban_emote_arr.remove(ban_emote)
						send_str = "%sEmote \"%s\" unbanned." % (ban_emote)
					else:
						send_str = "%sUsage: \"!unban emote <emote>\"" 
				else:
					send_str = "%sOnly mods can unban emotes." 
				self.write(send_str)
				return'''
	
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
		
		if self.repeat_on:
			if in_front(repeat_str, msg):
				if is_mod(user, self.channel_parsed, user_type):
					if in_front(repeat_add_str, msg):
						msg_arr = msg.split(" ")
						if len(msg_arr) > 3:
							del msg_arr[0:2]#remove command specifiers
							repeat_cmd = ''
							for cmd_part in range(len(msg_arr)):
								if cmd_part == len(msg_arr)-1:
									repeat_cmd = repeat_cmd.rstrip()#get rid of trailing space
									repeat_interval = msg_arr[cmd_part]
									
								else:
									repeat_cmd += msg_arr[cmd_part] + " "
							if not disconnect_cmd(repeat_cmd):
								current_time = time.time()
								repeat_set = [current_time, repeat_cmd, repeat_interval]
								self.repeat_arr.append(repeat_set)	
								send_str = "Repeat command \"%s\" added with interval %s." % (repeat_cmd, parse_sec_condensed(repeat_interval))
							else:
								send_str = "No \".disconnect\" or \"/disconnect\" variants allowed."
						else:
							send_str = "Usage: !repeat add <command> <interval>" 
					elif in_front(repeat_del_str, msg) or in_front(repeat_rem_str, msg):
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) > 2:
							repeat_cmd = msg_arr[2]
							if is_num(repeat_cmd):
								if repeat_cmd > 0 and repeat_cmd <= len(self.repeat_arr)
									send_str = "Repeat command \"%s\" with interval %s removed at index %s." % (self.repeat_arr[int(repeat_cmd)-1][1], parse_sec_condensed(self.repeat_arr[int(repeat_cmd)-1][2]), repeat_cmd)
									
									#should be the same index as the pair, after all.
									del self.repeat_arr[int(repeat_cmd)-1]
								else:
									send_str = "Invalid index for repeat command removal." 
							else:
								for repeat_set in self.repeat_arr:
									if repeat_cmd == repeat_set[1]:
										send_str = "Repeat command \"%s\" with interval %s removed." % (repeat_cmd, parse_sec_condensed(repeat_set[2]))		
										self.repeat_arr.remove(repeat_set)
										break
								else:
									send_str = "Specified repeat command does not exist." 
						else:
							send_str = "Usage: !repeat delete/remove <command/index>" 
					elif repeat_list_str == msg:
						if len(self.repeat_arr) == 0:
							send_str = "No active repeat commands." 
						else:
							send_str = "Active repeat commands: " 
							for repeat_set in range(len(self.repeat_arr)):
								repeat_cmd = self.repeat_arr[repeat_set][1]
								repeat_interval = self.repeat_arr[repeat_set][2]
								if (repeat_set != len(self.repeat_arr)-1):
									#every element but last one
									send_str += "(%s.) %s: %s, " % (repeat_set+1, repeat_cmd, parse_sec_condensed(repeat_interval))
								else:
									#last element in arr
									send_str += "(%s.) %s: %s." % (repeat_set+1, repeat_cmd, parse_sec_condensed(repeat_interval))
								
					elif repeat_clr_str == msg:
						self.repeat_arr = []
						send_str = "All repeat commands removed." 
					elif repeat_str == msg:
						send_str = "Add or remove commands to be repeated every specified interval. Syntax and more information can be found in the documentation." 
					else:
						send_str = "Usage: !repeat <add/delete/remove/list/clear> <command> <interval>" 
				else:
					#not moderino
					send_str = "You have to be a mod to use !repeat commands." 
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
		
		if self.cmd_on:
			if in_front(cmd_str, msg):
				if is_mod(user, self.channel_parsed, user_type):
					#add commands
					if in_front(cmd_add_str, msg):
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) == 3:
							if ":" in msg_arr[2] and in_front("!", msg_arr[2]):
								cmd_msg_arr = msg_arr[2].split(":")
								if len(cmd_msg_arr) == 2:
									cmd_phrase = cmd_msg_arr[0].rstrip().lstrip()
									cmd_reply = cmd_msg_arr[1].rstrip().lstrip()
									for default_cmd in self.default_cmd_arr:#dont add something that is already a default command
										if default_cmd == cmd_phrase:#cant do in front because then !banphrasejaklsdjfk is counted as a default cmd/not allowed
											send_str = "%s is already a default command." % (cmd_phrase)
											break
									else:
										for cmd_pair in self.cmd_arr:
											if cmd_phrase == cmd_pair[0]:
												#dont add duplicates
												send_str = "%s is already an custom command." % (cmd_pair[0])
												break
										else:
											if not disconnect_cmd(cmd_reply):
												cmd_pair = [cmd_phrase, cmd_reply]
												self.cmd_arr.append(cmd_pair)
												send_str = "Command \"%s\" added, with reply \"%s\"." % (cmd_phrase, cmd_reply)
											else:
												send_str = "No \".disconnect\" or \"/disconnect\" variants allowed."
								else:
									#incorrectly formatted, display usage
									send_str = "Usage: \"!command add !<command>:<reply>\"." 
							else:
								#incorrectly formatted, display usage
								send_str = "Usage: \"!command add !<command>:<reply>\"." 
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!command add !<command>:<reply>\"." 
					#delete commands
					elif in_front(cmd_del_str, msg) or in_front(cmd_rem_str, msg):
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) == 3:
							cmd_phrase = msg_arr[2]
							if is_num(cmd_phrase):
								if cmd_phrase > 0 and cmd_phrase <= len(self.cmd_arr):
									send_str = "Command %s:%s removed at index %s." % (self.cmd_arr[int(cmd_phrase)-1][0], self.cmd_arr[int(cmd_phrase)-1][1], cmd_phrase)
									#should be the same index as the pair, after all.
									del self.cmd_arr[int(cmd_phrase)-1]
								else:
									send_str = "Invalid index for command removal." 
							
							else:
								for cmd_pair in self.cmd_arr:
									if cmd_phrase == cmd_pair[0]:
										send_str = "Command %s:%s removed." % (cmd_pair[0], cmd_pair[1])	
										self.cmd_arr.remove(cmd_pair)
										break
								else:
									send_str = "Specified command does not exist." 
						else:
							#incorrectly formatted, display usage
							send_str = "Usage: \"!command delete/remove <command/index>\"." 
					#list commands
					elif cmd_list_str == msg:
						#check to make sure there are commands to list
						if len(self.cmd_arr) == 0:
							send_str = "No active commands." 
						else:
							send_str = "Active commands: " 
							for cmd_pair in range(len(self.cmd_arr)):
								cmd_phrase = self.cmd_arr[cmd_pair][0]
								cmd_reply = self.cmd_arr[cmd_pair][1]
								if (cmd_pair != len(self.cmd_arr)-1):
									#every element but last one
									send_str += "(%s.) %s: %s, " % (cmd_pair+1, cmd_phrase, cmd_reply)
								else:
									#last element in arr
									send_str += "(%s.) %s: %s." % (cmd_pair+1, cmd_phrase, cmd_reply)
									
					#clear commands
					elif cmd_clr_str == msg:
						self.cmd_arr = []
						send_str = "All custom commands removed." 
					#just cmd string, display usage
					elif cmd_str == msg:
						send_str = "Add or remove custom commands. Syntax and more information can be found in the documentation." 
					else:
						send_str = "Usage: !command add/delete/remove/list/clear" 
				else:
					send_str = "You have to be a mod to use !command commands." 
				self.write(send_str)
			else:			
				for cmd_pair in self.cmd_arr:
					if cmd_pair[0] == msg:
						reply = cmd_pair[1]
						if in_front("/w", reply) or in_front(".w", reply):
							whisper_response(reply)
						else:
							self.write(reply)
						return False
				return False
		else:
			return False
	
	def emote_stats_parse(self, user, msg, channel_parsed, user_type):
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
						send_str = "Total times %s has been sent: %s. %s per minute: %s." % (emote, self.count_dict[emote][0], emote, prettify_num(emote_per_min))
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
			for repeat_set in self.repeat_arr:
				repeat_time = repeat_set[0]
				repeat_cmd = repeat_set[1] 
				repeat_interval = prettify_num(repeat_set[2])
				if (current_time - repeat_time >= repeat_interval):
					repeat_set[0] = current_time#update the time
					self.write(repeat_cmd)
					self.main_parse(self.nickname, repeat_cmd, 'mod')
					
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
				
						
		#holy shit wish i thought of this earlier
		#only for debugging and development, will immediately stop execution of program
		#also because i am fucking tired of goldmine ads
		if 'goldmine' in msg or 'BTC' in msg or 'bitcoin' in msg or "rektmine" in msg:
			send_str = "/ban %s" % (user)
			self.write(send_str)
		if "e" == msg and (user == "darkelement75" or user == "dark_element_slave1"):
			full_exit()
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
		
		vote_return = self.vote_parse(user, msg, self.channel_parsed, user_type)
		if vote_return != False:
			if isinstance(vote_return, list):
				self.vote_option_arr = vote_return[0]
				self.vote_dict = vote_return[1]
				self.vote_users = vote_return[2]
				self.vote_total = vote_return[3]
			else:
				return
		
		if self.raffle_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.roulette_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.ball_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.uptime_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.chatters_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.viewers_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.subs_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.commercial_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.ban_emote_parse(user, msg, self.channel_parsed, user_type) != False:
			return
			
		if self.repeat_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.custom_command_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.emote_stats_parse(user, msg, self.channel_parsed, user_type) != False:
			return
		
		if self.mods_parse(user, msg, self.channel_parsed, user_type) != False:
			return
					
		#welcome newcomers - seems to be working with viewers and followers atm - need to figure out subs however
		#NOTE: TEMPORARILY DISABLED BECAUSE IT IS ANNOYING AS FUCK WHEN NOT PERMANENTLY ONLINE
		#new viewers
			#need to auth for sub list
		'''if user not in viewer_arr:
			#add to viewer_arr and then welcome them
			viewer_arr.append(user)
			send_str = "Hello newcomer %s, welcome to %s's self.channel!" % (user, self.channel_parsed)
			self.write(send_str)'''
		#new followers - currently disabled for the same reason the above one is
		#self.follower_arr = new_follower(self.follower_arr, self.channel_parsed, self)#will return False if there are none/service unavailable I suppose
		
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
		#for /mods response
		if args[0] == self.channel and "The moderators of this room are:" in args[1]:
			args[1] += ", and %s" % self.channel.replace("#", "")
			self.write(args[1])

	def write(self, msg):
		'''Send message to channel and log it'''
		self.msg(self.channel, msg)
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
		check_loop = LoopingCall(self.whisper_check)
		check_loop.start(0.003)
	
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


