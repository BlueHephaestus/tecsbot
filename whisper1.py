import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import sys, operator, time, urllib, json, math, os, random, unicodedata
from datetime import datetime, timedelta

def get_json_servers():
	url = "http://tmi.twitch.tv/servers?cluster=group"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return data
		
#sets variables for connection to twitch chat
bot_owner = 'darkelement75'
nick = 'tecsbot' 
ping_nick = "@%s" % nick
#for now making this whatever I input
channel = '#_tecsbot_1444071429976'
#channel = sys.argv[1]
channel_parsed = channel.replace("#", "")

server_json = get_json_servers()
server_arr = (server_json["servers"][0]).split(":")
server = server_arr[0]
port = int(server_arr[1])

password = 'o'

pre_msg = "PRIVMSG %s :" % channel

queue = 13 #sets variable for anti-spam queue functionality <- dafuq is this used for

#initial connect
irc = socket.socket()
irc.connect((server, port)) #connects to the server
#sends variables for connection to twitch chat
irc.send("CAP REQ :twitch.tv/commands\r\n")
irc.send('PASS ' + password + "\r\n")
irc.send('NICK ' + nick + "\r\n")
irc.send('JOIN ' + channel + "\r\n")

def connect():
	irc = socket.socket()
	irc.connect((server, port)) #connects to the server
	#sends variables for connection to twitch chat
	#/commands and /tags both work apparently, just gonna use this
	irc.send("CAP REQ :twitch.tv/commands\r\n")
	irc.send('PASS ' + password + "\r\n")
	irc.send('NICK ' + nick + "\r\n")
	irc.send('JOIN ' + channel + "\r\n")
	
def whisper(user, msg):
	send_str = "%s/w %s %s\r\n" % (pre_msg, user, msg)
	irc.send(send_str)
	
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
				
				
		#whisper("darkelement75", "ayy lmao")
				
				
				
	else:
		irc.close()
		time.sleep(3)
		connect()