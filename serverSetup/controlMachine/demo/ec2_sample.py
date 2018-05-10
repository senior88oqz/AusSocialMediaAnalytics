import boto
from boto.ec2.regioninfo import RegionInfo

region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')

ec2_conn = boto.connect_ec2(aws_access_key_id='XXXX'
                            , aws_secret_access_key='XXXX',
                            is_secure=True, region=region, port=8773,
                            path='/services/Cloud',
                            validate_certs=False)
