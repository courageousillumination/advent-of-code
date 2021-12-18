target = [[79,137], [-176,-117]]
# target = [[20, 30], [-10, -5]]

def run_trajectory(dx, dy):
    x, y = (0, 0)
    in_range = False
    max_height = 0
    for step in range(10000):
        # print(x, y, dx, dy)
        x += dx
        y += dy
        max_height = max([y, max_height])
        
        if dx != 0:
            dx += 1 if dx < 0 else -1
        dy -= 1
        if (target[0][0] <= x <= target[0][1] and target[1][0] <= y <= target[1][1]):
            
            in_range = True
        
        if x > target[0][1]:
            break
        
        if y < target[1][0]:
            break
    return in_range, max_height

def solution(lines):
    best = 0
    count = 0
    for x in range(0, 1000):
        for y in range(-1000, 1000):
            in_range, max_height = run_trajectory(x, y)
            
            if in_range:
                count += 1
                if best < max_height:
                    print((x,y), max_height)
                    best = max([max_height, best])
                print(count)

with open('input.txt') as f:
    lines = f.readlines()
    solution(lines)