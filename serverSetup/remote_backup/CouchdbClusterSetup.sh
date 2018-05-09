#!/bin/bash
# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au
export user=admin
export pass=admin
export declare IP=$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)
echo "DOCKER_OPTS=\"--bip=${IP}/22\"" |sudo tee -a /etc/default/docker
sudo service docker restart
sudo docker pull couchdb:2.1.1
sudo docker run -d --network="host" couchdb:2.1.1 --ip=${IP}
declare -a conts=(`sudo docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n1 -d'\n'`)
declare cont=${conts[0]}
echo "container#{$cont}"
sudo docker exec $cont bash -c "echo \"-name couchdb@${IP}\" >> /opt/couchdb/etc/vm.args"
sudo docker restart ${cont}
echo "setup admin account -> user:{$user}"
echo "-------------initializing couchdb----------"
sleep 20
curl localhost:5984
curl -XPUT "http://localhost:5984/_node/_local/_config/admins/${user}" --data "\"${pass}\"" 
echo "setup login ip"
curl -XPUT "http://{$user}:{$pass}@${IP}:5984/_node/couchdb@${IP}/_config/chttpd/bind_address" --data '"0.0.0.0"'
#create db
curl -XPUT "http://{$user}:{$pass}@${IP}:5984/test"
