# Image Server

This tool serves arbitrary images to ArtFrame devices.

4 bit grayscale images with equal dimension to that of your ArtFrame display resolution are served as-is. All other images are resized, cropped to proper dimensions and converted to grayscale with 4 bit depth and dithering.

# Usage

1. Run ```./image_server.py [path to image files]```

# Help

```
image_server.py [-h] [--port PORT] [path]

positional arguments:
  path                  folder that should be served (default: .)

optional arguments:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  port that the server will listen on (default: 8090)
```
