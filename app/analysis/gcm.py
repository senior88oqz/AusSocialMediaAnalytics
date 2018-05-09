import json
import re
from ssc import get_ssc_code
from multiprocessing import Pool

def getp(data):
    latitude = data["key"]["coordinates"][1]
    longitude = data["key"]["coordinates"][0]
    ssc_code = get_ssc_code(latitude, longitude)
    if ssc_code is not None:
        data["SSC"] = ssc_code
    else:
        data["SSC"] = "error"
    return data


with open("coordinates.json") as f1:
    fl = f1.readline()

with open("twt_SSC.json","w") as myfile:
    #myfile.write("{\"total_rows\":62002,\"offset\":0,\"rows\":[\n")
    myfile.write(fl) 
mydata = json.load(open('coordinates.json'))
cdlist = mydata["rows"]

pool = Pool()
result = pool.map(getp, cdlist)

#print (result)
with open("twt_SSC.json","a") as myfile2:
    for j in result:
        if j["SSC"] != "error":       
            myin = "{k},\n".format(k=json.dumps(j))
            myfile2.write(myin)

with open("twt_SSC.json","a") as myfile:
    myfile.write("{\"value\": \"Puput\",\"address\": \"217-223 Grattan St, Carlton VIC 3053, Australia\",  \"key\": {\"coordinates\": [144.9612697, -37.8001786], \"type\": \"Point\"}, \"SSC\": \"SSC21248\", \"id\": \"990850686521757697\"}\n]}")















