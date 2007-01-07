#
# NodeOrganizer.py
#
# Given a list of nodes from EdgeHog, this will organize them
# in a manner suitable for being drawn.
#
# Sept 19, 2006
# Nick Loadholtes nick@ironboundsoftware.com
#
# Released under the MIT license
#

import math, random
		
class NodeOrganizer:
	def __init__(self, size):
		#print "Organizing the Nodes"
		self.size = size
		self.theta = random.randint(1, 360) * (math.pi/180)
		
	def setNodeData(self, nodes, authlist):
		'''Use this method to set the data that will be displayed.'''
		self.nodes = nodes
		self.authlist = authlist
		self.starpattern = None
		center = self.size[0]/2, self.size[1]/2
		hseparation = center[0]/len(self.nodes)
		vseparation = center[1]/len(self.nodes)
		self.separation = (hseparation, vseparation)
		self.rings = 4
				
	def changeScreenSize(self, size):
		'''In case the screen gets resized, this way we can draw the picture
		to take that into account. Gotta blank out the star pattern so it can
		be redrawn correctly.'''
		self.size = size
		self.starpattern = None
		
	def generateStar(self):
		'''Generates a star-like pattern with the most authoritative node
		at the center of the other nodes.
		
		Returns a list of lists. Each inner list consists of
		
		1) The center of the node on the screen
		2) Its diameter
		3) Authoritativeness (0 being the highest, >0 being less authoritative)'
		4) The orignial node (so it can be looked up)
		
		Do Not call this method directly, only getStarPattern() should call this.'''
		output = []
		rankings = {}
		for node in self.authlist:
			nodecount = self.authlist.get(node)
			nodes = rankings.get(nodecount)
			if nodes == None:
				nodes = []
			nodes.append(node)
			rankings[nodecount] = nodes
		#
		# Determine the spatial separation based off of the number of nodes
		# and the size of the screen.
		#
		center = self.size[0]/2, self.size[1]/2
		hseparation = center[0]/len(self.nodes)
		vseparation = center[1]/len(self.nodes)
		self.separation = (hseparation, vseparation)
		#radius = math.sqrt(hseparation**2 + vseparation**2) 
		radius = min((hseparation, vseparation))
		diameter = radius/4
		#print rankings
		rank = 0
		ring = 1
		for i in reversed(sorted(rankings.keys())):
			nodes = rankings[i]
			nodesperspace = len(nodes)
			innerrank = 1
			for node in nodes:
				data = []
				print node
				if ring == 0:
					data.append((center[0], center[1] ))
				else:
					# Get a polar position, then convert it to cartesian
					x = int(radius * math.cos( ((self.theta * innerrank) + innerrank) / (ring + 1) ))
					y = int(radius * math.sin( ((self.theta * innerrank)  + innerrank) / (ring + 1) ))
					data.append((center[0] + (ring * x), center[1] + (ring * y)))
				data.append(diameter / (rank + 1))
				data.append(rank)
				data.append(node)
				output.append(data)
				innerrank += 1
			ring += 1
			rank += 1
		self.rings = ring
		return output
	
	def getStarPattern(self):
		'''Since the generateStar() method uses a random function to plot the
		location of the nodes, it is not a good idea to call it more than once per session
		otherwise it will mangle the nodes location everytime (plus screw up the edges).
		
		This method acts as a getter for the star pattern. You should not call generateStar()
		directly. Let this method handle that.'''
		if self.starpattern == None:
			self.starpattern = self.generateStar()
		return self.starpattern
		
		
	def generateClusters(self):
		''''Organizes the nodes into clusters so that the community formed by the
		nodes is more apparent than it might be in the Star configuration.
		
		Returns a list of lists. Each inner list consists of
		
		1) The center of the node on the screen
		2) Its diameter
		3) Authoritativeness (0 being the highest, >0 being less authoritative)'''
		output = []
		
		return output
	
if __name__ == '__main__':
	no = NodeOrganizer((800, 600))
	no.setNodeData({'1': ['2', '3', '4', '5'], '3': ['1', '4', '5'], '2': ['1', '3'], '5': ['3'], '4': ['1']},  {'1': 3, '3': 3, '2': 1, '5': 2, '4': 2})
	for x in range(1, 10):
		print no.getStarPattern()



