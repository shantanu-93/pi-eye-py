import boto3
from global_constants import GlobalConstants
"""
Upload video file objects to S3
"""
def upload_videos(video_files):
    s3 = boto3.resource('s3')
    content_bucket = s3.Bucket(GlobalConstants.VIDEO_BUCKET)
    for video_file in video_files:
        data = open(video_file, 'rb')
        content_bucket.put_object(Key=video_file, Body=data)

def upload_results(result_files):
    s3 = boto3.resource('s3')
    results_bucket = s3.Bucket(GlobalConstants.RESULTS_BUCKET)
    for result_file in result_files:
        data = open(result_file, 'rb')
        results_bucket.put_object(Key=result_file, Body=data)

