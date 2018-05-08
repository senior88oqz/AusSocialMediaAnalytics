#!/bin/bash
#ssh ubuntu@115.146.86.228
#sudo apt-add-repository -y ppa:ansible/ansible
#sudo apt-get update
#sudo apt-get install -y ansible
#scp -r /etc/ansible/* ubuntu@115.146.86.228:/home/ubuntu/
##on server
#sudo mv * /etc/ansible
##now set up ssh keys
#ssh-keygen
##on local, download pub
#ssh-copy-id -f -i servers.pub host0
#ssh-copy-id -f -i servers.pub host1
#ssh-copy-id -f -i servers.pub host2
#ssh-copy-id -f -i servers.pub host3
## now ssh to servers with private key
#
#
#ssh-agent bash
#ssh-add ~/.ssh/id_rsa

## put in ~/.bashrc
#eval $(ssh-agent)
#ssh-add ~/.ssh/where_ever_privake_key_is