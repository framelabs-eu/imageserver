import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')

from flask import Flask, request
from lib.imageserver import ImageRequestHandler, parse_configuration
from lib.imageprepare import prepare_file


app = Flask(__name__)

@app.route('/')
def hello_world():
    config = parse_configuration(request.headers)
    if not config.size:
        return "Headers 'Width' and 'Height' required, 'Orientation' optional", 412

    filepath = 'Glorious-blue-mountain-range.jpg'
    return prepare_file(filepath, config)
