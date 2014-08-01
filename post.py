#!/usr/bin/env python

print "Content-Type: text/html"
print

import cgi
import cgitb
cgitb.enable()

import cPickle
import time
import string
import os
from blogtools import postBuild,frontPage,rssBuild
import urllib2
import markdown
	
#Step 0: Load the data from the form
submission = cgi.FieldStorage()
title = str(submission["title"].value)
content = str(submission["content"].value)
tags = str(submission["tags"].value).split(",")

#Step 0.5: Generate a timestamp to use as a key
timestamp = int(time.time())

#Step 1: Create a clean title to use as a filename, and a file path.
cleantitle = title.lower().translate(None,string.punctuation).replace(" ","-")
month = time.strftime("%m")
year = time.strftime("%Y")
filepath = year + "/" + month + "/" + cleantitle

#Step 2: Add the new post to the master list.
f = open("postlist")
postlist = cPickle.load(f)
f.close()

postlist[timestamp] = (title,tags,filepath,[])

#Step 2.9: Check for Markdown. If the Markdown box is ticked, convert it to html
#Step 2.95: Replace Markdown <img to include a class to allow for resizing and stuff

if 'markdown' in submission:
	content = markdown.markdown(content)
	content = content.replace('<img','<img class="markdown"')

#Step 3: Put the post content in a text file.
if not os.path.exists(year):
	os.mkdir(year)
if not os.path.exists(year + "/" + month):
	os.mkdir(year + "/" + month)
txtpost = open(filepath + ".txt","w")
txtpost.write(content)
txtpost.close()

#Step 4: Build the html, and save it.
newpost = postBuild(timestamp,"templates/template.html",postlist)
htmlpost = open(filepath + ".html","w")
htmlpost.write(newpost)
htmlpost.close()

#Step 5: Find the previous post, and rebuild it to add a 'next' link
ork = postlist.keys()
ork.sort()
previd = ork[ork.index(timestamp)-1]
prevpost = postBuild(previd,"templates/template.html",postlist)
htmlprevpost = open(postlist[previd][2] + ".html","w")
htmlprevpost.write(prevpost)
htmlprevpost.close()


#Step 6: Do the homepage.
frontPage(postlist)

#Step 7: Do the RSS feed
rssBuild(postlist,"templates/atomentry.xml",10)
urllib2.urlopen("http://rockym93.net/update.py")

#Step 8: Write the master post list back to file
f = open("postlist","w")
cPickle.dump(postlist,f)
f.close()
