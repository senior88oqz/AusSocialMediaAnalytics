#!/bin/bash
cd /share/app/visu/
pwd
#source /share/app/visu/venv3/bin/activate
source ./venv3/bin/activate
which python
nohup cpulimit -l 100 python topic.py >> my.log
nohup cpulimit -l 70 python time_series.py >> my.log
