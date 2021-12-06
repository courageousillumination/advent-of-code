from typing import Counter


def solution(lines):
    vals = [0] * 9

    for z in [int(x) for x in lines[0].split(',')]:
        vals[z] += 1
    
    for i in range(0, 256):
        new_vals = [0] * 9
        for j in range(0, 8):
            new_vals[j] = vals[j+1]
        new_vals[6] += vals[0]
        new_vals[8] += vals[0]
        vals = new_vals
        print(i)
    print(sum(vals))
    
with open('input.txt') as f:
    lines = f.readlines()
    print(solution(lines))