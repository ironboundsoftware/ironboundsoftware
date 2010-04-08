#!/usr/bin/env python
# encoding: utf-8
"""
SGP4.py

This version of the SGP4 code is based on the updated code released
by the AIAA paper of 2006.

Created by Nick Loadholtes on 04/05/2010.
Copyright (c) 2010 Iron Bound Software. All rights reserved.
"""

import sys
import os
import unittest
from math import sqrt

WGS72OLD = 1
WGS72 = 2
WGS84 = 3


class SGP4:
	def __init__(self):
		pass
		
	def getGravConst(self, whichconst):
		"""Constants for propagator:
		    tumin       - minutes in one time unit
		    mu          - earth gravitational parameter
		    radiusearthkm - radius of the earth in km
		    xke         - reciprocal of tumin
		    j2, j3, j4  - un-normalized zonal harmonic values
		    j3oj2       - j3 divided by j2
		"""
		if whichconst == WGS72OLD:
			mu     = 398600.79964    
			radiusearthkm = 6378.135
			xke    = 0.0743669161
			tumin  = 1.0 / xke
			j2     =   0.001082616
			j3     =  -0.00000253881
			j4     =  -0.00000165597
			j3oj2  =  j3 / j2
			return (tumin, mu, radiusearthkm, xke, j2, j3, j4, j3oj2)
		if whichconst == WGS72:
			mu     = 398600.8
			radiusearthkm = 6378.135
			xke    = 60.0 / sqrt(radiusearthkm*radiusearthkm*radiusearthkm/mu)
			tumin  = 1.0 / xke
			j2     =   0.001082616
			j3     =  -0.00000253881
			j4     =  -0.00000165597
			j3oj2  =  j3 / j2
			return (tumin, mu, radiusearthkm, xke, j2, j3, j4, j3oj2)
		if whichconst == WGS84:
			mu     = 398600.5
			radiusearthkm = 6378.137
			xke    = 60.0 / sqrt(radiusearthkm*radiusearthkm*radiusearthkm/mu)
			tumin  = 1.0 / xke
			j2     =   0.00108262998905
			j3     =  -0.00000253215306
			j4     =  -0.00000161098761
			j3oj2  =  j3 / j2
			return (tumin, mu, radiusearthkm, xke, j2, j3, j4, j3oj2)
		return None


class SGP4Tests(unittest.TestCase):
	s = None
	def setUp(self):
		self.s = SGP4()
	
	def testGravConstWGS72OLD(self):
		"""testGravConstWGS72OLD"""
		results = self.s.getGravConst(WGS72OLD)
		self.assertTrue(len(results) == 8)
		self.assertAlmostEqual(0.0743669161, results[3])

	def testGravConstWGS72(self):
		"""testGravConstWGS72"""
		results = self.s.getGravConst(WGS72)
		self.assertTrue(len(results) == 8)
		self.assertAlmostEqual(0.074366916133173, results[3])
		
	def testGravConstWGS84(self):
		"""testGravConstWGS84"""
		results = self.s.getGravConst(WGS84)
		self.assertTrue(len(results) == 8)
		self.assertAlmostEqual(0.074366916133173, results[3])
		
if __name__ == '__main__':
	unittest.main()