#!/bin/bash
cd /share/app/visu
pwd
virtualenv -p python3 venv3
source ./venv3/bin/activate
which python
pip install couchdb nltk gensim pyldavis panda vincent
#sudo apt install cpulimit -y
#nohup cpulimit -l 50 python topic.py
