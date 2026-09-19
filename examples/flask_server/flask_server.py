import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')

from flask import Flask, request
from lib.imageserver import ImageRequestHandler, parse_configuration
from lib.imageprepare import prepare_file


app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        config = parse_configuration(request.headers.get('Width'), request.headers.get('Height'), request.headers.get('Orientation'))
    except ValueError:
        return "Headers 'Width' and 'Height' required, 'Orientation' optional", 400

    filepath = 'Glorious-blue-mountain-range.jpg'
    return prepare_file(filepath, config)
