#!/usr/bin/env python

print "Content-Type: text/html"
print

import cgi
import cgitb
cgitb.enable()
import blogtools


	
#Load the data from the form
submission = cgi.FieldStorage()
title = str(submission["title"].value)
content = str(submission["content"].value)
tags = str(submission["tags"].value).split(",")

#Generate a timestamp to use as a key
timestamp = int(time.time())

blogtools.newpost(timestamp, title, content, tags)
