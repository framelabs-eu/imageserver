from PIL import Image, ImageOps
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
    buf = bytearray(width * height // 2)

    for y in range(height):
        for x in range(0, width, 2):
            buf[(y*width+x)//2] = px[x, y] + (px[x+1, y] << 4)
    return buf

def preprocessing_needed(im, size):
    if im.mode != 'L':
        print(f'Image is not grayscale: {im.mode}')
        return True
    if im.size != size:
        print(f'Image has wrong dimensions: {im.size}, requested is {size}')
        return True
    if hasattr(im, 'depth') and im.depth != 4:
        print('Image needs to have 4 bit depth')
        return True
    return False

def prepare_image(im, config):
    print('Processing ...')

    # crop & resize
    crop = calculate_crop_area(im.size, config.size)
    im = im.resize(config.size, resample=Image.LANCZOS, box=crop)

    # grayscale. this mainly prevents image artifacts
    im = im.convert('I')
    # remove alpha channel to enable conversion to palette
    im = im.convert('RGB')
    # 4-bit grayscale & dither
    palette = Image.new('P', (1, 1))
    palette.putpalette(grayscale_palette())

    if hasattr(config, 'autocontrast'):
        im = ImageOps.autocontrast(im, cutoff=config.autocontrast, ignore=None, mask=None, preserve_tone=False)

    im = im.quantize(palette=palette, dither=Image.FLOYDSTEINBERG)

    if hasattr(config, 'orientation'):
        im = im.transpose(Image.ROTATE_90)

    # show image for debugging purposes
    # im.show()

    raw = to_raw(im)
    return zlib.compress(raw, level=9)

def prepare_file(filepath, config):
    im = Image.open(filepath)
    return prepare_image(im, config)
