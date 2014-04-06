#!/usr/bin/env python

import os
import sys
from time import time
import psycopg2
from psycopg2.extensions import register_adapter
import Image
from config import COVERART_DIR
import cube
import index
import StringIO

register_adapter(cube.Cube, cube.adapt_cube)

class MosaicGenerator(object):
    def __init__(self, index):
        self.conn = psycopg2.connect("dbname=mcoverart user=mcoverart")
        self.index = index

    def stitch_image(self, mbids, image_size, tile_size):
        mosaic = Image.new("RGB", (image_size, image_size), "black")
        for y, row in enumerate(mbids):
            for x, mbid in enumerate(row):
                path = os.path.join(COVERART_DIR, mbid[0:1], mbid[0:2], mbid + ".jpg")
                image = Image.open(path)
                image = image.resize((tile_size, tile_size))
                mosaic.paste(image, (x * tile_size, y * tile_size, 
                                              (x+1) * tile_size, (y+1) * tile_size))

        io = StringIO.StringIO()
        mosaic.save(io, "jpeg")
        return io
        
    def make_mosaic(self, mbid, image_size, tile_size):
        path = os.path.join(COVERART_DIR, mbid[0:1], mbid[0:2], mbid + ".jpg")
        image = Image.open(path)
        pixels = image.load()
        width, height = image.size

        rows = []
        dest_tiles = int(image_size / tile_size)
        src_tile_size = int(width / dest_tiles)
        pix_per_tile = src_tile_size * src_tile_size
        for y_tile in xrange(image_size / tile_size):
            row = []
            for x_tile in xrange(image_size / tile_size):
                avg_r = avg_g = avg_b = 0
                for x in xrange(src_tile_size):
                    for y in xrange(src_tile_size):
                        try: 
                            p = pixels[min(width - 1, (x_tile * src_tile_size) + x), 
                                       min(height - 1, (y_tile * src_tile_size) + y)]
                        except IndexError:
                            p = [0,0,0]

                        if isinstance(p, int):
                            avg_r += p
                            avg_g += p
                            avg_b += p
                        else:
                            avg_r += p[0]
                            avg_g += p[1]
                            avg_b += p[2]

                avg_r = int(avg_r / pix_per_tile)
                avg_g = int(avg_g / pix_per_tile)
                avg_b = int(avg_b / pix_per_tile)
                mbid = self.index.lookup_color(avg_r, avg_g, avg_b)
                row.append(mbid)
            rows.append(row)

        return self.stitch_image(rows, image_size, tile_size)

    def next_mbid(self, mbid, image_size, tile_size, x, y):
        path = os.path.join(COVERART_DIR, mbid[0:1], mbid[0:2], mbid + ".jpg")
        image = Image.open(path)
        pixels = image.load()
        width, height = image.size

        dest_tiles = int(image_size / tile_size)
        src_tile_size = int(width / dest_tiles)
        pix_per_tile = src_tile_size * src_tile_size

        avg_r = avg_g = avg_b = 0
        x_tile = x / tile_size
        y_tile = y / tile_size
        for x in xrange(src_tile_size):
            for y in xrange(src_tile_size):
                try: 
                    p = pixels[min(width - 1, (x_tile * src_tile_size) + x), 
                               min(height - 1, (y_tile * src_tile_size) + y)]
                except IndexError:
                    p = [0,0,0]

                if isinstance(p, int):
                    avg_r += p
                    avg_g += p
                    avg_b += p
                else:
                    avg_r += p[0]
                    avg_g += p[1]
                    avg_b += p[2]

        avg_r = int(avg_r / pix_per_tile)
        avg_g = int(avg_g / pix_per_tile)
        avg_b = int(avg_b / pix_per_tile)
        return self.index.lookup_color(avg_r, avg_g, avg_b)
                        
if __name__ == "__main__":
    ci = index.ColorIndex()
    ci.load_index()

    mg = MosaicGenerator(ci)                
    #mg.make_mosaic("088f0a9a-8519-4742-ad67-be09efca963a", 500, 10)
    mg.make_mosaic("083ce005-cb1c-477f-b53e-eb1f44938b53", 1000, 10)
