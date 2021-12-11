
def solution(lines):
    grid = [[int(y) for y in x.strip()] for x in lines]
    for row in grid:
        row.append(-float('infinity'))
        row.insert(0, -float('infinity'))
    grid.append([-float('infinity') for _ in grid[0]])
    grid.insert(0, [-float('infinity') for _ in grid[0]])
    flashes = 0
    gen = 0
    while True:
        gen += 1
        print(gen)
        # for row in grid:
        #     print(''.join([str(x) for x in row]))
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                grid[i][j] += 1
        has_flashed = True
        flashed = []
        while has_flashed:
            
            has_flashed = False
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    
                    if grid[i][j] > 9 and not (i,j) in flashed:
                        
                        flashes += 1
                        flashed.append((i,j))
                        grid[i-1][j-1] += 1
                        grid[i-1][j] += 1
                        grid[i-1][j+1] += 1
                        grid[i][j-1] += 1
                        grid[i][j] += 1
                        grid[i][j+1] += 1
                        grid[i+1][j-1] += 1
                        grid[i+1][j] += 1
                        grid[i+1][j+1] += 1
                        has_flashed = True
                if has_flashed:
                    break
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (grid[i][j] > 9):

                    grid[i][j] = 0
        
        if (len(flashed) == 100):
            print(gen)
            return
    print(flashes)
    
with open('input.txt') as f:
    lines = f.readlines()
    print(solution(lines))