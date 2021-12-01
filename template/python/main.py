def solution(lines):
    depths = [int(x) for x in lines]
    increases = 0
    last = depths[0]
    for i in range(1, len(depths)):
        if depths[i] > last:
            increases +=1 
        last = depths[i]
    print(increases)

def solution2(lines):
    depths = [int(x) for x in lines]
    increases = 0
    
    for i in range(3, len(depths)):
        window1 = [depths[i-1], depths[i-2], depths[i-3]]
        window2 = [depths[i], depths[i-2], depths[i-1]]
        if sum(window2) > sum(window1):
            increases +=1 
        
    print(increases)

with open('input.txt') as f:
    lines = f.readlines()
    print(solution2(lines))