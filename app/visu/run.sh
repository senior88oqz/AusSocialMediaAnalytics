#!/bin/bash
# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au

cd /share/app/visu/
pwd
#source /share/app/visu/venv3/bin/activate
source ./venv3/bin/activate
which python
nohup cpulimit -l 100 python topic.py 
nohup cpulimit -l 70 python time_series.py
