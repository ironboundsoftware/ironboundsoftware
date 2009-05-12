'''
Created on May 12, 2009

@author: nick.loadholtes
'''
import unittest
from formats import TLE

buffer = "ISS (ZARYA)\n\
1 25544U 98067A   04236.56031392  .00020137  00000-0  16538-3 0  5135\n\
2 25544  51.6335 341.7760 0007976 126.2523 325.9359 15.70406856328903"

class Test(unittest.TestCase):


	def testParse(self):
		tle = TLE.parseTLE(buffer)
		self.assertNotEquals(None, tle)
		self.assertEqual("ISS (ZARYA)", tle.name)
		self.assertEqual("25544", tle.objectId)
		self.assertEqual("98067A  ", tle.intDesgination)
		self.assertEqual(04236.56031392, tle.elementSetEpoch)
		self.assertEqual(.00020137, tle.firstDeriv)
		self.assertEqual(" 00000-0", tle.secondDeriv)
		self.assertEqual(" 16538-3", tle.bStarDrag)
		self.assertEqual("0", tle.elementSetType)
		self.assertEqual(513, tle.elementNumber)
		self.assertEqual(51.6335, tle.inclination)
		self.assertEqual(341.7760, tle.ra)
		self.assertEqual(0.0007976, tle.eccentricity)
		self.assertEqual(126.2523, tle.perigee)
		self.assertEqual(325.9359, tle.anomaly)
		self.assertEqual(15.70406856, tle.meanMotion)
		self.assertEqual(32890, tle.revolutions)

	def testParseBad(self):
		tle = TLE.parseTLE("")
		self.assertEquals(None, tle)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testParse']
	unittest.main()