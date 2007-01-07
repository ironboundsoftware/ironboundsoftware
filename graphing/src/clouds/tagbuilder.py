#
# tagbuilder.py
#
# Methods to gather up text and build a resulting tag cloud.
#
# Nick Loadholtes nick@ironboundsoftware.com
# Sep 1, 2006
#
# Released under the MIT license
#

from tagclouds import *
import sys, os

link = 'http://www.google.com/search?q='

if len(sys.argv) > 2 and sys.argv[2] != None:
	link = sys.argv[2]
	
for root, dirs, files in os.walk(sys.argv[1]):
    print root, dirs, files
    for file in files:
        createTagCloud(root + '/' + file, link)
        
writeOutputFile(sys.argv[1])
