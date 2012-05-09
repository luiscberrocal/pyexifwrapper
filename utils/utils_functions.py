'''
Created on May 8, 2012

@author: lberrocal
'''
import os, yaml
from files.filename_helpers import FilenameHelper

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