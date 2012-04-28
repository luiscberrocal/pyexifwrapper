# -*- coding: utf-8 -*-
#!/usr/bin/env python
# encoding: utf-8

"""
exif_tools.py

Created by Luis C. Berrocal on 2012-04-20.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import os, subprocess, re, datetime, yaml

class InvalidTagException(Exception):
	pass
class InvalidValueException(Exception):
	pass
class NoIPTCToTransferException(Exception):
	pass
class UnsupportedStandardException(Exception):
	pass

class ExifTool():
	
	#EXIT_TOOL = os.path.join(r"C:\Temp\python\iptcconvert\libs", "exiftool.exe")
	#pattern_iptc = re.compile(r'^\[IPTC\]\s*([\w\s-]*):\s(.*)')
	#pattern_xmp = re.compile(r'^\[XMP\]\s*([\w\s-]*):\s(.*)')
	#attern_pdf = re.compile(r'^\[PDF\]\s*([\w\s-]*):\s(.*)')
	#pattern_exif = re.compile(r'^\[EXIF\]\s*([\w\s-]*):\s(.*)')
	IPTC = 0
	XMP = 1
	PDF = 2
	__iptc_to_pdf = {"Headline" : "Subject",
	                "Keywords" : "Keywords",
	                "Writer-Editor" : "Author",
	                "Caption-Abstract" : "Title",
	                "DateCreated" : "xmp:Event",
	                "ProgramVersion" : None,
	                "OriginatingProgram" : None,
	                "ApplicationRecordVersion" : None,
	                "CopyrightNotice" :"xmp:Copyright",
	                "Source" : "xmp:Source",
	                "SpecialInstructions" : "xmp:Instructions",
	                "By-line" : "xmp:Creator",
	                "Credit" : "xmp:Credit"
	                }
	def __loadConfig(self):
		config_path = os.path.split(__file__)[0]
		f = open(config_path + os.sep + 'exif_config.yml')
		self.config = yaml.load(f)
		f.close()
		#print self.config
		#self.pattern_exif = re.compile(self.config['standards'][0]['exif']['pattern'])
		self.standards = {}
		for standard in self.config['standards']:
			#print standard["name"]
			self.standards[standard["name"]] = re.compile(standard["pattern"])
		#print "=== %s" % self.pattern_exif				
	def __init__(self, filename, verbose = False):
		self.__verbose = verbose
		if not os.path.exists(filename):
			raise Exception("File %s does not exist" % (filename))
		self.filename = filename
		self.__loadConfig()
		self.__load(filename)
	
	def __load(self, filename):
		self.standard_values = {}
		for standard, pattern in self.standards.iteritems():
			self.standard_values[standard]={}
		command =	[self.config["exif"]["application"], '-G', '-charset', self.config["exif"]["charset"], filename]
		p = subprocess.Popen(command , shell=self.config["exif"]["shell"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in p.stdout.readlines():
			#print line.decode("utf-8").rstrip('\n')
			for standard, pattern in self.standards.iteritems():
				#self.standards[standards]["values"] = {}
				match = pattern.match(line.decode("utf-8").rstrip('\n'))
				if match:
					self.standard_values[standard][match.group(1).replace(" ", "")] =  match.group(2)
					break
		retval = p.wait()
	
	def prettyPrint(self,*standards_to_print):
		for standard, values in self.standard_values.iteritems():
			if standards_to_print:
				if standard in standards_to_print:
					for tag, val in values.iteritems():
						print "%s %s %s" % (standard, tag, val)
			else:
				for tag, val in values.iteritems():
					print "%s %s %s" % (standard, tag, val)
		#print "Len iptc %d" % len(self.iptc)
	
	def addToAttribute(self, standard, key, value):
		values ={}
		values[key] = value
		if standard == self.IPTC:
			self.__setAtt("IPTC", values)
		elif standard == self.XMP:
			self.__setAtt("XMP", values)
		elif standard == self.PDF:
			self.__setAtt("PDF", values)
		else:
			raise Exception("Invalid standard")
	def setAttribute(self, standard, key, value):
		pass
	def __buildKey(self, standardName, tag, value):
		key = None
		if tag.find(":") == -1:
			key =  "-%s:%s='%s'" % (standardName.lower(), tag, value.rstrip('\n\r'))
		else:
			standard, tagname = tag.split(":")
			key =  "-%s:%s='%s'" % (standard.lower(), tagname, value.rstrip('\n\r'))
		#print "Key : " +  key
		return key
	
	def __setAtt(self, standardName, values, listAction ="replace"):
		invalid_tag_pattern = re.compile('Warning:\sTag\s\'(.*)\'\sdoes\snot\sexist')
		invalid_value_pattern = re.compile('Warning:\sInvalid\s(.*)')
		keycommand = [self.config["exif"]["application"]]
		
		for k, v in values.iteritems():
			if type(v) is list:
				if listAction =="replace":
					for vv in v:
						key = self.__buildKey(standardName, k,vv)
						keycommand.append(key)
				else:
					raise Exception("Unsupported list action %s" % listAction)
			else:
				key = self.__buildKey(standardName, k,v)
				#"-%s:%s='%s'" % (standardName.lower(), k, v)
				keycommand.append(key)
		keycommand.append('-charset')
		keycommand.append(self.config["exif"]["charset"])
		keycommand.append(self.filename)
		#print keycommand
		p = subprocess.Popen( keycommand, shell=self.config["exif"]["shell"], stdout=subprocess.PIPE, \
							  stderr=subprocess.STDOUT)
		lc = 1
		for line in p.stdout.readlines():
			invalid_tag_match = invalid_tag_pattern.match(line.rstrip('\n'))
			invalid_value_match = invalid_value_pattern.match(line.rstrip('\n'))
			if invalid_tag_match:
				raise InvalidTagException("Tag %s es Invalida para %s" % (invalid_tag_match.group(1), standardName.upper()))
			if invalid_value_match:
				raise InvalidValueException("Valor invalido %s"	 % invalid_value_match.group(0))
			print "%d %s" % (lc, line)
			lc += 1
		if lc > 2:
			raise Exception("More than one line on out for exittool for %s" % (self.filename))
		self.__load(self.filename)
	#----------------------------------------------------------------------
	def __isStandardNameValid(self, standardName):
		""""""
		valid_standard = False
		for st_name in self.config["standards"]:
			if st_name["name"] == standardName:
				valid_standard = True
				break
		return valid_standard
	#----------------------------------------------------------------------
	def getAttribute(self, tag_name, standard_name = None):
		""""""
		
		
	def setAttributes(self, standardName, values ={}):
		
		if self.__isStandardNameValid(standardName):
			self.__setAtt(standardName, values)
		else:
			raise UnsupportedStandardException("%s is not a valid Standard Name" % (standardName))
		
		
	def addIPTCFrom(self, filename):
		jpgiptc = ExifTool(filename)
		changes = {}
		for iptc_tag in jpgiptc.iptc.keys():
			if iptc_tag in self.__iptc_to_pdf:
				#print k
				if iptc_tag != "Keywords":
					if self.__iptc_to_pdf[iptc_tag]:
						changes[self.__iptc_to_pdf[iptc_tag]] = jpgiptc.iptc[iptc_tag]
				else:
					keywords = []
					for keyword in jpgiptc.iptc[iptc_tag].split(","):
						keywords.append(keyword.strip())
						#print "***** " + keyword
					changes[self.__iptc_to_pdf[iptc_tag]] = keywords
			else:
				#print self.__iptc_to_pdf
				raise InvalidTagException("The tag '%s' is not supported by __iptc_to_pdf. Value: %s " \
										  % (k, jpgiptc.iptc[iptc_tag]))
		if len(changes) > 1:
			self.setAttributes(self.PDF, changes)
		else:
			raise NoIPTCToTransferException("File %s has no valid IPTC tags to transfer" % filename)
			#print "NO IPTC to transfer"


class StandardTag():
	#----------------------------------------------------------------------
	def __init__(self, name, standard_name = None):
		""""""
		
		
	
if __name__ == '__main__':
	main()

