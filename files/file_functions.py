#!/usr/bin/env python
# encoding: utf-8
"""
file_functions.py

Created by Luis C. Berrocal on 2012-04-23.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os
def validateFile(path, filename):
	print filename[:4].decode('utf-8')
	if filename[:4] == "Guía":
		return False
	else:
		return True
		
def filecount(directory_name):
	return len([f for f in os.listdir(directory_name) \
		if os.path.isfile(os.path.join(directory_name,f)) and validateFile(directory_name, f)])

#def copyToSize(source_folder, target_folder, limit):
	
