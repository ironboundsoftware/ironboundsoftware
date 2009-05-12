'''
Created on May 5, 2009

@author: nick.loadholtes

obsdata comes from the MPC sample: http://www.cfa.harvard.edu/iau/info/ObsExamples.html

'''
import unittest
from formats import MPC

obsdata = ("    CJ93K010  C1995 01 12.44658 23 20 12.59 -73 00 31.9                      413",
"    PJ93X010  C1995 01 13.71552 12 08 44.80 +01 55 10.6                      413",
"    PJ94P01d  C1994 10 14.82517 09 57 25.32 +09 06 28.5          13.3 T      360",
"    PJ95A010  C1995 01 27.42558 07 45 16.64 +21 40 44.4          20.6 N      691",
"0007P         C1995 01 07.49677 10 07 09.83 +31 58 36.9                      691",
"0047P         C1994 12 31.38076 07 40 47.47 +37 40 09.1                      693",
"0116P         C1995 01 03.21177 02 40 39.14 +18 09 23.5          20.8 T      691",
"     J91R04W F 1994 04 03.00278 11 28 41.20 +04 14 24.8                      033",
"     J93P00C cC1994 07 04.57639 17 28 54.97 -38 12 17.1          17.1 V      360",
"     PLS2645   1994 03 04.63681 11 40 57.89 +06 07 08.6                      399",
"     T1S3196   1994 05 04.56403 14 26 06.83 -15 41 20.8          16.6        474",
"     T2S3187  A1973 09 19.21250 00 24 34.59 -01 08 26.0                      675",
"     T3S2318  C1994 07 12.22157 19 47 43.23 -15 45 37.3                      801",
"02965         C1994 07 13.97693 17 35 15.33 -00 26 18.9          16.1 R      046",
"     94ORX0 * C1994 06 08.98877 16 22 02.78 -17 49 13.7          18.5        104",)

class Test(unittest.TestCase):


	def testParse(self):
		""" Test to make sure we can parse the standard ref obs """
		mpc = MPC.parseMPC(obsdata[0])
		self.assertFalse(None == mpc)
		self.assertEquals(mpc.observatory, "413")
		for o in obsdata:
			mpc = MPC.parseMPC(o)
			self.assertFalse(None == mpc)
			self.assertEquals(o[-3:], mpc.observatory)
		print "obs->",mpc.observatory
		
	def testParseBlank(self):
		""" Blank """
		mpc = MPC.parseMPC("")
		self.assertTrue(None == mpc)
		mpc = MPC.parseMPC("          		  		  		  		  		  		  		  ")
		self.assertTrue(None == mpc)
		mpc = MPC.parseMPC(None)
		self.assertTrue(None == mpc)

	def testParseJunk(self):
		""" Junk """
		mpc = MPC.parseMPC("Junk blah blah")
		self.assertTrue(None == mpc)
			  		  

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testParse']
	unittest.main()
