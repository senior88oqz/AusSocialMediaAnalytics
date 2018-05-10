#!/bin/sh
# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au

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
