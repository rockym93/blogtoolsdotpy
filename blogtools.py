#!/usr/bin.env python
import time

#This is the page builder function.
#It takes a key from the master list, (must be loaded)
#constructs the local date from that key,
#takes the tags and title supplied,
#goes to [filepath].txt for the post text, 
#and finds the next and previous posts using the master list.
#Then it builds them into html using template.html
def postBuild(key,templatefile,postlist):
	#Date & Title
	printabledate = time.strftime("%A, %d %B %Y",time.gmtime(key + 28800))
	printabletime = time.strftime("%I:%M%p",time.gmtime(key + 28800))
	atomtime = time.strftime("%Y-%m-%dT%H:%M:%S+08:00",time.gmtime(key + 28800))
	printabletitle = postlist[key][0]
	#Tags
	printabletags = str()
	for i in postlist[key][1]:
		printabletags += '<a href="../../search.py?for=' + i + '&in=tags">' + i + '</a>,'
	printabletags.rstrip(",")
	#Content
	contentfile = open(postlist[key][2] + ".txt","r")
	printabletext = contentfile.read()
	contentfile.close()
	#Previous and next post buttons
	orderedkeys = postlist.keys()
	orderedkeys.sort()
	previouspost = "../../" + postlist[orderedkeys[orderedkeys.index(key)-1]][2] + ".html"
	#If this is the newest post, hide the 'next' link.
	if orderedkeys[-1] != key:
		nextpost = "../../" + postlist[orderedkeys[orderedkeys.index(key)+1]][2] + ".html"
	else:
		nextpost = False
	#Comments
	numcomments = str(len(postlist[key][3]))
	comments = ""
	for i in postlist[key][3]:
		cts = i[0]
		cauth = i[1]
		cf = open(postlist[key][2] + "." + str(cts))
		ctxt = cf.read()
		cf.close()
		comments += "<p class='comment'><b>" + cauth + " </b><br><i> " + time.ctime(cts+28800) + " </i><br><br>" + ctxt + "</p>\n"
	#Permalink
	permalink = postlist[key][2] + ".html"
	#Open template file
	tf= open(templatefile)
	template = tf.read()
	tf.close()
	#Fill in template file
	posthtml = template.replace("!DATE",printabledate)
	posthtml = posthtml.replace("!TIME",printabletime)
	posthtml = posthtml.replace("!ATOMTIME",atomtime)
	posthtml = posthtml.replace("!TAGS",printabletags)
	posthtml = posthtml.replace("!TITLE",printabletitle)
	posthtml = posthtml.replace("!TEXT",printabletext)
	posthtml = posthtml.replace("!PREVIOUS",previouspost)
	posthtml = posthtml.replace("!NUMCOMMENTS",numcomments)
	posthtml = posthtml.replace("!COMMENTS",comments)
	posthtml = posthtml.replace("!POST_ID",str(key))
	posthtml = posthtml.replace("!PERMALINK",permalink)
	if nextpost:
		posthtml = posthtml.replace("!NEXT",nextpost)
	else:
		posthtml = posthtml.replace("/*HIDDEN*/","display:none")
	return posthtml

def frontPage(postlist):
	keylist = postlist.keys()
	keylist.sort()
	for i in range(1,6):
		fp = open("frontpage/" + str(i) + ".html","w")
		fp.write(postBuild(keylist[i * -1],"templates/frontpost.html",postlist))
		fp.close()
	fp = open("previous","w")
	fp.write(postBuild(keylist[-5],"templates/frontprev.html",postlist))
	fp.close()
	
def rssBuild(postlist,template,length):
	keylist = postlist.keys()
	keylist.sort()
	feed = '<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>Rocky\'s Blag</title><subtitle>The thrilling adventures of... some guy?</subtitle><link href="http://blog.rockym93.net/atom.xml" rel="self" /><link href="http://blog.rockym93.net" /><id>tag:rockym93.net,2012-12-19:blogfeed</id><updated>' + time.strftime("%Y-%m-%dT%H:%M:%SZ") + '</updated>'
	for i in range(1, length+1):
		feed += postBuild(keylist[i*-1],template,postlist)
	feed += '</feed>'
	feedfile = open("atom.xml","w")
	feedfile.write(feed)
	feedfile.close()
		
