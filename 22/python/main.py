def has_intersection(cube1, cube2):
    [x1, y1, z1] = cube1
    [x2, y2, z2] = cube2
    return ((x2[0] <= x1[1] and x2[1] >= x1[0]) and
            (y2[0] <= y1[1] and y2[1] >= y1[0]) and
            (z2[0] <= z1[1] and z2[1] >= z1[0]))


# [[-27, -23], [-28, -9], [-21, 29]], 
# [[-40,-22], [-38,-28], [23,41]])

def is_valid(cube):
    [[x0, x1], [y0,y1], [z0, z1]] = cube
    return x0 <= x1 and y0 <= y1 and z0 <= z1 
def split_cuboid(cube1, cube2):
    # Split around cube 2. Returns all of the parts of
    # cuboid that do not intersect with cube2


    # Check the X coordinates.

    # Oh, mabye we need to update the cubes left?


    [x1, y1, z1] = cube1
    [x2, y2, z2] = cube2


    new_cubes = []

    

    
    new_cubes.append([[x1[0], x2[0]-1], y1, z1])
    new_cubes.append([[x2[1]+1, x1[1]], y1, z1])
    x1 = [max(x1[0], x2[0]), min(x1[1], x2[1])]

    new_cubes.append([x1, [y1[0], y2[0]-1], z1])
    new_cubes.append([x1, [y2[1]+1, y1[1]], z1])
    y1 = [max(y1[0], y2[0]), min(y1[1], y2[1])]

    # Filter out invalid cubes
    new_cubes = [c for c in new_cubes if is_valid(c)]

    # Intersect middle
    # if x1[0] < x2[0] <= x2[1] < x1[1]:
    #     new_cubes.append([[x1[0], x2[0]-1], y1[:], z1])
    #     new_cubes.append([[x2[1]+1, x1[1]], y1[:], z1])
    #     x1 = [x2[0], x2[1]]
    # elif x1[0] <= (x2[0]-1) and x1[1] <= (x2[1] + 1):
    #     new_cubes.append([[x1[0], x2[0]-1], y1[:], z1])
    #     x1 = [x2[0], x1[1]]
    # elif x1[0] >= (x2[0] - 1) and x1[1] >= (x2[1] + 1):
    #     new_cubes.append([[x2[1] + 1, x1[1]], y1[:], z1])
    #     x1 = [x1[0], x2[1]]
    # else:
    #     # Totally covered, do nothing
    #     pass

    
    # if y1[0] <= (y2[0] -1) <= (y2[1]+1) <= y1[1]:
    #     new_cubes.append([x1, [y1[0], y2[0]-1], z1])
    #     new_cubes.append([x1, [y2[1]+1, y1[1]], z1])
    #     y1 = [y2[0], y2[1]]
    # elif y1[0] <= (y2[0]-1) and y1[1] <= (y2[1] + 1):
    #     new_cubes.append([x1, [y1[0], y2[0]-1], z1])
    #     y1 = [y2[0], y1[1]]
    # elif y1[0] >= (y2[0] - 1) and y1[1] >= (y2[1] + 1):
    #     new_cubes.append([x1, [y2[1] + 1, y1[1]], z1])
    #     y1 = [y1[0], y2[1]]
    # else:
    #     # Totally covered, do nothing
    #     pass
    if z1[0] <= (z2[0] -1) <= (z2[1]+1) <= z1[1]:
        new_cubes.append([x1, y1, [z1[0], z2[0]-1]])
        new_cubes.append([x1, y1, [z2[1]+1, z1[1]]])
    elif z1[0] <= (z2[0]-1) and z1[1] <= (z2[1] + 1):
        new_cubes.append([x1, y1, [z1[0], z2[0]-1],])
    elif z1[0] >= (z2[0] - 1) and z1[1] >= (z2[1] + 1):
        new_cubes.append([x1, y1, [z2[1] + 1, z1[1]]])
    else:
        # Totally covered, do nothing
        pass
    return new_cubes




def solution(lines):
    # print(lines)
    commands = []
    for foo in lines:
        [a, b] = foo.split(" ")
        [x,y,z] = b.split(",")
        x = x[2:].split("..")
        y = y[2:].split("..")
        z = z[2:].split("..")
        x = [int(x[0]), int(x[1])]
        y = [int(y[0]), int(y[1])]
        z = [int(z[0]), int(z[1])]
        command = [a, x, y, z]
        commands.append(command)
    
    cubes = [[[False for _ in range(-50, 51)] for _ in range(-50, 51)] for _ in range(-50, 51)]
    # print(cubes)
    for [a, x, y, z] in commands:
            for x1 in range(max(x[0],-50), min(x[1] + 1, 51)):
                for y1 in range(max(y[0],-50), min(51, y[1] + 1)):
                    for z1 in range(max(z[0],-50), min(51, z[1] + 1)):
                        if x1 > 50 or x1 < -50 or y1 > 50 or y1 < -50 or z1 > 50 or z1 < -50:
                            continue
                        if a == 'on':
                            cubes[x1][y1][z1] = True
                        else:
                            cubes[x1][y1][z1] = False
    count = 0
    for a in range(-50, 51):
        for b in range(-50, 51):
            for c in range(-50, 51):
                if cubes[a][b][c]:
                    count += 1
    print(count)
    
    
    # Part 2

    # print(commands)
    onCuboids = []
    for [a, x, y, z] in commands:
        final_cubes = []
        for cube in onCuboids:
            if has_intersection(cube, [x, y,z]):
                splits = split_cuboid(cube, [x,y,z])
                print(cube, len(splits))
                final_cubes += splits
            else:
                final_cubes.append(cube)
        onCuboids = final_cubes

        if a == 'on':
            onCuboids.append([x, y, z])
        print("new")

    # for c in onCuboids:
    #     print(c)
    count = 0
    for [x,y,z] in onCuboids:
        count += (x[1]-x[0] + 1) * (y[1] - y[0] + 1) * (z[1] - z[0] + 1)
    print(count)

    print(len(onCuboids))
    
    # for a in range(-50, 51):
    #     for b in range(-50, 51):
    #         for c in range(-50, 51):
                
    #             found_in_on = []
    #             for [x,y,z] in onCuboids:
    #                 if x[0] <= a <= x[1] and y[0] <= b <= y[1] and z[0] <= c <= z[1]:
    #                     found_in_on.append([x,y,z])
    #             val = cubes[a][b][c]
    #             if (a,b,c) == (8, -36, -47):
    #                 print(val, found_in_on)
    #             if len(found_in_on) > 1:
    #                 print("Double counted", [a,b,c], found_in_on)
    #                 return
    #             if val and len(found_in_on) == 0:
    #                 print("Expected to find", a, b, c)
    #                 return
    #             if not val and len(found_in_on) > 0:
    #                 print(found_in_on)
    #                 print("Did not expect to find", a, b, c)
    #                 return
                # print(val, found_in_on)
    

with open('input.txt') as f:
    lines = f.readlines()
    solution(lines)

# a = has_intersection([[-27, -23], [-28, -9], [-21, 29]], 
# [[-40,-22], [-38,-28], [23,41]])
# print(a)
# -40..-22,y=-38..-28,z=23..41
# a = split_cuboid([[-20, 26], [-36, -30], [-47, 7]], [[-46,7], [-6,46], [-50,-1]])
# print(a)