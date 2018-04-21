#!/bin/sh

sudo python3 launch_instance.py 4 servers
ANSIBLE_HOST_KEY_CHECKING=False
#test connection between local and remote
ansible -m ping servers
ansible-playbook ./ips_to_remote_hosts.yml -b
#test connection between remote hosts
ansible host0 -m shell -a 'ping -c 3 host1'
ansible host0 -m shell -a 'ping -c 3 host2'
ansible host0 -m shell -a 'ping -c 3 host3'

#sudo service sshd restart

#mount extra volume& nfs setup
python3 attach_volume.py
ansible-playbook extra_nfs_setup.yml