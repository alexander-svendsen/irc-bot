# -*- coding: utf-8 -*-
__author__ = 'Alexander'


import time

import socket
import thread


#sets variables for connection to twitch chat
nick = 'segment_fault'
channel = '#vinzet'
server = 'irc.twitch.tv'
password = 'oauth:XXX'

irc = socket.socket()
irc.connect((server, 6667))  # connects to the server


def forever_print():
    while True:
        print irc.recv(1024)

#sends variables for connection to twitch chat
irc.send('PASS ' + password + '\r\n')
print "-> PASS " + password
irc.send('NICK ' + nick + '\r\n')
print "-> NICK " + nick
print irc.recv(1024)

thread.start_new(forever_print, ())
time.sleep(5)
#irc.send('USER ' + nick + ' 0 * :' + bot_owner + '\r\n')

irc.send('NAMES ' + channel + '\r\n')
print "-> NAMES " + channel

time.sleep(4)
irc.send('JOIN ' + channel + '\r\n')
print "-> JOIN " + channel


while(True):
    time.sleep(1)