#!/usr/bin/env python
#
# visitor.py
# Nick Loadholtes nick@ironboundsoftware.com
# May 9, 2007
#
# This is a quick file to show how to use the visitor pattern
# to execute commands based off of the input from a text file.
#

class Visitor:
	"""This is the interface for the Visitor pattern"""
	def visit(self):
		print "In Visitor.visit()"		

class Rule(Visitor):
	"""This is an example of a buisness rule using the visitor
	pattern/class"""
	msg = ""
	
	def __init__(self, msg):
		"""Set the message """
		self.msg = msg
		
	def visit(self):
		print "In Rule.visit():", self.msg
		
class DynaRule(Visitor):
	"""This class will take in some input and execute it if it can"""
	cmd = ""
	params = []
	def __init__(self, cmd, params):
		self.cmd = cmd
		self.params = params

	def visit(self):
		"""This methos will execute the rule using the """
		args = "("
		for param in self.params:
			args += param + ","
		args = args[:-1]+")"
		try:
			f = self.cmd + args
			eval(f)
		except Exception, e:
			print "Exception thrown: ",e
		
class RuleEngine:
	"""This engine will execute the rules that are added to it."""
	rules = []
	def __init__(self):
		"""Initilizes the rules"""
		self.rules = []
		
	def accept(self, rule):
		"""Add a rule!"""
		self.rules.append(rule)
		
	def process(self):
		"""This is where the rules are actually executed"""
		for rule in self.rules:
			rule.visit()

#
# Some rules
def sum(a,b):
	print "Sum of",a,"and",b,"is", (a+b)	