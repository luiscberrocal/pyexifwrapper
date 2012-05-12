'''
Created on May 12, 2012

@author: luiscberrocal
'''
import unittest
from test_config import TestConfig
from files.filename_helpers import FilenameHelper


class Test(unittest.TestCase):

    data = TestConfig.getInstance().config
    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testMd5Checksum(self):
        md5_results = {'toy': "e91112138e590ea070ed3b22e2e62bdc", 'ferns': "d5ce1efd5e2c36715121341403190a8a" }
        for k, v in self.data.iteritems():
            print k
            md5 = FilenameHelper.md5Checksum(v)
            print "%s %s" % (v, md5)
            self.assertEquals(md5_results[k], md5)
            
    def testSize(self):
        sizes_results = {'toy': (35.8193359375, 'KB'), 'ferns': (40.46875, 'KB') }
        for k, fn in self.data.iteritems():
            print k
            size = FilenameHelper.size(fn)
            print size
            self.assertEquals(sizes_results[k], size)
    def testSize_MB(self):
        sizes_results = {'toy': (0.034979820251464844, 'MB'), 'ferns': (0.039520263671875, 'MB') }
        for k, fn in self.data.iteritems():
            print k
            size = FilenameHelper.size(fn, "MB")
            print size
            self.assertEquals(sizes_results[k], size)        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()