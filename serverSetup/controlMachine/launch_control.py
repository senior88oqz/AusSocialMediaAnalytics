import time
from control_login import ec2_conn

# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au
# security group setting: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-rules-reference.html

ec2_conn.run_instances('ami-00003837',
                       key_name='id_khris',
                       instance_type='m1.small',
                       security_groups=['ssh'],
                       placement='melbourne-qh2')

instances = ec2_conn.get_only_instances()

for instance in instances:
    print('Creating new instance# {}.'.format(instance.id))

pending = True
while pending:
    time.sleep(15)
    if instance.state == 'running':
        pending=False
        print("Control machine is ready")
    else:
        print("Still pending")

