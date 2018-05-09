#!/bin/sh
#echo $IP
export user=admin
export pass=admin

echo $IP
#curl localhost:5984
curl -X GET "http://admin:admin@${IP}:5984/_all_dbs"

