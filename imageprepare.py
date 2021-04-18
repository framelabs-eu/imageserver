#!/usr/bin/env python3

from PIL import Image
import math
import zlib

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

def dither(img):
    px = img.load()
    # TODO optimize. no full array needed
    arr = [None]*(img.height * img.width)

    for _y in range(img.height):
        y = img.width * _y
        for x in range(img.width):
            arr[x+y] = px[x,_y]

    for _y in range(img.height):
        y = img.width * _y
        for x in range(img.width):
            oldpixel = arr[x + y]
            newpixel = sorted((0, round(oldpixel / 16) * 16, 255))[1]
            arr[x + y] = newpixel

            quant_error = oldpixel - newpixel
            if (x + 1 < img.width):
                arr[x + 1 + y] += quant_error * 7 / 16
                if _y + 1 < img.height:
                  arr[x + 1 + y + img.width] += quant_error * 1 / 16

            if _y + 1 < img.height:
                arr[x + y + img.width] += quant_error * 5 / 16
                if x > 0:
                    arr[x - 1 + y + img.width] += quant_error * 3 / 16

    for i in range(len(arr)):
        px[i%img.width, i/img.width] = arr[i]
    return img

def to_raw(image):
    px = image.load()
    width, height = image.size
    buf = bytearray()

    val = 0
    i = 0
    for y in range(height):
        for x in range(width):
            if i:
                val = px[x, y] // 16
            else:
                val += px[x, y] // 16 << 4
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
        # grayscale
        im = im.convert(mode='L')
        # dither
        im = dither(im)

    # show image for debugging purposes
    # im.show()

    raw = to_raw(im)
    return zlib.compress(raw, level=9)
