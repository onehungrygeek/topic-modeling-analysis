import random, json
file_name = input("Enter file name")

d = {}

f = open(file_name , 'r')
line = f.readlines()[0]
for key in line.split(","):
    key = key.strip(" ")
    key = key.strip("\n")
    value = input("Enter value for :{} ".format(key))
    value = value or int(5)
    print(int(value)/10)
    d[key] = int(value)/10

with open(file_name.split(".")[0] + ".json", 'w') as fp:
    json.dump(d, fp)



