#!/bin/bash
# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au

cd /share/app/visu
pwd
virtualenv -p python3 venv3
source ./venv3/bin/activate
which python
pip install couchdb nltk gensim pyldavis panda vincent
#sudo apt install cpulimit -y
#nohup cpulimit -l 50 python topic.py
