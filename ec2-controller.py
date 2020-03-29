import ec2_util as ec2
import queue_util as queue_util
from global_constants import GlobalConstants
# import paramiko as pk
const = GlobalConstants()

if __name__ == "__main__":
    # while True:
    instances = ec2.get_ec2_ids_state()
    active_instances = len(instances)
    watiing_msg_count = int(queue_util.get_msg_count(const.ANALYSIS_QUEUE_URL))
    print(watiing_msg_count)
    if watiing_msg_count>const.MIN_NO_AXN:
        stopped_instances = [k for k,v in instances.items() if v == 'stopped']
        start_count = min(len(stopped_instances), watiing_msg_count-const.MIN_NO_AXN)
        create_count = 0
        if start_count < watiing_msg_count-const.MIN_NO_AXN:
            create_count = watiing_msg_count - const.MIN_NO_AXN - start_count
        if start_count>0:
            ec2.start_instances (stopped_instances [0:start_count])

        if create_count>0 and active_instances<const.MAX_WORKERS:
            ec2.create_instance(min(create_count, const.MAX_WORKERS-active_instances))



        # client = pk.SSHClient()
        # client.set_missing_host_key_policy(pk.AutoAddPolicy())
        # client.connect('x.x.x.x', port=2222, username='user', password='pass')
        # stdin, stdout, stderr = client.exec_command('exit')
        # print(stdout)
        # client.close()
