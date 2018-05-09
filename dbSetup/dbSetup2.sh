#!/bin/bash
export user=admin
export pass=admin
export IP=$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)
echo $IP
sudo docker run --name ${HOSTNAME} -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=admin -e NODENAME=${IP} -v /mnt/extra:/opt/couchdb/data -p 5984:5984 -p 4369:4369 -p 5986:5986 -p 9100-9200:9100-9200 -d couchdb:2.1.1
sleep  20
echo "Testing-----"
curl ${IP}:5984
