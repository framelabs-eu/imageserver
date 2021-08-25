#!/usr/bin/env python3

from PIL import Image
import math
import zlib

def grayscale_palette():
    palette = []
    for i in range(0, 255, 16):
        palette += [i, i, i]
    return palette * 16

def calculate_crop_area(size_in, size_request):
    wi, hi = size_in
    w, h = size_request
    ratio_in = wi/hi
    ratio_out = w/h
    x = 0
    y = 0
    wo = None
    ho = None
    if ratio_in > ratio_out:
        wo = hi*ratio_out
        ho = hi
        x = (wi-wo)/2
    else:
        wo = wi
        ho = wi/ratio_out
        y = (hi-ho)/2
    return (x, y, x+wo, y+ho)

def to_raw(image):
    px = image.load()
    width, height = image.size
    buf = bytearray()

    val = 0
    i = 0
    for y in range(height):
        for x in range(width):
            if i:
                val = px[x, y]
            else:
                val += px[x, y] << 4
                buf.append(val)
            i = not i
    return buf

def preprocessing_needed(im, size):
    if im.mode != 'L':
        print(f'Image is not grayscale: {im.mode}')
        return True
    if im.size != size:
        print(f'Image has wrong dimensions: {im.size}, requested is {size}')
        return True
    if hasattr(im, 'depth') and im.depth != 4:
        print(f'Image needs to have 4 bit depth')
        return True
    return False

def prepare(filepath, size):
    im = Image.open(filepath)

    if preprocessing_needed(im, size):
        print(f'Preprocessing needed ...')

        # crop & resize
        crop = calculate_crop_area(im.size, size)
        im = im.resize(size, resample=Image.LANCZOS, box=crop)

        # remove alpha channel to enable conversion to palette
        im = im.convert('RGB')

        # 4-bit grayscale & dither
        palette = Image.new('P', (1, 1))
        palette.putpalette(grayscale_palette())

        im = im.quantize(palette=palette, dither=Image.FLOYDSTEINBERG)

    # show image for debugging purposes
    # im.show()

    raw = to_raw(im)
    return zlib.compress(raw, level=9)
