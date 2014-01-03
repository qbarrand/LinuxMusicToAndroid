#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import getopt

import utils.conf
from rhythmbox.sync import Rsync

version = 0.2

try:
    opts, args = getopt.getopt(sys.argv[1:], "bc:drs", ["config=", "debug", "rebase", "silent"])
except getopt.GetoptError as err:
    print str(err)
    sys.exit(2)

# Default config file path
config_path = "config.json"

# Loading configuration
for o, a in opts:
    if o in ("-c", "--config"):
        config_path = a

config = utils.conf.Conf(config_path)

# Loading app parameters
for o, a in opts:
    if o in ("-d", "--debug"):
        config.enable_debug()
    elif o == "--rebase":
        config.enable_rebase()
    elif o in ("-s", "--silent"):
        config.enable_silent()

banshee = False
rhythmbox = False

# Launching sync
for o, a in opts:    
    if o == "-b":
        banshee = True
    if o == "-r":
        rhythmbox = True

if banshee and rhythmbox:
    print "Options -b and -r are not compatible yet."
    sys.exit(2)
elif banshee:
    print "Banshee is currently not supported."
    # banshee_sync = Bsync(config)
    # banshee_sync.sync()
elif rhythmbox:
    rhythmbox_sync = Rsync(config)
    rhythmbox_sync.sync()
else:
    print "Please provide a sync mode (-b or -r)."
    sys.exit(2)  

print "All operations completed, exiting..."
