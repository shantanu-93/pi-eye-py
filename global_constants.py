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
        # with open(os.path.expanduser('..\\keys\\access.txt'), 'r') as fin:
        #     access_key = fin.readline()
        # with open(os.path.expanduser('..\\keys\\secret.txt'), 'r') as fin:
        #     secret_key = fin.readline()
        self.ACCESS_KEY = 'ASIAVMF4UUFAN7HUL2VP'
        self.SECRET_KEY = 'o9bk6xaR2oeJOL0IFB9XnMtD3059oUJ+5CBiq7Ul'
        self.SESSION_TOKEN = 'FwoGZXIvYXdzEPP//////////wEaDODIc641TjGfReoWHSK9AfQ33Ng53r3D/ClSJQVVqMnJOMwEMCinnsHMJtF9oDYk0E80Q1AYapQqYwR3hAbFzEhCMaKBjA+XNzdnYiLuzRPIC2Thj5OBh7xyHW/v+3PX7HqYOZVFFa5E0MPKhwEtGPrX/zJgJbkFj+0n1WVamtjmIPlzAMVf6NNazmVlVRzIelbopKuohB2LhPZhvqVVyVKfljTEB/nb1st3x5jFFfNeUvyC9YSeUBzE80IB7CqdrLh48rztkQTD3AcoQii1ncvzBTItVA/N7Yek0+V7kwp8/aDLpOlMxjqXN6/0yrx1/Ros7PR/i0cNk32z0+cPM7IB'

if __name__ == '__main__':
    g = GlobalConstants()
    # print(g.ACCESS_KEY)
