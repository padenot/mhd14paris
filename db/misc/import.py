#!/usr/bin/env python

import psycopg2
import sys

conn = psycopg2.connect("dbname=mcoverart user=mcoverart")
cur = conn.cursor()

count = 0
while True:
    line = sys.stdin.readline().strip()
    if not line: 
        break

    mbid, red, green, blue = line.split(",")
    mbid = mbid[1:-1]
    red = int(red)
    blue = int(blue)
    green = int(green)

    sql = '''INSERT INTO release (mbid, deezer_id, red, green, blue, color) 
             VALUES (%s, %s, %s, %s, %s, %s)''';
    cube = "(%d,%d,%d)" % (red, green, blue)
    cur.execute(sql, (mbid, '', red, green, blue, cube))
    conn.commit()

    count += 1
    if count % 1000 == 0:
        print count
