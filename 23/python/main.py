import functools

def target_col(grid, x, target_col):
    no_path = False
    if x < target_col:
        for x in range(x + 1, target_col):
            if grid[0][x] != '.':
                no_path = True
    else:
        for x in range(target_col, x):
            if grid[0][x] != '.':
                no_path = True   
    if no_path:
        return []
    if grid[2][target_col] == '.':
        return [(target_col, 2)]
    return [(target_col, 1)]

def explore_moves(grid, pos):
    (x,y) = pos
    valid_moves = []

    if grid[y][x] == 'D' and x == 8:
        return []
    if grid[y][x] == 'C' and x == 6:
        return []
    if grid[y][x] == 'B' and x == 4:
        return []
    if grid[y][x] == 'A' and x == 2:
        return []
        
    if y == 2:
        if grid[y-1][x] != '.':
            return [] # Fully blocked
        return explore_moves(grid, (x, y-1))
    if y == 1:
        valid_x_left = x - 1
        while valid_x_left >= 0:
            if valid_x_left == 2 or valid_x_left == 4 or valid_x_left == 6 or valid_x_left == 8:
                valid_x_left -= 1
            if (grid[0][valid_x_left] == '.'):
                valid_moves.append((valid_x_left, y-1))
                valid_x_left -= 1
            else:
                break
        valid_x_left = x + 1
        while valid_x_left < len(grid[0]):
            if valid_x_left == 2 or valid_x_left == 4 or valid_x_left == 6 or valid_x_left == 8:
                valid_x_left += 1
            if (grid[0][valid_x_left] == '.'):
                valid_moves.append((valid_x_left, y-1))
                valid_x_left += 1
            else:
                break
    if y == 0:
        if grid[y][x] == 'D':
            return target_col(grid, x, 8)
        if grid[y][x] == 'C':
            return target_col(grid, x, 6)
        if grid[y][x] == 'B':
            return target_col(grid, x, 4)
        if grid[y][x] == 'A':
            return target_col(grid, x, 2)
    return valid_moves

def make_move(grid, pos1, pos2):
    g = [[x for x in row] for row in grid]
    (x1, y1) = pos1
    (x2, y2) = pos2
    g[y2][x2] = grid[y1][x1]
    g[y1][x1] = '.'
    return g


def check_column(grid, col, val):
    for y in range(1, len(grid)):
        if grid[y][col] != val:
            return False
    return True
def is_done(grid):


    return (grid[1][2] == grid[2][2] == 'A' and
            grid[1][4] == grid[2][4] == 'B' and
            grid[1][6] == grid[2][6] == 'C' and
            grid[1][8] == grid[2][8] == 'D')

OPTIMAL = 20000

def grid_to_string(grid):
    return '\n'.join([' '.join(x) for x in grid])

def string_to_grid(str):
    return [x.split(' ') for x in str.split('\n')]

@functools.lru_cache(maxsize=None)
def get_optimal_grid(grid):
    grid = string_to_grid(grid)
    # if move_count >= 10:
    #     print(grid)
    # if currentCost > 20000 or move_count > 20:
    #     return 20000 # Not the best

    if is_done(grid):
        return 0

    
    
    optimal = 20000
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            char = grid[y][x]
            if char != '#' and char != '.':
                moves = explore_moves(grid, (x,y))
                # if char == 'D':
                #     print(moves, (x,y))
                # print(moves)
                for move in moves:
                    # if (move_count <= 1):
                    #     print("in here", move_count, len(moves))
                    g1 = make_move(grid, (x, y), move)
                    if char == 'A':
                        mult = 1
                    elif char == 'B':
                        mult = 10
                    elif char == 'C':
                        mult = 100
                    else:
                        mult = 1000
                    cost = (abs(x - move[0]) + abs(y - move[1])) * mult
                    best = cost + get_optimal_grid(grid_to_string(g1))
                    optimal = min(best, optimal)
                    global OPTIMAL
                    # if (optimal < OPTIMAL):
                    #     print("Got new optimal", optimal)
                    #     OPTIMAL = optimal
                    
    return optimal
def solution(lines):

    grid = [
        ['.','.','.','.','.','.','.','.','.','.','.'],
        ['#','#','D','#','C','#','A','#','B','#','#'],
        ['#','#','D','#','C','#','B','#','A','#','#'],
        ['#','#','D','#','B','#','A','#','C','#','#'],
        ['#','#','D','#','C','#','B','#','A','#','#']
    ]

    # grid = [
    #     ['.','.','.','.','.','.','.','D','.','.','.'],
    #     ['#','#','A','#','B','#','C','#','.','#','#'],
    #     ['#','#','A','#','B','#','C','#','D','#','#']
    # ]

    print(get_optimal_grid(grid_to_string(grid)))

    
    


    # CLear room 2

with open('input.txt') as f:
    lines = f.readlines()
    solution(lines)
