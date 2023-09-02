import os
from gsheets import Sheets
from gsheet_config import sheet_id, sheet_tab, sheet_cell, autocontrast

from examples.image_server.image_select import random_file_response

def gsheet_file_response(serve_path, config):
    config.autocontrast = autocontrast
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    client_secret_path = os.path.join(current_file_path, 'client_secret.json')
    sheets = Sheets.from_files(client_secret_path)
    gsheet_data = sheets[sheet_id]
    selected_dir = gsheet_data[sheet_tab][sheet_cell]
    new_path = os.path.join(serve_path, selected_dir)
    return random_file_response(new_path, config)
    
