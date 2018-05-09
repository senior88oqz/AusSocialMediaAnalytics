# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au

import json
import os
from collections import defaultdict
from datetime import datetime

from shapely.geometry import shape
from shapely.geometry.polygon import Polygon

from process_path import get_input_path
from process_path import get_output_path

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
MELB = Polygon([(144.2430, -38.5447), (144.2430, -37.1252), (145.8920, -37.1252), (145.8920, -38.5447)])
SYDNEY = Polygon([(150.9202, -34.0795), (150.9202, -33.6585), (151.36, -33.6585), (151.36, -34.0795)])


def process_sentiment():
    # Load ssc data
    sydney_suburbs = {}
    melb_suburbs = {}
    for file in ['nsw.json', 'vic.json']:
        with open(os.path.join(THIS_DIR, file), 'r') as fp:
            jobj = json.load(fp)
            for suburb in jobj:
                geo = suburb['geometry']
                sh = shape(geo)
                ssc_code = suburb['properties']['SSC_CODE']
                if MELB.contains(sh):
                    melb_suburbs[ssc_code] = suburb
                elif SYDNEY.contains(sh):
                    sydney_suburbs[ssc_code] = suburb

    melb_data = []
    sydney_data = []
    min_melb = 1
    max_melb = 0
    min_sydney = 1
    max_sydney = 0
    with open(get_input_path('cal_all_SSC.json'), 'r') as fp:
        jobj = json.load(fp)
        for row in jobj:
            ssc_code = row['SSC']
            rate = float(row['postive_twt_rate'])
            if ssc_code in melb_suburbs:
                suburb = melb_suburbs[ssc_code]
                suburb['properties']['value'] = rate
                suburb['properties']['text'] = '%.2f%%' % (rate * 100)
                if rate > max_melb:
                    max_melb = rate
                if rate < min_melb:
                    min_melb = rate
                melb_data.append(suburb)
            if ssc_code in sydney_suburbs:
                suburb = sydney_suburbs[ssc_code]
                suburb['properties']['value'] = rate
                suburb['properties']['text'] = '%.2f%%' % (rate * 100)
                if rate > max_sydney:
                    max_sydney = rate
                if rate < min_sydney:
                    min_sydney = rate
                sydney_data.append(suburb)
    for suburb in melb_data:
        rate = suburb['properties']['value']
        suburb['properties']['ratio'] = (rate - min_melb) / (max_melb - min_melb)

    for suburb in sydney_data:
        rate = suburb['properties']['value']
        suburb['properties']['ratio'] = (rate - min_sydney) / (max_sydney - min_sydney)

    json.dump({
        "totalFeatures": len(melb_data),
        "type": "FeatureCollection",
        'features': melb_data,
        'max_value_text': '%.2f%%' % (max_melb * 100),
        'min_value_text': '%.2f%%' % (min_melb * 100),
        'max_value': max_melb,
        'min_value': min_melb
    }, open(get_output_path('cal_mel_ssc.json'), 'w'))

    json.dump({
        "totalFeatures": len(sydney_data),
        "type": "FeatureCollection",
        'features': sydney_data,
        'max_value_text': '%.2f%%' % (max_sydney * 100),
        'min_value_text': '%.2f%%' % (min_sydney * 100),
        'max_value': max_sydney,
        'min_value': min_sydney
    }, open(get_output_path('cal_syd_ssc.json'), 'w'))


def process_popularity():
    with open(get_input_path('popularity.json'), 'r') as fp:
        jobj = json.load(fp)
        results = defaultdict(int)
        for row in jobj['rows']:
            coords = row['key']['coordinates']
            lng = round(coords[0] * 100.0) / 100.0
            lat = round(coords[1] * 100.0) / 100.0
            value = row['value']
            results[(lng, lat)] += value
        result_list = []
        for (lng, lat), value in results.items():
            result_list.append({'lng': lng, 'lat': lat, 'weight': value})
        with open(get_output_path('popularity-weighted.json'), 'w') as out_fp:
            json.dump(result_list, out_fp)


def main():
    process_sentiment()
    process_popularity()
    meta_path = get_output_path('meta.json')
    meta = {'update': str(datetime.now())[:-7]}
    json.dump(meta, open(meta_path, 'w'))


if __name__ == '__main__':
    main()
