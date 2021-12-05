def get_lines(text_lines):
    lines = []
    for txt in text_lines:
        [start, end] = txt.split(' -> ')
        [x1, y1] = start.split(',')
        [x2, y2] = end.split(',')
        lines.append(((int(x1), int(y1)), (int(x2), int(y2))))
    return lines

def is_non_diagonal(line):
    return line[0][0] == line[1][0] or line[0][1] == line[1][1]


def generate_points(line):
    if line[0][0] == line[1][0]:
        return [(line[0][0], y) for y in range(line[0][1], line[1][1] + 1)]
    elif line[0][1] == line[1][1]:
        return [(x, line[0][1]) for x in range(line[0][0], line[1][0] + 1)]
    else:
        y_dir = 1 if line[0][1] < line[1][1] else -1 
        points = [(line[0][0] + d, line[0][1] + d * y_dir) for d in range(0, line[1][0] - line[0][0] + 1)]
        return points

def intersection_points(l1, l2):
    p1 = set(generate_points(l1))
    p2 = set(generate_points(l2))
    return p1.intersection(p2)

def solution(text_lines):
    lines = [sorted(x) for x in get_lines(text_lines)]
    points = [generate_points(x) for x in lines]
    # print(points)
    point_set = set()
    intersect_set = set()
    for ps in points:
        for point in ps:
            if point in point_set:
                intersect_set.add(point)
            point_set.add(point)
    
    return len(intersect_set)

with open('input.txt') as f:
    lines = f.readlines()
    print(solution(lines))