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
from utils.utils_functions import isWindows, backupFile




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
		nfn = backupFile(self.fn)
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
		extool = ExifTool(fn, True)
		print extool.filename
		print "=" * len(extool.filename)
		dates = extool.getDateAttributes()
		for k, v in dates.iteritems():
			print "%40s = %s" % (k, v)
		
		extool = ExifTool(self.fn, False)
		print extool.filename
		print "=" * len(extool.filename)
		dates = extool.getDateAttributes()
		for k, v in dates.iteritems():
			print "%40s = %s" % (k, v)
		fn =ur'\\pi-nas\SECUREDAM\CumulusFinal\Ambiente\2004-04-06-003-JMH-055.jpg'
		extool = ExifTool(fn, False)
		print extool.filename
		print "=" * len(extool.filename)
		dates = extool.getDateAttributes()
		for k, v in dates.iteritems():
			print "%40s = %s" % (k, v)
	def test_WriteToXMP(self):
		method_name = sys._getframe(0).f_code.co_name
		print "**** %s ****" % method_name
		fn = ur'C:\Temp\python\iptcconvert\output\pdf_dates\2005-feb-08-Raúl Olmos.pdf'
		backup_folder = ur'C:\Temp\python\iptcconvert\output\pdf_dates'
		backup_file = backupFile(fn, outputPath=backup_folder, overwrite=True)
		print backup_file
		ex = ExifTool(fn, False)
		now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		ex.setAttributes("xmp", {"DateTimeOriginal": now})
		ex.prettyPrint()
    
if __name__ == '__main__':
	unittest.main()