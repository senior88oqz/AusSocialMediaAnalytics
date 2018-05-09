import json
import os
from operator import attrgetter

from shapely.geometry import Point
from shapely.geometry import shape
from shapely.geometry.polygon import Polygon

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))

_suburb_shapes = None
_count = 0
_count_max = 16

melbourne = Polygon([(143.7655, -38.8195), (143.7655, -37.2676), (145.7492, -37.2676), (145.7492, -38.8195)])
sydney = Polygon([(150.9202, -34.0795), (150.9202, -33.6585), (151.36, -33.6585), (151.36, -34.0795)])


class _Suburb(object):
    def __init__(self, count, sh, ssc_code, ssc_name):
        self.count = count
        self.shape = sh
        self.ssc_code = ssc_code
        self.ssc_name = ssc_name


def build_data():
    geojsons = [('NSW', 'nsw.json'), ('VIC', 'vic.json')]
    data = []
    for state, filename in geojsons:
        with open(os.path.join(_THIS_DIR, filename), 'r') as geojson_fp:
            for feature in json.load(geojson_fp)['features']:
                geo = feature['geometry']
                ssc_code = feature['properties']['SSC_CODE']
                ssc_name = feature['properties']['SSC_NAME']
                sh = shape(geo)
                if sh.disjoint(melbourne) and sh.disjoint(sydney):
                    continue
                else:
                    data.append({
                        'geometry': geo,
                        'ssc_code': ssc_code,
                        'ssc_name': ssc_name})
    json.dump(data, open(os.path.join(_THIS_DIR, 'suburbs.json'), 'w'))


def load_data():
    path = os.path.join(_THIS_DIR, 'suburbs.json')
    if not os.path.exists(path):
        build_data()
    data = []
    for item in json.load(open(path, 'r')):
        geo = item['geometry']
        ssc_code = item['ssc_code']
        ssc_name = item['ssc_name']
        data.append(_Suburb(0, shape(geo), ssc_code, ssc_name))
    return data


def _find(lat, lng):
    global _suburb_shapes
    global _count
    global _count_max
    if _suburb_shapes is None:
        _suburb_shapes = load_data()

    p = Point(lng, lat)
    if p.disjoint(melbourne) and p.disjoint(sydney):
        return None

    for sub in _suburb_shapes:
        if sub.shape.contains(p):
            _count += 1
            sub.count += 1
            if _count > _count_max:
                _count = 0
                _count_max *= 2
                _count_max = min(1000, _count_max)
                _suburb_shapes.sort(key=attrgetter('count'), reverse=True)
            return sub
    return None


def get_ssc_code(lat, lng):
    sub = _find(lat, lng)
    if sub is not None:
        return sub.ssc_code
    else:
        return None


def get_ssc_name(lat, lng):
    sub = _find(lat, lng)
    if sub is not None:
        return sub.ssc_name
    else:
        return None
