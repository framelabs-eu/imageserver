from http.server import BaseHTTPRequestHandler
from collections import namedtuple


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
                self.end_headers()
                self.wfile.write(error.encode())
                return

            status, headers, content = self.method(config)
            self.send_response(status)
            for header in headers:
                self.send_header(*header)
            self.end_headers()
            print(f'Status: {status}')
            if status != 200:
                print(f'Error: {content.decode()}')
            self.wfile.write(content)
        except Exception as e: # i.e. ConnectionResetError, BrokenPipe
            print(f'Error occured: {e}')
