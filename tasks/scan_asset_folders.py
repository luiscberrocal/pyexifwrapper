'''
Created on May 12, 2012

@author: luiscberrocal
'''
import os
from assets.models import AssetFolder
from django.utils import timezone
import optparse
from utils.utils_functions import shortenDisplay, isWindows

def loadFoldersToDB(root_directory):
    c=0
    for root_directory, dirs, files in os.walk(root_directory): #@UnusedVariable
        if len(files) != 0:
            c += 1
            if isWindows():
                mroot = root_directory.decode('cp1252')
            else:
                mroot = root_directory
            print "%4d %-100s %5d" % (c, shortenDisplay(mroot), len(files))
            af = AssetFolder(path = mroot, asset_count = len(files), last_scanned = timezone.now())
            af.save()
            print "-" * 150
        #print dirs
        #print files
        
if __name__ == '__main__':
    default_root_directory = None # ur'/Users/luiscberrocal/Pictures/iPhoto Library/Originals'
    parser = optparse.OptionParser()
    parser.add_option("-d", "--directory", dest="directory_to_scan",
                      default=default_root_directory, type="string",
                      help="Directory to parse")
    (options, args) = parser.parse_args()
    
    print "Scanning %s" % (options.directory_to_scan)
    loadFoldersToDB(options.directory_to_scan)
    
    

    

        
        #if c > 25:
        #    break
        