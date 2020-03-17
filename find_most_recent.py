import os

def allFilesIn(b='.'):
    result = []
    for d in os.listdir(b):
        bd = os.path.join(b, d)
        result.append(bd)
    return result
# print(allFilesIn('.\\record_videos'))
# latest_subdir = max(allFilesIn('.\\record_videos'), key=os.path.getmtime)

# print(latest_subdir)
