'''
Created on May 12, 2009

@author: nick.loadholtes
'''
import re
#from ..import SatId 
import SatId

class TLE:
	'''
	This class holds the data associated with a Two Line Element (TLE) description
	of a satellite orbit.
	
	Note: The checksums are not currently checked/computed.
	'''
#	print dir(SatId)
	#temp vars
#	xmnpda = SatId.minutes_per_day
#	temp = SatId.twopi/xmnpda/xmnpda
	#line 0
	name = ""
	#common to line 1 & 2
	objectId = ""
	intDesgination = ""
	classification = ""
	#line 1
	elementSetEpoch = 0.0
	firstDeriv = 0.0
	secondDeriv = 0.0
	bStarDrag = 0.0
	elementSetType = 0
	elementNumber = 0
	#line 2
	inclination = 0.0 #Declination?
	ra = 0.0
	eccentricity = 0.000001 #Can't have eccentricity of 0?
	perigee = 0.0
	anomaly = 0.0
	meanMotion = 1.0 # rev per day, default to 1 to prevent divide-by-zero
	revolutions = 0 # At Epoch
	
	def __init__(selfparams):
		'''
		Constructor
		'''
	
def parseTLE(buffer):
	"""Read in as many TLE items as we can... """
	if not buffer:
		return None
	lines = buffer.splitlines()
	x = 0
	output = []
	tle = None
	while x < len(lines):
		# print "\tLooking at " + lines[x]
		line = lines[x]
		firstchar = line[0]
		if "#" == firstchar:
			pass
			# print "Comment:" + line
		if "1" == firstchar:
			# print "New TLE"
			tle = parseLine1(tle, line)
		if "2" == firstchar:
			if tle:
				# print "Add to the TLE"
				output.append(parseLine2(tle, line))
				print tle
				tle = None
		x += 1		
	return output
	
def parseLine1(tle, line):
	"""Parse out the first line of the TLE"""
	tle = TLE()
	tle.classification = line[7]
	tle.intDesgination = line[9:17]
	tle.elementSetEpoch = float(line[18:32])
	tle.firstDeriv = float(line[33:43])
	tle.secondDeriv = (float(line[44:50])/100000.0) * (10.0**int(line[50:52]))
	tle.bStarDrag = (float(line[53:59])/100000.0) * (10.0**int(line[59:61]))
	tle.elementSetType = line[62]
	tle.elementNumber = int(line[64:68])
	return tle
	
def parseLine2(tle, line):
	"""Parse out the second line of the TLE"""
	#line 2
	tle.objectId = line[2:7]
	tle.inclination = float(line[8:16])# * SatId.radians_per_degree
	tle.ra = float(line[17:25]) #* SatId.radians_per_degree
	tle.eccentricity = float("0."+line[26:33]) 
	tle.perigee = float(line[34:42]) #* SatId.radians_per_degree
	tle.anomaly = float(line[43:51]) #* SatId.radians_per_degree
	tle.meanMotion = float(line[52:63])
	tle.revolutions = int(line[63:68])

	#Fixup
#		tle.meanMotion *= TLE.temp * TLE.xmnpda
#		tle.firstDeriv *= TLE.temp
#		tle.secondDeriv *= TLE.temp/TLE.xmnpda

	
	
