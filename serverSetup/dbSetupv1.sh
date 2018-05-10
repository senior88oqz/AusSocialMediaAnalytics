#!/bin/bash
# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au
export user=admin
export pass=admin
export declare IP=$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)
#echo "DOCKER_OPTS=\"--bip=${IP}/22\"" |sudo tee -a /etc/default/docker
sudo service docker restart
#sudo docker pull couchdb:2.1.1
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



#logs
#software install:
#
#-----------install docker----------------
#curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
#
#sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
#
#sudo apt-get update
#
#apt-cache policy docker-ce
#
#sudo apt-get install -y docker-ce
#
#-----------install nodejs &npm----------------
#curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh
#
#sudo bash nodesource_setup.sh
#
#sudo apt-get install nodejs
#
#-----------install grunt----------------------
#sudo npm install -g grunt
#
#-----------install jq-------------------------
#sudo apt-get install jq
#
#--create image, create new instances from the image
#
#-----------setup couchdb and cluster ----------------
#**sudo echo "DOCKER_OPTS="--bip=**local ip address**/22" >> /etc/default/docker
#
#sudo service docker restart
#
#sudo docker pull couchdb:2.1.1
#
#sudo docker run -d --network="host" couchdb:2.1.1 --ip="**local ip address**"
#
#**export declare myip=**local ip address**
#export user=admin
#export pass=admin
#declare -a conts=(`sudo docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n1 -d'\n'`)
#declare cont=${conts[0]}
#
#**sudo docker exec $cont bash -c "echo \"-name couchdb@**local ip address**\" >> /opt/couchdb/etc/vm.args"
#
#sudo docker restart $cont
#
#curl -XPUT "http://localhost:5984/_node/_local/_config/admins/${user}" --data "\"${pass}\""
#
#curl -XPUT "http://localhost:${pass}@${node}:5984/_node/couchdb@${myip}/_config/chttpd/bind_address" --data '"0.0.0.0"'
#
#
#---on master node--------------------
#**curl -X POST -H "Content-Type: application/json" http://$user:$pass@$myip:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin","port": 5984, "remote_node": "**remote node id**", "remote_current_user": "$user", "remote_current_password": "$pass" }'
#
#
#**curl -X POST -H "Content-Type: application/json" http://admin:admin@$myip:5984/_cluster_setup -d '{"action": "add_node", "host":"**remote node id**", "port": "5984", "username": "$user", "password":"$pass"}'
#
#curl -XPOST "http://${user}:${pass}@${myip}:5984/_cluster_setup" --header "Content-Type: application/json" --data "{\"action\": \"finish_cluster\"}"
#
#rev=`curl -XGET "http://$user:$pass@$myip:5986/_nodes/nonode@nohost" | sed -e 's/[{}"]//g' | cut -f3 -d:`
#
#curl -X DELETE "http://$user:$pass@$myip:5986/_nodes/nonode@nohost?rev=${rev}"
#
#==backup plan for node adding!
#**    curl -XPUT "http://${user}:${pass}@${myip}:5986/_nodes/couchdb@115.146.95.75" -d {}
#==check cluster group
#    curl -XGET http://${user}:${pass}@$myip:5984/_membership
#
