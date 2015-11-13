# -*- coding: latin-1 -*-
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
have user checked for mod status either at beginning of parse_msg and have that as a is_mod BOOL, or just only check when they have issued a command
make !vote results also show the current winner?
use round() wherever needed
use enumerate wherever needed
point system for watching stream/chatting/etc
	more points -> greater chance to win prizes/raffles/etcidk
twitch has 500 character cap on messages, split up messages when listing
	going to implement this, but when we make a function for general sending we need to have this covered just in case
!x delete 21, 1, 5 <--- multiple deleting possibility <--- can we make a function for deleting?
still not sure the ["streams"][0] bit in get_json_stream will always work, can there be a [1]? Will [0] always be correct?
allow streamer to choose what to let mods do?<--- could work with level system
is_mod's api call is very delayed, is there a better way?
!followers

use more try except/catch 
just use [str(v) for v in list_thing] to remove unicode from strings<--what code was he referring to
apparently there are a few specific characters that zalgo text needs
use twisted instead of sockets and shit, borkedbot is good apparently
add in functions for parsing each of the things in parse_msg, ie if link-whitelist_on: link_whitelist_parse(msg, etd) <--do we do this with the antispam? if we do we will have to have a way to stop going through when a value is returned
replace irc.send with something that has \r\n and pre msg in it
we can put the large num of variables in another file and import if necessary
need to add .self to more variables 

"""
#time for oauth 
	#this will allow us to get a list of subscribers
	#idk what else it does but it is how people add your app to their channel/acct
	#this also gives us the permissions to do stuff like get the sub list
import socket #imports module allowing connection to IRC
import thread, threading #imports module allowing timing functions
import sys, operator, time, urllib, json, math, os, random, unicodedata, requests, select
from datetime import datetime, timedelta
import re#regex
import string#string constants

def get_json_servers():
	url = "http://tmi.twitch.tv/servers?cluster=group"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return data
	
bot_owner = 'darkelement75'
nick = 'tecsbot' 
ping_nick = "@%s" % nick
permit_nick = "Tmi.twitch.tv 001 %s" % nick
#for now making this whatever I input
channel = '#_tecsbot_1444071429976'
#channel = sys.argv[1]
channel_parsed = channel.replace("#", "")

pre_msg = "PRIVMSG %s :" % channel

server_json = get_json_servers()
server_arr = (server_json["servers"][0]).split(":")
server = server_arr[0]
port = int(server_arr[1])

password = 'oauth:'

queue = 13 #sets variable for anti-spam queue functionality <- dafuq is this used for<--I wanna delete it

#initial connect
irc = socket.socket()
irc.connect((server, port)) #connects to the server
#sends variables for connection to twitch chat
irc.send('PASS ' + password + "\r\n")
irc.send('NICK ' + nick + "\r\n")
irc.send('JOIN ' + channel + "\r\n")

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

vote_total = 0
'''
#this is already in channel settings
blacklist_timeout = 10 #seconds
blacklist_arr = ["belgium"]
'''
#This determines whether to do search_str == msg, or search_str in message when looking for commands
cmd_match_full = True

#initial connect

access_token = '0w9a9qhr1igy777149s66iryox6tjb'




#for debugging
def full_exit():
	os._exit(1)

def connect_channel(channel):
	irc = socket.socket()
	irc.connect((server, 6667)) #connects to the server
	#sends variables for connection to twitch chat
	irc.send('PASS ' + password + "\r\n")
	irc.send('USER ' + nick + ' 0 * :' + bot_owner + "\r\n")
	irc.send('NICK ' + nick + "\r\n")
	irc.send('JOIN ' + channel + "\r\n")

def connect_group():
	irc = socket.socket()
	irc.connect((server, port)) #connects to the server
	#sends variables for connection to twitch chat
	#/commands and /tags both work apparently, just gonna use this
	irc.send("CAP REQ :twitch.tv/commands\r\n")
	irc.send("CAP REQ :twitch.tv/membership\r\n")
	irc.send("CAP REQ :twitch.tv/tags\r\n")
	irc.send('PASS ' + password + "\r\n")
	irc.send('NICK ' + nick + "\r\n")
	irc.send('JOIN ' + channel + "\r\n")
	
def start_log(log_file_path):
	#if log file already exists, delete it and create new one.
	#need to execute this when the stream starts, should wait for get_uptime_min to be less than 1?
	if os.path.exists(log_file_path):
		os.remove(log_file_path)
	new_log_file = open(log_file_path, 'w')
	new_log_file.close	
	
def create_dict(dict, emote_file_path):
	#create dictionary of emotes and set all counts to 0
	#for some reason nothing will read any more emotes out of this file after this loop goes through each line, once.
	emotes_file = open(emote_file_path, 'r')
	#log_file = open(log_file_path, 'r')
	for emote in emotes_file:
		emote = emote.rstrip()
		dict[emote] = []
		dict[emote].append(0)
	return dict

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
				count_dict[emote][0] += emote_count

def find_per_min(emote, channel_parsed):
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
	return requests.get(url).json()
	
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
	
def start_commercial(length, channel_parsed):
	url = "https://api.twitch.tv/kraken/channels/%s/commercial" % channel_parsed
	data = requests.post(url, data={'oauth_token': access_token, 'length' : length})
	print data.json()
	return data.json()
	
def stream_online(channel_parsed):
	#we use this return value to trigger the loop of everything.
	channel_json = get_json_stream(channel_parsed)
	stream_status = channel_json["streams"]
	if stream_status == None:
		return False
	else:
		return True
	
def get_uptime_min():
	channel_json = get_json_stream(channel_parsed)
	#parse out unnecessary stuffs
	start_time = channel_json["streams"]["created_at"].replace("Z", "").replace("T", "-")
	#convert to datetime object
	start_time = time.strptime(start_time, "%Y-%m-%d-%H:%M:%S")
	#convert to unix time so we can calculate amount of hours and seconds it's been up, and other calculations.
	uptime = time.mktime(start_time) - 4*3600
	#subtract 4 hours from the (now unix)time, making it equal in time zones to ours,
	#then take current time and created time and get the difference.
	uptime = time.time() - uptime
	minute = uptime / 60
	#return the minutes for epm calculations
	return minute

def get_uptime_str(pre_msg, channel_parsed):
	channel_json = get_json_stream(channel_parsed)
	#parse out unnecessary stuffs
	start_time = channel_json["streams"][0]["created_at"].replace("Z", "").replace("T", "-")
	#convert to datetime object
	start_time = time.strptime(start_time, "%Y-%m-%d-%H:%M:%S")
	#convert to unix time so we can calculate amount of hours and seconds it's been up, and other calculations.
	uptime = time.mktime(start_time) - 4*3600
	#subtract 4 hours from the (now unix)time, making it equal in time zones to ours,
	#then take current time and created time and get the difference.
	uptime = time.time() - uptime
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
	sec = float(math.floor((sec - hour *3600 - minute*60)))
	return_str = ""
	if sec.is_integer():
		sec = int(sec)
		
	return_str += get_time_return_str(hour, "hour")
	return_str += get_time_return_str(minute, "minute")
	return_str += get_time_return_str(sec, "second")
	if return_str.endswith(", "):
		return_str = return_str[:-2]
	return return_str

def parse_sec_condensed(sec):
	hour = int(math.floor(sec/3600))
	minute = int(math.floor((sec - hour *3600) / 60))
	sec = int(math.floor((sec - hour *3600 - minute*60)))
	if hour == 0 and minute == 0:
		return_str = "%ss" % (sec)
	elif hour == 0:
		return_str = "%sm %ss" % (minute, sec)
	else:
		return_str = "%sh %sm %ss" % (hour, minute, sec)	
	#return the string for sending
	return return_str
	
def is_mod(user, channel_parsed):
	'''
	itslikesnowboarding:    !8ball do you know how to make computers go faster?
	Unhandled exception in thread started by <bound method channel_bot_start.main of <__main__.channel_bot_start object at 0x0000000002C987F0>>
	Traceback (most recent call last):
	  File "C:\Python27\Scripts\tecsbot_main.py", line 2172, in main
		parse_msg(user, msg, irc)
	  File "C:\Python27\Scripts\tecsbot_main.py", line 1890, in parse_msg
		if self.ball_parse(user, msg, irc, pre_msg, channel_parsed) != False:
	  File "C:\Python27\Scripts\tecsbot_main.py", line 1586, in ball_parse
		if is_mod(user, channel_parsed):
	  File "C:\Python27\Scripts\tecsbot_main.py", line 394, in is_mod
		if user == str(mod):
	LookupError: unknown encoding: darkelement75'''
	channel_json = get_json_chatters(channel_parsed)
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
	return False

def is_streamer(user, channel_parsed):
	if user == channel_parsed:
		return True
	else:
		return False
	
def create_viewer_arr():
	channel_json = get_json_chatters(channel_parsed)
	viewer_arr = []
	viewers = channel_json["chatters"]["viewers"]
	viewer_arr.extend(viewers)
	return viewer_arr
	
def new_follower(follower_arr, channel_parsed, pre_msg):
	follows_json = get_json_follows(channel_parsed)
	#need to return follower if there are any, and false if not
	if follows_json["follows"][0]["user"]["display_name"] not in follower_arr:
		#if the first is not already recorded, then new follower
		follower_arr.append(follows_json["follows"][0]["user"]["display_name"])
		send_str = "%sHello %s! Thank you for following %s's channel!\r\n" % (pre_msg, follows_json["follows"][0]["user"]["display_name"], channel_parsed)
		irc.send(send_str)
	for follower in follows_json["follows"]:
		#add all that arent already recorded
		if follower["user"]["display_name"] not in follower_arr:
			follower_arr.append(follower["user"]["display_name"])
	return follower_arr

def timeout(user, irc, pre_msg, timeout):
	send_str = "%s/timeout %s %s\r\n" % (pre_msg, user, timeout)
	irc.send(send_str)

	#def whisper(user, msg, irc):
	'''
	alright so we need to have it always connected to the group chat of the channel, so we make a huge function for that so that
	it always stays on it, but how can we get it to accept new data while in execution?
	
	main.py /whisper.py can have all the child processes underneath it - each child process is a channel bot,
	need to figure out how to set up the child processes stuff with rpyc, but should be able to communicate between the main and child with stdin/stdout
	main function can have exposed_send function to accept send/whisper data from the child processes/channel bots
	maybe have them hosted under localhost with rpyc so that the main/child process thing works im not sure how that whole setup works 
	main whisper bot with exposed send function -> child channel bots sending whisper data
	I think/hope we gucci now
	'''
	################33
	#need to have multithreading hooked up before this will work
	'''send_str = "%s/w %s %s\r\n" % (pre_msg, user, msg)
	print send_str
	irc.send(send_str)'''
	
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
		
def set_value(set_on, set_feature, msg_arr, pre_msg, irc):
		if msg_arr[2] == "on":
			if set_on == True:
				send_str = "%s%s is already on.\r\n" % (pre_msg, set_feature.capitalize())
			else:
				set_on = True
				send_str = "%s%s turned on. You can do \"!set %s off\" to turn it off again.\r\n" % (pre_msg, set_feature.capitalize(), set_feature)
		elif msg_arr[2] == "off":
			if set_on == False:
				send_str = "%s%s is already off.\r\n" % (pre_msg, set_feature.capitalize())
			else:
				set_on = False
				send_str = "%s%s turned off. You can do \"!set %s on\" to turn it on again.\r\n" % (pre_msg, set_feature.capitalize(), set_feature)
		else:
			#usage
			send_str = "%sUsage: \"!set %s on/off \".\r\n" % (pre_msg, set_feature)
		irc.send(send_str)
		return set_on

def create_emote_arr(emote_file_path):
	emotes_file = open(emote_file_path, 'r')		
	emote_arr = []
	for emote in emotes_file:
		emote = emote.rstrip()
		emote_arr.append(emote)
	return emote_arr

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
	
def warn(user, msg, pre_msg, channel_parsed, irc, warn_arr, warn_duration, warn_cooldown, timeout_msg, timeout_duration):
	#function to warn if they havent already been warned, and time them out if they have.
	for warn_pair in warn_arr:
		if user == warn_pair[1]:
			#check if current time is longer than the warning duration from the last time name was entered
			current_time = time.time()
			if (current_time - warn_pair[0] <= warn_cooldown):
				#timeout user for long duration and remove from array
				timeout(user, irc, pre_msg, timeout_duration)
				warn_arr.remove(warn_pair)
				send_str = "%sNo %s allowed (%s)\r\n" % (pre_msg, timeout_msg, user.capitalize())
				irc.send(send_str)
				whisper_msg = "You were timed out for %s in %s (%s)" % (timeout_msg, channel_parsed, parse_sec(timeout_duration))
				whisper(user, whisper_msg)
				whisper_user = user
				return warn_arr
			else:
				#replace old entry with new one and send warning as well as timeout for warn_duration
				#short duration
				timeout(user, irc, pre_msg, warn_duration)
				warn_arr.remove(warn_pair)
				pair = [current_time, user]
				warn_arr.append(pair)
				send_str = "%sNo %s allowed (%s)(warning)\r\n" % (pre_msg, timeout_msg, user.capitalize())
				irc.send(send_str)
				whisper_msg = "You were timed out for %s in %s (%s, warning)" % (timeout_msg, channel_parsed, parse_sec(warn_duration))
				whisper(user, whisper_msg)				
				whisper_user = user
				return warn_arr
	else:
		#add new entry and send warning, with timeout for warn_duration
		#short duration
		timeout(user, irc, pre_msg, warn_duration)
		current_time = time.time()
		pair = [current_time, user]
		warn_arr.append(pair)
		send_str = "%sNo %s allowed (%s)(warning)\r\n" % (pre_msg, timeout_msg, user.capitalize())
		irc.send(send_str)
		whisper_msg = "You were timed out for %s in %s (%s, warning)" % (timeout_msg, channel_parsed, parse_sec(warn_duration))
		whisper(user, whisper_msg)
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

def long_print(next_str, send_str, pre_msg, irc):
	#this accounts for any messages longer than the character cap
	if math.floor((len(send_str)-len(pre_msg)+len(next_str)) / 500) > 0:
		if "\r\n" in next_str:
			#if it's the last string to be added, make sure this new message is necessary
			if math.floor((len(send_str)-len(pre_msg)+len(next_str)-4) / 500) > 0:
				send_str += "\r\n"
				irc.send(send_str)
				send_str = pre_msg + next_str
		else:
			send_str += "\r\n"
			irc.send(send_str)
			send_str = pre_msg + next_str
	else:
		send_str += next_str
	return send_str	
	
def whisper(user, msg):	
	send_str = "%s/w %s %s\r\n" % (pre_msg, user, msg)
	irc.send(send_str)

#def display_round(num):
	
class channel_bot_start(object):
	
	def __init__(self, channel):
		#take the object and make it 
		self.channel = channel # Grab the channel thing we're passed, and store it in the class
		
	def link_whitelist_parse(self, user, msg, irc, pre_msg, channel_parsed):
		link_whitelist_str = "!link whitelist"
		link_whitelist_add_str = "!link whitelist add"
		link_whitelist_del_str = "!link whitelist delete"
		link_whitelist_rem_str = "!link whitelist remove"
		link_whitelist_list_str = "!link whitelist list"
		link_whitelist_clr_str = "!link whitelist clear"

		if self.link_whitelist_on:
			if in_front(link_whitelist_str, msg):
				if is_mod(user, channel_parsed):
					msg_arr = msg.split(" ")
					if in_front(link_whitelist_add_str, msg):
						if len(msg_arr) > 3:
							link_whitelist = msg_arr[3]
							if re.search(self.link_regex, link_whitelist):#if is link according to our regex
								#is a url
								if link_whitelist in self.link_whitelist_arr:#if already whitelisted
									send_str = "%s%s is already a whitelisted link.\r\n" % (pre_msg, link_whitelist)
								else:
									self.link_whitelist_arr.append(link_whitelist)
									send_str = "%s%s added to list of whitelisted links.\r\n" % (pre_msg, link_whitelist)
							else:
								send_str = "%s%s is not a valid link.\r\n" % (pre_msg, link_whitelist)
						else:
							send_str = "%sUsage: \"!link whitelist add <link>\"\r\n" % pre_msg
					elif in_front(link_whitelist_del_str, msg) or in_front(link_whitelist_rem_str, msg):
						if len(msg_arr) > 3:
							link_whitelist = msg_arr[3]
							if is_num(link_whitelist):
								#we add on one to the actual index because users prefer to start with 1, rather than 0.
								link_whitelist = int(link_whitelist)
								if ((len(self.link_whitelist_arr)-1) >= link_whitelist-1):
									send_str = "%sLink %s removed at index %s.\r\n" % (pre_msg, self.link_whitelist_arr[link_whitelist-1], link_whitelist)
									del self.link_whitelist_arr[link_whitelist-1]
								else:
									send_str = "%sInvalid index for link removal.\r\n" % pre_msg
							else:
								if link_whitelist in self.link_whitelist_arr:
									self.link_whitelist_arr.remove(link_whitelist)
									send_str = "%sLink %s removed.\r\n" % (pre_msg, link_whitelist)									
								else:
									send_str = "%sSpecified link does not exist.\r\n" % pre_msg
						else:
							send_str = "%sUsage: \"!link whitelist delete/remove <link/index>\"\r\n" % pre_msg
					elif link_whitelist_list_str == msg:
							if len(self.link_whitelist_arr) == 0:
								send_str = "%sNo active links.\r\n" % pre_msg
							else:
								send_str = "%sActive links: " % pre_msg
								for link_whitelist in range(len(self.link_whitelist_arr)):
									if (link_whitelist != len(self.link_whitelist_arr) -1):
										#every element but last one
										next_str = "(%s.) %s, " % (link_whitelist+1, self.link_whitelist_arr[link_whitelist])
									else:
										#last element in arr
										next_str = "(%s.) %s.\r\n" % (link_whitelist+1, self.link_whitelist_arr[link_whitelist])
									send_str = long_print(next_str, send_str, pre_msg, irc)
					elif link_whitelist_clr_str == msg:
						self.link_whitelist_arr = []
						send_str = "%sAll links removed.\r\n" % pre_msg
					elif link_whitelist_str == msg:
						send_str = "%sAdd or remove links to timeout users who say them. Syntax and more information can be found in the documentation.\r\n" % pre_msg
					else:
						send_str = "%sUsage: \"!link whitelist add/delete/remove/list/clear\"\r\n" % pre_msg
				else:
					send_str = "%sYou have to be a mod to use !list whitelist commands.\r\n" % pre_msg
				irc.send(send_str)
			else:
				return False
		else:
			return False
	
	def spam_permit_parse(self, user, msg, irc, pre_msg, channel_parsed):
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
			if is_mod(user, channel_parsed):
				msg_arr = msg.split(" ")
				if in_front(permit_add_str, msg):#!permit add
					if len(msg_arr) >= 3:
						permit_user = msg_arr[2]
						if is_num(permit_user) == False and (permit_user != "time" or permit_user != "message" or permit_user != "permanent"):
							#!permit add <user>
							if len(msg_arr) == 3:
								current_time = time.time()
								permit_time = self.default_permit_time
								permit_type = "time"
								permit_pair = [current_time, permit_user, permit_time, permit_type]
								self.permit_arr.append(permit_pair)
								send_str = "%s%s's spam filter has been lifted for %s.\r\n" % (pre_msg, permit_user, parse_sec_condensed(permit_time))
							elif len(msg_arr) == 4:
								if msg_arr[3] == "time":
									#!permit add <user> time
									current_time = time.time()
									permit_time = self.default_permit_time
									permit_type = "time"
									permit_pair = [current_time, permit_user, permit_time, permit_type]
									self.permit_arr.append(permit_pair)
									send_str = "%s%s's spam filter has been lifted for %s.\r\n" % (pre_msg, permit_user, parse_sec_condensed(permit_time))
								elif msg_arr[3] == "message":
									#!permit add <user> message
									msg_count = self.default_permit_msg_count
									permit_type = "message"
									permit_pair = [0, permit_user, msg_count, permit_type]#0 = current msg count
									self.permit_arr.append(permit_pair)
									send_str = "%s%s's spam filter has been lifted for %s messages.\r\n" % (pre_msg, permit_user, msg_count)
								elif msg_arr[3] == "permanent":
									#!permit add <user> permanent
									permit_type = "permanent"
									permit_pair = [0, permit_user, 0, permit_type]#0 = current msg count
									self.permit_arr.append(permit_pair)
									send_str = "%s%s's spam filter has been permanently lifted.\r\n" % (pre_msg, permit_user)
								elif is_num(msg_arr[3]):
									#!permit add <user> <time duration>
									current_time = time.time()
									permit_time = check_int(float(msg_arr[3]))
									permit_type = "time"
									permit_pair = [current_time, permit_user, permit_time, permit_type]
									self.permit_arr.append(permit_pair)
									send_str = "%s%s's spam filter has been lifted for %s.\r\n" % (pre_msg, permit_user, parse_sec_condensed(permit_time))
								else:
									send_str = "%sUsage: !permit add <user> message/time <message count/time duration>\r\n" % pre_msg
							elif len(msg_arr) == 5:
								if msg_arr[3] == "time":
									if is_num(msg_arr[4]):
										#!permit add <user> <type> <time duration>
										current_time = time.time()
										permit_time = check_int(float(msg_arr[4]))
										permit_type = "time"
										permit_pair = [current_time, permit_user, permit_time, permit_type]
										self.permit_arr.append(permit_pair)
										send_str = "%s%s's spam filter has been lifted for %s.\r\n" % (pre_msg, permit_user, parse_sec_condensed(permit_time))
									else:
										send_str = "%sUsage: !permit add <user> message/time <message count/time duration>\r\n" % pre_msg
								elif msg_arr[3] == "message":
									if is_num(msg_arr[4]):
										#!permit add <user> <type> <message count>
										msg_count = check_int(float(msg_arr[4]))
										permit_type = "message"
										permit_pair = [0, permit_user, msg_count, permit_type]#0 = current msg count
										self.permit_arr.append(permit_pair)
										send_str = "%s%s's spam filter has been lifted for %s messages.\r\n" % (pre_msg, permit_user, msg_count)
									else:
										send_str = "%sUsage: !permit add <user> message/time <message count/time duration>\r\n" % pre_msg
								else:
									send_str = "%sUsage: !permit add <user> message/time <message count/time duration>\r\n" % pre_msg
							else:
								send_str = "%sUsage: !permit add <user> message/time <message count/time duration>\r\n" % pre_msg
						else:
							send_str = "%sUsage: !permit add <user> message/time <message count/time duration>\r\n" % pre_msg
					else:
						send_str = "%sUsage: !permit add <user> message/time <message count/time duration>\r\n" % pre_msg
							
				#delete/remove
				elif in_front(permit_del_str, msg) or in_front(permit_rem_str, msg):
					if len(msg_arr) == 3:
						permit_user = msg_arr[2]
						if is_num(permit_user):
							if ((len(self.permit_arr)-1) >= int(permit_user)-1):
								send_str = "%sPermit %s removed at index %s.\r\n" % (pre_msg, self.permit_arr[int(permit_user)-1][1], permit_user)
								#should be the same index as the pair, after all.
								del self.permit_arr[int(permit_user)-1]
							else:
								send_str = "%sInvalid index for permit removal.\r\n" % pre_msg										
						else:
							for permit_pair in self.permit_arr:
								if permit_user == permit_pair[1]:
									self.permit_arr.remove(permit_pair)
									send_str = "%sPermit \"%s\" removed.\r\n" % (pre_msg, permit_user)		
									break
							else:
								send_str = "%sSpecified permit does not exist.\r\n" % pre_msg
					else:
						#incorrectly formatted, display usage
						send_str = "%sUsage: \"!permit delete/remove <user/index>\".\r\n" % pre_msg
				#list
				elif permit_list_str == msg:
					if len(self.permit_arr) == 0:
						send_str = "%sNo users with active permits.\r\n" % pre_msg
					else:
						send_str = "%sUsers with active permits: " % pre_msg
						for permit_pair in range(len(self.permit_arr)):
							if (permit_pair != len(self.permit_arr) -1):
								#every element but last one
								if self.permit_arr[permit_pair][3] == "time":
									next_str = "(%s.) %s : %s, " % (permit_pair+1, self.permit_arr[permit_pair][1], parse_sec_condensed(self.permit_arr[permit_pair][2]))
								elif self.permit_arr[permit_pair][3] == "message":
									next_str = "(%s.) %s : %s messages, " % (permit_pair+1, self.permit_arr[permit_pair][1], self.permit_arr[permit_pair][2])
								else:
									next_str = "(%s.) %s : infinite, " % (permit_pair+1, self.permit_arr[permit_pair][1])
							else:
								#last element in arr
								if self.permit_arr[permit_pair][3] == "time":
									next_str = "(%s.) %s : %s.\r\n" % (permit_pair+1, self.permit_arr[permit_pair][1], parse_sec_condensed(self.permit_arr[permit_pair][2]))
								elif self.permit_arr[permit_pair][3] == "message":
									next_str = "(%s.) %s : %s messages.\r\n" % (permit_pair+1, self.permit_arr[permit_pair][1], self.permit_arr[permit_pair][2])
								else:
									next_str = "(%s.) %s : infinite.\r\n" % (permit_pair+1, self.permit_arr[permit_pair][1])
							send_str = long_print(next_str, send_str, pre_msg, irc)
				#clear
				elif permit_clr_str == msg:
					self.permit_arr = []
					send_str = "%sAll permits removed.\r\n" % pre_msg
				#normal
				elif permit_str == msg:
					if is_mod(user, channel_parsed):
						send_str = "%sAdd or remove spam permits, allowing a user to message anything for a certain number of messages, or a length of time. Syntax and more information can be found in the documentation.\r\n" % pre_msg
					else:
						send_str = "%sYou have to be a mod to use !permit commands\r\n" % pre_msg
				#!permit <user>...
				elif len(msg_arr) >= 2:
					permit_user = msg_arr[1]
					if is_num(permit_user) == False and (permit_user != "time" or permit_user != "message"):
						#!permit <user>
						if len(msg_arr) == 2:
							current_time = time.time()
							permit_time = self.default_permit_time
							permit_type = "time"
							permit_pair = [current_time, permit_user, permit_time, permit_type]
							self.permit_arr.append(permit_pair)
							send_str = "%s%s's spam filter has been lifted for %s.\r\n" % (pre_msg, permit_user, parse_sec_condensed(permit_time))
						elif len(msg_arr) == 3:
							if msg_arr[2] == "time":
								#!permit <user> time
								current_time = time.time()
								permit_time = self.default_permit_time
								permit_type = "time"
								permit_pair = [current_time, permit_user, permit_time, permit_type]
								self.permit_arr.append(permit_pair)
								send_str = "%s%s's spam filter has been lifted for %s.\r\n" % (pre_msg, permit_user, parse_sec_condensed(permit_time))
							elif msg_arr[2] == "message":
								#!permit <user> message
								msg_count = self.default_permit_msg_count
								permit_type = "message"
								permit_pair = [0, permit_user, msg_count, permit_type]#0 = current msg count
								self.permit_arr.append(permit_pair)
								send_str = "%s%s's spam filter has been lifted for %s messages.\r\n" % (pre_msg, permit_user, msg_count)
							elif msg_arr[2] == "permanent":
								#!permit <user> permanent
								permit_type = "permanent"
								permit_pair = [0, permit_user, 0, permit_type]#0 = current msg count
								self.permit_arr.append(permit_pair)
								send_str = "%s%s's spam filter has been permanently lifted.\r\n" % (pre_msg, permit_user)
							elif is_num(msg_arr[2]):
								#!permit <user> <time duration>
								current_time = time.time()
								permit_time = float(msg_arr[2])
								permit_type = "time"
								permit_pair = [current_time, permit_user, permit_time, permit_type]
								self.permit_arr.append(permit_pair)
								send_str = "%s%s's spam filter has been lifted for %s.\r\n" % (pre_msg, permit_user, parse_sec_condensed(permit_time))
							else:
								send_str = "%sUsage: !permit <user> message/time <message count/time duration>\r\n" % pre_msg
						elif len(msg_arr) == 4:
							if msg_arr[2] == "time":
								if is_num(msg_arr[3]):
									#!permit add <user> <type> <time duration>
									current_time = time.time()
									permit_time = float(msg_arr[3])
									permit_type = "time"
									permit_pair = [current_time, permit_user, permit_time, permit_type]
									self.permit_arr.append(permit_pair)
									send_str = "%s%s's spam filter has been lifted for %s.\r\n" % (pre_msg, permit_user, parse_sec_condensed(permit_time))
								else:
									send_str = "%sUsage: !permit <user> message/time <message count/time duration>\r\n" % pre_msg
							elif msg_arr[2] == "message":
								if is_num(msg_arr[3]):
									#!permit add <user> <type> <message count>
									
									msg_count = check_int(float(msg_arr[3]))
									permit_type = "message"
									permit_pair = [0, permit_user, msg_count, permit_type]#0 = current msg count
									self.permit_arr.append(permit_pair)
									send_str = "%s%s's spam filter has been lifted for %s messages.\r\n" % (pre_msg, permit_user, msg_count)
								else:
									send_str = "%sUsage: !permit <user> message/time <message count/time duration>\r\n" % pre_msg
							else:
								send_str = "%sUsage: !permit <user> message/time <message count/time duration>\r\n" % pre_msg
						else:
							send_str = "%sUsage: !permit <user> message/time <message count/time duration>\r\n" % pre_msg
					else:
						send_str = "%sUsage: !permit <user> message/time <message count/time duration>\r\n" % pre_msg
				else:
					if is_mod(user, channel_parsed):
						send_str = "%sAdd or remove spam permits, allowing a user to message anything for a certain number of messages, or a length of time. Syntax and more information can be found in the documentation.\r\n" % pre_msg
					else:
						send_str = "%sYou have to be a mod to use !permit commands\r\n" % pre_msg
			
			else:
				send_str = "%sYou have to be a mod to use !permit commands.\r\n" % pre_msg
			irc.send(send_str)	
		
		
		if in_front(unpermit_str, msg):
			if is_mod(user, channel_parsed):
				msg_arr = msg.split(" ")
				if len(msg_arr) == 2:
					permit_user = msg_arr[1]
					for permit_pair in self.permit_arr:
						if permit_pair[1] == permit_user:
							send_str = "%s%s's spam permit has been removed.\r\n" % (pre_msg, permit_user)
							self.permit_arr.remove(permit_pair)
							break
				else:
					send_str = "%sUsage: \"!unpermit <user>\"\r\n" % pre_msg
			else:
				send_str = "%sYou have to be a mod to unpermit users.\r\n" % pre_msg
			irc.send(send_str)
			
		
		#if !permit or !unpermit were used then parse_msg is over
		if in_front(permit_str, msg) or in_front(unpermit_str, msg):
			return True
		else:
			return False

	def antispam_parse(self, user, msg, irc, pre_msg, channel_parsed):
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
				if user.rstrip() == nick or "Tmi.twitch.tv" in user.capitalize().rstrip() or is_streamer(user, channel_parsed):
					return False
				else:
					#if it's not tecsbot
					#if user does not have a permit then start the checks
					if self.repeat_antispam_on:
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
										timeout(user, irc, pre_msg, spam_timeout)
										return True
									break
							else:
								#pop the element out, since it no longer is within 30 seconds of the first message.
								msg_info_arr.remove(msg_data)
						msg_info_arr.insert(0, msg_data_arr)#add in the new message to the beginning of the list
						
					#emote spam
					if self.emote_antispam_on:
						msg_emote_count = 0
						for emote in self.emote_arr:
							if msg.count(emote) != 0:
								msg_emote_count += msg.count(emote)
								if emote == "KappaPride":
									msg_emote_count = msg_emote_count - 1
							if msg_emote_count >= emote_max:
								self.emote_warn_arr = warn(user, msg, pre_msg, channel_parsed, irc, self.emote_warn_arr, emote_warn_duration, emote_warn_cooldown, emote_timeout_msg, emote_timeout_duration)
								return True
					#caps spam
					if self.caps_antispam_on:
						if len(msg) >= caps_perc_min_msg_len:
							if caps_perc(msg) >= 60:
								self.caps_warn_arr = warn(user, msg, pre_msg, channel_parsed, irc, self.caps_warn_arr, caps_warn_duration, caps_warn_cooldown, caps_timeout_msg, caps_timeout_duration)
								return True
					#fake purges
					if self.fake_purge_antispam_on:
						if msg in fake_purge_arr:
							self.fake_purge_warn_arr = warn(user, msg, pre_msg, channel_parsed, irc, self.fake_purge_warn_arr, fake_purge_warn_duration, fake_purge_warn_cooldown, fake_purge_timeout_msg, fake_purge_timeout_duration)
							return True
					#!skincode
					if self.skincode_antispam_on:
						if in_front(skincode_msg, msg):
							self.skincode_warn_arr = warn(user, msg, pre_msg, channel_parsed, irc, self.skincode_warn_arr, skincode_warn_duration, skincode_warn_cooldown, skincode_timeout_msg, skincode_timeout_duration)
							return True
					#long messages
					#lmao it was timing itself out need to have a permanent permit for tecsbot
					if self.long_msg_antispam_on:
						if len(msg) > msg_length_max:
							self.long_msg_warn_arr = warn(user, msg, pre_msg, channel_parsed, irc, self.long_msg_warn_arr, long_msg_warn_duration, long_msg_warn_cooldown, long_msg_timeout_msg, long_msg_timeout_duration)
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
									self.zalgo_warn_arr = warn(user, msg, pre_msg, channel_parsed, irc, self.zalgo_warn_arr, zalgo_warn_duration, zalgo_warn_cooldown, zalgo_timeout_msg, zalgo_timeout_duration)
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
								self.symbol_warn_arr = warn(user, msg, pre_msg, channel_parsed, irc, self.symbol_warn_arr, symbol_warn_duration, symbol_warn_cooldown, symbol_timeout_msg, symbol_timeout_duration)
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
												self.link_whitelist_warn_arr = warn(user, msg, pre_msg, channel_parsed, irc, self.link_whitelist_warn_arr, link_whitelist_warn_duration, link_whitelist_warn_cooldown, link_whitelist_timeout_msg, link_whitelist_timeout_duration)
												return True
										else:#the link was a pardoned one, let them free
											break
									else:
										if link_whitelist == word:
											break
								else:
									#link isn't whitelisted, time out user 
									self.link_whitelist_warn_arr = warn(user, msg, pre_msg, channel_parsed, irc, self.link_whitelist_warn_arr, link_whitelist_warn_duration, link_whitelist_warn_cooldown, link_whitelist_timeout_msg, link_whitelist_timeout_duration)
									return True
							
					#these need to be different types
					msg_arr = msg.split(" ")
					#long word spam
					if self.long_word_antispam_on:
						for word in msg_arr:
							if len(word) > long_word_limit and '\n' not in word:
								self.long_word_warn_arr = warn(user, msg, pre_msg, channel_parsed, irc, self.long_word_warn_arr, long_word_warn_duration, long_word_warn_cooldown, long_word_timeout_msg, long_word_timeout_duration)
								return True
					#/me
					if self.me_antispam_on:
						if in_front(me_msg, msg):
							self.me_warn_arr = warn(user, msg, pre_msg, channel_parsed, irc, self.me_warn_arr, me_warn_duration, me_warn_cooldown, me_timeout_msg, me_timeout_duration)
							return True
					'''the complicated general antispam that moobot offers
					if len(msg) > min_spam_chars:
						#idk how to go about making this without killing speed of program		
						pass'''
					return False
		else:
			return False
			
	def banphrase_parse(self, user, msg, irc, pre_msg, channel_parsed):
		#banphrase
		banphrase_str = "!banphrase"
		banphrase_add_str = "!banphrase add"
		banphrase_del_str = "!banphrase delete"
		banphrase_rem_str = "!banphrase remove"
		banphrase_list_str = "!banphrase list"
		banphrase_clr_str = "!banphrase clear"
		
		if self.banphrase_on:
			msg_arr = msg.split(" ", 2)
			if in_front(banphrase_str, msg):
				if is_mod(user, channel_parsed): 
					if in_front(banphrase_add_str, msg):
						#if is_mod(user, channel_parsed):
						if len(msg_arr) > 2:#need to have this if statement more often
							banphrase = msg_arr[2]
							self.banphrase_arr.append(banphrase)
							send_str = "%s\"%s\" added to list of banphrases.\r\n" % (pre_msg, banphrase)
						else:
							send_str = "%sUsage: \"!banphrase add <banphrase>\"" % pre_msg
						#else:
							#send_str = "%sYou have to be a mod to add banphrases.\r\n" % pre_msg
						#irc.send(send_str)
				
					elif in_front(banphrase_del_str, msg) or in_front(banphrase_rem_str, msg):
						#if is_mod(user, channel_parsed):
						if len(msg_arr) > 2:
							banphrase = msg_arr[2]
							if is_num(banphrase):
								#we add on one to the actual index because users prefer to start with 1, rather than 0.
								banphrase = int(banphrase)
								if ((len(self.banphrase_arr)-1) >= banphrase-1):
									send_str = "%sBanphrase \"%s\" removed at index %s.\r\n" % (pre_msg, self.banphrase_arr[banphrase-1], banphrase)
									del self.banphrase_arr[banphrase-1]
								else:
									send_str = "%sInvalid index for banphrase removal.\r\n" % pre_msg
							else:
								if banphrase in self.banphrase_arr:
									self.banphrase_arr.remove(banphrase)
									send_str = "%sBanphrase \"%s\" removed.\r\n" % (pre_msg, banphrase)									
								else:
									send_str = "%sSpecified banphrase does not exist.\r\n" % pre_msg
						else:
							send_str = "%sUsage: \"!banphrase delete/remove <banphrase/index>\"\r\n" % pre_msg
						#else:
							#send_str = "%sYou have to be a mod to remove banphrases.\r\n" % pre_msg	
						#irc.send(send_str)
					elif banphrase_list_str == msg:
						if len(self.banphrase_arr) == 0:
							send_str = "%sNo active banphrases.\r\n" % pre_msg
						else:
							send_str = "%sActive banphrases: " % pre_msg
							for banphrase in range(len(self.banphrase_arr)):
								if (banphrase != len(self.banphrase_arr) -1):
									#every element but last one
									next_str = "(%s.) %s, " % (banphrase+1, self.banphrase_arr[banphrase])
								else:
									#last element in arr
									next_str = "(%s.) %s.\r\n" % (banphrase+1, self.banphrase_arr[banphrase])
								send_str = long_print(next_str, send_str, pre_msg, irc)
					elif banphrase_clr_str == msg:
						self.banphrase_arr = []
						send_str = "%sAll banphrases removed.\r\n" % pre_msg
					elif banphrase_str == msg:
						send_str = "%sAdd or remove banphrases to timeout users who say them. Syntax and more information can be found in the documentation.\r\n" % pre_msg
					irc.send(send_str)
				else:
					send_str = "%sYou have to be a mod to use !banphrase commands.\r\n" % pre_msg
					irc.send(send_str)
			else:
				return False
		else:
			return False
	
	def test_parse(self, user, msg, irc, pre_msg, channel_parsed):
		#test
		test_str = "!test"
		test_reply = "Test successful."
		
		if msg == "!test":
			send_str = "%s%s\r\n" % (pre_msg, test_reply)
			irc.send(send_str)
		else:
			return False
			
	def autoreply_parse(self, user, msg, irc, pre_msg, channel_parsed):
		#autoreplies 
		
		autoreply_str = "!autoreply"
		autoreply_add_str = "!autoreply add"
		autoreply_del_str = "!autoreply delete"
		autoreply_rem_str = "!autoreply remove"
		autoreply_list_str = "!autoreply list"
		autoreply_clr_str = "!autoreply clear"
		
		if self.autoreply_on:
			if in_front(autoreply_str, msg):
				if is_mod(user, channel_parsed):
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
											send_str = "%s%s is already an autoreply phrase.\r\n" % (pre_msg, ar_pair[0])
											break
									else:
										ar_pair = [ar_phrase, ar_reply]
										self.ar_arr.append(ar_pair)
										#[phrase[reply],phrase[reply]]hopefully
										send_str = "%sPhrase \"%s\" added, with reply \"%s\".\r\n" % (pre_msg, ar_phrase, ar_reply)
								else:
									#incorrectly formatted, display usage
									send_str = "%sUsage: \"!autoreply add <phrase>:<reply>\".\r\n" % pre_msg
							else:
								#incorrectly formatted, display usage
								send_str = "%sUsage: \"!autoreply add <phrase>:<reply>\".\r\n" % pre_msg
						else:
							#incorrectly formatted, display usage
							send_str = "%sUsage: \"!autoreply add <phrase>:<reply>\".\r\n" % pre_msg
					#delete autoreplies
					elif in_front(autoreply_del_str, msg) or in_front(autoreply_rem_str, msg):
						msg_arr = msg.split(" ", 2)
						if len(msg_arr) == 3:
							ar_phrase = msg_arr[2]
							if is_num(ar_phrase):
								if ((len(self.ar_arr)-1) >= int(ar_phrase)-1):
									send_str = "%sAutoreply %s:%s removed at index %s.\r\n" % (pre_msg, self.ar_arr[int(ar_phrase)-1][0], self.ar_arr[int(ar_phrase)-1][1], ar_phrase)
									#should be the same index as the pair, after all.
									del self.ar_arr[int(ar_phrase)-1]
								else:
									send_str = "%sInvalid index for autoreply removal.\r\n" % pre_msg	
							
							else:
								for ar_pair in self.ar_arr:
									if ar_phrase == ar_pair[0]:
										send_str = "%sAutoreply %s:%s removed.\r\n" % (pre_msg, ar_pair[0], ar_pair[1])	
										self.ar_arr.remove(ar_pair)
										break
								else:
									send_str = "%sSpecified autoreply does not exist.\r\n" % pre_msg
						else:
							#incorrectly formatted, display usage
							send_str = "%sUsage: \"!autoreply delete/remove <phrase/index>\".\r\n" % pre_msg
					#list autoreplies
					elif autoreply_list_str == msg:
						#check to make sure there are autoreplies to list
						if len(self.ar_arr) == 0:
							send_str = "%sNo active autoreplies.\r\n" % pre_msg
						else:
							send_str = "%sActive autoreplies: " % pre_msg
							for ar_pair in range(len(self.ar_arr)):
								ar_phrase = self.ar_arr[ar_pair][0]
								ar_reply = self.ar_arr[ar_pair][1]
								if (ar_pair != len(self.ar_arr)-1):
									#every element but last one
									next_str = "(%s.) %s: %s, " % (ar_pair+1, ar_phrase, ar_reply)
								else:
									#last element in arr
									next_str = "(%s.) %s: %s.\r\n" % (ar_pair+1, ar_phrase, ar_reply)
								send_str = long_print(next_str, send_str, pre_msg, irc)	
					#clear autoreplies
					elif autoreply_clr_str == msg:
						self.ar_arr = []
						send_str = "%sAll autoreplies removed.\r\n" % pre_msg
					#just autoreply string, display usage
					elif autoreply_str == msg:
						send_str = "%sAdd or remove phrases that trigger automatic replies. Syntax and more information can be found in the documentation.\r\n" % pre_msg
					else:
						send_str = "%sUsage: !autoreply add/delete/remove/list/clear\r\n" % pre_msg
				else:
					send_str = "%sYou have to be a mod to use !autoreply commands.\r\n" % pre_msg
				irc.send(send_str)
			else:			
				if self.autoreply_on:
					for ar_pair in self.ar_arr:
						if ar_pair[0] == msg:
							send_str = "%s%s\r\n" % (pre_msg, ar_pair[1])
							irc.send(send_str)
							return False
				return False
		else:
			return False
	
	def set_parse(self, user, msg, irc, pre_msg, channel_parsed):
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
			if is_mod(user, channel_parsed):
				msg_arr = msg.split(" ")
				if len(msg_arr) == 3:
					
					#turn roulette on or off
					if in_front(set_roulette_str, msg):
						self.rol_on = set_value(self.rol_on, "roulette", msg_arr, pre_msg, irc)
						
					#turn 8ball on or off
					elif in_front(set_ball_str, msg):
						self.ball_on - set_value(self.ball_on, "8ball", msg_arr, pre_msg, irc)
						
					#banphrases
					elif in_front(set_banphrase_str, msg):
						self.banphrase_on = set_value(self.banphrase_on, "banphrase", msg_arr, pre_msg, irc)
					
					#autoreplies
					elif in_front(set_autoreply_str, msg):
						self.autoreply_on = set_value(self.autoreply_on, "autoreply", msg_arr, pre_msg, irc)
						
					#antispam
					elif in_front(set_antispam_str, msg):
						self.antispam_on = set_value(self.antispam_on, "antispam", msg_arr, pre_msg, irc)
						
					#repeat
					elif in_front(set_repeat_str, msg):
						self.repeat_on = set_value(self.repeat_on, "repeat", msg_arr, pre_msg, irc)
				
				elif len(msg_arr) == 4:
					#repeat antispam
					if in_front(set_repeat_antispam_str, msg):
						self.repeat_antispam_on = set_value(self.repeat_antispam_on, "repeat antispam", msg_arr, pre_msg, irc)
						
					#emote antispam
					elif in_front(set_emote_antispam_str, msg):
						self.emote_antispam_on = set_value(self.emote_antispam_on, "emote antispam", msg_arr, pre_msg, irc)
						
					#caps antispam
					elif in_front(set_caps_antispam_str, msg):
						self.caps_antispam_on = set_value(self.caps_antispam_on, "caps antispam", msg_arr, pre_msg, irc)
					
					#skincode antispam
					elif in_front(set_skincode_antispam_str, msg):
						self.skincode_antispam_on = set_value(self.skincode_antispam_on, "skincode antispam", msg_arr, pre_msg, irc)
					
					#zalgo antispam
					elif in_front(set_zalgo_antispam_str, msg):
						self.zalgo_antispam_on = set_value(self.zalgo_antispam_on, "zalgo antispam", msg_arr, pre_msg, irc)
					
					#symbol antispam
					elif in_front(set_symbol_antispam_str, msg):
						self.symbol_antispam_on = set_value(self.symbol_antispam_on, "symbol antispam", msg_arr, pre_msg, irc)
					
					#link antispam
					elif in_front(set_link_antispam_str, msg):
						self.link_antispam_on = set_value(self.link_antispam_on, "link antispam", msg_arr, pre_msg, irc)
					
					#me antispam
					elif in_front(set_me_antispam_str, msg):
						self.me_antispam_on = set_value(self.me_antispam_on, "me antispam", msg_arr, pre_msg, irc)
						
					#ban emotes
					elif in_front(set_ban_emotes_str, msg):
						self.ban_emotes_on = set_value(self.ban_emotes_on, "ban emotes", msg_arr, pre_msg, irc)
					
					#emote stats
					elif in_front(set_emote_stats_str, msg):
						self.emote_stats_on = set_value(self.emote_stats_on, "emote stats", msg_arr, pre_msg, irc)
						
				elif len(msg_arr) == 5:
					#fake purge antispam
					if in_front(set_fake_purge_antispam_str, msg):
						self.fake_purge_antispam_on = set_value(self.fake_purge_antispam_on, "fake purge antispam", msg_arr, pre_msg, irc)
					
					#long message antispam
					elif in_front(set_long_msg_antispam_str, msg):
						self.long_msg_antispam_on = set_value(self.long_msg_antispam_on, "long message antispam", msg_arr, pre_msg, irc)
					
					#long word antispam
					elif in_front(set_long_word_antispam_str, msg):
						self.long_word_antispam_on = set_value(self.long_word_antispam_on, "long word antispam", msg_arr, pre_msg, irc)
				else:
					#usage
					send_str = "%sUsage: \"!set <feature> on/off \".\r\n" % pre_msg
					irc.send(send_str)
				#just set_str, explain usage.
				if set_str == msg:
					send_str = "%sTurn features on or off. Usage: \"!set <feature> on/off \".\r\n" % pre_msg
					irc.send(send_str)
			else:
				#not mod
				send_str = "%sYou have to be a mod to use !set commands.\r\n" % pre_msg
				irc.send(send_str)
		else:
			return False
	
	def vote_parse(self, user, msg, irc, pre_msg, channel_parsed, vote_option_arr, vote_dict, vote_users, vote_total):
		#voting
		######################################################################################
		#non mods votes not being input
		#just needed %% to fix the problem, good luck future self I hope the SAT went well
		#-we'll see when we get the SAT scores wont we
		vote_str = "!vote"
		vote_start_str = "!vote start"
		vote_reset_str = "!vote reset"
		vote_results_str = "!vote results"
		vote_end_str = "!vote end"
		vote_close_str = "!vote close"
		
		msg_arr = msg.split(" ", 2)
		#save us from going into the loop if the vote is off and the command is not !vote start, done by a mod
		if in_front(vote_str, msg) and is_mod(user, channel_parsed) and self.vote_on == False:
			if in_front(vote_start_str, msg):
				pass
			else:
				send_str = "%sThere are no ongoing votes.\r\n" % pre_msg
				irc.send(send_str)
				return
			
		
		if in_front(vote_str, msg):
			if len(msg_arr) >= 2:
				if in_front(vote_start_str, msg):
					if len(msg_arr) >= 3:
						if is_mod(user, channel_parsed):
							#reset vote stuffs
							vote_dict = {}
							vote_users = []
							if self.vote_on:#if already ongoing poll
								send_str = "%sThere is already an ongoing poll.\r\n" % pre_msg
							else:
								self.vote_on = True
								send_str = "%sPoll opened! To vote use " % pre_msg
								vote_option_arr = msg_arr[2].split(",")
								for vote_option in range(len(vote_option_arr)): 
									vote_option_arr[vote_option] = vote_option_arr[vote_option].rstrip().lstrip()
									vote_dict[vote_option_arr[vote_option]] = [0]
									if vote_option != len(vote_option_arr) -1:
										send_str += "\"!vote %s\"/" % vote_option_arr[vote_option]
									else:
										send_str += "\"!vote %s\"\r\n" % vote_option_arr[vote_option]
								irc.send(send_str)		
								return [vote_option_arr, vote_dict, [], 0]
						else:
							send_str = "%sYou have to be a mod to start a poll.\r\n" % pre_msg
							irc.send(send_str)
					else:
						send_str = "%sUsage: !vote start <option1, option2, ...>\r\n" % pre_msg
				elif in_front(vote_reset_str, msg):
					if is_mod(user, channel_parsed):
						value_dict = sorted(vote_dict.items(), key=operator.itemgetter(1))
						for pair in value_dict:
							pair[1][0] = 0
						send_str = "%sVotes reset.\r\n" % pre_msg
						irc.send(send_str)
						return [vote_option_arr, vote_dict, [], 0]
					else:
						send_str = "%sYou have to be a mod to reset the poll votes.\r\n" % pre_msg
						irc.send(send_str)		
				elif in_front(vote_results_str, msg):
					if self.vote_on:
						if is_mod(user, channel_parsed):
							value_dict = sorted(vote_dict.items(), key=operator.itemgetter(1))
							if vote_total != 0:
								send_str = "%sCurrent Poll Stats: " % pre_msg
								for pair in reversed(value_dict):
									key = pair[0]
									value = pair[1][0]
									vote_perc = round((float(value) / vote_total) * 100, 2)
									if vote_perc.is_integer():
										vote_perc = int(vote_perc)
									send_str += "%s: %s%% " % (key, vote_perc)
								send_str += "Total votes: %s\r\n" % vote_total
								#display current results
							else:
								#prevent divide by 0 error.
								send_str = "%sNo votes to display.\r\n" % pre_msg
						else:
							send_str = "%sYou have to be a mod to display the current poll results.\r\n" %pre_msg
					else:
						send_str = "%sThere are no ongoing votes.\r\n" % pre_msg
					irc.send(send_str)
				elif in_front(vote_end_str, msg) or in_front(vote_close_str, msg):
					#close the vote
					if self.vote_on:
						if is_mod(user, channel_parsed):
							self.vote_on = False
							send_str = "%sPoll Results: " % pre_msg
							value_dict = sorted(vote_dict.items(), key=operator.itemgetter(1))
							if vote_total != 0:
								poll_winner = [['', 0]]
								for pair in value_dict:
									key = pair[0]
									value = pair[1][0]
									option_perc = (float(poll_winner[0][1])/vote_total * 100)
									if option_perc.is_integer():
										option_perc = int(option_perc)
									if value == poll_winner[0][1]:
										poll_winner.append([key, value])
									elif value > poll_winner[0][1]:
										poll_winner = [[key, value]]
									send_str += "%s: %s%% " % (key, option_perc)
								send_str += "Total votes: %s\r\n" % vote_total
								irc.send(send_str)
								winner_perc = round(float(poll_winner[0][1])/vote_total * 100, 2)
								if winner_perc.is_integer():
									winner_perc = int(winner_perc)
								if len(poll_winner) == 1:
									#1 winner
									if poll_winner[0][1] == 1:
										send_str = "%sPoll winner: %s with %s%% majority and %s total vote.\r\n" % (pre_msg, poll_winner[0][0], winner_perc, poll_winner[0][1])
									else:
										send_str = "%sPoll winner: %s with %s%% majority and %s total votes.\r\n" % (pre_msg, poll_winner[0][0], winner_perc, poll_winner[0][1])
								elif len(poll_winner) >= 2:
									send_str = "%sPoll is a draw between: " % pre_msg
									for vote_option in range(len(poll_winner)):
										if vote_option < len(poll_winner)-1:
											send_str += "%s, " % (poll_winner[vote_option][0])
										else:
											#last option in the arr
											if poll_winner[0][1] == 1:
												send_str += " and %s. They each had %s%% of the total vote and %s vote.\r\n" % (poll_winner[vote_option][0], winner_perc, poll_winner[0][1])
											else:	
												send_str += " and %s. They each had %s%% of the total vote and %s votes.\r\n" % (poll_winner[vote_option][0], winner_perc, poll_winner[0][1])
								else:
									send_str = "%sNo vote winner, this shouldn't happen. Contact me if it does. value_dict: %s, poll_winners: %s\r\n" % (pre_msg, value_dict, poll_winner)
									
							else:
								send_str = "%sNo votes to display.\r\n" % pre_msg
							irc.send(send_str)
						else:
							send_str = "%sYou have to be a mod to end a poll.\r\n" % pre_msg
							irc.send(send_str)
					else:
						send_str = "%sThere are no ongoing votes.\r\n" % pre_msg
				elif msg_arr[1].strip() in vote_option_arr and user not in vote_users:
					#msg_arr[1] is a vote option
					#input vote if user hasnt already voted
					vote_dict[msg_arr[1]][0] += 1
					vote_users.append(user)
					vote_total+=1
					return [vote_option_arr, vote_dict, vote_users, vote_total]
				else:
					if is_mod(user, channel_parsed):
						send_str = "%sUsage: !vote start/results/reset/end/close\r\n" % pre_msg
					else:
						for vote_option in range(len(vote_option_arr)): 
							send_str = "%sUsage: " % pre_msg
							if vote_option != len(vote_option_arr) -1:
								send_str += "\"!vote %s\"/" % vote_option_arr[vote_option]
							else:
								send_str += "\"!vote %s\"\r\n" % vote_option_arr[vote_option]
			else:
				if is_mod(user, channel_parsed):
					send_str = "%sUsage: !vote start/reset/results/end/close\r\n" % pre_msg
				else:
					send_str = "%sUsage: " % pre_msg
					for vote_option in range(len(vote_option_arr)): 
						if vote_option != len(vote_option_arr) -1:
							send_str += "\"!vote %s\"/" % vote_option_arr[vote_option]
						else:
							send_str += "\"!vote %s\"\r\n" % vote_option_arr[vote_option]
				irc.send(send_str)
		elif vote_str == msg:
			send_str = "%To vote use " % pre_msg
			for vote_option in range(len(vote_option_arr)): 
				if vote_option != len(vote_option_arr) -1:
					send_str += "\"!vote %s\"/" % vote_option_arr[vote_option]
				else:
					send_str += "\"!vote %s\"\r\n" % vote_option_arr[vote_option]
			irc.send(send_str)	
		else:
			return False
	
	def raffle_parse(self, user, msg, irc, pre_msg, channel_parsed):
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
					if is_mod(user, channel_parsed):
						send_str = "%sThere is already an ongoing raffle.\r\n" % pre_msg
					else:
						send_str = "%sOnly mods can start raffles.\r\n" % pre_msg
					irc.send(send_str)
					
				elif end_raffle_str == msg:
					if is_mod(user, channel_parsed):
						if len(self.raffle_users) > 0:
							winner = self.raffle_users[random.randint(0, (len(self.raffle_users) - 1))]
							#need to have prize of some sorts?
							send_str = "%s%s has won the raffle!\r\n" % (pre_msg, winner)
						else:
							send_str = "%sNo one joined the raffle, there is no winner.\r\n" % pre_msg
						self.raffle_on = False
						self.raffle_users = []
						
					else:
						send_str = "%sOnly mods can end raffles.\r\n" % pre_msg
					irc.send(send_str)
			else:
				if start_raffle_str == msg:
					if is_mod(user, channel_parsed):
						self.raffle_on = True
						send_str = "%sRaffle started. Join the raffle with \"!raffle\".\r\n" % (pre_msg)
					else:
						send_str = "%sOnly mods can start raffles.\r\n" % pre_msg
					irc.send(send_str)
				elif raffle_str == msg and is_mod(user, channel_parsed):
					send_str = "%sUsage: !raffle start/end\r\n" % pre_msg
					irc.send(send_str)
				elif end_raffle_str == msg:
					if is_mod(user, channel_parsed):
						send_str = "%sNo ongoing raffles.\r\n" % pre_msg
					else:
						send_str = "%sOnly mods can end raffles.\r\n" % pre_msg
					irc.send(send_str)	
					
		else:
			return False
	
	def roulette_parse(self, user, msg, irc, pre_msg, channel_parsed):
		#roulette
		#if user is mod then say it doesnt kill you or something
		#should absolutely just make the chance input in the GUI rather than text based.
		rol_str = "!roulette"
		rol_chance_str = "!roulette chance"
		
		if self.rol_on:
			if in_front(rol_str, msg):
				if rol_str == msg:
					#trigger roulette - allow custom messages for win/loss to replace default ones
					send_str = "%s/me places the revolver to %s's head\r\n" % (pre_msg, user)
					irc.send(send_str)
					time.sleep(1)
					if random.random() < self.rol_chance:
						#time out the user(ban from chat) for rol_timeout amount of seconds
						if is_mod(user, channel_parsed) == False:
							timeout(user, irc, pre_msg, self.rol_timeout)
							send_str = "%sThe trigger is pulled, and the revolver fires! %s lies dead in chat\r\n" % (pre_msg, user)
						else:
							send_str = "%sThe gun jams thanks to your super mod powers. %s lives!\r\n" % (pre_msg, user)
					else:
						#do nothing, notify of victory
						send_str = "%sThe trigger is pulled, and the revolver clicks. %s has lived to survive roulette!\r\n" % (pre_msg, user)
					irc.send(send_str)
				elif in_front(rol_chance_str, msg):
					if is_mod(user, channel_parsed):
						#get the new chance for ban in roulette
						msg_arr = msg.split(" ")
						if len(msg_arr) > 2:
							#percentage is input as chance, *.01 to change to decimal
							input_perc = msg_arr[2]
							if is_num(input_perc) == True:
								input_perc = float(input_perc)
								input_perc = check_int(input_perc)
							if input_perc > 100 or input_perc < 0 or is_num(input_perc) == False:
								send_str = "%sPlease input a percentage chance for roulette to be triggered, i.e. \"!roulette chance 50\". Chance must be between 0 and 100.\r\n" % pre_msg
							else:
								self.rol_chance = input_perc * .01
								input_perc = check_int(input_perc)
								send_str = "%sRoulette chance successfully changed to %s%%\r\n" % (pre_msg, input_perc)
						else:
							send_str = "%sUsage: !roulette chance <percent chance>\r\n" % pre_msg
					else:
						send_str = "%sOnly mods can change the chance of the roulette.\r\n" % pre_msg
					irc.send(send_str)
				else:
					if is_mod(user, channel_parsed):
						send_str = "%sUsage: !roulette chance <percent chance>\r\n" % pre_msg
						irc.send(send_str)
			else:
				return False
	
	def ball_parse(self, user, msg, irc, pre_msg, channel_parsed):#????
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
				if is_mod(user, channel_parsed):
					msg_arr = msg.split(" ", 2)
					if in_front(ball_add_str, msg):
						#if is_mod(user, channel_parsed):
						if len(msg_arr) > 2:#need to have this if statement more often
							ball_response = msg_arr[2]
							if ball_response not in self.ball_arr:
								self.ball_arr.append(ball_response)
								send_str = "%s\"%s\" added to list of 8ball responses.\r\n" % (pre_msg, ball_response)
							else:
								send_str = "%s%s is already an 8ball response.\r\n" % (pre_msg, ball_response)
						else:
							send_str = "%sUsage: \"!8ball add <8ball response>\r\n" % pre_msg
						irc.send(send_str)
						return
					elif in_front(ball_del_str, msg) or in_front(ball_rem_str, msg):
						if len(msg_arr) > 2:
							ball_response = msg_arr[2]
							if is_num(ball_response):
								#we add on one to the actual index because users prefer to start with 1, rather than 0.
								ball_response = int(ball_response)
								if ((len(self.ball_arr)-1) >= ball_response-1):
									send_str = "%s8Ball response \"%s\" removed at index %s.\r\n" % (pre_msg, self.ball_arr[ball_response-1], ball_response)
									del self.ball_arr[ball_response-1]
								else:
									send_str = "%sInvalid index for 8ball response removal.\r\n" % pre_msg
							else:
								if ball_response in self.ball_arr:
									self.ball_arr.remove(ball_response)
									send_str = "%s8Ball response \"%s\" removed.\r\n" % (pre_msg, ball_response)									
								else:
									send_str = "%sSpecified 8ball response does not exist.\r\n" % pre_msg
						else:
							send_str = "%sUsage: \"!8ball delete/remove <8ball response/index>\"\r\n" % pre_msg	
						irc.send(send_str)
						return
					elif in_front(ball_list_str, msg):
						if len(self.ball_arr) > 0:
							send_str = "%sCurrent 8ball responses: " % pre_msg
							for ball_response in range(len(self.ball_arr)):
								if (ball_response != len(self.ball_arr) -1):
									#if not last response in arr
									next_str = "(%s.) %s, " % (ball_response+1, self.ball_arr[ball_response])
								else:
									next_str = "(%s.) %s.\r\n" % (ball_response+1, self.ball_arr[ball_response])
								#this accounts for any messages longer than the character cap
								send_str = long_print(next_str, send_str, pre_msg, irc)
							irc.send(send_str)
						else:
							send_str = "%sThere are currently no 8ball responses.\r\n" % pre_msg
							irc.send(send_str)
						return
					elif ball_clr_str == msg:
						if len(self.ball_arr) > 0:
							self.ball_arr = []
							send_str = "%sAll 8ball responses removed.\r\n" % pre_msg
						else:	
							send_str = "%sThere are currently no 8ball responses.\r\n" % pre_msg
						irc.send(send_str)
						return
					elif ball_str == msg and is_mod(user, channel_parsed):
						send_str = "%sUsage: !8ball add/delete/remove/list/clear/<question>\r\n" % pre_msg
						irc.send(send_str)
						return

				if in_front(ball_str, msg) and "?" in msg: #and msg.rstrip().endswith("?") <-- is this better?
					msg_arr = msg.split(" ", 1)
					if len(msg_arr) == 2:
						if len(self.ball_arr) > 0:
							ball_response_index = random.randint(0, len(self.ball_arr)-1)
							ball_response = self.ball_arr[ball_response_index]
							send_str = "%sMagic 8 ball says... %s\r\n" % (pre_msg, ball_response)
						else:
							send_str = "%sThere are currently no 8ball responses.\r\n" % pre_msg
					elif ball_str == msg:
						send_str = "%sGet the Magic 8 Ball to answer your question. Usage: \"!8ball <question> \".\r\n" % pre_msg
					else:
						send_str = "%sUsage: \"!8ball <question> \".\r\n" % pre_msg
					irc.send(send_str)
		else:
			return False
	
	def uptime_parse(self, user, msg, irc, pre_msg, channel_parsed):
		#uptime
		uptime_str = "!uptime"
		
		if uptime_str == msg:
			send_str = "%s@%s has been live for: %s\r\n" % (pre_msg, channel_parsed, get_uptime_str(pre_msg, channel_parsed))
			irc.send(send_str)
		else:
			return False
	
	def chatters_parse(self, user, msg, irc, pre_msg, channel_parsed):
		chatters_str = "!chatters"
		#chatters
		if chatters_str == msg:
			chatter_data = get_json_chatters(channel_parsed)
			chatter_count = int(chatter_data["chatter_count"]) - 1 #don't count ourselves
			send_str = "%sThere are currently %s accounts in chat.\r\n" % (pre_msg, chatter_count)
			irc.send(send_str)
		else:
			return False
			
	def viewers_parse(self, user, msg, irc, pre_msg, channel_parsed):
		#viewers
		viewers_str = "!viewers"
		if viewers_str == msg:
			viewer_data = get_json_stream(channel_parsed)
			viewer_count = viewer_data["streams"][0]["viewers"]
			send_str = "%sThere are currently %s viewers in the channel.\r\n" % (pre_msg, viewer_count)
			irc.send(send_str)
		else:
			return False
			
	def subs_parse(self, user, msg, irc, pre_msg, channel_parsed):
		#subscribers
		subscribers_str = "!subscribers"
		subs_str = "!subs"	
		if subs_str == msg or subscribers_str == msg:
			sub_data = get_json_subs(channel_parsed)
		else:
			return False
			
	def commercial_parse(self, user, msg, irc, pre_msg, channel_parsed):
		#commercials
		comm_str = "!commercial"
		if comm_str == msg:
			if is_streamer(user, channel_parsed):
				msg_arr = msg.split(" ")
				if len(msg_arr) == 1:
					#start default length commercial
					comm_len = 30
					start_commercial(comm_len, channel_parsed)
					send_str = "%s%s commercial started.\r\n" % (pre_msg, parse_sec(comm_len))
				elif len(msg_arr) == 2:
					comm_len = msg_arr[1]
					if is_num(comm_len):
						if comm_len in comm_len_arr:
							start_commercial(comm_len, channel_parsed)
							send_str = "%s%s commercial started.\r\n" % (pre_msg, parse_sec(comm_len))
					else:
						#display usage
						send_str = "%sUsage: !commercial <length of commercial>\r\n"
				else:
					#display usage
					send_str = "%sUsage: !commercial <length of commercial>\r\n"
			else:
				#not mod
				send_str = "%sYou have to be the current streamer in order to start commercials.\r\n" % pre_msg
			irc.send(send_str)
		else:
			return False
	
	def ban_emote_parse(self, user, msg, irc, pre_msg, channel_parsed):
		#banphrase
		banphrase_str = "!banphrase"
		banphrase_add_str = "!banphrase add"
		banphrase_del_str = "!banphrase delete"
		banphrase_rem_str = "!banphrase remove"
		banphrase_list_str = "!banphrase list"
		banphrase_clr_str = "!banphrase clear"
		
		if self.banphrase_on:
			msg_arr = msg.split(" ", 2)
			if in_front(banphrase_str, msg):
				if is_mod(user, channel_parsed): 
					if in_front(banphrase_add_str, msg):
						#if is_mod(user, channel_parsed):
						if len(msg_arr) > 2:#need to have this if statement more often
							banphrase = msg_arr[2]
							self.banphrase_arr.append(banphrase)
							send_str = "%s\"%s\" added to list of banphrases.\r\n" % (pre_msg, banphrase)
						else:
							send_str = "%sUsage: \"!banphrase add <banphrase>\"" % pre_msg
						#else:
							#send_str = "%sYou have to be a mod to add banphrases.\r\n" % pre_msg
						#irc.send(send_str)
				
					elif in_front(banphrase_del_str, msg) or in_front(banphrase_rem_str, msg):
						#if is_mod(user, channel_parsed):
						if len(msg_arr) > 2:
							banphrase = msg_arr[2]
							if is_num(banphrase):
								#we add on one to the actual index because users prefer to start with 1, rather than 0.
								banphrase = int(banphrase)
								if ((len(self.banphrase_arr)-1) >= banphrase-1):
									send_str = "%sBanphrase \"%s\" removed at index %s.\r\n" % (pre_msg, self.banphrase_arr[banphrase-1], banphrase)
									del self.banphrase_arr[banphrase-1]
								else:
									send_str = "%sInvalid index for banphrase removal.\r\n" % pre_msg
							else:
								if banphrase in self.banphrase_arr:
									self.banphrase_arr.remove(banphrase)
									send_str = "%sBanphrase \"%s\" removed.\r\n" % (pre_msg, banphrase)									
								else:
									send_str = "%sSpecified banphrase does not exist.\r\n" % pre_msg
						else:
							send_str = "%sUsage: \"!banphrase delete/remove <banphrase/index>\"\r\n" % pre_msg
						#else:
							#send_str = "%sYou have to be a mod to remove banphrases.\r\n" % pre_msg	
						#irc.send(send_str)
					elif banphrase_list_str == msg:
						if len(self.banphrase_arr) == 0:
							send_str = "%sNo active banphrases.\r\n" % pre_msg
						else:
							send_str = "%sActive banphrases: " % pre_msg
							for banphrase in range(len(self.banphrase_arr)):
								if (banphrase != len(self.banphrase_arr) -1):
									#every element but last one
									next_str = "(%s.) %s, " % (banphrase+1, self.banphrase_arr[banphrase])
								else:
									#last element in arr
									next_str = "(%s.) %s.\r\n" % (banphrase+1, self.banphrase_arr[banphrase])
								send_str = long_print(next_str, send_str, pre_msg, irc)
					elif banphrase_clr_str == msg:
						self.banphrase_arr = []
						send_str = "%sAll banphrases removed.\r\n" % pre_msg
					elif banphrase_str == msg:
						send_str = "%sAdd or remove banphrases to timeout users who say them. Syntax and more information can be found in the documentation.\r\n" % pre_msg
					irc.send(send_str)
				else:
					send_str = "%sYou have to be a mod to use !banphrase commands.\r\n" % pre_msg
					irc.send(send_str)
			else:
				return False
		else:
			return False
		'''ban_emote_str = "!ban emote"
		unban_emote_str = "!unban emote"
		#ban emotes
		if self.ban_emote_on:
			if in_front(ban_emote_str, msg):
				if is_mod(user, channel_parsed):
					msg_arr = msg.split(" ")
					if msg_arr == 3:
						ban_emote = msg_arr[2]
						self.ban_emote_arr.append(ban_emote)
						send_str = "%sEmote \"%s\" banned.\r\n" % (pre_msg, ban_emote)
					else:
						send_str = "%sUsage: \"!ban emote <emote>\"\r\n" % pre_msg
				else:
					send_str = "%sOnly mods can ban emotes.\r\n" % pre_msg
				irc.send(send_str)
				return
			if in_front(unban_emote_str, msg):
				if is_mod(user, channel_parsed):
					msg_arr = msg.split(" ")
					if msg_arr == 3:
						ban_emote = msg_arr[2]
						self.ban_emote_arr.remove(ban_emote)
						send_str = "%sEmote \"%s\" unbanned.\r\n" % (pre_msg, ban_emote)
					else:
						send_str = "%sUsage: \"!unban emote <emote>\"\r\n" % pre_msg
				else:
					send_str = "%sOnly mods can unban emotes.\r\n" % pre_msg
				irc.send(send_str)
				return'''
	#def repeat_parse(self, user, msg, irc, pre_msg, channel_parsed):'''
	
	
	def main(self):
		
		pre_msg = "PRIVMSG %s :" % self.channel
		#filepaths
		emote_file_path = "C:\\Users\\DarkElement\\Desktop\\Programming\\Challenges\\twitch_bot\\emotes.txt"
		log_file_path = "C:\\Users\\DarkElement\\Desktop\\Programming\\Challenges\\twitch_bot\\logs\\%s.log" % self.channel

		bot_owner = 'darkelement75'
		nick = 'tecsbot' 
		ping_nick = "@%s" % nick
		#for now making this whatever I input0
		#self.channel = sys.argv[1]
		channel_parsed = self.channel.replace("#", "")
		server = 'irc.twitch.tv'
		password = 'oauth:'
		
		irc = socket.socket()
		irc.connect((server, 6667)) #connects to the server
		#sends variables for connection to twitch chat
		irc.send("CAP REQ :twitch.tv/tags\r\n")
		irc.send('PASS ' + password + "\r\n")
		irc.send('USER ' + nick + ' 0 * :' + bot_owner + "\r\n")
		irc.send('NICK ' + nick + "\r\n")
		irc.send('JOIN ' + self.channel + "\r\n")
		
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
		
		emotes_file = open(emote_file_path, 'r')
		log_file = open(log_file_path, 'r')	
		
		#should delete dictionary of values when/if stream goes offline.
		self.count_dict = {}
		self.count_dict = create_dict(self.count_dict, emote_file_path)
		#update_dict()
		#print_dict_by_value(count_dict)
		
		#start with empty array of followers
		self.follower_arr = []
		#add current viewers to viewer_arr so we dont welcome everyone
		self.viewer_arr = create_viewer_arr()
		self.raffle_users = []
		
		#self.vote_on = False
		self.link_whitelist_arr = []
		self.permit_arr = []
		self.banphrase_arr = []
		self.ar_arr = []
		self.ban_emote_arr = []
		self.cmd_dict = {}
		self.emote_arr = []
		
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
		
		if self.emote_arr == []:
			self.emote_arr = create_emote_arr(emote_file_path)
		'''if self.permit_arr == []:
			current_time = time.time()
			permit_pair = [current_time, nick, 420, "time"]
			self.permit_arr.append(permit_pair)
			permit_nick = "Tmi.twitch.tv 001 %s" % nick
			permit_pair = [current_time, permit_nick, 322, "time"]#number irrelevant
			self.permit_arr.append(permit_pair)'''
		
		#old regex = ur'\S+\.\w{2,6}\b(?!\.)'
		self.link_regex = re.compile(ur'\S+[^\d]\.\w{2,6}\b(?!\.)', re.MULTILINE)
		#if this one fails, try this one, i'm pretty sure it's actually better 
		#(?![\d\.]\b)(\S+\.[^\d]{2,6})\b
		
		def parse_msg(user, msg, irc):
			comm_len_arr = [30, 60, 90, 120, 150, 180]
			
			
			#need to make this off, until mod turns it on with a command
			#then it turns off again after elapsed voting time or mod ends raffle time with !winner or something so that a winner can be chosen
			#none of these declarations should be in here
			
			
			repeat_str = "!repeat"
			repeat_add_str = "!repeat add"
			repeat_del_str = "!repeat delete"
			repeat_rem_str = "!repeat remove"
			repeat_list_str = "!repeat list"
			repeat_clr_str = "!repeat clear"
			
			ban_emote_warn_duration = 1
			ban_emote_warn_cooldown = 30
			ban_emote_timeout_msg = "banned emotes"
			ban_emote_timeout_duration = 1
			
			banphrase_warn_duration = 1
			banphrase_warn_cooldown = 30
			banphrase_timeout_msg = "banned phrases"
			banphrase_timeout_duration = 1
			
			
			
			
			
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
					if permit_pair[1] != nick:
						#don't remove tecsbot
						if ((current_time - user_time) >= permit_time):
							self.permit_arr.remove(permit_pair)#should be fine since only one permit can be added at a time
				#do nothing if permanent permit
					
							
			#holy shit wish i thought of this earlier
			#only for debugging and development, will immediately stop execution of program
			#also because i am fucking tired of goldmine ads
			if 'goldmine' in msg or 'BTC' in msg or 'bitcoin' in msg or "rektmine" in msg:
				send_str = "%s/ban %s\r\n" % (pre_msg, user)
				irc.send(send_str)
			if "ert" == msg and (user == "darkelement75" or user == "dark_element_slave1"):
				full_exit()
			#link whitelists
			#has to be before anti spam so that adding/removing a link will not trigger and time out the user doing so
			if self.link_whitelist_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
			
			if self.spam_permit_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
			
			if self.antispam_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
			
			if self.banphrase_parse(user, msg, irc, pre_msg, channel_parsed) == False:
				#if the message had nothing to do with banphrases
				if self.banphrase_on:
					for banphrase in self.banphrase_arr:
						if banphrase in msg:
							self.banphrase_warn_arr = warn(user, msg, pre_msg, channel_parsed, irc, self.banphrase_warn_arr, banphrase_warn_duration, banphrase_warn_cooldown, banphrase_timeout_msg, banphrase_timeout_duration)
							break
			else:
				return
				
			
			#test command if bot is in chat
			if self.test_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
				
			if self.autoreply_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
			
			if self.set_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
			
			vote_return = self.vote_parse(user, msg, irc, pre_msg, channel_parsed, self.vote_option_arr, self.vote_dict, self.vote_users, self.vote_total)
			if vote_return != False:
				if isinstance(vote_return, list):
					self.vote_option_arr = vote_return[0]
					self.vote_dict = vote_return[1]
					self.vote_users = vote_return[2]
					self.vote_total = vote_return[3]
				else:
					return
			
			if self.raffle_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
				
			if self.roulette_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
				
			if self.ball_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
			
			if self.uptime_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
				
			if self.chatters_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
				
			if self.viewers_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
			
			if self.subs_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
				
			if self.commercial_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
				
			if self.ban_emote_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return
				
			'''if self.autoreply_parse(user, msg, irc, pre_msg, channel_parsed) != False:
				return'''
			
			
			#welcome newcomers - seems to be working with viewers and followers atm - need to figure out subs however
			#NOTE: TEMPORARILY DISABLED BECAUSE IT IS ANNOYING AS FUCK WHEN NOT PERMANENTLY ONLINE
			#new viewers
				#need to auth for sub list
			'''if user not in viewer_arr:
				#add to viewer_arr and then welcome them
				viewer_arr.append(user)
				send_str = "%sHello newcomer %s, welcome to %s's self.channel!\r\n" % (pre_msg, user, channel_parsed)
				irc.send(send_str)'''
			#new followers
			self.follower_arr = new_follower(self.follower_arr, channel_parsed, pre_msg)
			
			
					
			
			
			#repeat commands
			#can easily be mod commands by just inputting /ban, /timeout, etc
			#need to put all commands in an array so that we can do !random command 
			#!repeat add <command> interval
			#concatenate all commands after [1] and before [len(arr)-1]
			
			if self.repeat_on:
				if in_front(repeat_str, msg):
					if is_mod(user, channel_parsed):
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
								current_time = time.time()
								repeat_set = [current_time, repeat_cmd, repeat_interval]
								self.repeat_arr.append(repeat_set)	
								send_str = "%sRepeat command \"%s\" added with interval %s.\r\n" % (pre_msg, repeat_cmd, parse_sec(repeat_interval))
							else:
								send_str = "%sUsage: !repeat add <command> <interval>\r\n" % pre_msg
						elif in_front(repeat_del_str, msg) or in_front(repeat_rem_str, msg):
							msg_arr = msg.split(" ", 2)
							if len(msg_arr) > 2:
								repeat_cmd = msg_arr[2]
								if is_num(repeat_cmd):
									if ((len(self.repeat_arr)-1) >= int(repeat_cmd)-1):
										send_str = "%sRepeat command \"%s\" with interval %s removed at index %s.\r\n" % (pre_msg, self.repeat_arr[int(repeat_cmd)-1][1], parse_sec(self.repeat_arr[int(repeat_cmd)-1][2]), repeat_cmd)
										
										#should be the same index as the pair, after all.
										del self.repeat_arr[int(repeat_cmd)-1]
									else:
										send_str = "%sInvalid index for repeat command removal.\r\n" % pre_msg		
								else:
									for repeat_set in self.repeat_arr:
										if repeat_cmd == repeat_set[1]:
											send_str = "%sRepeat command \"%s\" with interval %s removed.\r\n" % (pre_msg, repeat_cmd, parse_sec(repeat_set[2]))		
											self.repeat_arr.remove(repeat_set)
											break
									else:
										send_str = "%sSpecified repeat command does not exist.\r\n" % pre_msg	
							else:
								send_str = "%sUsage: !repeat delete/remove <command/index>\r\n" % pre_msg
						elif repeat_list_str == msg:
							if len(self.repeat_arr) == 0:
								send_str = "%sNo active repeat commands.\r\n" % pre_msg
							else:
								send_str = "%sActive repeat commands: " % pre_msg
								for repeat_set in range(len(self.repeat_arr)):
									repeat_cmd = self.repeat_arr[repeat_set][1]
									repeat_interval = self.repeat_arr[repeat_set][2]
									if (repeat_set != len(self.repeat_arr)-1):
										#every element but last one
										next_str = "(%s.) %s: %s, " % (repeat_set+1, repeat_cmd, parse_sec(repeat_interval))
									else:
										#last element in arr
										next_str = "(%s.) %s: %s.\r\n" % (repeat_set+1, repeat_cmd, parse_sec(repeat_interval))
									send_str = long_print(next_str, send_str, pre_msg, irc)
						elif repeat_clr_str == msg:
							self.repeat_arr = []
							send_str = "%sAll repeat commands removed.\r\n" % pre_msg
						elif repeat_str == msg:
							send_str = "%sAdd or remove commands to be repeated every specified interval. Syntax and more information can be found in the documentation.\r\n" % pre_msg
						else:
							send_str = "%sUsage: !repeat <add/delete/remove/list/clear> <command> <interval>\r\n" % pre_msg
					else:
						#not moderino
						send_str = "%sYou have to be a mod to use !repeat commands.\r\n" % pre_msg
					irc.send(send_str)
					return
					
					
			#custom commands - these are the exact same as autoreplies. Do we need them regardless?
			'''cmd_str = "!command"
			add_cmd_str = "!command add"
			del_cmd_str = "!command delete"
			rem_cmd_str = "!command remove"
			#do we need to add confirm dialogues here?
			if add_cmd_str in msg:
				msg_arr = msg.split(" ", 2)
				
				cmd = msg_arr[1]
				response = msg_arr[2] 
				
				#send_str = "%sAre you sure you want to add '%s' with response '%s'?\r\n" % (pre_msg, cmd, response)
				#irc.send(send_str)
				self.cmd_dict[cmd] = []
				self.cmd_dict[cmd].append(0)
				self.cmd_dict[cmd][0] = response
				
				send_str = "%sCommand \"%s\" successfully added, with response \"%s\".\r\n" % (pre_msg, cmd, response)
				irc.send(send_str)
				
			if del_cmd_str in msg:
				msg_arr = msg.split(" ", 1)
				cmd = msg_arr[1]
				if cmd in self.cmd_dict:
					#send_str = "%sAre you sure you want to remove '%s' with response '%s'?" % (pre_msg, cmd, self.cmd_dict[cmd][0])	
					#irc.send(send_str)
					#changed this to remove because pop = uncessary
					self.cmd_dict.remove(cmd)
					send_str = "%sCommand '%s' successfully removed.\r\n" % (pre_msg, cmd)
					irc.send(send_str)
				else:
					send_str = "%sCommand '%s' not found. Perhaps you misspelled it?\r\n" % (pre_msg, cmd)
					irc.send(send_str)
				
			
			for cmd in self.cmd_dict:
				if cmd == msg:
					send_str = "%s%s\r\n" % (pre_msg, self.cmd_dict[cmd][0])
					irc.send(send_str)'''
			if self.ban_emote_on:
				for ban_emote in self.ban_emote_arr:
					if ban_emote in msg:
						self.ban_emote_warn_arr = warn(user, msg, pre_msg, channel_parsed, irc, self.ban_emote_warn_arr, ban_emote_warn_duration, ban_emote_warn_cooldown, ban_emote_timeout_msg, ban_emote_timeout_duration)
						break


			#this is probably what's taking so long, changing this to be a one time addon to an array with a function 
			#emote related commands - need to handle custom emotes
			if self.emote_stats_on:
				for emote in self.emote_arr:
					if emote in msg:
						#update dictionary with emote
						emote_count = msg.count(emote)
						self.count_dict[emote][0] += emote_count
						stats_str = "!stats %s" % emote
						if stats_str == msg:
							emote_per_min = find_per_min(emote, channel_parsed)
							send_str = "%sTotal times %s has been sent: %s. %s per minute: %s.\r\n" % (pre_msg, emote, self.count_dict[emote][0], emote, emote_per_min)
							irc.send(send_str)			
				
		
		while True:
			online_check_interval = 30
			#beginning of main execution loop
			#will continuously check if stream is online, if it isnt then it will break from inner loop 
			#and wait in outer loop.
			if stream_online(channel_parsed):	
				
				self.repeat_arr = []
				check_current_time = time.time()
				while True:
					
					irc.setblocking(0)
					socket_ready = select.select([irc], [], [], 0)
					if socket_ready[0]:
						data = irc.recv(1204) #gets output from IRC server
						
						if data:
							if data.find("PING") != -1:
								str = "PONG :tmi.twitch.tv\r\n".encode
								irc.send("PONG :tmi.twitch.tv\r\n".encode("utf-8")) #responds to PINGS from the server
								print "Ponging..."
							if in_front(":tmi.twitch.tv CAP * ACK", data):
								pass#for now
							else:
								data_arr = data.split(":", 2)
								test_arr = data.split(";", 6)
								print test_arr
								other_arr = test_arr[6].split(":", 2)
								user_type = other_arr[0]
								print user_type
								print other_arr[1]
								print other_arr[2]
								print data_arr
								if len(data_arr) == 3:
									print data
									print test_arr
									user = (data_arr[1].split("!"))[0]
									msg = data_arr[2]
									msg = msg.rstrip()
									#for even printing
									if len(user) < 7:
										print "%s:\t\t\t%s" % (user, msg)
									elif len(user) < 16:
										print "%s:\t\t%s" % (user, msg)
									else:
										print "%s:\t%s" % (user, msg)
									'''
									#this is already in channel settings
									#offensive word timeouts
									for blacklist in blacklist_arr:
										if blacklist in msg:	
											#time out the user(ban from chat) for blacklist_timeout amount of seconds
											timeout(user, irc, timeout)
									'''
									#more debugging stuff
									#start = time.time()
									parse_msg(user, msg, irc)
									#end = time.time() 
									#print end-start
						else:
							print "Reconnecting..."
							irc.close()
							time.sleep(3)
							connect_channel(self.channel)
					else:#if there is no data on the socket(irc)
						#checking for repeats
						if self.repeat_on:
							current_time = time.time()
							for repeat_set in self.repeat_arr:
								repeat_time = repeat_set[0]
								repeat_cmd = repeat_set[1] 
								repeat_interval = float(repeat_set[2]) 
								repeat_variance = .15
								repeat_interval = repeat_interval - repeat_variance
								#this will help for the small numbers in making that gap less forward, if possible.
								#using a percentage would quickly cause large inaccuracies in larger intervals, and only using a percentage for small ones would be so small that it did not matter. There is no perfect solution to this.
								#this way at least numbers that would result in being more late, i.e. .95 -> 1.3 are shortened considerably, while not affecting larger numbers
								#################
								if (current_time - repeat_time >= repeat_interval):
									repeat_set[0] = current_time#update the time
									
									send_str = "%s%s\r\n" % (pre_msg, repeat_cmd)#needs to send this to the previous part of the program
									#debugging stuff
									#send_str = "%s%s : %s\r\n" % (pre_msg, current_time - repeat_time, repeat_interval)
									irc.send(send_str)
									parse_msg(nick, repeat_cmd, irc)
						current_time = time.time()
						if current_time - check_current_time >= online_check_interval:
							check_current_time = time.time()
							if stream_online(channel_parsed) == False:
								break#should break us out of the current inner while loop
		
#main whisper bot where other threads with processes will be started
#sets variables for connection to twitch chat



#start channel bot thread
whisper_msg = ""
whisper_user = ""

try:
	thread.start_new_thread(channel_bot_start("#darkelement75").main, ())
except Exception as errtxt:
	print errtxt
	
while True:
	data = irc.recv(1204) #gets output from IRC server
	if data != [] and data != '':
		if data.find("PING") != -1:
			str = "PONG :tmi.twitch.tv\r\n".encode
			irc.send("PONG :tmi.twitch.tv\r\n".encode("utf-8")) #responds to PINGS from the server
			#print "Ponging..."
		data_arr = data.split(":", 2)
		if len(data_arr) == 3:
			user = (data_arr[1].split("!"))[0]
			msg = data_arr[2]
			msg = msg.rstrip()
			#for even printing
			if len(user) < 7:
				print "%s:\t\t\t%s" % (user, msg)
			elif len(user) < 16:
				print "%s:\t\t%s" % (user, msg)
			else:
				print "%s:\t%s" % (user, msg)
				
				
		#when any of the threads change both values whisper the message and reset the values
		if whisper_msg != "" and whisper_user != "":
			whisper(whisper_user, whisper_msg, pre_msg_group)
			whisper_msg = ""
			whisper_user = ""
				
				
	else:
		irc.close()
		time.sleep(3)
		connect_group()