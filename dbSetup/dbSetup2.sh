#!/bin/bash
# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au

export user=admin
export pass=admin
export IP=$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)
echo $IP
sudo docker run --name ${HOSTNAME} -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=admin -e NODENAME=${IP} -v /mnt/extra:/opt/couchdb/data -p 5984:5984 -p 4369:4369 -p 5986:5986 -p 9100-9200:9100-9200 -d couchdb:2.1.1
sleep  20
echo "Testing-----"
curl ${IP}:5984
