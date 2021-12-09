def solution(lines):
    lines = [[int(y) for y in x.strip()] for x in lines]
    total = 0
    low_points = []
    for i in range(0, len(lines)):
        for j in range(0, len(lines[i])):
            val = (lines[i][j])
            up = (lines[i-1][j]) if i > 0 else 10
            down = (lines[i+1][j]) if i < len(lines) -1 else 10
            left = (lines[i][j-1]) if j > 0 else 10
            right = (lines[i][j + 1]) if j < len(lines[i]) - 1 else 10
            if val < up and val < down and val < left and val < right:
                total += val + 1
                low_points.append((i, j))
    print(total) # part 1
    
    sizes = []
    for low_point in low_points:
        points_to_check = [low_point]
        points_checked = []


        while len(points_to_check):
            (i,j) = points_to_check.pop()

            val = lines[i][j]
            up = (lines[i-1][j]) if i > 0 else 10
            down = (lines[i+1][j]) if i < len(lines) -1 else 10
            left = (lines[i][j-1]) if j > 0 else 10
            right = (lines[i][j + 1]) if j < len(lines[i]) - 1 else 10

            if up > val and up < 9:
                points_to_check.append((i-1, j))
            
            if down > val and down < 9:
                points_to_check.append((i+1, j))
            
            if left > val and left < 9:
                points_to_check.append((i, j-1))
            
            if right > val and right < 9:
                points_to_check.append((i, j+1))
            
            points_checked.append((i,j))
            points_to_check = [x for x in points_to_check if not x in points_checked]
        
        sizes.append(len(points_checked))
    [a,b,c] =sorted(sizes)[-3:]
    print(a * b * c) # part 2

with open('input.txt') as f:
    lines = f.readlines()
    print(solution(lines))