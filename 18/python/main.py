import math
class SnailFish:
    children = []
    parent = None

def find_first_explode(snail_fish, depth=0):
    print(snail_fish)
    if not isinstance(snail_fish, SnailFish):
        return None
    if depth == 3:
        return snail_fish
    for child in snail_fish.children:
        explode = find_first_explode(child, depth + 1)
        if explode:
            return explode
    return None


def add_right(snail_fish, x):
    last_child = snail_fish.children[-1]
    if isinstance(last_child, SnailFish):
        add_right(last_child, x)
    else:
        snail_fish.children[-1] = last_child + x

def add_left(snail_fish, x):
    last_child = snail_fish.children[0]
    if isinstance(last_child, SnailFish):
        add_left(last_child, x)
    else:
        snail_fish.children[0] = last_child + x
    
def do_explode(snail_fish):
    node = find_first_explode(snail_fish)
    if node is not None:
        parent = node.parent
        i = parent.children.index(node)
        if i -1> 0:

            if isinstance(parent.children[0], SnailFish):
                add_right(parent.children, node.children[1])
            else:
                parent.children[1] = node.children[0]
        if i + 1< 2:
            if isinstance(parent.children[1], SnailFish):
                add_left(parent.children, node.children[1])
            else:
                parent.children[1] = node.children[1]


def to_tree(snail_fish):
    if not isinstance(snail_fish, list):
        return snail_fish
    root = SnailFish()
    for x in snail_fish:
        child = to_tree(x)
        if isinstance(child, SnailFish):
            child.parent = root
        root.children.append(child)
    return root

def to_list(snail_fish):
    if not isinstance(snail_fish, SnailFish):
        return snail_fish
    return [x for x in to_list(snail_fish)]

def reduce_snail_fish(snail_fish, depth=0):
    
    do_explode(snail_fish)
    print(to_list(snail_fish))
    return snail_fish


def explode_list(root):
    indicies = [0]
    current = root
    depth = 0
    last_left = None
    add_to_next = None
    to_finish = None

    while len(indicies):
        value = current[indicies[-1]]
        if isinstance(value, list):
            current = value
            indicies.append(0)
            depth += 1
        else:
            if add_to_next is not None:
                lr = root
                for x in indicies[:-1]:
                    lr = lr[x]

                lr[indicies[-1]] = lr[indicies[-1]]+ add_to_next
                to_finish[0][to_finish[1]] = 0
                return True
            
            if depth >= 4:
                

                c1 = root
                
                for x in indicies[:-1]:
                    c1 = c1[x]
                exploded = c1
                
                parent = root
                for x in indicies[:-2]:
                    parent = parent[x]
                # Go find the first number on the left
                
                if last_left is not None:
                    lp = root
                    for x in last_left[:-1]:
                        lp = lp[x]
                    # print(lp)
                    lp[last_left[-1]] = lp[last_left[-1]]+ exploded[0]

                # keep going right as far as we can.
                add_to_next = exploded[1]

                
                # Update the exploded pair
                to_finish = parent, indicies[-2]
                indicies[-1] = 1
            last_left = indicies[:]
            indicies[-1] += 1
            while indicies[-1] > 1:
                indicies.pop()
                if len(indicies) == 0:
                    break
                depth -= 1
                indicies[-1] += 1
                current = root
                for x in indicies[:-1]:
                    current = current[x]
    if to_finish is not None:
        to_finish[0][to_finish[1]] = 0
        return True
    return False
        
def split(root):
    for i in range(len(root)):
        if isinstance(root[i], int):
            if root[i] >= 10:
                root[i] = [math.floor(root[i] / 2), math.ceil(root[i] /2)]
                return True
        else:
            has_split = split(root[i])
            if has_split:
                return True
    
    return False
            
def magnitude(root):
    if not isinstance(root, list):
        return root
    return 3 * magnitude(root[0]) + 2 * magnitude(root[1])             
        

def add_vals(a, b):
    c = [a, b]
    reduced = True
    while reduced:
        reduced = explode_list(c) or split(c)
    return c

def solution(lines):
    a = add_vals(lines[0], lines[1])
    print(a)
    for i in range(2, len(lines)):
        a = add_vals(a, lines[i])
        print(a)
    print(magnitude(a))

def deep_copy(x):
    if not isinstance(x, list):
        return x
    return [deep_copy(y) for y in x]

def solution2(lines):
    max_val = 0
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            mag = magnitude(add_vals(deep_copy(lines[i]), deep_copy(lines[j])))
            max_val = max([mag, max_val])
            mag = magnitude(add_vals(deep_copy(lines[j]), deep_copy(lines[i])))
            max_val = max([mag, max_val])
            print(mag)
    print(max_val)



with open('input.txt') as f:
    lines = f.readlines()
    solution2(lines)

