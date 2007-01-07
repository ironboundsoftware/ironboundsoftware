 #!/usr/bin/python
 
 # plot.py

import wx
import wx.lib.plot as plot
from datareader import *

class StockPlot(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(180, 280))
        #self.data = [(1,2), (2,3), (3,5), (4,6), (5,8), (6,8), (10,10)]
        self.setData(readFromCSVFile('data/xom.csv'))
        btn1 = wx.Button(self,  1, 'scatter', (50,50))
        btn2 = wx.Button(self,  2, 'line', (50,90))
        btn3 = wx.Button(self,  3, 'bar', (50,130))
        btn4 = wx.Button(self,  4, 'quit', (50,170))
  
        wx.EVT_BUTTON(self, 1, self.OnScatter)
        wx.EVT_BUTTON(self, 2, self.OnLine)
        wx.EVT_BUTTON(self, 3, self.OnBar)
        wx.EVT_BUTTON(self, 4, self.OnQuit)
        wx.EVT_CLOSE(self, self.OnQuit)

    def OnScatter(self, event):
        frm = wx.Frame(self, -1, 'scatter', size=(1024, 768))
        client = plot.PlotCanvas(frm)
        markers = plot.PolyMarker(self.data, legend='', colour='pink', marker='triangle_down', size=1)
        gc = plot.PlotGraphics([markers], 'Scatter Graph', 'X Axis', 'Y Axis')
        client.Draw(gc, xAxis=(self.min_x, self.max_x), yAxis=(self.min_y, self.max_y))
        frm.Show(True)
  
    def OnLine(self, event):
        frm = wx.Frame(self, -1, 'line', size=(1024, 768))
        client = plot.PlotCanvas(frm)
        line = plot.PolyLine(self.data, legend='', colour='pink', width=1)
        monthline = plot.PolyLine(self.month, legend='', colour='green', width=1)
        #weekline =  plot.PolyLine(self.week, legend='', colour='red', width=1)
        gc = plot.PlotGraphics([line, monthline], 'Line Graph', 'X Axis', 'Y Axis')
        client.Draw(gc,  xAxis=(self.min_x, self.max_x), yAxis=(self.min_y, self.max_y))
        frm.Show(True)
  
    def OnBar(self, event):
        frm = wx.Frame(self, -1, 'bar', size=(600,450))
        client = plot.PlotCanvas(frm)
        bar1 = plot.PolyLine([(1, 0), (1,5)], legend='', colour='gray', width=25)
        bar2 = plot.PolyLine([(3, 0), (3,8)], legend='', colour='gray', width=25)
        bar3 = plot.PolyLine([(5, 0), (5,12)], legend='', colour='gray', width=25)
        bar4 = plot.PolyLine([(6, 0), (6,2)], legend='', colour='gray', width=25)
        gc = plot.PlotGraphics([bar1, bar2, bar3, bar4],'Bar Graph', 'X Axis', 'Y Axis')
        client.Draw(gc, xAxis=(0,15), yAxis=(0,15))
        frm.Show(True)
  
    def OnQuit(self, event):
        self.Destroy()
        
    def setData(self, input):
        tmp, self.max_y, self.min_y, self.max_x, self.min_x = input
        print len(tmp)
        self.data = []
        self.week = []
        self.month = []
        self.year = []
        if (len(tmp)/260) > 10: # there's about 260 trading days per year
            for x in range(0, len(tmp), 4): #This is a per-week view
                self.week.append(tmp[x])
            for x in range(0, len(tmp), 20): # This is the per-month view
                self.month.append(tmp[x])
            for x in range(0, len(tmp), 260): #This is the per  year view
                self.year.append(tmp[x])
            self.data = self.year
            print len(self.data)
            print "Lots of data!"
  
class MyApp(wx.App):
    def OnInit(self):
        dlg = StockPlot(None, -1, 'plot.py')
        dlg.Show(True)
        dlg.Centre()
        return True
  
app = MyApp(0)
app.MainLoop()