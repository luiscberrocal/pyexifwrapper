'''
Created on May 12, 2012

@author: luiscberrocal
'''
from utils.utils_functions import loadYamlConfig, isWindows, isMac
import os

class TestConfig(object):
    __instance = None
    
    '''
    classdocs
    '''
    def __init__(self):
        self.config = {}
        rconfig = loadYamlConfig(__file__, 'test_data_config.yml')
        if isWindows():
            path = rconfig['data_path']['windows']
        elif isMac():
            path = rconfig['data_path']['mac']
        else:
            raise Exception('Unsupported Operating system for TestConfig')
        for name, fn in rconfig['files'].iteritems():
            self.config[name] = os.path.join(path, fn)

    @staticmethod
    def getInstance():
        if TestConfig.__instance is None:
            TestConfig.__instance = TestConfig()
        return TestConfig.__instance
    
if __name__ == '__main__':
    tc = TestConfig.getInstance()
    print tc.config
    print id(tc)
    tc2 = TestConfig.getInstance()
    print id(tc2)
    
            
        
        