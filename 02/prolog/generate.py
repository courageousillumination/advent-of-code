import json
# Generate the command list [["up|down|forward", NUMBER]]
with open('input.txt') as f:
    lines = f.readlines()
    val = [[x.split(' ')[0], int(x.split(' ')[1])] for x in lines]
    val.reverse()
    print(json.dumps(val))