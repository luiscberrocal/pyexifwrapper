'''
Created on May 8, 2012

@author: lberrocal
'''
import os, yaml, shutil
from files.filename_helpers import FilenameHelper
import datetime


def shortenDisplay(stringval, maxlen = 80):
    sval = stringval
    if len(stringval) > maxlen:
        ln = maxlen / 2 - 3
        n = len(stringval) -ln
        sval = stringval[:ln] + "..." + stringval[n:]
    return sval
def loadYamlConfig(src_filename, config_filename = None):
    cfg_filename = None
    if config_filename:
        path = os.path.split(src_filename)[0]
        cfg_filename = os.path.join(path, config_filename)
    else:
        cfg_filename = FilenameHelper.changeExtension(src_filename, ".yml")
    cfg_file = open(cfg_filename, 'r')
    cfg = yaml.load(cfg_file)
    cfg_file.close()
    return cfg

def isWindows():
    import platform
    return platform.system() == 'Windows'
def isMac():
    import platform
    return platform.system() == 'Darwin'

def backupFile(fn, outputPath = None, overwrite = False):
    new_fn = FilenameHelper.addDateToFilename(fn)
    if outputPath:
        today= datetime.datetime.now().strftime('%Y-%m-%d')
        npath = os.path.join(outputPath, today )
        if not os.path.exists(npath):
            os.makedirs(npath)            
        filename = os.path.split(fn)[1]
        new_fn = os.path.join(npath, filename)
        if os.path.exists(new_fn) and not overwrite:
            raise IOError("File %s already exists function is set to not overwrite" % new_fn)
        elif os.path.exists(new_fn) and overwrite:
            new_fn = FilenameHelper.addDateToFilename(new_fn)
    shutil.copy2(fn, new_fn)
    if not os.path.exists(new_fn):
        raise IOError("Could not copy file %s to %s" %( fn, new_fn))    
    return new_fn