'''
Created on Aug 2, 2009

@author: njl
'''
import unittest	
from SatId import Ident

class Test(unittest.TestCase):
	i = None

	def setUp(self):
		self.i = Ident.Identify()

	def tearDown(self):
		pass

	def testIdent(self):
		self.i.identify(None)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testIdent']
	unittest.main()