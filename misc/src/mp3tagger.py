#!/usr/bin/python
#
# mp3tagger.py
#       Walks the directory tree, finds MP3's, updates the mp3tags if they are blank.
# Tested and worked fine for me, use at your own risk.
#
#       Nick Loadholtes 6/1/2005
#

from tagger import *

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


def tag(file):
        ''' This function looks at an mp3 file that is passed in and
determines if it is missing the artist and album fields. If it is, it
parses the path that leads to the file, assuming the path is
Artist->Album->Song. It then plugs in the Artist and Album data to the
ID3 tag in the mp3. This was written to help correct my mp3 library which
iTunes was chocking on because there were a lot of missing tags. This
function has had minimal testing, use at your own risk.

        This function uses the pytagger library from 
http://www.liquidx.net/pytagger/ which is a very cool python implementation
of ID3 tagging stuff. Check it out!'''
        print "file: ", file
        mp3_tag = ID3v2(file)
        if(mp3_tag.tag_exists):
                mp3_tag.parse_frames()
                for frame in mp3_tag.frames:
                        print "=>", frame.fid,  "->", str(frame.strings)
                        pass
                if(mp3_tag.frames == [] ):
                        import string
                        flds = (str(file)).split('/')
                        artist_frame = mp3_tag.new_frame('TPE1')
                        artist_frame.set_text(flds[0])
                        mp3_tag.frames.append(artist_frame)
                        album_frame = mp3_tag.new_frame('TALB')
                        album_frame.set_text(flds[1])
                        mp3_tag.frames.append(album_frame)
                        mp3_tag.commit() # This saves the tag data to the mp3 file
                        print file
        else:
                print "No mp3 tag data"


if __name__ == "__main__":
                files = Walk('.', 1, '*.mp3', 0)
                for file in files:
                        tag(file)