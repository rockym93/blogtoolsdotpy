#!/usr/bin/env python
import os
import time
import cPickle
import cgi
import cgitb
cgitb.enable()

f = open("postlist")
postlist = cPickle.load(f)
f.close()

keys = postlist.keys()
keys.sort()

query = cgi.FieldStorage()
search = query.getvalue("for")
type = query.getvalue("in")
print "Content-Type: text/html"
print 
templatefile = open("templates/search.html")
template = templatefile.read().split("#SEARCHRESULTS")
templatefile.close()
print template[0]

if type == "tags":
	if search == "all":
		print "showing all tags:<br>"
		alltags = dict()
		for i in keys:
			for tag in postlist[i][1]:
				if tag not in alltags.keys():
					alltags[tag] = []
				alltags[tag].append(postlist[i])
			
		for tag in alltags:
			print tag + "<ul>"
			for post in alltags[tag]:
				print "<li><a href='" + post[2] + ".html'>" + post[0] + "</a></li>"
			print "</ul>"
					
	else:
		print "posts tagged " + search + ":"
		print "<ul>"
		for i in keys:
			if search in postlist[i][1]:
				print "<li><a href='"+ postlist[i][2] + ".html'>" + postlist[i][0] + "</a></li>"
		print "</ul>"
elif type == "commenters":
	postswithcomments = {}
	commentlist = []
	if search == "all":
		for i in keys:
			if postlist[i][3]:
				for c in postlist[i][3]:
					postswithcomments[c[0]] = postlist[i]
					commentlist.append(c[0])
		commentlist.sort()
		commentlist.reverse()
		print "showing all comments: <ul>"
		for c in commentlist:
			print "<li>" + str(time.ctime(c)) + " on <a href='" + postswithcomments[c][2] + ".html'>" + postswithcomments[c][0] + "</a></li>"
		print "</ul>"
	else: 
		for i in keys:
			if postlist[i][3]:
				for c in postlist[i][3]:
					if c[1].lower() == search.lower():
						postswithcomments[c[0]] = postlist[i]
						commentlist.append(c[0])
		commentlist.sort()
		commentlist.reverse()
		print "comments by " + search + ":<ul>"
		for c in commentlist:
			print "<li>" + str(time.ctime(c)) + " on <a href='" + postswithcomments[c][2] + ".html'>" + postswithcomments[c][0] + "</a></li>"
		print "</ul>"
elif type == "title":
	titlelist = []
	for i in keys:
		if search.lower() in postlist[i][0].lower():
			titlelist.append(i)
	titlelist.sort()
	titlelist.reverse()
	print "titles containing " + search + ":<ul>"
	for t in titlelist:
		print "<li>" + str(time.ctime(t)) + " on <a href='" + postlist[t][2] + ".html'>" + postlist[t][0] + "</a></li>"
	print "</ul>"
else:
	print "<ul>"
	for i in keys:
		print "<li>" + time.strftime("%d/%m/%Y",time.gmtime(i + 28800)) + " - <a href='" + postlist[i][2] + ".html'>" + postlist[i][0] + "</a></li>"
	print "</ul>"

print template[1]

