from irc_client import *

#sets variables for connection to twitch chat
nick = 'segment_fault'
channel = '#vinzet'
password = 'XXXX'


irc = TwitchIRCClient(nick, password)
irc.start()

while not irc.connected:
    print "Waiting..."
    time.sleep(1)

print "Connected!"

irc.join_channel(channel)

while True:
    time.sleep(0.1)
    for message in irc:
        print message
        # if message.type == "PRIVMSG":
        #     print message
        #     if delaycount > 0:
        #         delaycount -= 1
        #         continue
        #
        #     command = message.message.split()[0]
        #     if command == "!points":
        #         irc.msg(channel, "{}: To check your points go to gamingforgood.net/profile".format(message.user))
        #         delaycount = 20



