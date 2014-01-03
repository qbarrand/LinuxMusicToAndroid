#!/usr/bin/python
#-*- coding:utf-8 -*-

##
# @file functions.py
#

import os
import urllib
import shutil
import sys


## Simple function offering a yes / no ouput.
#
# @param question String that should be displayed.
# @param default default slected option. Default value is "yes".
#
# @return a boolean (True or False.)
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = { "yes":True,
              "y":True,
              "ye":True,
              "no":False,
              "n":False }

    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")


## Simple function looking for doubles values in one list.
#
# @param check_list the list to check for doubles in.
#
# @return a list of the double values.
def check_doubles(check_list):
    doubles = []

    for e1 in range(0, len(check_list)):
        for e2 in range(e1 + 1, len(check_list)):
            if check_list[e1] == check_list[e2]:
                doubles.append(check_list[e1])

    return doubles


## Returns a file's basename from its URI.
#
# @param uri the file's URI.
#
# @return the file's basename (filename.extension).
def basename_from_uri(uri):
    return os.path.basename(urllib.unquote(uri)[7:])


## Return a file's path from its URI.
#
# @param uri the file's URI.
#
# @return the file's path.
def path_from_uri(uri):
    return urllib.unquote(uri)[7:]


## Get all the tracks that are present in local_tracks but not in remote_tracks.
#
# @param local_tracks tracks that belong to the computer's music manager playlist.
# @param remote_tracks tracks that are present on the device.
#
# @return a list of the tracks that need to be copied to the device.
def get_tocopy_tracks(local_tracks, remote_tracks):
    tocopy = []

    for track in local_tracks:
        if track not in remote_tracks:
            tocopy.append(track)

    return tocopy


## Get all the tracks that are present in remote_tracks but not in local_tracks.
#
# @param local_tracks tracks that belong to the computer's music manager playlist.
# @param remote_tracks tracks that are present on the device.
#
# @return a list of the tracks that need to be removed from the device.
def get_todelete_tracks(local_tracks, remote_tracks):
    todelete = []

    for track in remote_tracks:
        if track not in local_tracks:
            todelete.append(track)

    return todelete