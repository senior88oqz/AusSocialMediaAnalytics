#!/bin/bash
# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au

sudo docker stop $(sudo docker ps -a -q)
#sudo docker rm $(sudo docker ps -a -f status=exited -q)
sudo docker rm $(sudo docker ps -a -q)
sudo docker ps -a
