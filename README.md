# ArtFrame Image Server

This tool can serve arbitrary images to ArtFrames in **Mode: WiFi** with firmware _1.4_ or above.

4 bit grayscale PNG files with equal dimension to that of your ArtFrame display resolution are served as-is. All other images are cropped, resized and dithered.

| ⚠ NOTE |
| ------------------------------------------------------------ |
| **Although arbitrary image formats [[1]](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html) and sizes are supported, for best visual results and performance, you should prepare your images manually before serving them.** |

# Usage

1. Run ```./imageserver.py [path to image files]```
2. Configure the ArtFrame to use the IP and port of the machine that imageserver.py was started on. Example: "http://framelabs.eu:8090/"

# Help

```
imageserver.py [-h] [--port PORT] [path]

positional arguments:
  path                  folder that should be served (default: .)

optional arguments:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  port that the server will listen on (default: 8090)
```
