#!/usr/bin/env python
'''slidepuzzle.py

        A sliding puzzle game
        by Nick Loadholtes

        No warranty provided with this code. Use at your own risk.

        version 1.3
'''

import random, cmath, curses, curses.wrapper, curses.ascii

side = "|"
newline = "\n"
_topborder = "_"
topb = ""
newscreen = "\n\n\n\n\n\n\n\n\n"
actual = []
size = 3
keypress = ""
stdscr = ""
gameinplay = 1
gamewon = 0
spacelocation = 0

def makeTopBorder():
        sizeofboard = (size * 3) +1
        pos = 0
        global topb
        topb = ""
        while pos < sizeofboard:
                topb += _topborder
                pos += 1

# 
#works
def displayBoard():
        global stdscr, actual
        sizeofboard = (size * size) -1
        y = 0
        x = 0
        number = 0
        output = newline + topb + newline
        while y < size:
                while x < size:
                        if(number < len(actual)):
                                output += side + "%(#)2s" % {"#":str(actual[number])}
                                number += 1
                                x += 1
                        else :
                                break

                output += newline + topb + newline
                x = 0
                y += 1

        stdscr.clear()
        curses.init_pair(3, 7, 4)
        stdscr.addstr(0, 0, output, curses.color_pair(3))
        stdscr.refresh()

#
# Returns a "random" number from the range of size^2
def getNumberFromRange():
        return random.randrange(1, (size * size) )

#
# Generates a randomized board 
def generateBoard():
        global actual, spacelocation
        sizeofboard = (size * size)
        x = 0
        actual = []
        while x < sizeofboard -1:
                num = getNumberFromRange()
                while checkBoard(num) != 0:
                        num = getNumberFromRange()
                actual.append(num)
                x += 1
        actual.append(" ")
        spacelocation = sizeofboard - 1

#
# 
def checkBoard(num):
        for x in actual:
                if x == num:
                        return 1
        return 0

#
# Checks to see if there is a win condition
def checkForWin():
        global size, actual, gameinplay, stdscr, gamewon
        sizeofboard = (size * size) - 1
        broken = 0
        if( (actual[sizeofboard])  == " "):
                y = 1
                for x in actual:
                    if(x != y):
                        if(x != " "):
                            broken = 1
                            break
                    y = y + 1
                if (broken == 0):
                    gameinplay = 0
                    gamewon = 1


#
# Request a size from  the user. Size can be 1-9 (but
# should be 2-9)
def getSize():
        global size, stdscr
        msg = "\nThe default size is " + str(size) + "\nWhat size board would you like?"
        size = "a"
        while (not curses.ascii.isdigit(size) ):
                  stdscr.addstr(msg)
                  stdscr.refresh()
                  size = stdscr.getch()
        size = size- 48

#
# Get the user input (during the game) and either quit or
# attempt to move the space.
def getInput():
        global keypress, stdscr, gameinplay
        stdscr.addstr("Press an arrow key to move the space (q to quit)?")
        stdscr.refresh()
        keypress = stdscr.getch()
        if(keypress == curses.KEY_UP):
                doMovement(2)
        elif(keypress == curses.KEY_DOWN):
                doMovement(1)
        elif(keypress == curses.KEY_LEFT):
                doMovement(4)
        elif(keypress == curses.KEY_RIGHT):
                doMovement(3)
        elif(keypress == 81 or keypress ==113):
                gameinplay = 0
        stdscr.refresh()

#
# Attempt to move the space. If it can't be move, nothing
# happens and the game loop re-prompts for a move.
def doMovement(direction):
        global actual, spacelocation, size, stdscr
        row = spacelocation / size
        if(direction == 1):
                newlocation = spacelocation + size
        elif(direction == 2):
                newlocation = spacelocation - size
        elif(direction == 3):
                newlocation = spacelocation + 1
                newrow = newlocation / size
                if(newrow != row):
                        newlocation -= 1
        elif(direction == 4):
                newlocation = spacelocation - 1
                newrow = newlocation / size
                if(newrow != row):
                        newlocation += 1
        if(newlocation > -1 and newlocation < (size*size)):
                tmp = actual[newlocation]
                actual[spacelocation] = tmp
                actual[newlocation] = " "
                spacelocation = newlocation

#
# The main loop of the game.
def gameLoop(screen):
        global stdscr, gameinplay, gamewon
        curses.echo()
        stdscr = screen
        stillplaying = 1
        while stillplaying :
                gameinplay = 1
                getSize()
                generateBoard()
                makeTopBorder()
                while gameinplay:
                        displayBoard()
                        getInput()
                        checkForWin()
                        if gamewon:
                            displayBoard()
                            stdscr.addstr("\n\n\t\tYOU WON!!!!!!!!!\n\n")
                            stdscr.refresh()
                stdscr.addstr("\nWould you like to play another game? (y to continue): ")
                stdscr.refresh()
                stillplaying = stdscr.getch()
                if(stillplaying == 89 or stillplaying == 121): # Q or q
                        stillplaying = 1
                else:
                        stillplaying = 0

#
# The main method to start the game.
if __name__ == "__main__":
        print "Welcome to the slide puzzle!\n"
        curses.wrapper(gameLoop)
        print "Good bye!"