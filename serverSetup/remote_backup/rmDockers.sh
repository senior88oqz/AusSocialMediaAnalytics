#!/bin/bash

sudo docker stop $(sudo docker ps -a -q)
#sudo docker rm $(sudo docker ps -a -f status=exited -q)
sudo docker rm $(sudo docker ps -a -q)
sudo docker ps -a
