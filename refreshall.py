#!/usr/bin/env python
import time
import cPickle
from blogtools import postBuild,frontPage,rssBuild

f = open("postlist")
postlist = cPickle.load(f)
f.close()

keylist = postlist.keys()

for key in keylist:
	f = open(postlist[key][2] + ".html","w")
	f.write(postBuild(key,"templates/template.html",postlist))
	f.close()
	print postlist[key][0] + " rebuilt."

frontPage(postlist)
print "main page rebuilt"
rssBuild(postlist,"templates/atomentry.xml",10)
print "atom feed rebuilt"
