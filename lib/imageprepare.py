import zlib
from dataclasses import dataclass, field

from PIL import Image, ImageOps


def grayscale_palette():
    palette = []
    for i in range(0, 256, 17):
        palette += [i, i, i]
    return palette


@dataclass
class Config:
    size: tuple[int, int]
    orientation: int
    palette: list[int] = field(default_factory=grayscale_palette)


def to_raw(image):
    raw = image.tobytes()
    return bytearray(raw[i] | raw[i+1] << 4 for i in range(0, len(raw), 2))

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


def convert_image(im, config):
    # crop & resize
    im = ImageOps.fit(im, config.size, centering=(0.5, 0.5), method=Image.Resampling.LANCZOS)
    # grayscale. this mainly prevents image artifacts
    im = im.convert('I')
    # remove alpha channel to enable conversion to palette
    im = im.convert('RGB')
    # 4-bit grayscale & dither
    palette = Image.new('P', (1, 1))
    palette.putpalette(config.palette)

    im = im.quantize(palette=palette, dither=Image.FLOYDSTEINBERG)

    if config.orientation:
        im = im.transpose(Image.ROTATE_90)

    # show image for debugging purposes
    # im.show()
    return im


def prepare_image(im, config):
    im = convert_image(im, config)
    raw = to_raw(im)
    return zlib.compress(raw, level=9)

def prepare_file(filepath, config):
    im = Image.open(filepath)
    return prepare_image(im, config)
