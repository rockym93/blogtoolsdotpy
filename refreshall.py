#!/usr/bin/env python
import blogtools

for i in blogtools.postlist:
	blogtools.refresh(i)

blogtools.buildfront()
