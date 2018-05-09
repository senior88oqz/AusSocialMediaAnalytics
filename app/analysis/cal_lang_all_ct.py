import json
import sys
from operator import itemgetter
from collections import OrderedDict


def main(argv):
    file=json.load(open("twt_lang_main_ct.json",'r'))
    data=file["rows"]
    sorted_data=sorted(data, key=lambda x: (x["key"][0],x["value"]["sum"]), reverse=True)
    city_count = {
        "Sydney": {}, "Melbourne": {}, "Brisbane": {}, "Perth": {},
        "Adelaide": {}
    }
    text_file = open("data/lang_list.txt", "r")
    lines = text_file.readlines()
    lang_tran_list = {}
    for line in lines:
        line = line.split(' - ')
        lang_tran_list[line[1]] = line[0]
    for row in sorted_data:
        for key in lang_tran_list.keys():
            if row["key"][1] in key:
                row["key"][1]=lang_tran_list[key]
    index=0
    city_index=list(OrderedDict.fromkeys([d['key'][0] for d in sorted_data]))
    #print city_index
    city=city_index[index]
    count=0
    for idx in range(len(sorted_data)):
        lang=sorted_data[idx]["key"][1]
        if lang=="English" or lang=="und":
            continue
        else:
            city_in_list=sorted_data[idx]["key"][0]
            if city_in_list==city:
                if count<10:
                    city_count[city][lang]=str(sorted_data[idx]["value"]["sum"])
                    count+=1
                else:
                    continue
            else:
                count=1
                index+=1
                city = city_index[index]
                city_count[city][lang] = str(sorted_data[idx]["value"]["sum"])
    output_file_name="result/cal_lang_all_ct.json"
    with open(output_file_name, 'w') as fp:
        json.dump(city_count, fp)

if __name__ == "__main__":
    main(sys.argv[1:])

#