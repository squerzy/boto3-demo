import boto3
import time

# Initialize a session using Amazon EC2
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

# Create a Key Pair
key_pair_name = 'jerzy-key-python'
try:
    key_pair = ec2.create_key_pair(KeyName=key_pair_name)
    print(f'Key Pair Created: {key_pair.name}')
    with open(f'{key_pair_name}.pem', 'w') as file:
        file.write(key_pair.key_material)
except Exception as e:
    print(f'Error Creating Key Pair: {e}')

# Create a Security Group
sg_name = 'jerzy-sg-python'
try:
    security_group = ec2.create_security_group(GroupName=sg_name, Description='SG for Jerzy EC2 Instance')
    sg_id = security_group.id
    print(f'Security Group Created: {sg_id}')

    # Authorize inbound SSH traffic
    security_group.authorize_ingress(
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
    )
    print('Port 22 Opened for Public Access')
except Exception as e:
    print(f'Error Creating Security Group: {e}')

# Create an EC2 instance
ami_id = 'ami-08f32efd140b7d89f'   # Replace with the AMI ID you want to use
instance_type = 't2.micro'  # Change as per your needs

try:
    instance = ec2.create_instances(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        KeyName=key_pair_name,
        SecurityGroupIds=[sg_id]
    )
    print(f'EC2 Instance Created: {instance[0].id}')
    print('Waiting for the instance to be running...')
    instance[0].wait_until_running()
    print('Instance is now running')
except Exception as e:
    print(f'Error Creating EC2 Instance: {e}')

