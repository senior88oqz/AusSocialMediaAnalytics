from login import ec2_conn
import sys

group_name = sys.argv[1]

instances = ec2_conn.get_only_instances()


for instance in instances:
    print('\nID: {}\tIP: {}\t'
          'Placement: {}\tStatus: {}'.format(instance.id,
                                             instance.private_ip_address,
                                             instance.placement,
                                             instance.state))

# with open('/etc/ansible/hosts', 'a') as f1, \
#         open('ips', 'a') as f2, \
#         open('/etc/ansible/group_vars/{}'.format(group_name), 'w') as f3:
#     f1.write("[{}]\n".format(group_name))
#     f3.write('---\nansible_ssh_user:ubuntu')
#     for i in range(len(instances)):
#         f1.write("host{} ansible_ssh_host={}\n".format(i, instances[i].private_ip_address))
#         f2.write("{}\t host{}\n".format(instances[i].private_ip_address, i))
#
#
