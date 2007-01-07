#!/usr/bin/env python
#
# thumbnailer.py
# 
# A quick and dirty script to walk a directory tree, find jpg's,
# make a thumbnail, and make a 800x600 version. Also makes an
# HTML file to show all of the thumbnails (with links to the
# 800x600 version). Designed to take the high quality pics 
# from digital camera and produce a web friendly version gallery.
#
# by Nick Loadholtes
# Nov 2004
#

import Image
import os

imagelist = []

#
# This function by  Robin Parmar's receipe on the python cookbook:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52664
def Walk( root, recurse=0, pattern='*', return_folders=0 ):
        import fnmatch, os, string

        # initialize
        result = []

        # must have at least root folder
        try:
                names = os.listdir(root)
        except os.error:
                return result

        # expand pattern
        pattern = pattern or '*'
        pat_list = string.splitfields( pattern , ';' )

        # check each file
        for name in names:
                fullname = os.path.normpath(os.path.join(root, name))

                # grab if it matches our pattern and entry type
                for pat in pat_list:
                        if fnmatch.fnmatch(name, pat):
                                if os.path.isfile(fullname) or (return_folders and os.path.isdir(fullname)):
                                        result.append(fullname)
                                continue

                # recursively scan other folders, appending results
                if recurse:
                        if os.path.isdir(fullname) and not os.path.islink(fullname):
                                result = result + Walk( fullname, recurse, pattern, return_folders )

        return result

#
# This function takes a jpg in and creates a thumbnail version and a 800x600 version
# while leaving the original file intact.
def thumbnail(filename):
        global imagelist
        print "Crunching: ", filename
        outfile = os.path.splitext(filename)[0] + ".thumb.jpg"
        outfile2 = os.path.splitext(filename)[0] + ".med_res.jpg"
        print "\tOutfiles: ", outfile, " ", outfile2
        img = Image.open(filename)
        thumbsize = 64,64
        img.thumbnail(thumbsize)
        img.save(outfile, "JPEG")
        img2 = Image.open(filename)
        imgsize = img2.size
        if(imgsize[0] > imgsize[1]):
                size = 800,600
        else:
                size = 600,800
        medimg = img2.resize(size)
        medimg.save(outfile2, "JPEG")

        imagelist.append('<a href=\''+ outfile2+ '\'><img src=\''+outfile+'\'/><br/>'+os.path.splitext(filename)[0]+'</a><br/><br/>\n')



if __name__ == '__main__':
        files = Walk('.', 1, '*.jpg', 0)
        print 'There are %s files below current location:' % len(files)
        for file in files:
                thumbnail(file)
        htmlbuff = '<html><body>\n'
        for line in imagelist:
                htmlbuff += line
        htmlbuff += '</body></html>'
        print htmlbuff
        f = open('index.html', 'w')
        f.write(htmlbuff)
