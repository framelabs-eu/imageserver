# VLC Cover Art Server

This tool serves the cover art of the currently playing song in VLC to ArtFrame devices.

# Usage

1. Enable VLC's web interface via _View_ > _Add interface_ > _Web_
2. Set a password for VLC's web interface via _Settings_ > _Interface_ > _Main interfaces_ > _Lua_ > _Lua HTTP_ > _Password_
3. Run ```./vlc_cover_server.py -q PASSWORD```, where _PASSWORD_ is the password of VLC's web interface.

# Help

```
vlc_cover_server.py [-h] [--port PORT] [--vlcurl VLCURL] --password PASSWORD

required arguments:
--password PASSWORD, -q PASSWORD Password for VLC's web interface (default: None)

optional arguments:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  Port that the server will listen on (default: 8090)
  --vlcurl VLCURL, -u VLCURL
                        Url of VLC's web interface (default: 127.0.0.1:8080)
```
