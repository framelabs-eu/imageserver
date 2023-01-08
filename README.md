# ArtFrame Image Server Library

This is a library and example applications for serving content to [ArtFrame](https://framelabs.eu/) devices.

# Usage

1. Configure your ArtFrame to *Mode: WiFi*
2. Set the Image Server URL to point to your computer (i.e. "http://192.168.0.100:8090/")
3. Install dependencies: ```pip3 install -r requirements.txt```
4. Run one of the examples

# Examples

## [Image Server](examples/image_server)
Serve image files from a folder.

## [VLC Cover Art Server](examples/vlc_cover_server)
Serve the cover art of the song currently playing in VLC.

## [Google Sheet directory Server switch](examples/gsheet_switch)
Serve image files from a folder selected from Google Sheet cell.
