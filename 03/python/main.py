def solution(lines):
    gamma = []
    epsilon = []
    for i in range(0, len(lines[0]) - 1):
        vals = []
        for line in  lines:
            vals.append(line[i])
        # print(vals)
        if vals.count('0') > vals.count('1'):
            gamma.append('0')
            epsilon.append('1')
        else:
            gamma.append('1')
            epsilon.append('0')
    print (''.join(gamma))
    print(''.join(epsilon))

def solution2(lines1):
    lines = lines1
    for i in range(0, len(lines[0]) - 1):
        vals = []
        for line in  lines:
            vals.append(line[i])
        if vals.count('0') > vals.count('1'):
            most_common = '0'
        else:
            most_common = '1'
        lines = [x for x in lines if x[i] == most_common]
        if (len(lines) == 1):
            print(lines[0])
    

    lines = lines1
    for i in range(0, len(lines[0]) - 1):
        vals = []
        for line in  lines:
            vals.append(line[i])
        if vals.count('0') > vals.count('1'):
            most_common = '1'
        else:
            most_common = '0'
        lines = [x for x in lines if x[i] == most_common]
        if (len(lines) == 1):
            print(lines[0])


with open('input.txt') as f:
    lines = f.readlines()
    print(solution2(lines))