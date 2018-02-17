#!/usr/bin/python
# coding=utf-8

import unittest
import pc

class TestPc(unittest.TestCase):
    
    #let's suppose the url file is not there
    def test_getOrig(self, ):
        self.assertRaises(FileNotFoundError, pc.getOrig, 'doesnotexist')
    
    def test_urlTest(self, ):
        self.assertEqual(pc.urlTest('http://jkkjkj'), False)
        self.assertEqual(pc.urlTest('http://jkkjkj. ed'), False)
        self.assertEqual(pc.urlTest('http://url.com'), True)
    
    
if __name__ == '__main__':
    unittest.main()
