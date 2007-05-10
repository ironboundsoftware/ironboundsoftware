#!/usr/bin/env python
#
# tester.py
# Nick Loadholtes nick@ironboundsoftware.com
# May 9, 2007
#
# A tester for the visitor.py file
#

from visitor import *

re = RuleEngine()

r1 = Rule("test1")
r2 = Rule("test2")

re.accept(r1)
re.accept(r2)

re.process()

#
# Now to test command execution
re = RuleEngine()

f = open("data.txt")
for line in f:
	cmds = line.strip().split(" ")
	rule = DynaRule(cmds[0], cmds[1:])
	re.accept(rule)
	print "Commands from file: ", cmds

re.process()