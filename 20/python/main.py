
def refine(image, algo):
    new_image = [[x for x in row] for row in image]
    for i in range(1, len(image)-1):
        for j in range(1, len(image[i])-1):
            # print(i, j, len(image), len(image[i+1]))
            p1 = image[i-1][j-1]
            p2 = image[i-1][j]
            p3 = image[i-1][j+1]
            p4 = image[i][j-1]
            p5 = image[i][j]
            p6 = image[i][j+1]
            p7 = image[i+1][j-1]
            p8 = image[i+1][j]
            p9 = image[i+1][j+1]

            
            b = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9

            # print(b)
            # print(b)
            c = ''.join(['0' if x == '.' else '1' for x in b])
            indx = int(c,2)

            # print(c, indx, algo[indx])
            # print(indx, c)
            # print(algo)
            new_image[i][j] = algo[indx]
    
    next = '#' if new_image[0][0] == '.' else "."
    print(next)
    for j in range(len(new_image)):
        new_image[j][0] = next
        new_image[j][-1] = next
    new_image[0] = [next for _ in range(len(new_image[0]))]
    new_image[-1] = [next for _ in range(len(new_image[0]))]

    return new_image
           
            
def solution(lines):
    algo = lines[0]
    image = [[y for y in x.strip()] for x in lines[2:]]
    # expand image for infinite plane
    # for x in range(0, 10):
    for i in range(len(image)):
        image[i] = ["."] * 100 + image[i] + ["."] * 100
    image_line_length = len(image[0])
    for i in range(100):
        image.insert(0, ["."] * image_line_length)
        image.append(["."] * image_line_length)
    
    new_image = image
    for _ in range(50):
        new_image = refine(new_image, algo)
    
    count = 0
    for x in new_image:
        for y in x:
            if y == '#':
                count += 1
    print(count)

with open('input.txt') as f:
    lines = f.readlines()
    solution(lines)
   