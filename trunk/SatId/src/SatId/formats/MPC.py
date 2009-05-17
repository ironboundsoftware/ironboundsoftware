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
	
def parseMPC(obs):
	""" This method examines a string, and if it can parse an observation
	out of it, it returns a MPC object. Otherwise you get None."""
	if not obs:
		return None
	if len(obs) < 80:
		return None
	mpc = MPC()
	mpc.observatory = obs[77:80]
	mpc.magnitude = obs[66:71]
	mpc.decl = obs[44:56]
	mpc.ra = obs[32:44]
	mpc.dateOfObservation = obs[15:32]
	mpc.note2 = obs[14]
	mpc.note1 = obs[13]
	return mpc
	
	
	