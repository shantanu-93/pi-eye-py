import ec2_util as ec2
import queue_util as queue_util
from global_constants import GlobalConstants

const = GlobalConstants()

if __name__ == "__main__":
    instances = ec2.get_ec2_ids_state()
    # while True:
    watiing_msg_count = int(queue_util.get_msg_count(const.ANALYSIS_QUEUE))
    print(watiing_msg_count)
    if watiing_msg_count>4:
        stopped_instances = [k for k,v in instances.items() if v == 'stopped']
        start_count = min(len(stopped_instances), watiing_msg_count-4)
        ec2.start_ec2_instances (stopped_instances [0:start_count])
