#TODO:
"""
more channel functionality
create own commands functionality
	needs to be very user-friendly
	currently !addcom and !delcom
	need to add in ability to do <user>, reference user who wrote message.
needs to be running on home comp at all times
multi channel processing for comparison stats?
famous person has joined chat
timezone for streamer
donations <-if this isnt already done very well
hours til next strim?
score of current game/tourney/bo3/etc
voting, songs, game, etc
voting
	mod starts with !vote option1 option2 option3 or more
	others can !vote option1 to vote for it
	after certain time/mod does !vote end, results displayed.
welcome newcomers
	custom message
	need to auth before getting subs
need to make it possible to enable/disable everything -checkboxes
sub notifications
raffle - need expiration timer? - threading?
commercials? 
commands for mods to change game or title or other(commercials?)
social media info
repeat info, like social media info
spam control <- r9k will count it as spam if multiple people say same thing, need to only worry about one person
allow users to program question responses like ALICE? <-- interesting idea for a solo channel
currently playing song
overall and per day -time user has watched stream
	other user tracking stuff
overrall and per day -messages of user, high score, etc
need help for each command
	!help <command>
	putting it all in documentation instead of this will likely be better.
	<command> will output this
!roulette
	have time of timout as 3 text fields: hours, minutes, seconds.
		Also have option for permanent ban.
	also allow chance to be input as 1 out of <textfield> ie 6, then just divide 1/<textfield>6 to get the chance.
gui/input boxes in twitch integration could simply assign values to dictionary here, although it may end up being more complicated. <--waiting for stack overflow
how to keep permanently on, desktop is best current option, other than some form of cloud hosting/streamer hosting<-- see stackoverflow response
still cant track emotes it's not seeing, can't see them if it's not online. Permanent online is necessary for accurate emote stats.<-- ^
allow customization of (almost?) any response to a command. Should allow default customisation but give a warning. Need reset to default as well.
can we highlight ourmessages too? 
dont disable bot, only change some responses when offline stream
remember to only allow some commands to work if user is mod/owner
	different responses for mods/owners
implement more if x != "" b/c this will fuck up everything if not present
"remove/delete" more
warnings for dangerous commands? <- nah, better to put it once in documentation then to remind them every time they use it
log/dict/array of recent commands? <-doubt this would actually help with an undo command
different levels of authority?
tecsbot moderator group?
when put online it will greet the first(?) viewer and followr on the list
is our spam prevention really necessary/doing anything in it's current state?
more advanced !test results
different responses input for 8ball?
8ball -> have to have question mark in the question argument?
autoreplies -> if phrase in string?
better spam prevention options/modes/commands
better way to parse unicode - is this good now
checkbox to enable/disable errors in chat, such as usage/have to be mod
checkbox for whispers for warning messages ie excessive use of caps warning/etc
test spam prevention
test voting
test permit improvements <-lmao
	need to improve spam filters first 
test sets for autoreplies & banphrases
warnings for timeouts
excludes for "regulars" and subs
"""
import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import sys, operator, time, urllib, json, math, os, random, unicodedata
from datetime import datetime, timedelta

#sets variables for connection to twitch chat
bot_owner = 'darkelement75'
nick = 'tecsbot' 
ping_nick = "@%s" % nick
#for now making this whatever I input
channel = '#darkelement75'
#channel = sys.argv[1]
channel_parsed = channel.replace("#", "")
server = 'irc.twitch.tv'
password = ''

queue = 13 #sets variable for anti-spam queue functionality

#filepaths
emote_file_path = "C:\\Users\\DarkElement\\Desktop\\Programming\\Challenges\\twitch_bot\\emotes.txt"
log_file_path = "C:\\Users\\DarkElement\\Desktop\\Programming\\Challenges\\twitch_bot\\logs\\%s.log" % channel

#for added commands
cmd_dict = {}

#for emotes array
emote_arr = []
#misc
pre_msg = "PRIVMSG %s :" % channel

#things to be input as settings
rol_chance = .5
rol_timeout= 60 #seconds
spam_cooldown = 30 #seconds
spam_timeout = 10 #seconds
emote_max = 2 #low for testing, max number of emotes allowed in a message before timing user out
#need to have different timeout durations for different types, also allow one universal timeout however.
emote_timeout_msg = "You have been timed out for sending a message that had %s caps or more." % emote_max

#need to have 10 second warning for both of these
caps_perc_min_msg_len = 8
caps_perc_max = 60
#caps_num_max = 50

#min_symbol_num = 3
max_symbol_num = 8
min_symbol_perc = 15
max_symbol_perc = 40

msg_length_max = 375

caps_timeout_msg = "You have been timed out for sending a message that had %s caps or more." % caps_perc_max
#caps_timeout_msg = "You have been timed out for sending a message that was %s% caps or more." % caps_num_max

permit_time = 30 #seconds
banphrase_timeout = 10 #seconds

'''
#this is already in channel settings
blacklist_timeout = 10 #seconds
blacklist_arr = ["belgium"]
'''
#This determines whether to do search_str == msg, or search_str in message when looking for commands
cmd_match_full = True

#initial connect
irc = socket.socket()
irc.connect((server, 6667)) #connects to the server
#sends variables for connection to twitch chat
irc.send('PASS ' + password + "\r\n")
irc.send('USER ' + nick + ' 0 * :' + bot_owner + "\r\n")
irc.send('NICK ' + nick + "\r\n")
irc.send('JOIN ' + channel + "\r\n")


	
def connect():
	irc = socket.socket()
	irc.connect((server, 6667)) #connects to the server
	#sends variables for connection to twitch chat
	irc.send('PASS ' + password + "\r\n")
	irc.send('USER ' + nick + ' 0 * :' + bot_owner + "\r\n")
	irc.send('NICK ' + nick + "\r\n")
	irc.send('JOIN ' + channel + "\r\n")

def start_log():
	#if log file already exists, delete it and create new one.
	#need to execute this when the stream starts, should wait for get_uptime_min to be less than 1?
	if os.path.exists(log_file_path):
		os.remove(log_file_path)
	new_log_file = open(log_file_path, 'w')
	new_log_file.close	
	
def create_dict(dict):
	#create dictionary of emotes and set all counts to 0
	#for some reason nothing will read any more emotes out of this file after this loop goes through each line, once.
	emotes_file = open(emote_file_path, 'r')
	log_file = open(log_file_path, 'r')
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

def find_per_min(emote):
	emote_count = count_dict[emote][0]
	#this number is from the start of the program to the current time of the query, 
	#giving the amount of minutes from the start of the program.
	min = get_uptime_min()
	emote_per_min = emote_count / min
	return emote_per_min

def get_json_stream():
	url = "https://api.twitch.tv/kraken/streams/%s" % channel_parsed
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return data
	
def get_json_chatters():
	url = "https://tmi.twitch.tv/group/user/%s/chatters" % channel_parsed
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return data
	
def stream_online():
	#need to use this return value to trigger the loop of everything.
	channel_json = get_json_stream()
	stream_status = channel_json["stream"]
	if stream_status == None:
		stream_status = False
	else:
		stream_status = True
	return stream_status
	
def get_uptime_min():
	channel_json = get_json_stream()
	#parse out unnecessary stuffs
	start_time = channel_json["stream"]["created_at"].replace("Z", "").replace("T", "-")
	#convert to datetime object
	start_time = time.strptime(start_time, "%Y-%m-%d-%H:%M:%S")
	#convert to unix time so we can calculate amount of hours and seconds it's been up, and other calculations.
	uptime = time.mktime(start_time) - 4*3600
	#subtract 4 hours from the (now unix)time, making it equal in time zones to ours,
	#then take current time and created time and get the difference.
	uptime = time.time() - uptime
	min = uptime / 60
	#return the minutes for epm calculations
	return min

def get_uptime_str():
	channel_json = get_json_stream()
	#parse out unnecessary stuffs
	start_time = channel_json["stream"]["created_at"].replace("Z", "").replace("T", "-")
	#convert to datetime object
	start_time = time.strptime(start_time, "%Y-%m-%d-%H:%M:%S")
	#convert to unix time so we can calculate amount of hours and seconds it's been up, and other calculations.
	uptime = time.mktime(start_time) - 4*3600
	#subtract 4 hours from the (now unix)time, making it equal in time zones to ours,
	#then take current time and created time and get the difference.
	uptime = time.time() - uptime
	hour = int(math.floor(uptime/3600))
	min = int(math.floor((uptime - hour *3600) / 60))
	sec = int(math.floor((uptime - hour *3600 - min*60)))
	if hour == 0 and min == 0:
		send_str = "%s@%s has been live for: %ss\r\n" % (pre_msg, channel_parsed, sec)
	elif hour == 0:
		send_str = "%s@%s has been live for: %sm %ss\r\n" % (pre_msg, channel_parsed, min, sec)
	else:
		send_str = "%s@%s has been live for: %sh %sm %ss\r\n" % (pre_msg, channel_parsed, hour, min, sec)	
	#return the string for sending
	return send_str

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
	hour = int(math.floor(sec/3600))
	min = int(math.floor((sec - hour *3600) / 60))
	sec = int(math.floor((sec - hour *3600 - min*60)))
	return_str = ""
	
	get_time_return_str(hour, "hour")
	get_time_return_str(min, "second")
	get_time_return_str(sec, "minute")
	if return_str.endswith(", "):
		return_str = return_str[:-2]
	return return_str
	
def is_mod(user):
	channel_json = get_json_chatters()
	mods_arr = channel_json["chatters"]["moderators"]
	if user == channel_parsed:
		#if the user is the streamer
		#can possibly add in new function to replace this and add for more different responses if triggered by streamer, is_owner
		#or just return a different value
		return True
	for mod in mods_arr:
		if user == mod.encode("ascii"):#sure they'll be something wrong with this
			return True
	return False

def create_viewer_arr():
	channel_json = get_json_chatters()
	viewer_arr = []
	for viewer in channel_json["chatters"]["viewers"]:
		viewer_arr.append(str(viewer))
	return viewer_arr
	
def get_json_follows():
	url = "https://api.twitch.tv/kraken/channels/%s/follows/" % channel_parsed
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return data

def new_follower(follower_arr):
	follows_json = get_json_follows()
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

def timeout(user, irc, timeout):
	send_str = "%s/timeout %s %s\r\n" % (pre_msg, user, timeout)
	irc.send(send_str)

def whisper(user, msg, irc):
	send_str = "%s/w %s %s\r\n" % (pre_msg, user, msg)
	irc.send(send_str)
	
def is_num(x):
	try:
		float(x)
		return True
	except ValueError:
		return False
	
def set_value(set_on, set_feature, msg_arr, irc):
		if msg_arr[2] == "on":
			set_on = True
			send_str = "%s%s turned on. You can do \"!set %s off\" to turn it off again.\r\n" % (pre_msg, set_feature.capitalize(), set_feature)
		elif msg_arr[2] == "off":
			set_on = False
			send_str = "%s%s turned off. You can do \"!set %s on\" to turn it on again.\r\n" % (pre_msg, set_feature.capitalize(), set_feature)
		else:
			#usage
			send_str = "%sUsage: \"!set %s on/off \".\r\n" % (pre_msg, set_feature)
		irc.send(send_str)
		return set_on

def create_emote_arr():
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
	caps = ''
	for letter in msg:
		if letter.isupper():
			caps+=letter
	return len(caps) / len(msg)
	
def warn(user, msg, irc, warn_arr, warn_duration, warn_cooldown, timeout_msg, timeout_duration):
	#function to warn if they havent already been warned, and time them out if they have.
	for warn_pair in warn_arr:
		if user == warn_pair[1]:
			#check if current time is longer than the warning duration from the last time name was entered
			current_time = time.time()
			if (current_time - warn_pair[0] <= warn_cooldown):
				#timeout user for long duration and remove from array
				timeout(user, irc, timeout_duration)
				warn_arr.remove(warn_pair)
				send_str = "No %s allowed (%s)" % (timeout_msg, user.capitalize())
				irc.send(send_str)
				whisper_msg = "You were timed out for %s in %s (%s)" % (timeout_msg, channel_parsed, parse_sec(timeout_duration))
				whisper(user, whisper_msg, irc)
				break
			else:
				#replace old entry with new one and send warning as well as timeout for warn_duration
				timeout(user, irc, warn_duration)
				warn_arr.remove(warn_pair)
				pair = [current_time, user]
				warn_arr.append(pair)
				send_str = "No %s allowed (%s)(warning)" % (timeout_msg, user.capitalize())
				whisper_msg = "You were timed out for %s in %s (%s, warning)" % (timeout_msg, channel_parsed, parse_sec(timeout_duration))
				whisper(user, whisper_msg, irc)
				irc.send(send_str)
				break
	else:	
		#add new entry and send warning, with timeout for warn_duration
		timeout(user, irc, warn_duration)
		current_time = time.time()
		pair = [current_time, user]
		warn_arr.append(pair)
		send_str = "No %s allowed (%s)(warning)" % (timeout_msg, user.capitalize())
		whisper_msg = "You were timed out for %s in %s (%s, warning)" % (timeout_msg, channel_parsed, parse_sec(timeout_duration))
		whisper(user, whisper_msg, irc)
		irc.send(send_str)
	return warn_arr
		
def symbol_count(msg):
	reg_chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0',',','.',' ','\'','\"']
	msg_symbol_count = 0
	for char in msg:
		if char not in msg:
			msg_symbol_count += 1
	return msg_symbol_count		
	
while True:
	#beginning of main execution loop
	#will continuously check if stream is online, if it isnt then it will break from inner loop 
	#and wait in outer loop.
	if stream_online() == True:	
		
		start_log()
		emotes_file = open(emote_file_path, 'r')
		log_file = open(log_file_path, 'r')	

		#should delete dictionary of values when/if stream goes offline.
		count_dict = {}
		count_dict = create_dict(count_dict)
		#update_dict()
		#print_dict_by_value(count_dict)
		
		#add current viewers to viewer_arr so we dont welcome everyone
		create_viewer_arr()
		#start with empty array of followers
		follower_arr = []
		viewer_arr = create_viewer_arr()
		raffle_users = []
		raffle_on = False
		msg_info_arr = []
		vote_on = False
		permit_arr = []
		banphrase_arr = []
		ar_arr = []
		rol_on = True
		ball_on = True
		banphrase_on = True
		autoreply_on = True
		
		caps_warn_arr = []
		emotes_warn_arr = []
		fake_purge_warn_arr = []
		long_msg_warn_arr = []
		
		if emote_arr == []:
			emote_arr = create_emote_arr()
		while stream_online() == True:
			#need to make this off, until mod turns it on with a command
			#then it turns off again after elapsed voting time or mod ends raffle time with !winner or something so that a winner can be chosen
			uptime_str = "!uptime"
			start_raffle_str = "!raffle start"
			join_raffle_str = "!raffle"
			end_raffle_str = "!raffle end"
			vote_str = "!vote"
			
			permit_str = "!permit"
			permit_del_str = "!permit delete"
			permit_rem_str = "!permit remove"
			permit_list_str = "!permit list"
			permit_clr_str = "!permit clear"
			
			banphrase_str = "!banphrase"
			banphrase_add_str = "!banphrase add"
			banphrase_del_str = "!banphrase delete"
			banphrase_rem_str = "!banphrase remove"
			banphrase_list_str = "!banphrase list"
			banphrase_clr_str = "!banphrase clear"
			
			test_str = "!test"
			test_reply = "Test successful."
			
			autoreply_str = "!autoreply"
			autoreply_add_str = "!autoreply add"
			autoreply_del_str = "!autoreply delete"
			autoreply_rem_str = "!autoreply remove"
			autoreply_list_str = "!autoreply list"
			autoreply_clr_str = "!autoreply clear"
			
			set_str = "!set"
			set_roulette_str = "!set roulette"
			set_ball_str = "!set 8ball"
			set_banphrase_str = "!set banphrase"
			set_autoreply_str = "!set autoreply"
			
			rol_cmd_str = "!roulette"
			rol_chance_str = "!roulette chance"
			
			#timeout_msg = "No <timeout_msg> allowed"
			caps_warn_duration = 10
			caps_warn_cooldown = 30
			caps_timeout_msg = "excessive use of caps"
			caps_timeout_duration = 600
			
			emote_warn_duration = 10
			emote_warn_cooldown = 30
			emote_timeout_msg = "excessive use of emotes"
			emote_timeout_duration = 600
			
			fake_purge_warn_duration = 10
			fake_purge_warn_cooldown = 30
			fake_purge_timeout_msg = "fake purges"
			fake_purge_timeout_duration = 600
			
			long_msg_warn_duration = 10
			long_msg_warn_cooldown = 30
			long_msg_timeout_msg = "excessively long messages"
			long_msg_timeout_duration = 600
			
			zalgo_warn_duration = 10
			zalgo_warn_cooldown = 30
			zalgo_timeout_msg = "zalgo symbols"
			zalgo_timeout_duration = 600
			
			ball_str = "!8ball"
			ball_list_str = "!8ball list"
			#move this up a level when we allow editing of these values
			#also maybe disable the list command? since they would likely be edting these values in a gui online.
			ball_arr = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Reply hazy try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again", "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]
			
			chatters_str = "!chatters"
			viewers_str = "!viewers"
			data = irc.recv(1204) #gets output from IRC server
			if data != [] and data != '':
				if data.find("PING") != -1:
					str = "PONG :tmi.twitch.tv\r\n".encode
					irc.send("PONG :tmi.twitch.tv\r\n".encode("utf-8")) #responds to PINGS from the server

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
					'''
					#this is already in channel settings
					#offensive word timeouts
					for blacklist in blacklist_arr:
						if blacklist in msg:	
							#time out the user(ban from chat) for blacklist_timeout amount of seconds
							timeout(user, irc, timeout)
					'''
					#spam permits
					if permit_str in msg:
						if is_mod(user):
							msg_arr = msg.split(" ")
							if len(msg_arr) == 2:
								permit_user = msg_arr[1]
								current_time = time.time()
								permit_pair = [current_time, permit_user]
								permit_arr.append(permit_pair)
								'''permit_dict[current_time] = []
								permit_dict[current_time].append(0)
								permit_dict[current_time][0] = permit_user'''
								#[[<current unix time> : <user who is permitted>],[],...]
								send_str = "%s%s's spam filter has been lifted for %s seconds\r\n" % (pre_msg, permit_user, permit_time)
							
								#possible future functionality
								'''#manual delete/remove
								elif permit_del_str in msg or permit_rem_str in msg:
									if len(msg_arr) == 3:
										permit_user = msg_arr[2]
										if is_num(permit_user):
											if ((len(permit_arr)-1) >= int(permit_user)-1):
												send_str = "%sPermit %s removed at index %s.\r\n" % (pre_msg, permit_arr[int(permit_user)][1], permit_user)
												#should be the same index as the pair, after all.
												del permit_arr[int(permit_user)]
											else:
												send_str = "%sInvalid index for permit removal.\r\n" % pre_msg										
										else:
											for permit_pair in permit_arr:
												if permit_user == permit_pair[1]:
													permit_arr.remove(permit_pair)
													send_str = "%sPermit \"%s\" removed.\r\n" % (pre_msg, permit_user)		
													break
											else:
												send_str = "%sSpecified permit does not exist.\r\n" % pre_msg
									else:
										#incorrectly formatted, display usage
										send_str = "%sUsage: \"!permit delete/remove <user/index>\".\r\n" % pre_msg
								#list
								elif permit_list_str == msg:
									if len(permit_arr) == 0:
										send_str = "%sNo users with active permits.\r\n" % pre_msg
									else:
										send_str = "%sUsers with active permits: " % pre_msg
										for permit_pair in range(len(permit_arr)):
											if (permit_pair != len(permit_arr) -1):
												#every element but last one
												send_str += "(%s.) %s, " % (permit_pair+1, permit_arr[permit_pair][1])
											else:
												#last element in arr
												send_str += "(%s.) %s.\r\n" % (permit_pair+1, permit_arr[permit_pair][1])
								#clear
								elif permit_clr_str == msg:
									permit_arr = []
									send_str = "%sAll permits removed.\r\n" % pre_msg'''
							#normal
							elif permit_str == msg:
								send_str = "%sUsage: \"!permit <user>\"\r\n" % pre_msg
							#idk
							else:
								send_str = "%sUsage: \"!permit <user>\"\r\n" % pre_msg
						else:
							send_str = "%sYou have to be a mod to permit users.\r\n" % pre_msg
						irc.send(send_str)	
					current_time = time.time()
					#remove from the permit_dict once they have been there more than the permit_time
					for permit_pair in permit_arr:
						user_time = permit_pair[0]
						if ((current_time - user_time) >= permit_time):
							#changed this to remove because pop = unnecessary
							permit_arr.remove(permit_pair)
							#we could just break here but I would feel guilty, lets hope it works for now, if it doesnt we can either:
								#a) break here, making there a short delay in de-permitting people if there are a lot of them
								#b) figure out a way to reloop, or something so that it continues going through the dictionary even though elements in it have been removed.
							
					#antispam
					#add time, user, and message to array of 30second old messages
					current_time = time.time() #unix time of message sent
					msg_data_arr = [current_time, user, msg]
					for msg_data in msg_info_arr:
						if msg_data_arr[0] - msg_data[0] < spam_cooldown: #only see messages that are within 30 seconds of newest messages
							if msg_data_arr[1] == msg_data[1] and msg_data_arr[2] == msg_data[2]: #if new message has the same user and same message as a previous message
								#if identical new message was sent within spam cooldown, then timeout user and stop looking through messages
								for user_time in permit_dict:
									if user_time[0] == user: 
										#if user is permitted to spam, don't time him out
										break
								else:
									timeout(user, irc, spam_timeout)
								break
						else:
							#pop the element out, since it no longer is within 30 seconds of the first message.
							msg_info_arr.remove(msg_data)
					msg_info_arr.insert(0, msg_data_arr)#add in the new message to the beginning of the list
					#emote spam timeouts
						#whisper they were timed out for emote spam
					msg_emote_count = 0
					
					#emote spam
					for emote in emote_arr:
						if msg.count(emote) != 0:
							msg_emote_count += msg.count(emote)
						if msg_emote_count >= emote_max:
							emote_warn_arr = warn(user, msg, irc, emote_warn_arr, emote_warn_duration, emote_warn_cooldown, emote_timeout_msg, caps_timeout_duration)
							break
					#caps spam
					if len(msg) >= caps_perc_min_msg_len:
						if caps_perc(msg) > 60:
							caps_warn_arr = warn(user, msg, irc, caps_warn_arr, caps_warn_duration, caps_warn_cooldown, caps_timeout_msg, caps_timeout_duration)
					#fake purges
					fake_purge_arr = ["<message deleted>"] # gonna need more of these
					if msg in fake_purge_arr:
						fake_purge_warn_arr = warn(user, msg, irc, fake_purge_warn_arr, fake_purge_warn_duration, fake_purge_warn_cooldown, fake_purge_timeout_msg, fake_purge_timeout_duration)
					#long messages
					if len(msg) > msg_length_max:
						long_msg_warn_arr = warn(user, msg, irc, long_msg_warn_arr, long_msg_warn_duration, long_msg_warn_cooldown, long_msg_timeout_msg, long_msg_timeout_duration)
					#zalgo symbols
					#Very likely this will take a lot of time, find more efficient method if so
					for char in msg:
						if isinstance(char, unicode):
							print char
							if unicodedata.combining(char) != 0:
								zalgo_warn_arr = warn(user, msg, irc, zalgo_warn_arr, zalgo_warn_duration, zalgo_warn_cooldown, zalgo_timeout_msg, zalgo_timeout_duration)
								break
					#block symbols
					
					#excessive symbols
					
					max_symbol_num = 8
					min_symbol_chars = 15
					max_symbol_perc = 40
					#if there are more than min_symbol_chars in message, check the percentage and amount
					if len(msg) > min_symbol_chars:
						symbol_count = symbol_count(msg)
						symbol_perc = symbol_count / len(msg)
						#if the limits are exceeded for num or percentage
						if symbol_count > max_symbol_num or symbol_perc > max_symbol_perc:
							#######################################
						
					
						
					#banphrase
					if banphrase_on:
						msg_arr = msg.split(" ")
						if banphrase_str in msg:
							if is_mod(user): 
								if banphrase_add_str in msg:
									#if is_mod(user):
									if len(msg_arr) > 2:#need to have this if statement more often
										banphrase = msg_arr[2]
										banphrase_arr.append(banphrase)
										send_str = "%s\"%s\" added to list of banphrases.\r\n" % (pre_msg, banphrase)
									else:
										send_str = "%sUsage: \"!banphrase add <banphrase>\"" % pre_msg
									#else:
										#send_str = "%sYou have to be a mod to add banphrases.\r\n" % pre_msg
									#irc.send(send_str)
							
								if banphrase_del_str in msg or banphrase_rem_str in msg:
									#if is_mod(user):
									if len(msg_arr) > 2:
										banphrase = msg_arr[2]
										if is_num(banphrase):
											#we add on one to the actual index because users prefer to start with 1, rather than 0.
											banphrase = int(banphrase)
											if ((len(banphrase_arr)-1) >= banphrase-1):
												send_str = "%sBanphrase %s removed at index %s.\r\n" % (pre_msg, banphrase_arr[banphrase-1], banphrase)
												del banphrase_arr[banphrase-1]
											else:
												send_str = "%sInvalid index for banphrase removal.\r\n" % pre_msg
										else:
											if banphrase in banphrase_arr:
												banphrase_arr.remove(banphrase)
												send_str = "%sBanphrase \"%s\" removed.\r\n" % (pre_msg, banphrase)									
											else:
												send_str = "%sSpecified banphrase does not exist.\r\n" % pre_msg
									else:
										send_str = "%sUsage: \"!banphrase delete/remove <banphrase/index>\"\r\n" % pre_msg
									#else:
										#send_str = "%sYou have to be a mod to remove banphrases.\r\n" % pre_msg	
									#irc.send(send_str)
								if banphrase_list_str == msg:
									if len(banphrase_arr) == 0:
										send_str = "%sNo active banphrases.\r\n" % pre_msg
									else:
										send_str = "%sActive banphrases: " % pre_msg
										for banphrase in range(len(banphrase_arr)):
											if (banphrase != len(banphrase_arr) -1):
												#every element but last one
												send_str += "(%s.) %s, " % (banphrase+1, banphrase_arr[banphrase])
											else:
												#last element in arr
												send_str += "(%s.) %s.\r\n" % (banphrase+1, banphrase_arr[banphrase])
								if banphrase_clr_str == msg:
									banphrase_arr = []
									send_str = "%sAll banphrases removed.\r\n" % pre_msg
								if banphrase_str == msg:
									send_str = "%sAdd or remove banphrases to timeout users who say them. Syntax and more information can be found in the documentation.\r\n" % pre_msg
								irc.send(send_str)
							else:
								send_str = "%sYou have to be a mod to use !banphrase commands.\r\n" % pre_msg
								irc.send(send_str)

					#test command if bot is in chat
					if msg == "!test":
						send_str = "%s%s\r\n" % (pre_msg, test_reply)
						irc.send(send_str)
					
					#autoreplies 
					if autoreply_on:
						if autoreply_str in msg:
							if is_mod(user):
								#add autoreplies
								if autoreply_add_str in msg:
									msg_arr = msg.split(" ", 2)
									if len(msg_arr) == 3:
										if ":" in msg_arr[2]:
											ar_msg_arr = msg_arr[2].split(":")
											if len(ar_msg_arr) == 2:
												ar_phrase = ar_msg_arr[0]
												ar_reply = ar_msg_arr[1]
												ar_pair = [ar_phrase, ar_reply]
												ar_arr.append(ar_pair)
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
								elif autoreply_del_str in msg or autoreply_rem_str in msg:
									msg_arr = msg.split(" ", 2)
									if len(msg_arr) == 3:
										ar_phrase = msg_arr[2]
										if is_num(ar_phrase):
											if ((len(ar_arr)-1) >= int(ar_phrase)-1):
												send_str = "%sAutoreply %s removed at index %s.\r\n" % (pre_msg, ar_arr[int(ar_phrase)], ar_phrase)
												#should be the same index as the pair, after all.
												del ar_arr[int(ar_phrase)]
											else:
												send_str = "%sInvalid index for autoreply removal.\r\n" % pre_msg										
										else:
											for ar_pair in ar_arr:
												if ar_phrase == ar_pair[0]:
													ar_arr.remove(ar_pair)
													send_str = "%sAutoreply \"%s\" removed.\r\n" % (pre_msg, ar_phrase)		
													break
											else:
												send_str = "%sSpecified autoreply does not exist.\r\n" % pre_msg
									else:
										#incorrectly formatted, display usage
										send_str = "%sUsage: \"!autoreply delete/remove <phrase/index>\".\r\n" % pre_msg
								#list autoreplies
								elif autoreply_list_str == msg:
									#check to make sure there are autoreplies to list
									if len(ar_arr) == 0:
										send_str = "%sNo active autoreplies.\r\n" % pre_msg
									else:
										send_str = "%sActive autoreplies: " % pre_msg
										for ar_pair in range(len(ar_arr)):
											ar_phrase = ar_arr[ar_pair][0]
											ar_reply = ar_arr[ar_pair][1]
											if (ar_pair != len(ar_arr)-1):
												#every element but last one
												send_str += "(%s.) %s: %s, " % (ar_pair+1, ar_phrase, ar_reply)
											else:
												#last element in arr
												send_str += "(%s.) %s: %s.\r\n" % (ar_pair+1, ar_phrase, ar_reply)
								
								#clear autoreplies
								elif autoreply_clr_str == msg:
									ar_arr = []
									send_str = "%sAll autoreplies removed.\r\n" % pre_msg
								#just autoreply string, display usage
								elif autoreply_str == msg:
									send_str = "%sAdd or remove phrases that trigger automatic replies. Syntax and more information can be found in the documentation.\r\n" % pre_msg
							else:
								send_str = "%sYou have to be a mod to use !autoreply commands.\r\n" % pre_msg
							irc.send(send_str)
					#sets
					if set_str in msg:
						if is_mod(user):
							msg_arr = msg.split(" ")
							if len(msg_arr) == 3:
								#turn roulette on or off
								if set_roulette_str in msg:
									rol_on = set_value(rol_on, "roulette", msg_arr, irc)
									
								#turn 8ball on or off
								if set_ball_str in msg:
									ball_on - set_value(ball_on, "8ball", msg_arr, irc)
									
								#banphrases
								if set_banphrase_str in msg:
									banphrase_on = set_value(banphrase_on, "banphrase", msg_arr, irc)
								
								#autoreplies
								if set_autoreply_str in msg:
									autoreply_on = set_value(autoreply_on, "autoreply", msg_arr, irc)
									
							else:
								#usage
									send_str = "%sUsage: \"!set <feature> on/off \".\r\n" % pre_msg
							#just set_str, explain usage.
							if set_str == msg:
								send_str = "%sTurn features on or off. Usage: \"!set <feature> on/off \".\r\n" % pre_msg
							irc.send(send_str)
						else:
							#not mod
							send_str = "%sYou have to be a mod to use !set commands.\r\n" % pre_msg
							irc.send(send_str)
					#welcome newcomers - seems to be working with viewers and followers atm - need to figure out subs however
					#new viewers
						#need to auth for sub list
					if user not in viewer_arr:
						#add to viewer_arr and then welcome them
						viewer_arr.append(user)
						send_str = "%sHello newcomer %s, welcome to %s's channel!\r\n" % (pre_msg, user, channel_parsed)
						irc.send(send_str)
					#new followers
					follower_arr = new_follower(follower_arr)
					
					#uptime
					if uptime_str == msg:
						irc.send(get_uptime_str())
					
					#voting
					msg_arr = msg.split(" ", 2)
					if len(msg_arr) >= 2:
						if msg_arr[0] == vote_str:
							if msg_arr[1] == "start" and len(msg_arr) >= 3:
								vote_dict = {}
								vote_users = []
								vote_on = True
								vote_total = 0
								send_str = "%sPoll opened! To vote use " % pre_msg
								vote_option_arr = msg_arr[2].split(",")
								for vote_option in range(len(vote_option_arr)): 
									vote_dict[vote_option_arr[vote_option]] = [0]
									if vote_option != len(vote_option_arr) -1:
										send_str += "\"!vote %s\"/" % vote_option_arr[vote_option]
									else:
										send_str += "\"!vote %s\"\r\n" % vote_option_arr[vote_option]
								irc.send(send_str)		
							elif msg_arr[1] == "reset":
								vote_dict = {}
								send_str = "%sVotes reset.\r\n" % pre_msg
							elif msg_arr[1] == "results":
								if vote_on:
									if is_mod(user):
										send_str = "%sCurrent Poll Results: " % pre_msg
										value_dict = sorted(vote_dict.items(), key=operator.itemgetter(1))
										for pair in value_dict:
											key = pair[0]
											value = pair[1]
											send_str += "%s: %s% " % (key, int(value[0]/vote_total*100))
										send_str += "Total votes: %s\r\n" % vote_total
										#display current results
									else:
										send_str = "%sYou have to be a moderator to display the current poll results.\r\n" %pre_msg
								else:
									send_str = "%sThere are no ongoing votes.\r\n" % pre_msg
								irc.send(send_str)
							elif msg_arr[1] == "end": #/close?
								#close the vote
								if is_mod(user):
									vote_on = False
									send_str = "%sPoll Results: " % pre_msg
									value_dict = sorted(vote_dict.items(), key=operator.itemgetter(1))
									for pair in value_dict:
										key = pair[0]
										value = pair[1]
										#if value = 0
										send_str += "%s: %s% " % (key, int(value[0]/vote_total*100))
									send_str += "Total votes: %s\r\n" % vote_total
									irc.send(send_str)
							elif msg == vote_str:
								send_str = "%To vote use " % pre_msg
								for vote_option in range(len(vote_option_arr)): 
									if vote_option != len(vote_option_arr) -1:
										send_str += "\"!vote %s\"/" % vote_option_arr[vote_option]
									else:
										send_str += "\"!vote %s\"\r\n" % vote_option_arr[vote_option]
								irc.send(send_str)		
							else:
								for vote_option in vote_option_arr:
									if msg_arr[1] == vote_option and user not in vote_users:
										#input vote if user hasnt already voted
										vote_dict[vote_option][0] += 1
										vote_users.append(user)
							
					#raffle
					if start_raffle_str == msg:
						if is_mod(user) == True:
							raffle_on = True
							send_str = "%sRaffle started. Join the raffle with \"!raffle\".\r\n" % (pre_msg)
						else:
							send_str = "%s%s only mods can start raffles.\r\n" % (pre_msg, user)
						irc.send(send_str)
						
					if raffle_on == True:
						#avoid duplicatess
						if join_raffle_str == msg and user not in raffle_users:
							raffle_users.append(user)
						if end_raffle_str == msg:
							if is_mod(user) == True:
								winner = raffle_users[random.randint(0, (len(raffle_users) - 1))]
								#need to have prize of some sorts?
								send_str = "%s%s has won the raffle!\r\n" % (pre_msg, winner)
								irc.send(send_str)
								raffle_on = False
							else:
								send_str = "%s%s only mods can end raffles.\r\n" % (pre_msg, user)
								irc.send(send_str)
					#roulette
					#if user is mod then say it doesnt kill you or something
					if rol_on:
						if rol_cmd_str in msg:
							if rol_cmd_str == msg:
								#trigger roulette - allow custom messages for win/loss to replace default ones
								send_str = "%s/me places the revolver to %s's head\r\n" % (pre_msg, user)
								irc.send(send_str)
								#for dramatic effect
									#definitely allow editing of this time
								time.sleep(2)
								if random.random() < rol_chance:
									#time out the user(ban from chat) for rol_timeout amount of seconds
									if is_mod(user) == False:
										timeout(user, irc, rol_timeout)
										send_str = "%sThe trigger is pulled, and the revolver fires! %s lies dead in chat\r\n" % (pre_msg, user)
									else:
										send_str = "%sThe gun jams thanks to your super mod powers. %s lives!\r\n" % (pre_msg, user)
									irc.send(send_str)
								else:
									#do nothing, notify of victory
									send_str = "%sThe trigger is pulled, and the revolver clicks. %s has lived to survive roulette!\r\n" % (pre_msg, user)
									irc.send(send_str)
							if rol_chance_str in msg:
								#get the new chance for ban in roulette
								msg_arr = msg.split(" ")
								#percentage is input as chance, *.01 to change to decimal
								input_perc = int(msg_arr[2])
								if input_perc > 100 or input_perc < 0:
									send_str = "%sPlease input a percentage chance for roulette to be triggered, i.e. \"!roulette chance 50\". Chance must be greater than zero, and less than 100.\r\n" % pre_msg
									irc.send(send_str)
									break
								else:
									rol_chance = input_perc * .01
									send_str = "%sRoulette chance successfully changed to %s%\r\n" % (pre_msg, input_perc)
									irc.send(send_str)
					
					#8ball
					if ball_list_str == msg:
						if is_mod(user):
							send_str = "%sCurrent Possible 8ball responses: "
							for ball_response in range(len(ball_arr)):
								if (ball_response != len(ball_arr) -1):
									#if not last response in arr
									send_str += "(%s.)%s, " % (ball_response+1, ball_arr[ball_response])
								else:
									send_str += "(%s.)%s.\r\n" % (ball_response+1, ball_arr[ball_response])
						else:
							send_str = "%sOnly mods can list 8ball commands.\r\n" % pre_msg
						irc.send(send_str)
					if ball_on:
						if ball_str in msg:
							msg_arr = msg.split(" ", 1)
							if len(msg_arr) == 2:
								ball_response_index = random.randint(0, 19)
								ball_response = ball_arr[ball_response_index]
								send_str = "%sMagic 8 ball says...%s\r\n" % (pre_msg, ball_response)
							elif ball_str == msg:
								send_str = "%sGet the Magic 8 Ball to answer your question. Usage: \"!8ball <question> \".\r\n" % pre_msg
							else:
								send_str = "%sUsage: \"!8ball <question> \".\r\n" % pre_msg
							irc.send(send_str)
					
					#chatters
					if chatters_str == msg:
						chatter_data = get_json_chatters()
						chatter_count = chatter_data["chatter_count"]
						send_str = "%sThere are currently %s accounts in chat.\r\n" % (pre_msg, chatter_count)
						irc.send(send_str)
						
					#viewers
					if viewers_str == msg:
						viewer_data = get_json_chatters()
						viewer_arr = viewer_data["chatters"]["viewers"]
						viewer_count = len(viewer_arr) #i doubt this will work
						send_str = "%sThere are currently %s viewers in the channel.\r\n" % (pre_msg, viewer_count)
						irc.send(send_str)
					#custom commands - these are the exact same as autoreplies. Dont see how we need them.
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
						cmd_dict[cmd] = []
						cmd_dict[cmd].append(0)
						cmd_dict[cmd][0] = response
						
						send_str = "%sCommand \"%s\" successfully added, with response \"%s\".\r\n" % (pre_msg, cmd, response)
						irc.send(send_str)
						
					if del_cmd_str in msg:
						msg_arr = msg.split(" ", 1)
						cmd = msg_arr[1]
						if cmd in cmd_dict:
							#send_str = "%sAre you sure you want to remove '%s' with response '%s'?" % (pre_msg, cmd, cmd_dict[cmd][0])	
							#irc.send(send_str)
							#changed this to remove because pop = uncessary
							cmd_dict.remove(cmd)
							send_str = "%sCommand '%s' successfully removed.\r\n" % (pre_msg, cmd)
							irc.send(send_str)
						else:
							send_str = "%sCommand '%s' not found. Perhaps you misspelled it?\r\n" % (pre_msg, cmd)
							irc.send(send_str)
						
						
					for cmd in cmd_dict:
						if cmd == msg:
							send_str = "%s%s\r\n" % (pre_msg, cmd_dict[cmd][0])
							irc.send(send_str)'''
					for banphrase in banphrase_arr:
						if banphrase in msg:
							timeout(user, irc, banphrase_timeout)
							break
					for ar_pair in ar_arr:
						if ar_pair[0] == msg:
							send_str = "%s%s\r\n" % (pre_msg, ar_pair[1])
							irc.send(send_str)
					#this is probably what's taking so long, changing this to be a one time addon to an array with a function 
					#emote related commands - need to handle custom emotes
					for emote in emote_arr:
						if msg.count(emote) != 0:
							#update dictionary with emote
							emote_count = msg.count(emote)
							count_dict[emote][0] += emote_count
							stats_str = "!stats %s" % emote
							if stats_str == msg:
								emote_per_min = find_per_min(emote)
								send_str = "%sTotal times %s has been sent: %s. %s per minute: %s.\r\n" % (pre_msg, emote, count_dict[emote][0], emote, emote_per_min)
								irc.send(send_str)			
							
			else:
				irc.close()
				time.sleep(3)
				connect()
		
