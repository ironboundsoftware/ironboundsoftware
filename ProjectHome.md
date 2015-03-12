This is the code that Iron Bound Software is making available to the public. Before this was scattered about all over the internet, now its all in one nice spot. All of this code is provided as is, no promises on anything working. Use at your own risk.

Basically there are two things: graphing and utilities.

Graphing:
Some utilities I've been working on to do graphing in python.

Right now there are two main things: clouds and networks.

The clouds source directory contains some code to read text, count words, and then print out an HTML cloud of the words (words are sized logarithmically). Read the comments in the source code for the full details. More or less, this project is done.

The networks source directory contains an attempt to draw a network diagram based on the relationships in a file. (The format is: 1 2) This project is not done, and is being worked on.

Misc:
  * mp3tagger.py - This is a quick and dirty little program to update the ID3 tags in your music directory. If a file is missing the artist and album info, this file will parse the directory path and plug in the right values. See the code for more documentation.
  * gui.py,tester.py,story2.txt - This is a GUI app I wrote to see what is involved in writing a Tkinter program. This program is used to build a basic script for the game engine I'm working on. The tester.py program runs the script in a 'Choose-Your-Own-Adventure' style game. Story2.txt is the test script called 'The house of two rooms'. Enjoy!
  * slidepuzzle.py - Version 1.3 - This is a simple curses (i.e. text based) python implementation of the sliding puzzle game (also known as a NxN puzzle). You pick a number from 2 to 9 and it will draw up a random board with a space missing. You move the space around by pressing the arrow key of the direction you want the space to move. When the numbers are all in order, the puzzle is solved. This version does the check for a win. So now if you are a winner, the program will let you know.
  * coinflip.py - A quick experiment in seeing if a 1000 coin flips results in a 50-50 distribution of heads and tails.
  * mpgmaker.py - A Python version of a program that makes MPEG's out of JPG's
  * tail.py - A tail program written in python for use on systems that don't have the tail utility (i.e. Windows). Based on code from the cookbook
  * thumbnailer.py - A program I wrote to walk the directory tree, find jpg's, create a thumbnail version and a 800x600 version, and then create a HTML page that lists all of the thumbnail images (with links to the 800x600 version). I wrote this to help organize a couple of directories that had over 500 digital camera photos.



