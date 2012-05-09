# -*- coding: utf-8 -*-
'''
Created on May 9, 2012

@author: lberrocal
'''
import sys, os
from files.filename_helpers import FilenameHelper
from shutil import copy2


if __name__ == '__main__':
    '''http://www.pycs.net/users/0000323/stories/14.html'''
    test_encondings = ['utf-8', 'cp1252', 'iso-8859-1', 'ascii']
    print "sys.stdin.encoding:     %s" % (sys.stdin.encoding)
    print "sys.stdout.encoding:    %s" % (sys.stdout.encoding)
    print "sys.getdefaultencoding: %s" % (sys.getdefaultencoding())
    name_str = "Panamá"
    name_unicode = u"Panamá"
    
    print "String  : %s"  %(name_str)
    print "Unicode : %s"  %(name_unicode)
    print "ENCODING string"
    for enc in test_encondings:
        try:
            print "\rString encode %10s : %s"  %(enc, name_str.encode(enc))
        except:
            print "\rCannot encode string for %s " % (enc)
    
    print "DECODING string"
    for enc in test_encondings:
        try:
            print "\rString decode %10s : %s"  %(enc, name_str.decode(enc))
        except:
            print "\rCannot decode string for %s " % (enc)
    print "ENCODING unicode"
    for enc in test_encondings:
        try:
            print "\rString encode %10s : %s"  %(enc, name_unicode.encode(enc))
        except:
            print "\rCannot encode string for %s " % (enc)
    print "DECODING unicode"
    for enc in test_encondings:
        try:
            print "\rString decode %10s : %s"  %(enc, name_unicode.decode(enc))
        except:
            print "\rCannot decode string for %s " % (enc)
    
    print "=" *50
    word = 'Piráña'
    letters = list(word)
    for let in letters:
        msg = let + " : "
        for x in let:
            msg += str(hex(ord(x)))
        print msg
    print '-'*60
    fn =r'C:\Temp\python\iptcconvert\output\1996-DesignaciónAdministradorPCC.jpg'
    exists = os.path.exists(fn)
    print "%s [%d] %s" % (fn, len(fn), exists)
    
    print '-'*60
    fn = ur'C:\Temp\python\iptcconvert\output\1996-DesignaciónAdministradorPCC.jpg'
    exists = os.path.exists(fn)
    print "%s [%d] %s" % (fn, len(fn), exists)
    nfn = FilenameHelper.addDateToFilename(fn)
    copy2(fn, nfn)
    exists = os.path.exists(nfn)
    print "%s [%d] %s" % (nfn, len(nfn), exists)
    
    
    
    
