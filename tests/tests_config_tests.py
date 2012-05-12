'''
Created on May 12, 2012

@author: luiscberrocal
'''
import unittest
from tests.test_config import TestConfig



class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testInstance(self):
        tc = TestConfig.getInstance()
        id1 = id(tc)
        tc2 = TestConfig.getInstance()
        id2 = id(tc2)
        self.assertEqual(id1, id2)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInstance']
    unittest.main()