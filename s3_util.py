import glob
import os
from codecs import lookup

import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime, timezone, timedelta
from global_constants import GlobalConstants
import csv

"""
Upload file objects to S3
"""
# pylint: disable=E1101
const = GlobalConstants()
s3_resource = boto3.resource('s3')
''', region_name=const.REGION,
    aws_access_key_id=const.ACCESS_KEY,
    aws_secret_access_key=const.SECRET_KEY)'''
s3_client = boto3.client('s3')
''', region_name=const.REGION,
    aws_access_key_id=const.ACCESS_KEY,
    aws_secret_access_key=const.SECRET_KEY)'''

# upload videos to s3
# videos is a list
def upload_videos(video_files): # earlier ec2_vids
    content_bucket = s3_resource.Bucket(const.VIDEO_BUCKET)
    for video_file in video_files:
        data = open(video_file, 'rb')
        content_bucket.put_object(Key=os.path.basename(video_file), Body=data)

# upload results to s3
# results is a list
def upload_results(key,value):
    results_bucket = s3_resource.Bucket(const.RESULTS_BUCKET)
    # for result_file in result_files:
        # data = open(result_file, 'rb')
    results_bucket.put_object(Key=key, Body=value)

# download file from s3
def download_video(filename, target_dir):
    try:
        s3_client.download_file(const.VIDEO_BUCKET, filename, os.path.join(target_dir,filename))
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except Exception:
        print("Exception in se_util.download_video()")
    return True

def get_result_time_stamp(filename):
    result_bucket = s3_resource.Bucket(const.RESULTS_BUCKET)
    print(result_bucket)
    # for obj in s3_bucket.objects.all():
    #     pass



if __name__ == "__main__":

    s3_client = boto3.client('s3',
    aws_access_key_id='AKIA23OOWAPBPSRM2BMP',
    aws_secret_access_key='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',
    region_name='us-east-1')

