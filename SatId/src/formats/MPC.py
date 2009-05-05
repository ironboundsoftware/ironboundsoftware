'''
Created on May 5, 2009

@author: nick.loadholtes

5/5/2009: Based on the information at: http://www.cfa.harvard.edu/iau/info/OpticalObs.html

'''

class MPC:
	'''
	This class represents an MPC observation. Not all fields in this class are used at once,
	depending on the type of observed object, some will be blank. 
	'''
	#Minor Planets
	identifier = None
	provisional = None
	discovery = None
	orbitType = None
	satIdentifier = None
	note1 = None
	note2 = None
	dateOfObservation = None
	ra = None
	decl = None
	magnitude = None
	observatory = None	
	

	def __init__(selfparams):
		'''
		Constructor
		'''
	
def parse(obs):
	""" This method examines a string, and if it can parse an observation
	out of it, it returns a MPC object. Otherwise you get None."""
	mpc = None
	
	return mpc
	
	
	