#!/usr/bin/env python

import os
import sys
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
    
from flask import Flask, Response
app = Flask(__name__)

COVERART_DIR = "/home/robert/musicbrainz/coverart"

@app.route("/image/<mbid>")
def serve_image(mbid):
    path = os.path.join(COVERART_DIR, mbid[0:1], mbid[0:2], mbid + ".jpg")
    try:
        fh = open(path, "r")
    except IOError:
        raise NotFound

    image = fh.read()
    fh.close()

    return Response(image, mimetype='image/jpg')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
