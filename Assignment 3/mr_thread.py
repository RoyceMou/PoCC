#!/usr/bin/python
#  
#
# Vanderbilt University Computer Science
# Author: Aniruddha Gokhale
# Course: CS4287-5287 Principles of Cloud Computing
# Created: Fall 2016
#
# Purpose: MapReduce Threading
#

# system and time
import os
import sys

# shared data structure and threading
import threading

# subclass from the threading.Thread
class MR_Thread (threading.Thread):
    # constructor
    def __init__ (self, name, func, data):
        threading.Thread.__init__(self)
        self.func = func
        self.arg = {'name' : name,
                    'data' : data}

    # override the run method which is invoked by start
    def run (self):
        print "Starting " + self.name
        self.func (self.arg)
        print "Exiting " + self.name

