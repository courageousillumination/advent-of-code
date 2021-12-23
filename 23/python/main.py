import functools

def target_col(grid, x, target_col, val):
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

    for y in range(len(grid)-1, 0, -1):
        v = grid[y][target_col]
        if v != '.' and v != val:
            return [] # Don't go in, it's not empty
    
    for y in range(len(grid)-1, 0, -1):
        if grid[y][target_col] == '.':
            return [(target_col, y)]

    print("Never happens")

def explore_moves(grid, pos, val):
    (x,y) = pos
    valid_moves = []

    if val == 'D' and x == 8 and check_column(grid, 8, 'D',True):
        return []
    if val == 'C' and x == 6 and  check_column(grid, 6, 'C',True):
        return []
    if val == 'B' and x == 4 and check_column(grid, 4, 'B', True):
        return []
    if val == 'A' and x == 2 and check_column(grid, 2, 'A', True):
        return []

    if y >= 2:
        if grid[y-1][x] != '.':
            return [] # Fully blocked
        return explore_moves(grid, (x, y-1), val)
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
    
    if val == 'D':
        end_pos = target_col(grid, x, 8, 'D')
    elif val == 'C':
        end_pos = target_col(grid, x, 6, 'C')
    elif val == 'B':
        end_pos = target_col(grid, x, 4, 'B')
    elif val == 'A':
        end_pos = target_col(grid, x, 2, 'A')
    
    
    if y == 0:
        return end_pos
    return valid_moves + end_pos

def make_move(grid, pos1, pos2):
    g = [[x for x in row] for row in grid]
    (x1, y1) = pos1
    (x2, y2) = pos2
    g[y2][x2] = grid[y1][x1]
    g[y1][x1] = '.'
    return g


def check_column(grid, col, val, partial=False):
    for y in range(1, len(grid)):
        v = grid[y][col]
        if partial:
            if v != val and v != '.':
                return False
        else:
            if v != val:
                return False
    return True

def is_done(grid):
    return (check_column(grid, 2, 'A') and
            check_column(grid, 4, 'B')and
            check_column(grid, 6, 'C') and
            check_column(grid, 8, 'D'))

def grid_to_string(grid):
    return '\n'.join([' '.join(x) for x in grid])

def string_to_grid(str):
    return [x.split(' ') for x in str.split('\n')]

@functools.lru_cache(maxsize=None)
def get_optimal_grid(grid):
    grid = string_to_grid(grid)
    if is_done(grid):
        print("Finished!")
        return 0
    optimal = float("infinity")
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            char = grid[y][x]
            if char != '#' and char != '.':
                # print(grid[y][x])
                moves = explore_moves(grid, (x,y), char)
                for move in moves:
                    g1 = make_move(grid, (x, y), move)
                    if char == 'A':
                        mult = 1
                    elif char == 'B':
                        mult = 10
                    elif char == 'C':
                        mult = 100
                    else:
                        mult = 1000

                    x_cost = abs(x - move[0])
                    y_cost = y + move[1]
                    cost = (x_cost + y_cost) * mult # Needs to be recomputed
                    best = cost + get_optimal_grid(grid_to_string(g1))
                    optimal = min(best, optimal)
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
    #     ['.','.','.','.','.','.','.','.','.','.','.'],
    #     ['#','#','B','#','C','#','B','#','D','#','#'],
    #     ['#','#','D','#','C','#','B','#','A','#','#'],
    #     ['#','#','D','#','B','#','A','#','C','#','#'],
    #     ['#','#','A','#','D','#','C','#','A','#','#']
    # ]

    grid = [
        ['.','.','.','.','.','.','.','.','.','.','.'],
        ['#','#','B','#','A','#','C','#','D','#','#'],
        ['#','#','A','#','B','#','C','#','D','#','#']
    ]

    print(get_optimal_grid(grid_to_string(grid)))

    
    


    # CLear room 2

with open('input.txt') as f:
    lines = f.readlines()
    solution(lines)
