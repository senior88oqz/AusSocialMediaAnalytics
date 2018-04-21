import sys
import time
from login import ec2_conn

# security group setting: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-rules-reference.html

number_of_instances = int(sys.argv[1])
group_name = sys.argv[2]

ec2_conn.run_instances('ami-00003837',
                       max_count=number_of_instances,
                       key_name='id_khris',
                       instance_type='m1.medium',
                       security_groups=['ssh'],
                       placement='melbourne-qh2')

instances = ec2_conn.get_only_instances()

for instance in instances:
    print('Creating new instance# {}.'.format(instance.id))

pending = True
count = 0
while pending:
    time.sleep(15)
    instances = ec2_conn.get_only_instances()
    for instance in instances:
        if instance.state == 'running':
            count += 1
    if count == number_of_instances:
        pending = False
        print("All instances are ready")
    else:
        print("Still pending")
        count = 0

with open('/etc/ansible/hosts', 'a') as f1, \
        open('ips', 'w') as f2, \
        open('/etc/ansible/group_vars/{}'.format(group_name), 'w') as f3:
    f1.write("[{}]\n".format(group_name))
    f3.write('---\nansible_ssh_user: ubuntu')
    for i in range(len(instances)):
        f1.write("host{} ansible_ssh_host={}\n".format(i, instances[i].private_ip_address))
        f2.write("{}\t host{}\n".format(instances[i].private_ip_address, i))

    # --> go to nectar dashboard modify instance name respectively
