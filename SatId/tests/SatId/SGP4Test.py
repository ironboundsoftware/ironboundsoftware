'''
Created on May 14, 2009

@author: njl
'''
import unittest
import SatId
from SatId import SGP
from SatId.formats import TLE
from math import pi

#
# Sample input and results from reference implementation.
#
#Sample TLE
#1 88888U 80275.98708465 .00073094 13844-3 66816-4 0 8
#2 88888 72.8435 115.9689 0086731 52.6988 110.5714 16.05824518 105
#
#SGP4 results
#TSINCE 				X 							Y 								Z
#0. 						2328.97048951 	-5995.22076416 		1719.97067261
#360.00000000 	2456.10705566 	-6071.93853760 		1222.89727783
#720.00000000 	2567.56195068 	-6112.50384522 		713.96397400
#1080.00000000 2663.09078980 	-6115.48229980 		196.39640427
#1440.00000000 2742.55133057 	-6079.67144775 		-326.38095856
#
#XDOT 				YDOT 				ZDOT
#2.91207230 	-0.98341546 	-7.09081703
#2.67938992 	-0.44829041 	-7.22879231
#2.44024599 	0.09810869 	-7.31995916
#2.19611958 	0.65241995 	-7.36282432
#1.94850229 	1.21106251 	-7.35619372
#

class Test(unittest.TestCase):

	def testNoneForInput(self):
		s = SGP.SGP4(None,3)
		self.assertEqual((None, None, None), s)

	def testSample(self):
		tle = TLE.TLE() 
		s = SGP.SGP4(tle,3)
		self.assertNotEqual((None, None, None), s)
		self.assertEqual((0, 0, 0), s)

	def testWTF(self):
		import SatId
		print "Looking at SatId"

		
class TestFunkyRadianNormalizer(unittest.TestCase):
	f = None
	
	def setUp(self):
		self.f = SGP.fmod2p
		
	def testNormal(self):
		self.assertEqual(0, self.f(0))
	
	def test3Pi(self):
		self.assertEqual(pi, self.f(3*pi))
	
	def testPi(self):
		self.assertEqual(pi, self.f(pi))
		
	def test2Pi(self):
		self.assertEqual(0, self.f(2*pi))

	
	
	
	
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testSample']
	unittest.main()
	
	
	