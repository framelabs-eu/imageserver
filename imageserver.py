#!/usr/bin/env python3

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

import argparse
import os
from pathlib import Path
import random

from imageprepare import prepare_file


def get_content(filepath, size):
    try:
        rawz = prepare_file(filepath, size)
        return rawz
    except Exception:
        print(f'File \'{filepath}\' is not supported')
        return None

def random_file_content(path, size):
    for root, _, files in os.walk(path):
        # print(files)
        if not len(files):
            print(f'No files at \'{path}\'')
            return None
        random.shuffle(files)
        for filename in files:
            filepath = os.path.join(root, filename)
            content = get_content(filepath, size)
            if content:
                return filename, content
    return None

def parse_size(headers):
    try:
        width = int(headers['Width'])
        height = int(headers['Height'])
        return (width, height)
    except:
        return None

class ImageRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            size = parse_size(self.headers)
            if not size:
                error = "Headers 'Width' and 'Height' required"
                print(error)
                self.send_response(412)
                self.wfile.write(error.encode())
                self.end_headers()
                return
            response = random_file_content(self.serve_path, size)
            if not response:
                print('No serveable file found')
                self.send_response(404)
                self.end_headers()
            else:
                filename, content = response
                print(f'Serving \'{filename}\' at {size}')
                self.send_response(200)
                self.end_headers()
                self.wfile.write(content)
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
