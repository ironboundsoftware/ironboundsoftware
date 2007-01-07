#
# SNAplot.py
#
# Methods to plot out networks from a SNA perspective
#
# Aug 29, 2006
# Nick Loadholtes nick@ironboundsoftware.com
#
# Released under the MIT license
#

import wx
from EdgeHog import *
from NodeOrganizer import *

class SNAPlot(wx.Window):
	def __init__(self, parent, id, size, title):
		wx.Window.__init__(self, parent, id, wx.Point(0,0), size, style=wx.NO_FULL_REPAINT_ON_RESIZE)
		self.SetBackgroundColour("WHITE")
		self.thickness = 1

		self.buffer = wx.EmptyBitmap(max(1,size.width), max(1,size.height))
		dc = wx.BufferedDC(None, self.buffer)
		dc.SetBackground(wx.Brush(self.GetBackgroundColour()))

		self.buffer = wx.EmptyBitmap(max(1,size.width), max(1,size.height))
		dc = wx.BufferedDC(None, self.buffer)
		dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
		dc.Clear()
		
		self.eh = EdgeHog()
		self.eh.parseEdgeFile('data/edges_small.txt')
		self.nodeorganizer = NodeOrganizer(size)		
		self.nodeorganizer.setNodeData(self.eh.getNodes(), self.eh.getAuthRankings())

		self.InitBuffer()

		# Event Bindings
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_IDLE, self.OnIdle)
		self.Bind(wx.EVT_CLOSE, self.OnQuit)
		print self.GetClientSize()
		
	def InitBuffer(self):
		"""Initialize the bitmap used for buffering the display."""
		size = self.GetClientSize()

		self.buffer = wx.EmptyBitmap(max(1,size.width), max(1,size.height))
		dc = wx.BufferedDC(None, self.buffer)
		dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
		dc.Clear()
		
		#
		# Initialize
		#
		self.nodeorganizer.changeScreenSize(size)
		self.drawDebugRings(dc)		
		self.drawLine(dc)
		self.drawNode(dc)

		self.reInitBuffer = False
		
				
	def OnSize(self, event):
		"""
		Called when the window is resized.  We set a flag so the idle
		handler will resize the buffer.
		"""
		self.reInitBuffer = True


	def OnIdle(self, event):
		"""
		If the size was changed then resize the bitmap used for double
		buffering to match the window size.  We do it in Idle time so
		there is only one refresh after resizing is done, not lots while
		it is happening.
		"""
		if self.reInitBuffer:
			self.InitBuffer()
			self.Refresh(False)
			
	def OnPaint(self, event):
		"""
		Called when the window is exposed.
		"""
		# Create a buffered paint DC.  It will create the real
		# wx.PaintDC and then blit the bitmap to it when dc is
		# deleted.  Since we don't need to draw anything else
		# here that's all there is to it.
		dc = wx.BufferedPaintDC(self, self.buffer)		

	def drawLine(self, dc):
		'''This draws the edges of the graph, connecting the nodes to 
		each other.'''
		dc.BeginDrawing()
		pen = wx.Pen('Black', 1, wx.SOLID)
		dc.SetPen(pen)
		line = ((0, 0, 300,100), (5, 0, 110,110), (10, 40, 120,120), (15, 0, 130, 130))
		center = self.GetClientSize()
		center = (center[0]/2, center[1]/2)
		nodelist = self.nodeorganizer.getStarPattern()
		print nodelist
		for node in nodelist:
			#For each node, get the other nodes it is connected to
			center = node[0]
			#print center
			others = {}
			others = self.eh.getNodes()
			print "Others:", others
			print "Node:", node
			for other in others:
				location = None
				otherlist = others[other]
				print "\tOther is:", other, "Otherlist is:",otherlist
				if other == node[3]:
					for y in otherlist:
						location = None
						for z in nodelist:
							if y == z[3]:
								location = z[0]
								print "\t\tY is ", y, "Nodeitem is", z, "location", location, "center", center
								place = ((center[0], center[1], location[0], location[1]))
								dc.DrawLine(*place)
								break
		dc.EndDrawing()
		
	def drawNode(self, dc):
		'''This draws the nodes on the screen'''
		dc.BeginDrawing()
		pen = wx.Pen('Red', 3, wx.SOLID)
		dc.SetPen(pen)
		nodelist = self.nodeorganizer.getStarPattern()
		for node in nodelist:
			location = node[0]
			diameter = node[1]
			auth = node[2]
			dc.DrawCircle(location[0], location[1], diameter)
		dc.EndDrawing()
		
	def drawDebugRings(self, dc):
		'''This method draws the rings that represent the regions where a node
		could be. '''
		dc.BeginDrawing()
		pen = wx.Pen('Green', 3, wx.LONG_DASH)
		dc.SetPen(pen)
		center = self.GetClientSize()
		rings = self.nodeorganizer.rings
		separation = self.nodeorganizer.separation
		ring = rings
		while ring > 0:
			dc.DrawCircle(center.width/2, center.height/2, separation[0] * ring )
			ring -= 1
		dc.EndDrawing()
				  
	def OnQuit(self, event):
		self.Destroy()

if __name__ == '__main__':
  app = wx.PySimpleApp()
  win = wx.Frame(None, 0, 'Blah', size=(1024,768))
  plot = SNAPlot(win, -1, wx.Size(1024, 768), 'blah')
  win.Show(True)
  app.MainLoop()
