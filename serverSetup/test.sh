#!/bin/sh

#ansible servers -bm shell -a'fdisk -l'
#ansible servers -bm shell -a'mkdir /mnt/extra'
#ansible servers -bm shell -a'mkfs.ext4 /dev/extra'
#ansible servers -bm shell -a'mount /dev/extra /mnt/extra'
#ansible servers -bm shell -a'df -h'

#ansible host0 -bm shell -a'mkdir /share'
#ansible host0 -bm shell -a'mkfs.ext4 /dev/share'
#ansible host0 -bm shell -a'mount /dev/share /share'
#ansible host0 -bm shell -a'df -h'

#ansible-playbook nfs_setup.yml

python3 attach_volume.py
ansible-playbook extra_nfs_setup.yml
