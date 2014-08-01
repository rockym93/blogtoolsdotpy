#!/usr/bin/env python
import time,os,pickle
from blogtools import *

print "time,os,pickle,blogtools imported."

postlist = pickle.load(open("postlist"))
keylist = postlist.keys()
keylist.sort()

print "postlist unpickled."

def save():
	pickle.dump(postlist,open("postlist","w"))

print "don't forget to save()"
