'''
Created on May 14, 2009

@author: njl
'''
import unittest
from SatId import SGP

class Test(unittest.TestCase):


	def testSample(self):
		s = SGP.SGP4(None,3)
		self.assertNotEqual((None, None, None), s)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testSample']
	unittest.main()