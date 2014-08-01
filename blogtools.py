#!/usr/bin/env python
import time
import cPickle
import string
import os
import urllib2
import markdown

if not os.path.exists("postlist"):
	f = open("postlist","w")
	cPickle.dump({},f)
	f.close()

f = open("postlist")
postlist = cPickle.load(f)
f.close()

keylist = postlist.keys()
keylist.sort()

def newpost(timestamp, title, content, tags):
	#Step 1: Create a clean title to use as a filename, and a file path.
	cleantitle = title.lower().translate(None,string.punctuation).replace(" ","-")
	month = time.strftime("%m")
	year = time.strftime("%Y")
	filepath = year + "/" + month + "/" + cleantitle
	
	#Step 2: Add the new post to the master list.
	
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
	newpost = buildpost(timestamp,"templates/template.html")
	htmlpost = open(filepath + ".html","w")
	htmlpost.write(newpost)
	htmlpost.close()
	
	#Step 5: Find the previous post, and rebuild it to add a 'next' link
	previd = keylist[-1]
	refresh(previd)
	
	#Step 6: Do the homepage.
	buildfront()
	
	#Step 7: Do the RSS feed
	buildfeed()
	urllib2.urlopen("http://rockym93.net/update.py")
	
	#Step 8: Write the master post list back to file
	save()


#This is the page builder function.
#It takes a key from the master list, (must be loaded)
#constructs the local date from that key,
#takes the tags and title supplied,
#goes to [filepath].txt for the post text, 
#and finds the next and previous posts using the master list.
#Then it builds them into html using the template given
def buildpost(key,templatefile):
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
	previouspost = "../../" + postlist[keylist[keylist.index(key)-1]][2] + ".html"
	#If this is the newest post, hide the 'next' link.
	if keylist[-1] != key:
		nextpost = "../../" + postlist[keylist[keylist.index(key)+1]][2] + ".html"
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

def buildfront(length=5):
	'''rebuilds the front page'''
	for i in range(1,length + 1):
		try:
			fp = open("frontpage/" + str(i) + ".html","w")
			fp.write(buildpost(keylist[i * -1],"templates/frontpost.html",postlist))
			fp.close()
		except IndexError:
			pass
	fp = open("previous","w")
	fp.write(buildpost(keylist[-5],"templates/frontprev.html",postlist))
	fp.close()
	
def buildfeed(length=10):
	'''rebuilds the atom feed'''
	feed = '<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>Rocky\'s Blag</title><subtitle>The thrilling adventures of... some guy?</subtitle><link href="http://blog.rockym93.net/atom.xml" rel="self" /><link href="http://blog.rockym93.net" /><id>tag:rockym93.net,2012-12-19:blogfeed</id><updated>' + time.strftime("%Y-%m-%dT%H:%M:%SZ") + '</updated>'
	for i in range(1, length+1):
		try:
			feed += buildpost(keylist[i*-1],"templates/atomentry.xml",postlist)
		except IndexError:
			pass
	feed += '</feed>'
	feedfile = open("atom.xml","w")
	feedfile.write(feed)
	feedfile.close()

def save():
	'''saves the currently open module instance of the postlist'''
	f = open("postlist","w")
	cPickle.dump(postlist,f)
	f.close()

def refresh(post):
	'''refreshes an individual post'''
	f = open(postlist[post][2] + ".html","w")
	f.write(buildpost(post, "templates/template.html"))
	f.close()

		
