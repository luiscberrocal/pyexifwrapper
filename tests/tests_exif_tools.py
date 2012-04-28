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
import sys, shutil, os

from files.filename_helpers import FilenameHelper

def createCopy(fn, outputPath = None):
	new_fn = FilenameHelper.addDateToFilename(fn)
	if outputPath:
		path, filename = os.path.split(new_fn)
		new_fn = os.path.join(outputPath, filename)
	shutil.copy2(fn, new_fn)
	return new_fn

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
	def testSetAttributes(self):
		method_name = sys._getframe(0).f_code.co_name
		print "**** %s ****" % method_name		
		fn =r"/Users/luiscberrocal/Pictures/IMG_3109.JPG"
		nfn = createCopy(fn)
		extool = ExifTool(nfn, False)
		title = "XMP Title set on %s" % (datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
		print nfn
		print "-" * len(nfn)
		extool.setAttributes("xmp",{"Title": title})
		extool.prettyPrint("xmp")
    
if __name__ == '__main__':
	unittest.main()