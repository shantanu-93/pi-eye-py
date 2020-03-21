import boto3
import os
from global_constants import GlobalConstants
"""
Upload video file objects to S3
"""
const = GlobalConstants()
def upload_videos(video_files):
    s3 = boto3.resource('s3', region_name=const.REGION,
            aws_access_key_id=const.ACCESS_KEY,
            aws_secret_access_key=const.SECRET_KEY)
    content_bucket = s3.Bucket(const.VIDEO_BUCKET)
    for video_file in video_files:
        data = open(video_file, 'rb')
        content_bucket.put_object(Key=os.path.basename(video_file), Body=data)

def upload_results(result_files):
    # s3 = boto3.resource('s3')
    s3 = boto3.resource('s3', region_name=const.REGION,
        aws_access_key_id=const.ACCESS_KEY,
        aws_secret_access_key=const.SECRET_KEY)
    results_bucket = s3.Bucket(const.RESULTS_BUCKET)
    for result_file in result_files:
        data = open(result_file, 'rb')
        results_bucket.put_object(Key=result_file, Body=data)

# download from s3
def download_video(filename, target_dir):
    s3 = boto3.client('s3', region_name=const.REGION,
        aws_access_key_id=const.ACCESS_KEY,
        aws_secret_access_key=const.SECRET_KEY)
    s3.download_file(const.VIDEO_BUCKET, filename, os.path.join(target_dir,filename))

if __name__ == "__main__":
    upload_videos(['./analysis_queue_videos/record.h264'])
    download_video('record.h264', './analysis_queue_videos')



