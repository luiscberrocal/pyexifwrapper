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
from utils.utils_functions import isWindows

def createCopy(fn, outputPath = None):
	new_fn = FilenameHelper.addDateToFilename(fn)
	if outputPath:
		filename = os.path.split(new_fn)[1]
		new_fn = os.path.join(outputPath, filename)
	shutil.copy2(fn, new_fn)
	if not os.path.exists(new_fn):
		raise IOError("Could not copy file %s to %s" %( fn, new_fn))	
	return new_fn

class tests_exif_tools(unittest.TestCase):
	def setUp(self):
		#self.fn =r"/Users/luiscberrocal/Pictures/IMG_3109.JPG"
		#self.fn =r'C:\Temp\python\iptcconvert\output\2006-05-19-035-NAY-143.jpg'
		#self.fn = ur'C:\Temp\python\2005-08-30-018-ADEG-199.jpg'
		self.fn = u'C:\\Users\\lberrocal\\git\\pyexifwrapper\\test_data\\IMG_2976.jpg'
	def testPrettyPrint(self):
		method_name = sys._getframe(0).f_code.co_name
		print "**** %s ****" % method_name
		
		#fn = r'/Users/luiscberrocal/Documents/Luis Alberto La Batalla Final.mov'
		extool = ExifTool(self.fn, False)
		extool.prettyPrint()
	def testConfig(self):
		method_name = sys._getframe(0).f_code.co_name
		print "**** %s ****" % method_name		
		#fn = r'/Users/luiscberrocal/Documents/Luis Alberto La Batalla Final.mov'
		extool = ExifTool(self.fn, False)
		print extool.config
	def testSetAttributes(self):
		method_name = sys._getframe(0).f_code.co_name
		print "**** %s ****" % method_name		
		#fn =r"/Users/luiscberrocal/Pictures/IMG_3109.JPG"
		nfn = createCopy(self.fn)
		extool = ExifTool(nfn, False)
		title = u"XMP Title set on %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		print nfn
		print "-" * len(nfn)
		extool.setAttributes("xmp",{"Title": title})
		extool.prettyPrint("xmp")
		#print extool.getAttribute("xmp:Title")
		self.assertEquals(title, extool.getAttribute("xmp:Title"))
		
	def test_GetAttributes(self):
		method_name = sys._getframe(0).f_code.co_name
		print "**** %s ****" % method_name		
		#fn =r"/Users/luiscberrocal/Pictures/IMG_3109.JPG"
		extool = ExifTool(self.fn, False)
		make = extool.getAttribute("exif:Make")
		self.assertEquals(make, "Canon")
		flash = extool.getAttribute("Flash", "exif")
		self.assertEquals(flash,"Off, Did not fire")
	def test_checkForDates(self):
		method_name = sys._getframe(0).f_code.co_name
		print "**** %s ****" % method_name
		fn = ur'C:\Temp\python\iptcconvert\output\pdf_dates\2005-feb-08-Raúl Olmos.pdf'
		print fn
		extool = ExifTool(fn, False)
		extool.prettyPrint()
		print "Len exif %d" % (len(extool.standard_values['exif']))
    
if __name__ == '__main__':
	unittest.main()