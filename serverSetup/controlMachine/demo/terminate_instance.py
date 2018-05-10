from login import ec2_conn

INSTANCE_ID = 'i-638654e7'

ec2_conn.terminate_instances(instance_ids=[INSTANCE_ID])

print('New instance {} has benn terminated.'.format(INSTANCE_ID))
