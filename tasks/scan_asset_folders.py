'''
Created on May 12, 2012

@author: luiscberrocal
'''
import os
from assets.models import AssetFolder
from django.utils import timezone

if __name__ == '__main__':
    mroot = ur'/Users/luiscberrocal/Pictures/iPhoto Library/Originals'
    c=0
    for mroot, dirs, files in os.walk(mroot):
        if len(files) != 0:
            c += 1
            print "%4d %-100s %5d" % (c, mroot, len(files))
            af = AssetFolder(path = mroot, asset_count = len(files), last_scanned = timezone.now())
            af.save()
        #print dirs
        #print files
        print "-" * 150
        
        #if c > 25:
        #    break
        