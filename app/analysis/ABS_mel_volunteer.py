import json
import sys
import os
import csv
FILTER_NUM=100 #number of twitters at least in one suburb
def main():
    #input_twt_file_name="mel_postcode_list.json"
    input_abs_file_name="data/pre_2016Census_G19_VIC_SSC.csv"
    output_file_name="result/ABS_mel_volunteer.json"
    #twt_data = json.load(open(input_twt_file_name,'rb'))
    mel_data=[]
    with open(input_abs_file_name, 'rb') as csvfile:
        vic_data = csv.reader(csvfile)
        list_vic_data = list(vic_data)
        for row in list_vic_data:
            if "CODE" not in row[0]:
                #row[0]=row[0].replace("SSC","")
                row[3]="%.4f" % float(row[3])
                mel_data+=[{"SSC":row[0],"volunteer_percentage":row[3]}]
    with open(output_file_name, 'w') as fp:
        json.dump(mel_data, fp)
if __name__ == "__main__":
    main()

#postcode:str,volunteer_percentagge:str