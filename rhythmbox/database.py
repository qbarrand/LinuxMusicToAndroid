#!/usr/bin/python
#-*- coding:utf-8 -*-

##
# @file sync.py
#
# Utilities for handling database interactions with Rhythmbox.

from lxml import etree

def getTracksFromPlaylist(playlists_xml, playlist):
	xml_doc = etree.parse(playlists_xml)

	tracks = []

	for track in xml_doc.xpath("//playlist[@name='" + playlist + "']/location"):
		tracks.append(track.text) 

	return tracks