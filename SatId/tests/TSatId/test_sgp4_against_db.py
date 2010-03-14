#!/usr/bin/env python
# encoding: utf-8
"""
test_sgp4_against_db.py

Created by Nick Loadholtes on 03/14/2010.
Copyright (c) 2010 Iron Bound Software. All rights reserved.
"""

import unittest
import sqlite3

from SatId import SGP
from SatId.formats import TLE


class test_sgp4_against_db(unittest.TestCase):
	DBfile = "../obs.db"
	tles = []
	tlefile = "../SGP4-VER.TLE"
	
	def setUp(self):
		f = open(self.tlefile)
		buff = f.read()
		# print buff
		self.tles = TLE.parseTLE(buff)
		f.close()
		# cur.execute("create table sattimes (id int, satid text, " +
		# 	                "t real, x real, y real, z real, x_dot real, y_dot real, z_dot real)")
	    
	def testCalcValues(self):
		"""Reads the DB file, compares those values against what SGP calcs."""
		conn = sqlite3.connect(self.DBfile)
		cur = conn.cursor()
		for tle in self.tles:
			# print "Looking at", tle, tle.objectId
			cur.execute("select id,t,x,y,z from sattimes where id="+ tle.objectId)
			for pos in cur:
				# print "Pos=",pos
				xyz = pos[2:]
				t = pos[1]
				satid = pos[0]
				sgp_xyz = SGP.SGP4(tle, t)
				if xyz == sgp_xyz:
					print "Match:",satid, t, xyz
				else:
					percentError(xyz, sgp_xyz)
				# self.assertEquals(xyz, sgp_xyz)
		conn.close()
		self.assertTrue(False)
		
def percentError(expected, actual):
	""" Looks at what was expected vs what we got and displays a 
	percent error."""
	output =[0.0,0.0,0.0]
	for x in range(0,3):
		a = actual[x]
		b = expected[x]
		output[x] = ((b-a)/float(b)) * 100
	print "\tPercent Error: ", output
	return output
    
if __name__ == '__main__':
	unittest.main()