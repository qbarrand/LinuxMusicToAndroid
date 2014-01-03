#!/usr/bin/python
#-*- coding:utf-8 -*-

## 
# @file conf.py
#
# The configuration instance used everywhere in the application.

import json
import sys

class Conf:

	## The constructor.
	#
	# @param config_path path to the configuration file that should be loaded.
	def __init__(self, config_path):
		# Retrieving data from the config.json file
		config_file	 = open(config_path)
		config = json.loads(config_file.read()	)
		config_file.close()

		## Debug mode (@c -d or @c --debug arguments).
		#
		# If this option is enabled, a detailed debugging output is sent to the standard output.
		self.debug = False

		## Determines if a full copy should be made.
		#
		# If this option is enabled, the remote tracks and database on the Android device
		# are erased.
		self.rebase = False

		## Silent mode (-s or --silent).
		#
		# If this option is enabled, output is redirected from stdout to the lmtoa.log file.
		self.silent = False

		## Array containing some device-related properties.
		#
		# Included properties :
		#    - path : the path to the Android mounted filesystem.
		self.android = {}
		self.android['path'] = config['android']['path'] + "/lmtoa/"

		## Array containing some Banshee-related properties.
		#
		# Included properties :
		#    - db_path : the path to the Banshee central database.
		#    - playlist : the name of the playlist to be synchronized.
		self.banshee = {}
		self.banshee['db_path'] = config['banshee']['db_path']
		self.banshee['playlist'] = config['banshee']['playlist']

		## Array containing some Rhythmbox-related properties.
		#
		# Included properties :
		#    - playlist : the path to Rhythmbox playlists.xml.
		self.rhythmbox = {}
		self.rhythmbox['playlists_xml'] = config['rhythmbox']['playlists_xml']
		self.rhythmbox['playlist_name'] = config['rhythmbox']['playlist_name']


	## Enables utils.conf.Conf.debug.
	#
	# @param self the instance pointer.
	def enable_debug(self):
		print "Debug mode enabled"
		self.debug = True


	## Enables utils.conf.Conf.rebase.
	#
	# @param self the instance pointer.
	def enable_rebase(self):
		if self.debug:
			print "Rebase mode enabled"

		self.rebase = True


	## Enables utils.conf.Conf.silent.
	#
	# @param self the instance pointer.
	def enable_silent(self):
		if self.debug:
			print "Silent mode enabled"

		self.silent = True
		sys.stdout = open("lmtoa.log", "w")
