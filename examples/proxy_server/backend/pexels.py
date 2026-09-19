import json
import os
import random
import urllib.parse
import urllib.request

from PIL import Image

MAX_RESULTS = 100
DEFAULT_KEYWORD = 'architecture'


def get_image(keyword, config):
    if not keyword:
        keyword = DEFAULT_KEYWORD
    headers = {'Authorization': os.getenv('PEXELS_API_KEY'), 'User-Agent': 'Mozilla/5.0'}
    # TODO orientation
    params = urllib.parse.urlencode({'query': keyword, 'orientation': 'landscape', 'per_page': MAX_RESULTS})
    request = urllib.request.Request(f'https://api.pexels.com/v1/search?{params}', headers=headers)
    # alternatively use 'curated?{params}' instead of 'search?{params}'

    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.load(response)

    photo = random.choice(data['photos'])
    image_url = photo['src']['original']

    print('Serving', image_url)
    format = {'fit': 'crop', 'w': config.size[0], 'h': config.size[1]}
    image_request = urllib.request.Request(image_url + '?' + urllib.parse.urlencode(format), headers=headers)
    with urllib.request.urlopen(image_request, timeout=10) as response:
        return Image.open(response)
