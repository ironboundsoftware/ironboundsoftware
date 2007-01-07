#!/usr/bin/env python
'''
        tail.py

        Nick Loadholtes
        May 20, 2004
        based off of code from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/157035
        
        This is a program to tail a file. Intended to be used somewhere
        where the normal unix tail command is not available (i.e. Windows)
        '''

import time, os, sys

def tailfile(filename):
        #open the file
        file = open(filename,'r')

        #Find the size of the file and move to the end
        st_results = os.stat(filename)
        st_size = st_results[6]
        file.seek(st_size)

        while 1:
                where = file.tell()
                line = file.readline()
                if not line:
                        time.sleep(1)
                        file.seek(where)
                else:
                        print line, # already has newline

if __name__ == "__main__":
        try:
                if(sys.argv[1]):
                        try:
                                tailfile(sys.argv[1])
                        except KeyboardInterrupt:
                                print
        except IndexError:
                print "Usage: python tail.py <file_you_want_to_tail>"
