from re import search
# from os.path import isfile

# out is string
def parse_result(out): 
    objs = []
    # if isfile(file):
    #     with open(file) as f:
    for line in out:
        if(search(r'([\w.]+): ([\d.]+)',line)):
            who = search(r'([\w.]+): ([\d.]+)', line)
            if who.group(1) not in objs:
                objs.append(who.group(1))
    return ','.join(str(s) for s in objs)

if __name__ == '__main__':
    pass