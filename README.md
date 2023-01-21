# ArtFrame Image Server Library

This is a library and example applications for serving content to [ArtFrame](https://framelabs.eu/) devices.

## Usage

1. Discover your computer local network IP address, can run `ifconfig` or `ipconfig getifaddr en0` on MacOSX terminal or check in you OS network advanced settings GUI
1. Install dependencies: ```pip3 install -r requirements.txt```
1. Run one of the examples
1. Configure your ArtFrame to *Mode: WiFi*
1. Set the Image Server URL to point to your computer (i.e. "http://192.168.0.100:8090/")

if you use [VScode IDE](https://code.visualstudio.com) there are prepared [tasks](.vscode/tasks-base.json) for usage and [launch](.vscode/launch-base.json) config for debugging.

## Examples

## [Image Server](examples/image_server)
Serve image files from a folder.

## [VLC Cover Art Server](examples/vlc_cover_server)
Serve the cover art of the song currently playing in VLC.

## [Google Sheet directory Server switch](examples/gsheet_switch)
Serve image files from a folder selected from Google Sheet cell.
