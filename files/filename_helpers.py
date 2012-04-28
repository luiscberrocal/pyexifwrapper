# -*- coding: cp1252 -*-
import fnmatch
import os, datetime, hashlib


class FilenameHelper:
        @staticmethod
        def getExtension(filename):
                ext = os.path.splitext(filename)[1]
                return ext[1:].lower()
        @staticmethod
        def addDateToFilename(filename):
                path, ext = os.path.splitext(filename)
                now = datetime.datetime.now()
                return "%s_%s%s" % (path, now.strftime('%Y%m%d_%H%M%S'), ext)
        @staticmethod
        def addNumberToFilename(filename, number, new_ext = None):
                path, ext = os.path.splitext(filename)
                now = datetime.datetime.now()
                if new_ext:
                        ext = new_ext
                return "%s_%03d%s" % (path, number, ext)
        
        @staticmethod
        def __checksum(filePath,digest):
                fh = open(filePath, 'rb')
                m = hashlib.new(digest)
                while True:
                        data = fh.read(8192)
                        if not data:
                                break
                        m.update(data)
                fh.close()
                return m.hexdigest()
        
        @staticmethod
        def md5Checksum(filePath):
            return FilenameHelper.__checksum(filePath,'md5')
        @staticmethod
        def sha1Checksum(filePath):
            return FilenameHelper.__checksum(filePath,'sha1')
        @staticmethod
        def size(filename, output_unit = None):
                units = [("KB", 1.0), ("MB", 2.0) , ("GB", 3.0), ("TB", 4.0)]
                s = os.path.getsize(filename)
                sr = 0.0
                u = ""
                if not output_unit is None:
                        for unit in units:
                                #print output_unit.upper(), unit
                                if output_unit.upper() == unit[0]:
                                        #print "** %s ** "  % unit[0]
                                        sr = s / 1024.0**unit[1]
                                        #print s
                                        u = unit[0]
                                        break
                else:
                        for unit in units:
                                #print unit
                                sr = s / 1024.0**unit[1]
                                #print s
                                u = unit[0]
                                if sr < 1024.0:            
                                        break
                return sr, u

def filenameHelperTest():
        fn = r'C:\Temp\python\iptcconvert\output\1996-DesignaciónAdministradorPCC.pdf'
        ext = FilenameHelper.addDateToFilename(fn)
        print ext
        ext = FilenameHelper.addNumberToFilename(fn,2)
        print ext
        cs = FilenameHelper.md5Checksum(fn)
        print "Check sum md5 %s" % (cs)
        cs = FilenameHelper.sha1Checksum(fn)
        print "Check sum sha1 %s" % (cs)
        s = FilenameHelper.size(fn)
        print "Size : %.2f %s" % (s)
        s = FilenameHelper.size(fn,"kb")
        print "Size : %.2f %s" % (s)
        
if __name__ == '__main__':
        filenameHelperTest()
        
