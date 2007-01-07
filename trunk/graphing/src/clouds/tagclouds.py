#
# tagclouds.py
#
# Methods to create tag clouds. Code based on "Building Tag Clouds in Perl and PHP" by Jim Bumgardner
#
# Nick Loadholtes nick@ironboundsoftware.com
# Aug 29, 2006
#
# Released under the MIT license
#

from math import *
import pickle
import re

logcurve = True
maxtagcount = 1
mintagcount = 1000000
tagdict = {}
linkto = ''
removewords = [ 'the', 'and', 'or', 'a', 'if', 'or', 'at', 'as', 'to', 'an', 'then', 'that', 'there', 'is', 'it', 'for', 'in', 'for', 'its', 'i', 'has', 'this', 'of', 'be']

def createTagCloud(filename, link):
	global mintagcount, maxtagcount, tagdict, linkto
	print "Starting createTagCloud for ", filename
	file = open(filename)
	tagfilename = str(filename + '.tags')
	print tagfilename
	#tagfile = open(tagfilename, 'w+')
	linkto = link

	for line in file:
		line = line.lower()
		cleanedline = re.sub("[^a-zA-Z -]", ' ', line)
		#print cleanedline
		words = re.split('\s', cleanedline)
		for word in words:
			w = word.strip()
			if len(w) > 0:
				if not tagdict.has_key(w):
					tagdict[w] = 1				
				tagdict[w] += 1
				#print w
	for banned in removewords:
		if tagdict.has_key(banned):
			del tagdict[banned]
		
	#Find the max and min of the tagdict values
	mintagcount = min(tagdict.values())
	maxtagcount = max(tagdict.values())
	
	#Dump out the tagfile and clean up other files
	#pickle.dump(tagdict, tagfile)
	#tagfile.close()    
	file.close()
	
def writeOutputFile(filename):
	global tagdict, linkto
	# output beginning of tag cloud
	outputfile = open(filename+".html", 'w+')
	outputfile.write('<html><head><link href="mystyle.css" rel="stylesheet" type="text/css"></head><body><div class="cdiv"><p class="cbox">\n')
	
	#Get the keys in a sorted order
	keys = tagdict.keys()
	keys.sort()
	for key in keys:
		outputfile.write("<a href=\""+linkto+key+"\" style=\"font-size:" + str(determineFontSize(tagdict[key]))+"px;\">"+key+"</a> &nbsp;\n")

	## output end of tag file
	outputfile.write("</p></div></body></html>")
	outputfile.close()

def determineFontSize(tagcount):
	global logcurve, mintagcount, maxtagcount
	minlog = log(mintagcount)
	maxlog = log(maxtagcount)
	logrange = 1
	
	if(maxlog != minlog):
		logrange = maxlog - minlog
		
	minfontsize = 8
	maxfontsize = 48
	fontrange = maxfontsize - minfontsize
    
	if logcurve:
		countratio = (log(tagcount)-minlog)/logrange
	else:
		countratio = (tagcount-mintagcount)/(maxtagcount-mintagcount)

	fontsize = minfontsize + fontrange * countratio
	return int(fontsize)


if __name__ == '__main__':
    createTagCloud("test.txt")
    writeOutputFile("test.txt")
    
