#
# EdgeHog.py
#
# A class to gather up and organize the edges (and implicitly the verticies)
#
# Sept 15, 2006
# Nick Loadholtes nick@ironboundsoftware.com
#
# Released under the MIT license
#

import re

class EdgeHog:
	''' A bit of explanation: There are edges and there are nodes. There are relationships between
	them that are pretty interesting. For example, how many nodes does this node link to? How
	many nodes link to it? To help answer these burning questions, I present these 3 dicts:
	
	nodes = The raw data
	hubnodes = The number of outbound links each node has
	authnodes = The number of links that point to this node
	
	'''
	def __init__(self):
		self.edges = {}
		self.nodes = {}
		self.hubnodes = {}
		self.authnodes = {}
		
	def parseEdgeFile(self, filename):
		f = open(filename, 'r')
		for line in f.readlines():
			l = re.split('[ ]', line.strip())
			nodelist = self.nodes.get(l[0])
			authnodecount = self.authnodes.get(l[1])
			if nodelist == None:
				nodelist = []
			if authnodecount == None:
				authnodecount = 0
			nodelist.append(l[1])
			authnodecount += 1
			self.nodes[l[0]] = nodelist
			self.authnodes[l[1]] = authnodecount
		#print "node=>", self.nodes
		#print "auth->", self.authnodes
		# This will give a reverse mapping to number of links the node has to others
		for node in self.nodes:
			nodelist = self.nodes.get(node)
			hubcount = self.hubnodes.get(len(nodelist))
			if hubcount == None:
				hubcount = []
			hubcount.append(node)
			self.hubnodes[len(nodelist)] = hubcount
		#print self.hubnodes
		
	def getNodes(self):
		'''This returns the node list, and the nodes each one points to.'''
		return self.nodes
	
	def getAuthRankings(self):
		'''This returns the nodes and how many nodes link to them. This is a form
		of ranking that shows how authoritative the node is.'''
		return self.authnodes
			
if __name__ == '__main__':
	eh = EdgeHog()
	eh.parseEdgeFile('data/edges_small.txt')