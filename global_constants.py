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

        