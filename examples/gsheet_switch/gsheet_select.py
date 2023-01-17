import os
from gsheets import Sheets
from gsheet_config import sheetId, sheetTab, sheetCell, autocontrast

from examples.image_server.image_select import random_file_response

def gsheet_file_response(serve_path, config):
    config.autocontrast = autocontrast
    currentFilePath = os.path.dirname(os.path.realpath(__file__))
    clientSecretPath = os.path.join(currentFilePath, 'client_secret.json')
    sheets = Sheets.from_files(clientSecretPath)
    gsheetData = sheets[sheetId]
    selectedDir = gsheetData[sheetTab][sheetCell]
    newPath = os.path.join(serve_path, selectedDir)
    return random_file_response(newPath, config)
    
