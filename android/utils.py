#!/bin/python
#-*- coding:utf-8 -*-

import os
import shutil
import sys


## Checks if a directory on the remote device exists. If not, creates the directory.
#
# @param dir the path to the directory to be checked.
def check_dir(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)


## Copies all the file in a list to a specified folder.
#
# @param tocopy list of the files to be copied.
# @param destination folder in which we want the files to be copied.
def copy_files(tocopy, destination):
    i = 0

    for current_file in tocopy:
        base = os.path.basename(current_file)
        i += 1
        sys.stdout.write("[" + str(i) + " / " + str(len(tocopy)) + "] " + base)
        shutil.copy(current_file, destination + "/" + base)
        sys.stdout.write(" done.\n")



## Deletes all the files in a list located on a specified folder.
#
# @param todelete list of the file names to be deleted.
# @param destination folder in which the files to be deleted should be located.
def delete_files(todelete, destination):
    i = 0

    for current_file in todelete:
        base = os.path.basename(current_file)
        i += 1
        sys.stdout.write("[" + str(i) + " / " + str(len(todelete)) + "] " + base)
        os.remove(destination + "/" + base)
        sys.stdout.write(" done.\n")   