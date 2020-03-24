import re

result = []
b = 0
l=0
flag = 0
obj = {}
with open("demo.txt") as f:

    # contents = f.read()
    # count = sum(1 for match in re.finditer(r"\bObjects\b", contents))

    for line in f:

        l += 1
        # print(l)

        if(re.match(r"\bObjects\b", line)):
            b += 1
            frame = "frame %d" % b
            # print(frame)
            flag = 1

        if(re.search(r'([\w.]+): ([\d.]+)',line)):
            who = re.search(r'([\w.]+): ([\d.]+)', line)
            # print(who.group(1))
            objs = who.group(1)
            # print(who.group(2))
            percentage = who.group(2)
            obj[objs] = percentage
            # print(obj)

        if(re.match(r"\bFPS\b", line) and flag == 1):
            temp = {frame:obj.copy()}
            # print("obj:",obj)
            # print("temp:",temp)
            result.append(temp)
            # print("result:", result)
            flag = 0


print(result)