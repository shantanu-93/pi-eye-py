from re import search
# from os.path import isfile

# out is string
def parse_result(out): 
    objs = []
    # if isfile(file):
    #     with open(file) as f:
    op = out.decode().split("\n")
    for line in op:
        if(search(r'([\w.]+): ([\d.]+)',line)):
            who = search(r'([\w.]+): ([\d.]+)', line)
            if who.group(1) not in objs:
                objs.append(who.group(1))
    return ','.join(str(s) for s in objs)

if __name__ == '__main__':
<<<<<<< HEAD
    a = 'demo.txt'
    r = parse_result(a)
    print("r:" + r)
    # r = parse_result('/home/shantanu/pi-eye-py/pi_results/2020-03-25_04.37.54_result.txt')
    # print(r)
    # r = parse_result('/home/shantanu/pi-eye-py/pi_results/2020-03-25_04.38.51_result.txt')
    # print(r)
    # r = parse_result('/home/shantanu/pi-eye-py/pi_result/2020-03-25_04.38.51_result.txt')
    # print(r)
=======
    pass
>>>>>>> 4c1210a0a5dcc996f5ed445e84358725138db011
