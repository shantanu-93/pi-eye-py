import os
import datetime
import boto3
import queue_util as queue_util
import global_constants
from botocore.exceptions import ClientError

const = global_constants.GlobalConstants()


script = """#!/bin/bash
echo "automatically generated from user data"
python3 ec2-instance.py
"""

sqs = boto3.client('sqs')
''', region_name=const.REGION,
        aws_access_key_id=const.ACCESS_KEY,
        aws_secret_access_key=const.SECRET_KEY)'''
ec2_client = boto3.client('ec2')
''', region_name=const.REGION,
        aws_access_key_id=const.ACCESS_KEY,
        aws_secret_access_key=const.SECRET_KEY)'''
ec2_resource = boto3.resource('ec2')
''', region_name=const.REGION,
        aws_access_key_id=const.ACCESS_KEY,
        aws_secret_access_key=const.SECRET_KEY)'''
# pylint: disable=E1101
def get_ec2_ids_state():
    instances = {}
    for instance in ec2_resource.instances.all():
        instances[instance.id] = instance.state['Name']
    return instances
    # response = ec2_client.describe_instances() instance.network_interfaces_attribute.Description['PrivateIpAddress']
    # for reservation in response["Reservations"]:
    #     for instance in reservation["Instances"]:
    #         # This sample print will output entire Dictionary object
    #         # print(instance)
    #         # This will print will output the value of the Dictionary key 'InstanceId'
    #         # print(instance["InstanceId"])
    #         instances.append(instance["InstanceId"])

def create_instance(count):
    ec2_resource.create_instances(
        # BlockDeviceMappings=[
        #     {
        #         'DeviceName': 'Worker',
        #         'VirtualName': 'string',
        #         'Ebs': {
        #             'DeleteOnTermination': True,
        #             'Iops': 123,
        #             'SnapshotId': 'string',
        #             'VolumeSize': 123,
        #             'VolumeType': 'standard'|'io1'|'gp2'|'sc1'|'st1',
        #             'KmsKeyId': 'string',
        #             'Encrypted': False
        #         },
        #         'NoDevice': 'string'
        #     },
        # ],
        ImageId= const.AMI_ID,
        MinCount=1,
        MaxCount=count,
        InstanceType='t2.micro',
        # KeyName=const.KEY_FILENAME,
        Monitoring={
            'Enabled': False
            },
        Placement={
            'AvailabilityZone': const.AVAILABILITY_ZONE,
            },
        # UserData='string',
        DisableApiTermination=False,
        DryRun = False,
        EbsOptimized = False,
        SecurityGroupIds=[
            const.SECURITY_GROUP_ID,
        ],
        # IamInstanceProfile={
        #     'Arn': 'string',
        #     'Name': 'string'
        # },
        InstanceInitiatedShutdownBehavior='stop',
        UserData = script,
    )

# instance_id is a list
def start_instances(instance_id):
    # Do a dryrun first to verify permissions
    try:
        ec2_client.start_instances(InstanceIds=instance_id, DryRun=True)
        ec2_client.run_instances(DryRun=True,MinCount=1,MaxCount=1,UserData=script)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise
    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2_client.start_instances(InstanceIds=instance_id, DryRun=False)
        ec2_client.run_instances(DryRun=False,MinCount=1,MaxCount=1,UserData=script)
        print(response)
    except ClientError as e:
        print(e)

# instance_id is a list
def stop_instances(instance_id):
    # Do a dryrun first to verify permissions
    try:
        ec2_client.stop_instances(InstanceIds=instance_id, DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise
    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2_client.stop_instances(InstanceIds=instance_id, DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

if __name__ == "__main__":
    #create_instance(1)
    #print(script)
    # instances = get_ec2_ids_state()
    # stop_instances([k for k,v in instances.items() if v == 'running'])
    pass
