#!/usr/bin/env python
# encoding: utf-8
"""
tests_exif_tools.py

Created by Luis C. Berrocal on 2012-04-20.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import unittest
from exif.exif_tools import *

class tests_exif_tools(unittest.TestCase):
	def setUp(self):
		pass
	def testInit(self):
		fn =r"/Users/luiscberrocal/Pictures/IMG_3109.JPG"
		fn = r'/Users/luiscberrocal/Documents/Luis Alberto La Batalla Final.mov'
		extool = ExifTool(fn, True)
    
if __name__ == '__main__':
	unittest.main()