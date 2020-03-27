from re import search
from os.path import isfile

def parse_result(file):
    objs = []
    if isfile(file):
        with open(file) as f:
            for line in f:
                if(search(r'([\w.]+): ([\d.]+)',line)):
                    who = search(r'([\w.]+): ([\d.]+)', line)
                    if who.group(1) not in objs:
                        objs.append(who.group(1))
    return ','.join(str(s) for s in objs)

if __name__ == '__main__':
    r = parse_result('/home/shantanu/pi-eye-py/pi_results/2020-03-25_04.38.32_result.txt')
    print(r)
    r = parse_result('/home/shantanu/pi-eye-py/pi_results/2020-03-25_04.37.54_result.txt')
    print(r)
    r = parse_result('/home/shantanu/pi-eye-py/pi_results/2020-03-25_04.38.51_result.txt')
    print(r)
    r = parse_result('/home/shantanu/pi-eye-py/pi_result/2020-03-25_04.38.51_result.txt')
    print(r)
    