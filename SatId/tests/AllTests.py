'''
Created on Sep 5, 2009

@author: njl
'''

import unittest
import MPCTest, TLETest
import TSatId.AllSatIdTests

if __name__ == '__main__':
#	alltests = unittest.TestSuite()
#	alltests.addTest(MPCTest.suite())
	alltests = unittest.TestSuite([MPCTest.suite(), TLETest.suite(),
								TSatId.AllSatIdTests.suite()])
	runner = unittest.TextTestRunner()
	runner.run(alltests) 
	
