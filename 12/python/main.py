from collections import defaultdict


def is_valid_to_visit(node, path):
    # Part 1
    # return (not node.islower() or node not in path)

    # Part 2
    if node == "start":
        return False
    if node == "end":
        return True
    if not node.islower(): # Always allow revisiting upper case
        return True
    lower = [x for x in path if x.islower()]
    if len(lower) == len(set(lower)):
        return True
    return node not in path
     

def explore(nodes, path):
    if path[-1] == "end":
        return [path]
    new_nodes = [x for x in nodes[path[-1]] if is_valid_to_visit(x, path)]
    paths = []
    for node in new_nodes:
        paths += explore(nodes, path + [node])
    
    return paths
    

def solution(lines):
    nodes = defaultdict(lambda: [])
    for line in lines:
        [src, dest] = line.strip().split("-")
        nodes[src].append(dest)
        nodes[dest].append(src)

    
    paths = explore(nodes, ['start'])
    for path in paths:
        print(",".join(path))
    print(len(paths))

with open('input.txt') as f:
    lines = f.readlines()
    solution(lines)