
#!/usr/bin/python
#-*- coding:utf-8 -*-

##
# @file sync.py
#
# Utilities for handling a synchronization with a Banshee playlist.

import database
import json
import shutil
import sys

from utils.functions import *
import android.utils

## Provides services for synchronizing tracks from Rhythmbox.
class Rsync:

	remote_folder = "rhythmbox/"
	remote_database_name = ".banshee.lmtoa"
	remote_database_version = "0.1"

	## Constructor.
	#
	# @param self the instance pointer.
	# @param config the app's configuration instance.
	def __init__(self, config):
		if config.debug:
			print "Creating new Rsync instance"

		## The app's utils.conf.Conf instance.
		self.config = config


	## Launches a synchronization.
	#
	# @param self the Rsync instance pointer.
	def sync(self):
		print "Beginning Rhythmbox sync"

		uris = []

		try:
			uris = database.getTracksFromPlaylist(self.config.rhythmbox['playlists_xml'], self.config.rhythmbox['playlist_name'])
		except IOError:
			print "Could not read Rythmbox playlists.xml file."
			return

		if not uris:
			print "Playlist " + self.config.rhythmbox['playlist_name'] + "is empty."
			return

		# local_tracks : dict { uri : basename }
		local_tracks = {}

		for uri in uris:
			local_tracks[path_from_uri(uri).decode('utf-8')] = basename_from_uri(uri).decode('utf-8')

		if self.config.rebase:
			print "Rebase mode enabled. This will wipe the music folder on the device."
			if query_yes_no("Proceed anyway ?", default="no"):
				self.purge()

		print "Resolving deltas, please wait..."

		if self.config.rebase:
			remote_tracks = {}
		else:
			remote_tracks = self.load_database_from_device()

		tocopy = get_tocopy_tracks(local_tracks, remote_tracks)
		if self.config.debug:
			print "Tracks to be copied :"
			print tocopy

		todelete = get_todelete_tracks(local_tracks, remote_tracks)
		if self.config.debug:
			print "Tracks to be deleted :"
			print todelete

		# If there are things to do (lists not empty)
		if tocopy or todelete:
			print str(len(tocopy)) + " track(s) to copy and " + str(len(todelete)) + " track(s) to delete."
			if not query_yes_no("Proceed to sync ?", default="yes"):
				return

			remote_tracks = self.update_remote(remote_tracks, tocopy, todelete)
			
			android.utils.check_dir(self.config.android['path'] + self.remote_folder)
			
			if tocopy:
				print "Copying new tracks..."
				android.utils.copy_files(tocopy, self.config.android['path'] + self.remote_folder)
			
			if todelete:
				print "Deleting obsolete tracks..."
				android.utils.delete_files(todelete, self.config.android['path'] + self.remote_folder)

			print "Updating remote database..."
			self.write_database_to_device(self.config.rhythmbox['playlist_name'], remote_tracks)
		else:
			print "Everything up to date."


	## Writes the JSON database (dictionnary that contains an updated dictionnary of the pair { track_path : track_basename } of tracks the device should contain).
	#
	# @param self the Rsync instance pointer.
	def write_database_to_device(self, new_playlist_name, new_playlist_data):
		new_db = self.load_database_from_device()
		
		if not new_db:
			sys.stdout.write("Creating a new remote database...")
			new_db = {}
		else:
			sys.stdout.write("Appending changes to remote database...")

		new_db[".#_DO_NOT_EDIT_THIS_FILE_!_#_"] = "Thanks ;-)"
		new_db["version"] = self.remote_database_version		
		new_db[	new_playlist_name] = new_playlist_data

		f = open(self.config.android["path"] + self.remote_folder + self.remote_database_name, 'w')
		json.dump(new_db, f, indent=True)
		f.close()

		sys.stdout.write(" done.\n")


	## Loads the JSON-formatted database from the device that contains all the present tracks.
	#
	# @param sel the Rsync instance.
	def load_database_from_device(self):
		try:
			f = open(self.config.android["path"] + self.remote_folder + self.remote_database_name)
			library = json.loads(f.read())
			f.close()

			if library["version"] != self.remote_database_version:
				print "Warning : remote Rhythmbox database seems to be incompatible. Things may not work as expected."
				if not query_yes_no("Proceed anyway ?", default="yes"):
					return

			remote_tracks = library[self.config.rhythmbox['playlist_name']]
			
			if self.config.debug:
				print "Found remote database, reading from it..."
		except:
			if not self.config.rebase:
				print "Remote database not found"
			remote_tracks = {}

		return remote_tracks


	## Deletes the whole remote folder on device the initialize a fresh new synchronization.
	#
	# @param sel the Rsync instance.
	def purge(self):
		try:
			shutil.rmtree(self.config.android["path"] + self.remote_folder)
		except:
			print "Could not purge previous tracks."


	##
	#
	#
	def update_remote(self, remote_tracks, tocopy, todelete):
		# Remove old tracks
		for track in tocopy:
			remote_tracks[track] = basename_from_uri(track)

		# Add new ones
		for track in todelete:
			del remote_tracks[track]

		return remote_tracks
