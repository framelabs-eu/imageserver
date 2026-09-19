import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')


from collections.abc import Iterable
from wsgiref.types import StartResponse, WSGIEnvironment

import backend.pexels as fetcher

from lib.imageprepare import prepare_image
from lib.imageserver import parse_configuration


def application(env: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]:
    try:
        config = parse_configuration(env.get('HTTP_WIDTH'), env.get('HTTP_HEIGHT'), env.get('HTTP_ORIENTATION'))
    except ValueError:
        _ = start_response('400 Bad Request', [('Content-Type', 'text/plain')])
        return [b'Could not parse headers\n']

    keyword: str = env.get('PATH_INFO')[1:]  # omit leading /
    print(f'{keyword=}')

    im = fetcher.get_image(keyword, config)
    bin = prepare_image(im, config)
    im.close()
    status = '200 OK'
    _ = start_response(status, [('Content-Type', 'application/octet-stream')])
    return [bin]


# Test server
if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    with make_server('127.0.0.1', 8090, application) as httpd:
        print(f'Serving on port {httpd.server_port}...')
        httpd.serve_forever()
