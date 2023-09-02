#!/usr/bin/env python3

import sys

from imageprepare import prepare_file, color_palette_18c, color_palette_19c, color_palette_22c
from imageserver import defconfig

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f'Usage: {sys.argv[0]} [input path] [output path] [temperature]')
        exit(-1)

    image_path = sys.argv[1]
    output_path = sys.argv[2]
    temperature = sys.argv[3]

    config = defconfig()
    config.size = (1600, 1200)

    if int(temperature) < 18:
        print("Using 18c palette")
        config.palette = color_palette_18c
    elif int(temperature) <= 20:
        print("Using 19c palette")
        config.palette = color_palette_19c
    else:
        print(f"T={temperature} >20, using 22c palette")
        config.palette = color_palette_22c

    raw = prepare_file(image_path, config)
    with open(output_path, "wb") as f:
        f.write(raw)
