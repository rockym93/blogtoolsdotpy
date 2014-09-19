#!/usr/bin/env python
import time
import yaml
import string
import os
import urllib2
import markdown

if not os.path.exists("postlist"):
	f = open("postlist","w")
	yaml.dump({},f)
	f.close()

f = open("postlist")
postlist = yaml.load(f)
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
	
	postlist[timestamp] = [title,tags,filepath,[]]
	keylist.append(timestamp)
	
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
	previd = keylist[-2]
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
	#Tags
	printabletags = str()
	for i in postlist[key][1]:
		printabletags += '<a href="../../search.py?for=' + i + '&in=tags">' + i + '</a>,'
	printabletags.rstrip(",")
	
	#Content
	contentfile = open(postlist[key][2] + ".txt","r")
	printabletext = markdown.markdown(contentfile.read())
	contentfile.close()
	
	#Previous and next post buttons
	if keylist[0] != key:
		previouspost = "../../" + postlist[keylist[keylist.index(key)-1]][2] + ".html"
	else:
		previouspost = ""
	
	if keylist[-1] != key:
		nextpost = "../../" + postlist[keylist[keylist.index(key)+1]][2] + ".html"
	else:
		nextpost = ""
	
	#Comments
	comments = ""
	for i in postlist[key][3]:
		cts = i[0]
		cauth = i[1]
		cf = open(postlist[key][2] + "." + str(cts))
		ctxt = cf.read()
		cf.close()
		comments += "<div class='comment'><b>" + cauth + " </b><br><i> " + time.ctime(cts+28800) + " </i><br><br>" + ctxt + "</div>\n"
	
	#Open template file
	tf= open(templatefile)
	template = tf.read()
	tf.close()
	
	#Fill in template file
	posthtml = template.format(
	date = time.strftime("%A, %d %B %Y",time.gmtime(key + 28800)),
	time = time.strftime("%I:%M%p",time.gmtime(key + 28800)),
	atomtime = time.strftime("%Y-%m-%dT%H:%M:%S+08:00",time.gmtime(key + 28800)),
	tags = printabletags,
	title = postlist[key][0],
	text = printabletext,
	nextpost = nextpost,
	numcomments = str(len(postlist[key][3])),
	comments = comments,
	postid = str(key),
	permalink = postlist[key][2] + ".html",
	previous = previouspost,
	next = nextpost
	)

	if not nextpost:
		posthtml = posthtml.replace("/*nexthide*/","display:none")
	if not previouspost:
		posthtml = posthtml.replace("/*prevhide*/","display:none")
	return posthtml

def buildfront(length=5):
	'''rebuilds the front page'''
	f = open("templates/index.html")
	front = f.read()
	f.close()
	
	frontposts = ""
	previous = ""
	
	for i in range(1,length + 1):
		try:
			frontposts +=  buildpost(keylist[i * -1],"templates/frontpost.html")
		except IndexError:
			pass
	if len(keylist) > length:
		previous = postlist[keylist[-(length + 1)][2] + ".html"
	
	front.format(
	content = frontposts,
	previous = previous
	)
	indexfile = open("index.html","w")
	indexfile.write(front)
	indexfile.close()

def buildfeed(length=10):
	'''rebuilds the atom feed'''
	feed = '<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>Rocky\'s Blag</title><subtitle>The thrilling adventures of... some guy?</subtitle><link href="http://blog.rockym93.net/atom.xml" rel="self" /><link href="http://blog.rockym93.net" /><id>tag:rockym93.net,2012-12-19:blogfeed</id><updated>' + time.strftime("%Y-%m-%dT%H:%M:%SZ") + '</updated>'
	for i in range(1, length+1):
		try:
			feed += buildpost(keylist[i*-1],"templates/atomentry.xml")
		except IndexError:
			pass
	feed += '</feed>'
	feedfile = open("atom.xml","w")
	feedfile.write(feed)
	feedfile.close()

def save():
	'''saves the currently open module instance of the postlist'''
	f = open("postlist","w")
	yaml.dump(postlist,f)
	f.close()

def refresh(post):
	'''refreshes an individual post'''
	f = open(postlist[post][2] + ".html","w")
	f.write(buildpost(post, "templates/template.html"))
	f.close()

		
