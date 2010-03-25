'''
Created on May 12, 2009

@author: nick.loadholtes
'''
import unittest
from SatId.formats import TLE


buffer = "ISS (ZARYA)\n\
1 25544U 98067A   04236.56031392  .00020137  00000-0  16538-3 0  5135\n\
2 25544  51.6335 341.7760 0007976 126.2523 325.9359 15.70406856328903"

class TestTLE(unittest.TestCase):
	tlefile = "tests/SGP4-VER.TLE"

	def testParse(self):
		tles = TLE.parseTLE(buffer)
		self.assertEqual(1, len(tles))
		tle = tles[0]
		print "TLE->" + str(tle)
		self.assertNotEquals(None, tle)
		# self.assertEqual("ISS (ZARYA)", tle.name)
		self.assertEqual("25544", tle.objectId)
		self.assertEqual("98067A  ", tle.intDesgination)
		self.assertEqual(04236.56031392, tle.elementSetEpoch)
		self.assertEqual(0.00020137, tle.firstDeriv)
		self.assertEqual(0.0, tle.secondDeriv)
		self.assertEqual(0.00016538, tle.bStarDrag)
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
		
	def testTLEFileBad(self):
		"""There's a big file of test TLEs, lets make sure we can read it."""
		tle = TLE.parseTLE(self.tlefile)
		self.assertNotEquals(None,tle)
		# Should this test pass? It isn't reading in the file... It 
		# is trying to parse the tlefile string.
		print "TLE is" + str(tle)
		
	def testTLEFile(self):
		"""A read of the TLE test file"""
		f = open(self.tlefile)
		buff = f.read()
		# print buff
		tles = TLE.parseTLE(buff)
		self.assertNotEquals(None, tles)
		self.assertEquals(33, len(tles))
		self.assertEquals("14128", tles[7].objectId)
		

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(Test)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testParse']
	unittest.main()