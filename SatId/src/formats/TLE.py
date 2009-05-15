'''
Created on May 12, 2009

@author: nick.loadholtes
'''
import re
from SatId import *

class TLE(object):
	'''
	This class holds the data associated with a Two Line Element (TLE) description
	of a satellite orbit.
	
	Note: The checksums are not currently checked/computed.
	'''
	#line 0
	name = ""
	#common to line 1 & 2
	objectId = ""
	intDesgination = ""
	classification = ""
	#line 1
	elementSetEpoch = 0.0
	firstDeriv = 0.0
	secondDeriv = ""
	bStarDrag = ""
	elementSetType = 0
	elementNumber = 0
	#line 2
	inclination = 0.0 #Declination?
	ra = 0.0
	eccentricity = 0
	perigee = 0.0
	anomaly = 0.0
	meanMotion = 0.0 # rev per day
	revolutions = 0 # At Epoch
	


	def __init__(selfparams):
		'''
		Constructor
		'''
	
def parseTLE(buffer):
	"""Read in as many TLE items as we can... """
	if not buffer:
		return None
	lines = re.split('\n', buffer)
	tle = TLE()
	x = 0
	while x < len(lines)-1:
		line = lines[x]
		tle.name = line[:24]
		#line 1
		x += 1
		line = lines[x]
		tle.classification = line[7]
		tle.intDesgination = line[9:17]
		tle.elementSetEpoch = float(line[18:32])
		tle.firstDeriv = float(line[33:43])
		tle.secondDeriv = (float(line[44:50])/100000.0) * (10.0**int(line[50:52]))
		tle.bStarDrag = (float(line[53:59])/100000.0) * (10.0**int(line[59:61]))
		tle.elementSetType = line[62]
		tle.elementNumber = int(line[64:68])
		
		#line 2
		x += 1
		line = lines[x]
		tle.objectId = line[2:7]
		tle.inclination = float(line[8:16])
		tle.ra = float(line[17:25])
		tle.eccentricity = float("0."+line[26:33])
		tle.perigee = float(line[34:42])
		tle.anomaly = float(line[43:51])
		tle.meanMotion = float(line[52:63])
		tle.revolutions = int(line[63:68])	
	return tle
	
	
	
	
	
	
	
