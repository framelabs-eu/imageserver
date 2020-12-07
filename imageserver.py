#!/usr/bin/env python3

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

import argparse
import os
from pathlib import Path
import random
import zlib

serve_path = None


def get_content(file):
    if not file:
        return None

    with open(file, 'rb') as content_file:
        content = content_file.read()  # TODO Don't read everything at once?
        try:
            decompressor = zlib.decompressobj()
            content_decompressed = decompressor.decompress(content, 1)
            return content
        except Exception:
            print(f'File \'{file}\' is not supported')
            return None


def random_file_content(path):
    for root, _, files in os.walk(path):
        # print(files)
        if not len(files):
            print(f'Path \'{path}\' is empty')
            return None
        random.shuffle(files)
        for filename in files:
            filepath = os.path.join(root, filename)
            content = get_content(filepath)
            if content:
                return filename, content
    return None


class ImageRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        topic = self.path[1:]

        try:
            # TODO: Is a path attack possible here?
            response = random_file_content(serve_path / topic)
            if not response:
                print(f'Topic not found: \'{topic}\'')
                self.send_response(404)
                self.end_headers()
            else:
                filename, content = response
                print(f'Serving topic \'{topic}\': \'{filename}\'')
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
    serve_path = Path(args.path)
    print(f'Serving \'{serve_path.resolve()}\' on port {port}')

    httpd = ThreadingHTTPServer(('', port), ImageRequestHandler)
    httpd.serve_forever()
