# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au
from login import ec2_conn

instances = ec2_conn.get_only_instances()

for instance in instances:
    vol_req = ec2_conn.create_volume(50, 'melbourne-qh2')
    ec2_conn.attach_volume(vol_req.id, instance.id, device='/dev/vdc')

# nfs
vol_req = ec2_conn.create_volume(10, 'melbourne-qh2')
ec2_conn.attach_volume(vol_req.id, instances[0].id, device='/dev/vdd')
