#!/usr/bin/env python
# encoding: utf-8
"""
tests_file_functions.py

Created by Luis C. Berrocal on 2012-04-23.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import unittest
from files.file_functions import *

class tests_file_functions(unittest.TestCase):
	def setUp(self):
		pass
	def testFileCount(self):
		dir =r'/Users/luiscberrocal/Documents/Magic Briefcase'
		dir = r'/Users/luiscberrocal/Documents/Magic Briefcase/Sample Documents'
		c = filecount(dir)
		print "%s (%d files)" % (dir, c)
    
if __name__ == '__main__':
	unittest.main()