#!/bin/sh
# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au

#echo $IP
export user=admin
export pass=admin

echo $IP
#curl localhost:5984
curl -X GET "http://admin:admin@${IP}:5984/_all_dbs"
curl -X GET "http://admin:admin@${IP}:5984/_membership"
