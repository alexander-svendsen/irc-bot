from irc_client import *
from config import *
import ConfigParser
import os.path

Config = ConfigParser.ConfigParser()
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print ("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

nick = ""
password = ""

if os.path.isfile(CONFIG_FILE):
    print "Found config, reading nick and password"
    Config.read(CONFIG_FILE)
    nick = ConfigSectionMap("personal_info")['nick']
    password = ConfigSectionMap("personal_info")['password']
else:
    print "No config found, Input nick and password, Hit enter to continue"
    nick = raw_input("NICK: ")
    password = raw_input("PASSWORD: ")

    cfgfile = open(CONFIG_FILE, 'w')
    Config.add_section('personal_info')
    Config.set('personal_info', 'nick', nick)
    Config.set('personal_info', 'password', password)
    Config.write(cfgfile)
    cfgfile.close()


print "Connecting to twitch"

irc = TwitchIRCClient(nick, password)
irc.start()

while not irc.connected:
    print "Waiting..."
    time.sleep(1)

print "Connected!"

irc.join_channel(CHANNEL)

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



