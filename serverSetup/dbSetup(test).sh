#!/bin/bash

export declare IP=$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)
export USER=admin
export PASS=admin
declare -a conts=(`sudo docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n1 -d'\n'`)
declare cont=${conts[0]}
echo "DOCKER_OPTS=\"--bip=${IP}/22\"" |sudo tee -a /etc/default/docker
sudo service docker restart
sudo docker pull couchdb:2.1.1
sudo docker run -d --network="host" couchdb:2.1.1 --ip=${IP}
sudo docker exec $cont bash -c "echo \"-name couchdb@${IP}\" | sudo tee /opt/couchdb/etc/vm.args"
#sudo docker restart ${cont}
#curl -XPUT "http://localhost:5984/_node/_local/_config/admins/${USER}" --data "\"${PASS}\""

#curl -XPUT "http://localhost:${PASS}@${node}:5984/_node/couchdb@${IP}/_config/chttpd/bind_address" --data '"0.0.0.0"'
