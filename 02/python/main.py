def solution(lines):
    x = 0
    y = 0
    aim = 0
    for z in lines:
        [a, b] = z.split(' ')
        if a == "forward":
            x += int(b)
            y += aim * int(b)
        if a == "down":
            aim += int(b)
        if a == "up":
            aim -= int(b)
        
    print(x * y)


with open('input.txt') as f:
    lines = f.readlines()
    print(solution(lines))