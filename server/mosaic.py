#!/usr/bin/env python

import os
import sys
import psycopg2
from psycopg2.extensions import register_adapter
import Image
from config import COVERART_DIR
import cube

register_adapter(cube.Cube, cube.adapt_cube)

class MosaicGenerator(object):
    def __init__(self):
        self.conn = psycopg2.connect("dbname=mcoverart user=mcoverart")

    def lookup_color(self, red, green, blue):
        cur = self.conn.cursor()

        query = """SELECT mbid, deezer_id
                     FROM release
                 ORDER BY cube_distance(color, %s) 
                    LIMIT 1"""

        cur.execute(query, (cube.Cube(red, green, blue),))
        row = cur.fetchall()
        return row[0][0],row[0][1]

    def make_mosaic(self, mbid, image_size, tile_size):
        path = os.path.join(COVERART_DIR, mbid[0:1], mbid[0:2], mbid + ".jpg")
        image = Image.open(path)
        #l = list(i.getdata())
        pixels = image.load()
        width, height = image.size
        pix_per_tile = tile_size * tile_size

        for x_tile in xrange(width / tile_size):
            for y_tile in xrange(height / tile_size):
                avg_r = avg_g = avg_b = 0
                for x in xrange(tile_size):
                    for y in xrange(tile_size):
                        p = pixels[(x_tile * tile_size) + x, (y_tile * tile_size) + y]
                        avg_r += p[0]
                        avg_g += p[1]
                        avg_b += p[2]

                avg_r = int(avg_r / pix_per_tile)
                avg_g = int(avg_g / pix_per_tile)
                avg_b = int(avg_b / pix_per_tile)
                print "(%d, %d, %d)" % (avg_r, avg_g, avg_b)
                mbid, deezer_id = self.lookup_color(avg_r, avg_g, avg_b)
                print mbid
                return
                        
mg = MosaicGenerator()                
mg.make_mosaic("088f0a9a-8519-4742-ad67-be09efca963a", 500, 10)
mg.make_mosaic("083ce005-cb1c-477f-b53e-eb1f44938b53", 500, 10)
