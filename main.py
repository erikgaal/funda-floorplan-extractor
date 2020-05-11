import sys
import math
import urllib.request
from util import chunk
import xml.etree.ElementTree as etree

def parsefloor(floor):
    areas = [parsearea(area) for area in floor.findall('.//area')]

    return {
        'areas': areas,
    }

 
def parsearea(area):
    points = area.find('points').text.split(',')
    points = [[float(point) for point in points.split()] for points in points]

    return {
        'points': list(map(lambda p: tuple(p[:3]), points)),
        'color': area.find('color').text,
    }


def floor2obj(floor):
    return '\n\n'.join([area2obj(area) for area in floor['areas']])


def area2obj(area):
    c = '# area'
    vs = ['v {} {} {}'.format(x, z, y) for (x, y, z) in area['points']]
    l = 'f {}'.format(' '.join(['-{}'.format(i) for i in reversed(range(1, len(area['points']) + 1))]))

    return '\n'.join([c] + vs + [l])


if __name__ == "__main__":
    url = sys.argv[1]

    with urllib.request.urlopen(url) as response:
        body = response.read()

    # Parse the XML tree
    tree = etree.fromstring(body)

    # Find the "floors" section
    floors = tree.findall('.//floor')

    # Parse the first floor to a usable format
    # TODO: Allow the user to pick a floor to convert
    floor = parsefloor(floors[0])

    # Convert the floor to Wavefront object
    obj = floor2obj(floor)

    # Output
    sys.stdout.write(obj)
