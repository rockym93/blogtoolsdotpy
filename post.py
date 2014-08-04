#!/usr/bin/env python

print "Content-Type: text/html"
print

import time
import cgi
import cgitb
cgitb.enable()
import blogtools



#Load the data from the form
submission = cgi.FieldStorage()
title = str(submission["title"].value).decode("utf-8")
content = str(submission["content"].value).decode("utf-8")
tags = str(submission["tags"].value).split(",")

#Generate a timestamp to use as a key
timestamp = int(time.time())

blogtools.newpost(timestamp, title, content, tags)
