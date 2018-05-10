from login import ec2_conn

groups = ec2_conn.get_all_security_groups()

for grp in groups:
    print('group id: {}, group name: {}'.format(grp.id, grp.name))