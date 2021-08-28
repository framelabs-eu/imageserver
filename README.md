# ArtFrame Image Server

This tool can serve arbitrary images to ArtFrames in **Mode: WiFi** with firmware _1.4_ or above.

4 bit grayscale images with equal dimension to that of your ArtFrame display resolution are served as-is. All other images are resized, cropped to proper dimensions and converted to grayscale with 4 bit depth and dithering.

# Usage

1. Install dependencies: ```pip3 install pillow```
2. Run ```./imageserver.py [path to image files]```
3. Configure the ArtFrame to use the IP and port of the machine that imageserver.py was started on. Example: "http://framelabs.eu:8090/"

# Help

```
imageserver.py [-h] [--port PORT] [path]

positional arguments:
  path                  folder that should be served (default: .)

optional arguments:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  port that the server will listen on (default: 8090)
```
