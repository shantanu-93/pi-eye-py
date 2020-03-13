import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)
data = open('test_upload.txt', 'rb')
s3.Bucket('content-bucket-546').put_object(Key='test_upload.txt', Body=data)