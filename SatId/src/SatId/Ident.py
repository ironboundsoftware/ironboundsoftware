'''
Created on Aug 2, 2009

@author: njl
'''

import SatId.formats.MPC as MPC

class Identify:
	'''
	This class wraps the following:
	
	1) Load in observations
	2) Load in satellite positions
	3) Compare
	4) Report what's what.
	'''

	def __init__(selfparams):
		'''
		Constructor
		'''
		pass
		
	def loadSatellites(self):
		'''Loads the positional data for the satellites'''
		pass
	
	def loadObservations(self, obs):
		'''Loads the observations'''
		mpcobs = MPC.parseMPC(obs)
		return mpcobs
	
	def analyze(self):
		'''Compare the observations to the satellites to find any potential 
		matches. '''
		pass
	
	def identify(self, obs):
		'''The main entry point'''
		self.loadObservations(obs)
		self.loadSatellites()
		self.analyze()
		