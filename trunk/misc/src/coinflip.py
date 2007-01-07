#!/usr/bin/env python
#
#       coinflip.py
#       by Nick Loadholtes
#       5/12/2004
#
#       A simulation to flip coins. Please don't use this for anything other
# than simple amusement. I have no idea how good (or bad) the python
# random number generator is.
#

import random

def flipcoin(numtoss):
        x = 0;
        heads = 0;
        tails = 0;
        while(x<numtoss):
                num =  random.randrange(1, 100000000)
                if(num % 2 == 0):
                        heads = heads + 1
                else:
                        tails = tails + 1
                x = x +1

        print "Heads= "+str(heads)+ " Tails= "+ str(tails)

        return 0

if __name__ == "__main__":
        print "Are you ready to flip some coins?"
        num = input("How many flips you would you like to do (0 to quit)? ")
        while(num != 0):
                flipcoin(num)
                num = input("How many flips you would you like to do (0 to quit)? ")