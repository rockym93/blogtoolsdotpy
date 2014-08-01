#!/usr/bin/env python
print "Content-Type: text/html"
print

import cgi
import cgitb
cgitb.enable()
import time
import cPickle
import blogtools

form = cgi.FieldStorage()
if form.getvalue("captcha") == "apple":
	
	timestamp = int(time.time())
	author = form.getvalue("username")
	parent = int(form.getvalue("id"))
	
	blogtools.postlist[parent][3].append((timestamp,author))
	content = form.getvalue("comment")
	content = content.replace("<","&lt")
	content = content.replace(">","&gt")
	#content = content.encode("ascii","ignore")
	content = content.replace("\n","<br />")
	
	txtfile = open(blogtools.postlist[parent][2] + "." + str(timestamp),"w")
	txtfile.write(content)
	txtfile.close()
	
	blogtools.refresh(parent)
	
	blogtools.buildfront() #just in case
	
	blogtools.save()
	
	print "<html><head><title>Comment posted.</title></head><body>"
	print "Thanks, " + author + ". Your comment has been posted.<br>"
	print "<a href='" + blogtools.postlist[parent][2] + ".html'>&lt;Back</a>"
	print "</body></html>"
else:
	print "<html><head><title>Post failed.</title></head><body>"
	print "Sorry, your comment has not been posted.<br>"
	print "It looks like you failed the spambot filter. If you're not a spambot, why not go back and try again?"
	print "</body></html>"
