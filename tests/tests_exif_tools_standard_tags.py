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


class tests_exif_tools_standard_tags(unittest.TestCase):
	def setUp(self):
		pass
	def test_isStandardNameValid(self):
		method_name = sys._getframe(0).f_code.co_name
		print "**** %s ****" % method_name
		isv = StandardTag.isStandardNameValid("xmp")
		self.assertTrue(isv)
		
		isv = StandardTag.isStandardNameValid("opt")
		self.assertFalse(isv)
	#----------------------------------------------------------------------
	def test_init_name_only(self):
		method_name = sys._getframe(0).f_code.co_name
		print "**** %s ****" % method_name
		tag = StandardTag("xmp:Title")
		self.assertEquals("xmp", tag.standard_name)
		self.assertEquals("Title", tag.name)
	#----------------------------------------------------------------------
	def test_init_exception(self):
		""""""
		method_name = sys._getframe(0).f_code.co_name
		print "**** %s ****" % method_name
		try:
			tag = StandardTag("xrp:Title")
			self.fail("Did not raised execption)")
		except UnsupportedStandardException, e:
			print e
			
	#----------------------------------------------------------------------
	def test_getCommadKey(self):
		""""""
		method_name = sys._getframe(0).f_code.co_name
		print "**** %s ****" % method_name
		xmp_title = StandardTag( "Title","xmp")
		key = xmp_title.getCommandKey("This is an xmp Title")
		self.assertEquals(key, "-xmp:Title='This is an xmp Title'")
		print key
	#----------------------------------------------------------------------
	def test_getCommadKey_None(self):
		""""""
		method_name = sys._getframe(0).f_code.co_name
		print "**** %s ****" % method_name
		xmp_title = StandardTag( "Title","xmp")
		key = xmp_title.getCommandKey(None)
		self.assertEquals(key, "-xmp:Title=")
		print key	
	
		
		
	
    
if __name__ == '__main__':
	unittest.main()