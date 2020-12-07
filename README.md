# ArtFrame Image Server

This image server can serve images to ArtFrames when they are configured in **Mode: Remote**.

# Usage

1. Prepare images using the [online image converter](https://framelabs.eu/wp-content/uploads/converter.html).
2. Run ```./imageserver.py [path_to_converted_files]```
3. Configure the ArtFrame to use the IP and port of the machine that imageserver.py was started on

# Help

```bash
imageserver.py [-h] [--port PORT] [path]

positional arguments:
  path                  folder that should be served (default: .)

optional arguments:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  port that the server will listen on (default: 8090)
```

