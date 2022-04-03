#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')

import argparse
from http.server import ThreadingHTTPServer

from lib.imageserver import ImageRequestHandler
from lib.imageprepare import prepare_image

from vlc_cover_gen import vlc_cover_gen


ARTFRAME_LIFECYCLE = 6  # the ArtFrame takes 2 secs to boot, and approximately another 4 to connect to WiFi and download an image

def vlc_cover_response(vlcurl, password, config):
    im, remaining = vlc_cover_gen(vlcurl, password)
    out = prepare_image(im, config)
    sleep_time = max(remaining - ARTFRAME_LIFECYCLE, 0)

    headers = [('Cache-Control', f'max-age={sleep_time}')]
    return (200, headers, out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ArtFrame VLC cover art server.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--port', '-p', help='Port that the server will listen on', required=False, type=int, default=8090)
    parser.add_argument('--vlcurl', '-u', help='Url of VLC\'s web interface', required=False, default='127.0.0.1:8080')
    parser.add_argument('--password', '-q', help='Password for VLC\'s web interface', required=True)

    args = parser.parse_args()
    port = args.port
    vlcurl = args.vlcurl
    password = args.password
    ImageRequestHandler.method = staticmethod(lambda config: vlc_cover_response(vlcurl, password, config))
    print(f'Listening on port {port}')

    httpd = ThreadingHTTPServer(('', port), ImageRequestHandler)
    httpd.serve_forever()
