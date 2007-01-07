#!/usr/bin/env python
#
#       Creates an MPG from a bunch of jpgs
#
#       Based off of a perl version by Stephen B. Jenkins (pg 65 Dr. Dobbs Journal, April 2004)
#       Python version:Nick Loadholtes
#       May 5, 2004
#

import time, urllib, os

WAITINTERVAL= 61
LOCATION = 'http://www.jwz.org/webcollage/collage.jpg'
WIN32PATH ="C:\\Program Files\\ImageMagick-6.0.0-Q16\\convert"
LINUXPATH = " "
PATH = WIN32PATH

def gather():
        print "Gathering pictures..."
        while(1):
                (year, month, day, hour, min) = time.localtime()[0:5]
                filename =  "img%d_%d_%d_%d_%d.jpg" % (year,month,day,hour,min)
                print "Getting ", filename
                urllib.urlretrieve(LOCATION, filename)
                time.sleep(WAITINTERVAL)

def generate():
        print "Generating the MPG!"
        (year, month, day, hour, min) = time.localtime()[0:5]
        filename =  "%d_%d_%d_%d_%d.mpg" % (year,month,day,hour,min)
        mpgargs = ("-adjoin", " *.jpg ", filename)
        os.execv(WIN32PATH, mpgargs)

if __name__ == "__main__":
        print "Starting!"
        try:
                gather()
        except KeyboardInterrupt:
                generate()