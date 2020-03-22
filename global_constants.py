import os
class GlobalConstants:

    def __init__(self):
        # S3 buckets
        self.VIDEO_BUCKET = 'content-bucket-546'
        self.RESULTS_BUCKET = 'results-bucket-546'
        # Queue names
        self.UPLOAD_QUEUE = 'content-upload-q.fifo'
        self.ANALYSIS_QUEUE = 'video-analysis-q.fifo'
        self.DELETE_QUEUE = 'content-deletion-q.fifo'
        self.MONITOR_QUEUE = 'ec2-monitor-q.fifo'
        self.SHUTDOWN_QUEUE = 'ec2-shutdown-q.fifo'
        #
        self.REGION = 'us-east-1'
        with open(os.path.expanduser('~/keys/access.txt'), 'r') as fin:
            access_key = fin.readline()
        with open(os.path.expanduser('~/keys/secret.txt'), 'r') as fin:
            secret_key = fin.readline()
        self.ACCESS_KEY = access_key
        self.SECRET_KEY = secret_key

        # minimum number of requests above which to create a new instance
        self.MIN_NO_AXN = 4
        # maximum number of worker instances
        self.MAX_WORKERS = 19
        # AMI image to create new instances
        self.AMI_ID = 'ami-0903fd482d7208724'

        ################ CONFIGURABLE PARAMS - CHANGE AS PER YOUR EC2 ###################
        # Security Group of your master
        self.SECURITY_GROUP_ID = 'sg-0ad9dd43f69b8fbe4'
        # key file of master server
        ## Change as per your key
        self.KEY_FILENAME = 'sg_ec2_key'
