#!/bin/bash

apt-get update
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install -y --allow-unauthenticated docker-ce
echo "verfiying docker installation.."
docker run hello-world

