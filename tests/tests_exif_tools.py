#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
tests_exif_tools.py

Created by Luis C. Berrocal on 2012-04-20.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import unittest
from exif.exif_tools import *
from exif.ExifWrapper import *
import sys


class tests_exif_tools(unittest.TestCase):
	def setUp(self):
		pass
	def testPrettyPrint(self):
		method_name = sys._getframe(0).f_code.co_name
		print "**** %s ****" % method_name
		fn =r"/Users/luiscberrocal/Pictures/IMG_3109.JPG"
		#fn = r'/Users/luiscberrocal/Documents/Luis Alberto La Batalla Final.mov'
		extool = ExifTool(fn, False)
		extool.prettyPrint()
	def testConfig(self):
		method_name = sys._getframe(0).f_code.co_name
		print "**** %s ****" % method_name
		fn =r"/Users/luiscberrocal/Pictures/IMG_3109.JPG"
		#fn = r'/Users/luiscberrocal/Documents/Luis Alberto La Batalla Final.mov'
		extool = ExifTool(fn, False)
		print extool.config
    
if __name__ == '__main__':
	unittest.main()