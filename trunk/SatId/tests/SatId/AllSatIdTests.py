'''
Created on Sep 5, 2009

@author: njl
'''
import unittest
import IdentTest, SGP4Test

def suite():
	tests =unittest.TestSuite([IdentTest.suite(), SGP4Test.suite()]) 
	return  tests

if __name__ == "__main__":
	runner = unittest.TextTestRunner()
	runner.run(suite())
	