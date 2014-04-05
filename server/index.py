#!/usr/bin/env python

import os
import sys
from time import time
import psycopg2
from psycopg2.extensions import register_adapter
import Image
from config import COVERART_DIR
import cube

register_adapter(cube.Cube, cube.adapt_cube)

COLORS_PER_BIN = 8

class ColorIndex(object):
    def __init__(self):
        self.conn = psycopg2.connect("dbname=mcoverart user=mcoverart")
        self.index = {}

    def load_index(self):
        cur = self.conn.cursor()
        query = """SELECT red, green, blue, mbid FROM color_index"""
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            self.index["%s,%s,%s" % (row[0], row[1], row[2])] = row[3]
        print "loaded %d rows into color index" % len(self.index.keys())

    def lookup_color(self, red, green, blue):
        red = (red / COLORS_PER_BIN) * COLORS_PER_BIN
        green = (green / COLORS_PER_BIN) * COLORS_PER_BIN
        blue = (blue / COLORS_PER_BIN) * COLORS_PER_BIN
        try:
            return self.index["%d,%d,%d" % (red, green, blue)]
        except KeyError:
            return ""

    def make_index(self):
        cur = self.conn.cursor()
        for r in xrange(256 / COLORS_PER_BIN):
            for g in xrange(256 / COLORS_PER_BIN):
                for b in xrange(256 / COLORS_PER_BIN):
                    red = r * COLORS_PER_BIN
                    green = g * COLORS_PER_BIN
                    blue = b * COLORS_PER_BIN
                    mbid = self._k_lookup_color(red, green, blue)
                    cur.execute("""INSERT INTO color_index (red, green, blue, mbid) 
                                   VALUES (%s, %s, %s, %s)""", (red, green, blue, mbid))
                    print "%d,%d,%d: %s" % (red, green, blue, mbid)
                self.conn.commit()

    def _k_lookup_color(self, red, green, blue):
        cur = self.conn.cursor()

        query = """SELECT mbid
                     FROM release
                 ORDER BY cube_distance(color, %s) 
                    LIMIT 1"""

        cur.execute(query, (cube.Cube(red, green, blue),))
        row = cur.fetchall()
        return row[0][0]

if __name__ == "__main__":
    ci = ColorIndex()                
    ci.make_index()
