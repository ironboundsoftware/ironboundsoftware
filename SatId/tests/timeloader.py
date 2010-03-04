#!/usr/bin/env python
#
# timeloader.py
# Loads in the times/positions for the test satellites

import sys
import sqlite3

def main(infile, outfile):
    print "Reading in " + infile+" "+outfile
    fin = open(infile)
    fout = open(outfile, "w+")
    fout.close()
    conn = sqlite3.connect(outfile)
    cur = conn.cursor()
    cur.execute("create table sattimes (id int, satid text, " +
                "t real, x real, y real, z real, x_dot real, y_dot real, z_dot real)")

    lines = fin.read()
    satid = ""
    for line in lines.splitlines():
        tokens = line.split()
        if 2 == len(tokens):
            satid = tokens[0]
            continue
        if None == tokens:
            continue
        tokens = tokens[:7]
        tokens.reverse()
        tokens.append("xx")
        tokens.append(satid)
        tokens.reverse()
        # print tokens
        cur.execute("insert into sattimes values(?,?,?,?,?,?,?,?,?)", tokens)
        # print satid + "-" + str(tokens)
    conn.commit()
    conn.close()
    fin.close()
    
    
    
    
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
