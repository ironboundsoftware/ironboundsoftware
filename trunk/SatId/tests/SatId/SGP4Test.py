'''
Created on May 14, 2009

@author: njl
'''
import unittest
import SatId
from SatId import SGP

class Test(unittest.TestCase):


	def testSample(self):
		s = SGP.SGP4(None,3)
		self.assertNotEqual((None, None, None), s)

	def testWTF(self):
		import SatId
		print "Looking at SatId"

		
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testSample']
	unittest.main()