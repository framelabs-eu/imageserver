#!/usr/bin/env python3

import requests

from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont


def vlc_cover_gen(url, password):
    im = Image.new('L', (1000, 1333))
    draw = ImageDraw.Draw(im)

    try:
        r = requests.get(f'http://{url}/requests/status.json', auth=('', password))
        if r.status_code != 200:
            print(f'Unsuccessful: {r.status_code}')
            return (im, -1)
        r.encoding = 'utf-8'
        data = r.json()
    except Exception as e:
        print('Error:', e)
        return (im, -1)


    current_pos = int(data['time'])
    length = int(data['length'])
    remaining = length - current_pos

    try:
        artist = data['information']['category']['meta']['artist']
        title = data['information']['category']['meta']['title']
        artwork = data['information']['category']['meta']['artwork_url']
        artwork = artwork.replace('file://', '')
        artwork = requests.compat.unquote(artwork)
    except Exception as e:
        print('Error:', e)
        return (im, remaining)
    print(f'Artist: {artist}, title: {title}, remaining time: {remaining}')

    cover = Image.open(artwork)
    cover = cover.resize((1000, 1000))
    im.paste(cover, (0, 333))

    font = font_manager.FontProperties(family='sans-serif', weight='bold')
    fontfile = font_manager.findfont(font)
    font = ImageFont.truetype(fontfile, 48)

    draw.multiline_text((500,111), artist, font=font, fill=255, anchor='mm')
    draw.multiline_text((500,222), title, font=font, fill=255, anchor='mm')

    im = im.rotate(90, expand=True)
    return (im, remaining)


if __name__ == '__main__':
    im, remaining = vlc_cover_gen('127.0.0.1:8080', ' ')
    print(f'Remaining secs: {remaining}')
    # im.show()
