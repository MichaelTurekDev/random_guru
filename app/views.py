import random

import requests
from lxml import etree
from flask import render_template

from app import app
from app.controllers.api.history_controller import history_controller


base_url = 'https://refactoring.guru'


def scrape_pattern_elements():
    '''
    Fetch element data from all design patterns in catalog.
    # Returns:
        3-tuple of anchor, image, and pattern name lists corresponding to each
        pattern found.
    '''
    response = requests.get(base_url + '/design-patterns/catalog')

    if (response.status_code != 200):
        print(f'Could not connect. Status code: {response.status_code}')
        exit()

    # Parse HTML for pattern-related element data
    root = etree.fromstring(response.text, etree.HTMLParser())
    anchors = root.xpath('//div[@class="patterns-catalog"]/div/a')
    images = root.xpath('//span[@class="pattern-image"]/img')
    names = root.xpath('//span[@class="pattern-name"]/text()')

    # Sanity check
    assert len(anchors) == len(images) == len(names)

    return anchors, images, names


def get_patterns() -> list[dict]:
    '''
    Assemble collection of pattern meta data from webpage scrapings.
    # Returns:
        list of dictionaries each storing a pattern's meta data.
    '''
    anchors, images, names = scrape_pattern_elements()

    # Build pattern dictionaries for unvisited patterns
    patterns = list()
    for anchor, image, name in zip(anchors, images, names):
        patterns.append({
            'name': name,
            'url': base_url + anchor.attrib['href'],
            'img': base_url + image.attrib['src']
        })

    return patterns


@app.route('/')
def index() -> None:
    # Fetch unvisted patterns using visited history
    history = history_controller.get()
    patterns = get_patterns()

    # Clear history once cycled through
    if len(history) == len(patterns):
        history_controller.clear()

    # Select random unvisited pattern and mark it visited in database
    unvisited = [p for p in patterns if p['name'] not in history]
    pattern = random.choice(unvisited)
    history_controller.add(pattern['name'])

    return render_template('index.html', pattern=pattern)
