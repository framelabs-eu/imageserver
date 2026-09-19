from http.server import BaseHTTPRequestHandler
from .imageprepare import Config

WIDTH_DEFAULT = 1200
HEIGHT_DEFAULT = 825
ORIENTATION_DEFAULT = 0

WIDTH_RANGE = range(2, 2560 + 1, 2)
HEIGHT_RANGE = range(1, 1440 + 1)
ORIENTATION_RANGE = range(0, 360, 90)


def parse_configuration(width: str | None, height: str | None, orientation: str | None):
    def parse_int(value_str: str | None, default: int, range: range) -> int:
        if not value_str:
            return default
        value = int(value_str)
        if value not in range:
            raise ValueError
        return value

    return Config((parse_int(width, WIDTH_DEFAULT, WIDTH_RANGE), parse_int(height, HEIGHT_DEFAULT, HEIGHT_RANGE)), parse_int(orientation, ORIENTATION_DEFAULT, ORIENTATION_RANGE))

class ImageRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            config = parse_configuration(self.headers['Width'], self.headers['Height'], self.headers['Orientation'])
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
