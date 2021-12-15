
def adjust_value(val, i):
    res = (val + i)
    if res >= 10:
        return (res % 10) + 1
    return res

def expand_grid(grid):
    result = []

    for j in range(0, 5):
        tile00 =  [[adjust_value(x, j) for x in row] for row in grid]
        tile01 = [[adjust_value(x, 1+j) for x in row] for row in grid]
        tile02 = [[adjust_value(x, 2+j) for x in row] for row in grid]
        tile03 = [[adjust_value(x, 3+j) for x in row] for row in grid]
        tile04 = [[adjust_value(x, 4+j) for x in row] for row in grid]
        row1 = [tile00[i] + tile01[i] + tile02[i] + tile03[i] + tile04[i] for i in range(len(tile00))]
        for row in row1:
            result.append(row)
    return result

def solution(lines):
    grid = [[int(x) for x in row.strip()] for row in lines]
    run_grid(grid)
    run_grid(expand_grid(grid))


def run_grid(grid):
    min_cost = [[float('inf') for x in row] for row in grid]
    updated = True
    min_cost[0][0] = 0
    while updated:
        updated = False
        for i in range(0, len(grid)):
            for j in range(0, len(grid)):
                values = []
                if i > 0:
                    left = min_cost[i-1][j] + grid[i][j]
                    values.append(left)
                if i < len(grid) - 1:
                    right = min_cost[i+1][j] + grid[i][j]
                    values.append(right)
                if j > 0:
                    top = min_cost[i][j-1] + grid[i][j]
                    values.append(top)
                if j < len(grid) - 1:
                    bottom = min_cost[i][j+1] + grid[i][j]
                    values.append(bottom)
                for x in values:
                    if x < min_cost[i][j]:
                        min_cost[i][j] = x
                        updated = True
    print(min_cost[-1][-1])



with open('input.txt') as f:
    lines = f.readlines()
    solution(lines)