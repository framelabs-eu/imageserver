#!/usr/bin/env python3

import sys
sys.path.append("../../")

import argparse
from http.server import ThreadingHTTPServer
from pathlib import Path

from lib.imageserver import ImageRequestHandler

from image_select import random_file_response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ArtFrame image server.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--port', '-p', help='port that the server will listen on', required=False, type=int, default=8090)
    parser.add_argument('path', help='folder that should be served', nargs='?', default='.')

    args = parser.parse_args()
    port = args.port
    serve_path = Path(args.path).resolve()
    ImageRequestHandler.method = staticmethod(lambda config: random_file_response(serve_path, config))
    print(f'Serving \'{serve_path}\' on port {port}')

    httpd = ThreadingHTTPServer(('', port), ImageRequestHandler)
    httpd.serve_forever()
