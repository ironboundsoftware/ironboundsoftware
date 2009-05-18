#!/bin/env python
#
# gui.py
# by Nick Loadholtes
#
# This is a GUI I built to help build script files as 
# an experiment to build a Choose-Your-Own-Adventure
# style game. 
# 
# Use tester.py to run the file generated by this program.
# Use at your own risk, no warranty.

from Tkinter import *
from tkFileDialog import *
import pickle


class CYOAGUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.datafield = ""
        self.namefield = ""
        self.nodes = {} # contains {node id : (node title, node text, (child relationships))
        self.editing = None
        self.counter = -1
        self.loading = False

        self.grid()
        self.createControlWidgets()

    def createControlWidgets(self):
        self.createMenus()
        self.createTextFields()

    def createMenus(self):
        self.MENUBAR = Menu(self.master)
        self.MENUBAR.add_command(label="Open", command=self.fileopen)
        self.MENUBAR.add_command(label="Save", command=self.filecmd)
        self.MENUBAR.add_command(label="Quit", command=self.quitapp)
        self.master.config(menu=self.MENUBAR)

    def createTextFields(self):
        self.NAMEFIELDLABEL = Label(text="Node Title:", justify=LEFT).grid(row=0, column=0)
        self.NAMEFIELD = Text(width=30, height=1)
        self.NAMEFIELD.grid(row=0, column=1)
        self.DATAFIELDLABEL = Label(text="Node Text:", justify=LEFT).grid(row=1, column=0)
        self.DATAFIELD = Text(self.master, width=30, height=5)
        self.DATAFIELD.grid(row=1, column=1)
        self.PARENTLISTLABEL = Label(text="Child Nodes: ", justify=LEFT).grid(row=2, column=0)
        self.PARENTLIST = Listbox(self.master, height=4, width=30, selectmode=EXTENDED)
        self.scrollbar = Scrollbar(self.master, command=self.PARENTLIST.yview)
        self.scrollbar.grid(row=2, column=2, sticky=W+E)
        self.PARENTLIST.bind("<Double-Button-1>", self.loadnode)
        self.PARENTLIST.grid(row=2, column=1)
        self.SAVE = Button(self.master)
        self.SAVE["text"] = "Save"
        self.SAVE["command"] = self.save
        self.SAVE.grid(row=3, column=0)
        self.NEWNODE = Button(self.master)
        self.NEWNODE["text"] = "New Node"
        self.NEWNODE["command"] = self.newnode
        self.NEWNODE.grid(row=3, column=1)
        self.populatefields()

    def populatefields(self):
        self.PARENTLIST.delete(0, END)
        if self.loading == True:
            self.loading = False
        else:
            self.PARENTLIST.insert(END, "The End")
        for item in sorted(self.nodes.keys()):
            node = self.nodes[item]
            print "=>", node
            self.PARENTLIST.insert(END, node[0])
        self.counter = len(self.nodes.keys())

    def newnode(self):
        self.save()
        self.DATAFIELD.delete(0.0, END)
        self.NAMEFIELD.delete(0.0, END)

    def loadnode(self, event):
        selected = self.PARENTLIST.curselection()
        print selected
        if selected == ():
            selected=0
        else:
            selected = selected[0]
        key = self.nodes.keys()[int(selected)-1] #I think this is the only place this is needed
        node = self.nodes.get(key)
        self.NAMEFIELD.delete(0.0, END)
        self.NAMEFIELD.insert(0.0, node[0])
        self.DATAFIELD.delete(0.0, END)
        self.DATAFIELD.insert(0.0, node[1])
        self.editing = key
        self.PARENTLIST.select_clear(selected)
        for i in node[2]:
            self.PARENTLIST.select_set(i)


    def save(self):
        nodetitle = self.NAMEFIELD.get(0.0, END).strip()
        nodetext = self.DATAFIELD.get(0.0, END).strip()
        selected = self.PARENTLIST.curselection()
        print selected
        if selected == ():
            selected=0
        if self.editing != None:
            key = self.editing
            self.editing = None
        else:
            self.PARENTLIST.insert(END, nodetitle)
            self.counter = self.counter + 1
            key = self.counter
        self.nodes[key] = (nodetitle, nodetext, selected)


    def filecmd(self):
        filename = asksaveasfilename()
        if filename:
            f = open(filename, 'w')
            pickle.dump(self.nodes, f)
            f.close()

    def fileopen(self):
        filename = askopenfilename()
        if filename:
            self.loadfile(filename)

    def loadfile(self, filename):
        f = open(filename)
        self.nodes = pickle.load(f)
        f.close()
        self.populatefields()

    def quitapp(self):
        print "nodes: " + str(self.nodes)
        self.quit()


root = Tk()
root.title("Script Builder")
gui = CYOAGUI()
gui.mainloop()