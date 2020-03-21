import boto3
import queue_util as queue_util
import global_constants
from botocore.exceptions import ClientError

const = global_constants.GlobalConstants()

sqs = boto3.client('sqs', region_name=const.REGION,
        aws_access_key_id=const.ACCESS_KEY,
        aws_secret_access_key=const.SECRET_KEY)
ec2_client = boto3.client('ec2', region_name=const.REGION,
        aws_access_key_id=const.ACCESS_KEY,
        aws_secret_access_key=const.SECRET_KEY)
ec2_resource = boto3.resource('ec2', region_name=const.REGION,
        aws_access_key_id=const.ACCESS_KEY,
        aws_secret_access_key=const.SECRET_KEY)

def get_ec2_ids_state():
    instances = {}
    for instance in ec2_resource.instances.all():
        instances[instance.id] = instance.state['Name']
    return instances
    # response = ec2_client.describe_instances()
    # for reservation in response["Reservations"]:
    #     for instance in reservation["Instances"]:
    #         # This sample print will output entire Dictionary object
    #         # print(instance)
    #         # This will print will output the value of the Dictionary key 'InstanceId'
    #         # print(instance["InstanceId"])
    #         instances.append(instance["InstanceId"])

# instance_id is a list
def start_ec2_instances(instance_id):
    # Do a dryrun first to verify permissions
    try:
        ec2_client.start_instances(InstanceIds=instance_id, DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise
    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2_client.start_instances(InstanceIds=instance_id, DryRun=False)
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
