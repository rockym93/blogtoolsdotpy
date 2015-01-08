#!/usr/bin/env python
import time
import yaml
import string
import os
import urllib2
import markdown
import io

if not os.path.exists("postlist"):
	with file("postlist","w") as f:
		yaml.dump({},f)

with file("postlist") as f:
	postlist = yaml.load(f)


keylist = postlist.keys()
keylist.sort()

def newpost(timestamp, title, content, tags):
	'''create a new post, complete with files and postlist entries.'''
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
#	txtpost = open(filepath + ".txt","w")
	txtpost = io.open(filepath + ".txt", mode='wt', encoding='utf-8')
	txtpost.write(content)
	txtpost.close()
	
	#Step 4: Build the html, and save it.
	newpost = buildpost(timestamp,"templates/template.html")
#	htmlpost = open(filepath + ".html","w")
	htmlpost = io.open(filepath + ".html", mode='wt', encoding='utf-8')
	htmlpost.write(newpost)
	htmlpost.close()
	
	#Step 5: Find the previous post, and rebuild it to add a 'next' link
	previd = keylist[-2]
	refresh(previd)
	
	#Step 6: Do the homepage.
	buildfront()
	
	#Step 7: Do the RSS feed
	buildfeed()
	
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
	'''fill in a template (from file at given path) with the details of given post'''
	#Tags
	printabletags = str()
	for i in postlist[key][1]:
		printabletags += '<a href="/search.py?for=' + i + '&amp;in=tags">' + i + '</a>,'
	printabletags.rstrip(",")
	
	#Content
#	contentfile = open(postlist[key][2] + ".txt","r")
	contentfile = io.open(postlist[key][2] + ".txt", mode='rt', encoding='utf-8')
	mdtext = contentfile.read()
	printabletext = markdown.markdown(mdtext)
	contentfile.close()
	
	#Summary
	summary = mdtext.split('\n')[0]
	
	#Previous and next post buttons
	if keylist[0] != key:
		previouspost = "/" + postlist[keylist[keylist.index(key)-1]][2] + ".html"
	else:
		previouspost = ""
	
	if keylist[-1] != key:
		nextpost = "/" + postlist[keylist[keylist.index(key)+1]][2] + ".html"
	else:
		nextpost = ""
	
	#Comments
	comments = ""
	for i in postlist[key][3]:
		cts = i[0]
		cauth = i[1]
#		cf = open(postlist[key][2] + "." + str(cts))
		cf = io.open(postlist[key][2] + "." + str(cts), mode='rt', encoding='utf-8')
		ctxt = cf.read()
		cf.close()
		comments += "<div class='comment'><b>" + cauth + " </b><br /><i> " + time.ctime(cts+28800) + " </i><br /><br />" + ctxt + "</div>\n"
	
	#Open template file
	with io.open(templatefile, mode='rt', encoding='utf-8') as tf:
		template = tf.read()
		
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
	next = nextpost,
	summary = summary
	)

	if not nextpost:
		posthtml = posthtml.replace("/*nexthide*/","display:none")
	if not previouspost:
		posthtml = posthtml.replace("/*prevhide*/","display:none")
	return posthtml

def buildfront(length=5):
	'''rebuilds the front page'''
	with io.open("templates/index.html", mode='rt', encoding='utf-8') as f:
		front = f.read()
	
	frontposts = ""
	previous = ""
	
	for i in range(1,length + 1):
		try:
			frontposts +=  buildpost(keylist[i * -1],"templates/frontpost.html")
		except IndexError:
			pass
	if len(keylist) > length:
		previous = postlist[keylist[-(length + 1)]][2] + ".html"
	
	front = front.format(
	content = frontposts,
	previous = previous
	)
#	indexfile = open("index.html","wt")
	indexfile = io.open('index.html', mode='wt', encoding='utf-8')
	indexfile.write(front)
	indexfile.close()

def buildfeed(length=10):
	'''rebuilds the atom feed'''
	with io.open("templates/atom.xml", mode='rt', encoding='utf-8') as f:
		feed = f.read()
	feedposts = ""
	for i in range(1, length+1):
		try:
			feedposts += buildpost(keylist[i*-1],"templates/atomentry.xml")
		except IndexError:
			pass
	feed = feed.format(
	content = feedposts,
	updated = time.strftime("%Y-%m-%dT%H:%M:%SZ")
	)
#	feedfile = open("atom.xml","w")
	feedfile = io.open('atom.xml', mode='wt', encoding='utf-8')
	feedfile.write(feed)
	feedfile.close()

def save():
	'''saves the currently open module instance of the postlist'''
	with file("postlist","w") as f:
		yaml.dump(postlist,f)

def refresh(post):
	'''refreshes an individual post'''
#	f = open(postlist[post][2] + ".html","w")
	f = io.open(postlist[post][2] + ".html", mode='wt', encoding='utf-8')
	f.write(buildpost(post, "templates/template.html"))
	f.close()

		
