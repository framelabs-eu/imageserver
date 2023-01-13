import os
from gsheets import Sheets
from gsheet_config import sheetId, sheetTab, sheetCell

from examples.image_server.image_select import random_file_response

def gsheet_file_response(serve_path, config):
    config.autocontrast = 3
    sheets = Sheets.from_files('./client_secret.json')
    gsheetData = sheets[sheetId]
    selectedDir = gsheetData[sheetTab][sheetCell]
    newPath = os.path.join(serve_path, selectedDir)
    return random_file_response(newPath, config)
    
