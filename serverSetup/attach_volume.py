from login import ec2_conn

instances = ec2_conn.get_only_instances()

for instance in instances:
    vol_req = ec2_conn.create_volume(50, 'melbourne-qh2')
    ec2_conn.attach_volume(vol_req.id, instance.id, device='/dev/vdc')

# nfs
vol_req = ec2_conn.create_volume(10, 'melbourne-qh2')
ec2_conn.attach_volume(vol_req.id, instances[0].id, device='/dev/vdd')
