#!/usr/bin/env python3

import argparse
import os
import random

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from collections import namedtuple
from pathlib import Path

from imageprepare import prepare_file


def get_content(filepath, config):
    try:
        rawz = prepare_file(filepath, config)
        return rawz
    except Exception:
        print(f'File \'{filepath}\' is not supported')
        return None

def random_file_content(path, config):
    for root, _, files in os.walk(path):
        # print(files)
        if not len(files):
            return (404, f'No files at \'{path}\''.encode())
        random.shuffle(files)
        for filename in files:
            filepath = os.path.join(root, filename)
            content = get_content(filepath, config)
            if content:
                print(f'Serving {filename}')
                return (200, content)
    return (404, f'No servable files at \'{path}\''.encode())

def defconfig():
    config = namedtuple('config', [])
    config.size = None
    config.orientation = 0
    return config

def parse_configuration(headers):
    config = defconfig()
    try:
        width = int(headers['Width'])
        height = int(headers['Height'])
        config.size = (width, height)
        config.orientation = int(headers['Orientation'])
    except:
        pass
    return config

class ImageRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            config = parse_configuration(self.headers)
            print(f'Request for {config.size}, rotation: {config.orientation}')
            if not config.size:
                error = "Headers 'Width' and 'Height' required, 'Orientation' optional"
                print(error)
                self.send_response(412)
                self.wfile.write(error.encode())
                self.end_headers()
                return

            status, content = random_file_content(self.serve_path, config)
            self.send_response(status)
            print(f'Status: {status}')
            if status != 200:
                print(f'Error: {content.decode()}')
            self.wfile.write(content)
            self.end_headers()
        except Exception as e: # i.e. ConnectionResetError, BrokenPipe
            print(f'Error occured: {e}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ArtFrame image server.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--port', '-p', help='port that the server will listen on', required=False, type=int, default=8090)
    parser.add_argument('path', help='folder that should be served', nargs='?', default='.')

    args = parser.parse_args()
    port = args.port
    ImageRequestHandler.serve_path = Path(args.path).resolve()
    print(f'Serving \'{ImageRequestHandler.serve_path}\' on port {port}')

    httpd = ThreadingHTTPServer(('', port), ImageRequestHandler)
    httpd.serve_forever()
