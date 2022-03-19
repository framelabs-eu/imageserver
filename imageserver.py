#!/usr/bin/env python3

import argparse

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from collections import namedtuple
from pathlib import Path

import method


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

            status, filename, content = self.method(config)
            self.send_response(status)
            self._headers_buffer.append(f'Location: {filename}\r\n'.encode()) # use non-standard-compliant utf8 instead of latin1
            self.end_headers()
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
    serve_path = Path(args.path).resolve()
    ImageRequestHandler.method = staticmethod(lambda config: method.random_file_content(serve_path, config))
    print(f'Serving \'{serve_path}\' on port {port}')

    httpd = ThreadingHTTPServer(('', port), ImageRequestHandler)
    httpd.serve_forever()
