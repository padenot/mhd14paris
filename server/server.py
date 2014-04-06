#!/usr/bin/env python

import os
import sys
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
from config import COVERART_DIR
import index
import mosaic
    
STATIC_PATH = "/static"
STATIC_FOLDER = "static"
TEMPLATE_FOLDER = "templates"

from flask import Flask, Response, render_template, request
app = Flask(__name__,
            static_url_path = STATIC_PATH,
            static_folder = STATIC_FOLDER,
            template_folder = TEMPLATE_FOLDER)

@app.route("/")
def serve_index():
    return render_template("index", title="Coverart Nonsense!")

@app.route("/nonsense", methods=['POST'])
def serve_nonsense():
    mbid = request.form.get('mbid')
    return render_template("nonsense", mbid=mbid)

@app.route("/image/<mbid>")
def serve_image(mbid):
    path = os.path.join(COVERART_DIR, mbid[0:1], mbid[0:2], mbid + ".jpg")
    try:
        fh = open(path, "r")
    except IOError:
        raise NotFound

    image = fh.read()
    fh.close()

    r = Response(image, mimetype='image/jpg')
    r.headers.add("Access-Control-Allow-Origin", "*")
    return r

@app.route("/mosaic/<mbid>/<int:img_size>/<int:tile_size>")
def serve_mosaic(mbid, img_size, tile_size):
    if img_size < 10 or tile_size < 1:
        raise BadRequest

    if img_size % tile_size != 0:
        raise BadRequest

    mg = mosaic.MosaicGenerator(app.color_index)
    io = mg.make_mosaic(mbid, img_size, tile_size)
    r = Response(io.getvalue(), mimetype='image/jpg')
    r.headers.add("Access-Control-Allow-Origin", "*")
    return r

@app.route("/next/<mbid>/<int:img_size>/<int:tile_size>/<int:x>/<int:y>")
def next_mbid(mbid, img_size, tile_size, x, y):
    mg = mosaic.MosaicGenerator(app.color_index)
    mbid = mg.next_mbid(mbid, img_size, tile_size, x, y)
    if not mbid:
        raise BadRequest

    r = Response(mbid)
    r.headers.add("Access-Control-Allow-Origin", "*")
    return r

if __name__ == "__main__":
    print "Loading color index..."
    ci = index.ColorIndex()
    ci.load_index()

    print "Starting app..."
    app.color_index = ci
    app.run(threaded=True, debug=True, host="0.0.0.0", port=8080)
