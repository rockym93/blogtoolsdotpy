#!/usr/bin/env python

import pickle
import yaml

f = open("postlist","r")
postlist = pickle.load(f)
f.close()

for i in postlist:
	postlist[i] = list(postlist[i])

f = open("postlist","w")
yaml.dump(postlist,f)
f.close()
