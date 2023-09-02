#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')

from gsheet_select import gsheet_file_response

from examples.image_server.image_server import image_server

if __name__ == '__main__':
    image_server(gsheet_file_response)
