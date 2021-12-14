from collections import defaultdict

def fold_up(input_points, at):
    result = []
    for (x,y) in input_points:
        if y < at:
            result.append((x,y))
        else:
            result.append((x, at - (y - at)))
    return result

def fold_left(input_points, at):
    result = []
    for (x,y) in input_points:
        if x < at:
            result.append((x,y))
        else:
            result.append((at - (x - at), y))
    return list(set(result))

def solution(lines):
   print(lines)
   [input_points, instructions] = (lines).split('\n\n')
   input_points = [x.split(",") for x in input_points.split("\n")]
   input_points = [(int(x), int(y)) for [x,y] in input_points]

   instructions = [x.split("=") for x in instructions.split("\n")]
   instructions = [(x[-1], int(y)) for x,y in instructions]
   print(instructions)

   for dir, at in instructions:
       if dir == 'x':
           input_points = fold_left(input_points, at)
        
       if dir == 'y':
           input_points = fold_up(input_points, at)
   max_x = max(x for (x, _) in input_points)
   max_y = max(x for (_, x) in input_points)
   for y in range(max_y+1):
       for x in range(max_x+1):
           if (x,y) in input_points:
               print("#", end="")
           else:
                print(".", end="")
       print("\n", end="")

   
#    grid = [[False for x in range(2000)] for y in range(2000)]
#    for x,y in input_points:
#        grid[x][y] = True
#    print(grid)

with open('input.txt') as f:
    lines = f.read()
    solution(lines)