# -*- coding: utf-8 -*-
import socket
import threading
import time

from config import *


class TwitchIRCClient(threading.Thread):
    def __init__(self, nick, password):
        threading.Thread.__init__(self)
        self.nick = nick
        self.password = password
        self.host = (TWITCH_SERVER_HOST, TWITCH_SERVER_PORT)

        self._buffer = ""
        self._socket = socket.socket()
        self.connected = False
        self.output = list()
        self.daemon = True
        self._users = []

    def _connect(self):
        self._socket.connect(self.host)
        self.send("PASS {}".format(self.password))
        self.send("NICK {}".format(self.nick))
        self.connected = True
        print "Connected"

    def disconnect(self):
        self.connected = False
        self._socket.close()
        self.output.append("* Disconnected!")

    # Method to handle incomming data
    def _receive(self):
        self._buffer += self._socket.recv(1024)
        temp = self._buffer.split("\n")
        self._buffer = temp.pop()

        for line in temp:
            line = line.rstrip()
            line = line.split()

            if "001" in line:
                self.connected = True

            if line[0] == "PING":
                self.send("PONG {}".format(line[1]))
            if line[1] == '353':
                #parsing out users
                if len(line) >= 5:
                    line[5] = line[5][1:]  # removing the ':'nick sign
                    for user in line[5:]:
                        if user != self.nick:
                            self._users.append(user)
                self.output.append("Currently found {} number of users!".format(len(self._users)))

            if "PART" in line:
                nick = line[0].split('!')[0][1:]
                if nick != self.nick:
                    if nick in self._users:
                        self._users.remove(nick)
                    else:
                        print "A user left that wasn't there"
                self.output.append("User left: {} number of users!".format(len(self._users)))

            if "JOIN" in line:
                nick = line[0].split('!')[0][1:]
                if nick != self.nick:
                    self._users.append(nick)
                    self.output.append("User Joined: {} number of users!".format(len(self._users)))



    def __iter__(self):
        return self

    def next(self):
        if self.output:
            return self.output.pop(0)
        raise StopIteration

    def clear_output(self):
        self.output = []

    def join_channel(self, channel):
        self._channel = channel
        self.send("JOIN " + channel)

    def private_msg(self, name, msg):
        self.send("PRIVMSG " + name + " :" + msg)

    def send(self, text):
        cmd = text + '\r\n'
        self._socket.send(cmd)

    def run(self):
        while True:
            if self.connected is False:
                try:
                    self._connect()
                except:
                    time.sleep(3)
            else:
                try:
                    self._receive()
                except Exception as e:
                    print e
                    print "WRONG STUFF HAPPENED"
                    self.disconnect()
                    time.sleep(5)

    def part(self):
        self.send("PART " + self._channel)

