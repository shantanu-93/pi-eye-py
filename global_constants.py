class GlobalConstants:

    def __init__(self):
        # S3 buckets
        self.VIDEO_BUCKET = 'content-bucket-546'
        self.RESULTS_BUCKET = 'results-bucket-546'
        # Queue names
        self.CONTENT_QUEUE = 'content-upload-q'
        self.ANALYSIS_QUEUE = 'video-analysis-q'
        self.DELETE_QUEUE = 'content-deletion-q'
        self.MONITOR_QUEUE = 'ec2-monitor-q'
        self.SHUTDOWN_QUEUE = 'ec2-shutdown-q'
        #
                
        