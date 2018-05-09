#!/bin/bash
#run harvest
ansible -m shell -a '/share/app/harvest/terminate1.sh' host1
ansible -m shell -a '/share/app/harvest/run1.sh' host1
ansible -m shell -a '/share/app/harvest/terminate2.sh' host3
ansible -m shell -a '/share/app/harvest/run2.sh' host3

#screen exmaple
#screen -S tempt -d -m /share/app/analysis/get_view.sh
#screen -r tempt
#alt + a + d

#run analysis
ansible -m shell -a '/share/app/analysis/run.sh &>> /share/app/analysis/analysis.log' host1
ansible -m shell -a 'screen -S analysis -d -m /share/app/analysis/run.sh &>> /share/app/analysis/analysis.log' host1

#run topic/time
ansible -m shell -a '/share/app/visu/run.sh &>> /share/app/visu/control_log' host2

#run server
ansible -m shell -a '/share/app/web/stopserver.sh' host3
ansible -m shell -a '/share/app/web/runserver.sh' host3
