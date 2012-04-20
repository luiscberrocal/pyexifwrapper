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

class ExifTool():
	#EXIT_TOOL = os.path.join(r"C:\Temp\python\iptcconvert\libs", "exiftool.exe")
	pattern_iptc = re.compile(r'^\[IPTC\]\s*([\w\s-]*):\s(.*)')
	pattern_xmp = re.compile(r'^\[XMP\]\s*([\w\s-]*):\s(.*)')
	pattern_pdf = re.compile(r'^\[PDF\]\s*([\w\s-]*):\s(.*)')
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
	def __init__(self, filename, verbose = False):
		self.__verbose = verbose
		if not os.path.exists(filename):
			raise Exception("File %s does not exist" % (filename))
		self.filename = filename
		config_path = os.path.split(__file__)[0]
		f = open(config_path + os.sep + 'exif_config.yml')
		self.config = yaml.load(f)
		f.close()
		print self.config
		self.__load(filename)
	
	def __load(self, filename):
		self.iptc = {}
		self.xmp = {}
		self.pdf = {}
		
		p = subprocess.Popen( (self.config["exif"]["application"], '-G', '-charset', self.config["exif"]["charset"], filename), shell=self.config["exif"]["shell"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in p.stdout.readlines():
			#print line.decode("utf-8").rstrip('\n')
			m_iptc = self.pattern_iptc.match(line.decode("utf-8").rstrip('\n'))
			m_xmp = self.pattern_xmp.match(line.decode("utf-8").rstrip('\n'))
			m_pdf = self.pattern_pdf.match(line.decode("utf-8").rstrip('\n'))
			if m_iptc:
				self.iptc[m_iptc.group(1).replace(" ", "")] =  m_iptc.group(2)
				#print "IPTC %s = %s" % (m_iptc.group(1), m_iptc.group(2))
			elif m_xmp:
				self.xmp[m_xmp.group(1).replace(" ", "")] = m_xmp.group(2)
				#print "XMP	 %s = %s" % (m_xmp.group(1), m_xmp.group(2))
			elif m_pdf:
				self.pdf[m_pdf.group(1).replace(" ", "")] = m_pdf.group(2)
				#print "XMP	 %s = %s" % (m_xmp.group(1), m_xmp.group(2))
			else:
				if self.__verbose:
					print "**" + line.decode("utf-8").rstrip('\n')
		retval = p.wait()
	
	def prettyPrint(self):
		print "Len iptc %d" % len(self.iptc)
		for key, v in self.iptc.iteritems():
			print "IPTC %s : %s" % (key, v)
		for key, v in self.xmp.iteritems():
			print "XMP %s : %s" % (key, v)
		for key, v in self.pdf.iteritems():
			print "PDF %s : %s" % (key, v)
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
		if standard == self.IPTC:
			key = "-iptc:%s='%s'" % (key, value)
			p = subprocess.Popen( (self.EXIT_TOOL, key, '-charset', 'Latin', self.filename), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			for line in p.stdout.readlines():
				print line
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
		keycommand = [self.EXIT_TOOL]
		
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
		keycommand.append('Latin')
		keycommand.append(self.filename)
		#print keycommand
		p = subprocess.Popen( keycommand, shell=True, stdout=subprocess.PIPE, \
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
	def setAttributes(self, standard, values ={}):
		if standard == self.IPTC:
			self.__setAtt("IPTC", values)
		elif standard == self.XMP:
			self.__setAtt("XMP", values)
		elif standard == self.PDF:
			self.__setAtt("PDF", values)
		else:
			raise Exception("Invalid standard")
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

if __name__ == '__main__':
	main()

