#!/bin/bash
# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au
export user=admin
export pass=admin
echo $IP $user
#curl -X POST -H "Content-Type: application/json" http://${user}:${pass}@localhost:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin","port": 5984, "node_count": "2", "remote_node": "115.146.85.150", "remote_current_user": "admin", "remote_current_password": "admin" }'
#curl -X POST -H "Content-Type: application/json" http://${user}:${pass}@localhost:5984/_cluster_setup -d '{"action": "add_node", "host":"115.146.85.150", "port": "5984", "username": "admin", "password":"admin"}'

#curl -XPOST "http://${user}:${pass}@localhost:5984/_cluster_setup" --header "Content-Type: application/json" --data '{"action": "finish_cluster"}'

#curl http://${user}:${pass}@localhost:5984/_cluster_setup
