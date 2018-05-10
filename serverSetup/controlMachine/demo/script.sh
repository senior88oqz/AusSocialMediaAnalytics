#!/bin/sh

sudo python3 launch_instance.py 2 demo
ANSIBLE_HOST_KEY_CHECKING=False
#test connection between local and remote
ansible -m ping demo
ansible-playbook copy_to_remote.yml
ansible -m shell -a 'ls' demo
ansible -m shell -a 'sudo ~/installDocker.sh' demo
ansible -m shell -a 'sudo ~/dbSetup2.sh' demo
ansible -m shell -a 'sudo ~/listDB.sh' demo

#sudo service sshd restart

