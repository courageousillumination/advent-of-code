import math
class SnailFish:
    children = []
    parent = None


# def find_first_depth(snail)


# def maybe_explode(snail_fish, depth=1):
#     if depth == 3:
#         return True
#     for i in range(snail_fish):
#         if isinstance(snail_fish, list):
#             if depth == 2:

            # if maybe_explode(snail_fish[i], depth +1):
            #     pass


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

            # add_right(parent.children[i-1], node.children[0])
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

    # for x in snail_fish:
    #     pass


    # for i in range(snail_fish):
    #     if isinstance(snail_fish, list):
    #         maybe_explode(snail_fish[i])





def explode_list(root):
    indicies = [0]
    current = root
    depth = 0
    last_left = None
    add_to_next = None
    to_finish = None

    while len(indicies):
        # print(current, indicies)
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

                # print(lr)
                lr[indicies[-1]] = lr[indicies[-1]]+ add_to_next
                to_finish[0][to_finish[1]] = 0
                return True
            
            if depth >= 4:
                # print("Oh no, explode!")
                # Go up a level
                # exploded = 

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
                # parent[indicies[-2]] = 0

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
                # print(indicies, root)
                for x in indicies[:-1]:
                    current = current[x]
    # print("fishing", to_finish)
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

# def explode_string(x):
#     depth = 0
#     for i in range(len(x)):
#         char = x[i]
#         print(char, depth)
#         if char == '[':
#             depth += 1
#         elif char == ']':
#             depth -= 1
#         elif char == ',':
#             pass
#         else:
            
#             if depth > 4:
#                 # print(i, x)
#                 # left = x[:i-1]
                
#                 left = x[:i]
#                 left_num = int(x[i:].split(',')[0])
#                 right_num = int(x[i:].split(',')[1].split(']')[0])
#                 try:
#                     right = x[i:].split(',', 2)[2]
#                 except:
#                     right = ']' + x[i:].split(']', 1)[-1]
#                 print("right", right, x[i:], i)
#                 print("left", left)
                
                
#                 new_left = ""
#                 for j in range(len(left) -1, 0, -1):
#                     char = left[j]
#                     if char != '[' and char != ']' and char != ',':
#                         left_num = int(left[:j+1].split("[")[-1]) + left_num
#                         print(left[:j+1], new_left, left)
#                         new_left = left[:j] + str(left_num) + new_left
#                         break
#                     else:
#                         new_left = char + new_left
                
#                 new_right = ""
#                 for j in range(len(right)):
#                     char = right[j]
#                     if char != '[' and char != ']' and char != ',':
#                         print(right, j)
#                         right_num = int(right[j:].split("]")[0]) + right_num
#                         new_right = new_right +   str(right_num) + "]" + right[j:].split("]",1)[-1]
#                         break
#                     else:
#                         new_right = char + new_right
#                 print(new_left, new_right)
#                 # print(new_left + "0" + new_right)
#                 # for j in range(len(right)):
#                 #     char = right[j]
#                 #     if char != '[' and char != ']' and char != ',':
#                 #         right[j] = int(right[j]) + int(right_num)
#                 #         break
#                 return x


def solution(lines):
    snail_fish = lines
    # for x in lines:
    #     try:
    #         snail_fish.append((eval(x)))
    #     except:
    #         print(x)
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
            # deep_copy = []
            mag = magnitude(add_vals(deep_copy(lines[i]), deep_copy(lines[j])))
            max_val = max([mag, max_val])
            mag = magnitude(add_vals(deep_copy(lines[j]), deep_copy(lines[i])))
            max_val = max([mag, max_val])
            print(mag)
    print(max_val)

    # print(a)


# with open('input.txt') as f:
#     lines = f.readlines()
#     solution(lines)

lines = [
    [[2,[[4,8],7]],[[9,7],[[2,0],9]]],
    [0,[7,5]],
    [[[5,[6,9]],4],[3,3]],
    [[[6,[6,9]],4],[[[4,8],8],[6,5]]],
    [[[[1,4],[2,1]],[6,0]],[[[9,1],[4,2]],[[0,4],0]]],
    [[9,4],[[8,6],1]],
    [[[[0,7],0],7],[1,[2,9]]],
    [[[2,9],[[8,4],[4,0]]],[[[6,2],2],[9,5]]],
    [[[0,[5,8]],[6,8]],[[[0,7],4],[[2,8],4]]],
    [[3,[[4,1],[0,7]]],[[1,[5,1]],4]],
    [[[[2,9],6],[[5,3],2]],[[8,[2,0]],9]],
    [0,[[[2,7],9],[1,8]]],
    [[[2,[6,2]],[[4,0],[9,6]]],[[6,1],[8,9]]],
    [[[[9,6],9],[5,[1,8]]],[[[9,6],9],[[2,0],[3,8]]]],
    [[[[4,3],[0,8]],4],[6,6]],
    [[[[4,3],7],[[7,0],5]],[2,[[9,9],4]]],
    [[[[4,3],[1,7]],[[3,1],[0,9]]],0],
    [[5,[[2,5],[2,8]]],[[4,0],[[5,2],[9,8]]]],
    [[[0,[3,5]],7],[[[5,9],2],4]],
    [[9,[[4,4],8]],[[[2,8],1],[[0,9],5]]],
    [[[6,8],[0,1]],[[8,2],[2,0]]],
    [[[1,9],[[9,1],2]],[[6,4],[[7,7],[8,3]]]],
    [[1,[5,[7,6]]],[[[4,7],4],5]],
    [[[8,0],9],[[[6,0],4],1]],
    [[[4,[4,2]],7],[[6,[0,9]],[[3,0],[7,6]]]],
    [[[[3,4],[9,0]],[4,4]],[[9,6],7]],
    [4,[[8,3],[7,1]]],
    [6,[6,8]],
    [[[[0,6],[7,6]],[5,3]],[[[8,9],[6,0]],[[8,5],7]]],
    [[[[0,3],1],5],[[[4,3],[3,2]],[2,[5,9]]]],
    [[[[3,1],0],[1,[8,4]]],[4,5]],
    [[[0,[4,1]],1],[[1,6],[[4,8],[8,3]]]],
    [[[1,4],6],[9,[1,2]]],
    [[9,[[0,7],1]],[[0,9],[0,[4,4]]]],
    [[1,[7,4]],[[2,[5,3]],[[6,6],9]]],
    [0,[0,[0,[0,4]]]],
    [[[[9,7],[4,9]],[9,[3,5]]],[[9,7],7]],
    [5,[9,[[4,1],[2,9]]]],
    [[0,[8,4]],1],
    [[[9,[3,3]],[8,6]],[7,[[1,6],0]]],
    [[[1,[0,7]],[[9,1],8]],[[[2,2],5],[[7,1],[2,2]]]],
    [[[7,[0,3]],4],[[6,[1,6]],[8,7]]],
    [[[[4,8],3],[[6,1],7]],[8,[3,[7,8]]]],
    [3,[[[9,6],9],3]],
    [[[5,[1,0]],[1,4]],5],
    [[[[4,7],2],[[7,0],[6,7]]],[[1,[0,3]],0]],
    [9,[[3,7],[6,1]]],
    [[[2,5],[[0,7],[0,7]]],[[[0,3],2],8]],
    [[[[4,4],7],[2,[0,7]]],[[[1,4],[6,6]],[[8,9],[5,2]]]],
    [[[[0,8],5],[[3,5],7]],[[[5,6],[0,0]],[[3,8],6]]],
    [4,[8,[9,[2,3]]]],
    [[[[6,6],9],0],[[[2,9],[0,8]],5]],
    [[[8,[4,0]],[[2,1],[7,3]]],[8,7]],
    [[6,[9,[1,8]]],[[7,[7,9]],[[2,3],1]]],
    [[6,[[1,7],1]],[[[5,3],[2,0]],[[4,4],9]]],
    [[[[8,0],[0,3]],[[4,8],[0,9]]],[8,[7,[8,6]]]],
    [6,0],
    [[[[5,2],0],[3,3]],[0,4]],
    [[[9,5],[6,4]],[[[7,2],0],8]],
    [[[0,9],[5,[2,3]]],2],
    [[[[5,4],[2,9]],[1,[9,0]]],[[9,9],[9,6]]],
    [[[7,[4,8]],[9,8]],[[[1,3],0],[4,[4,7]]]],
    [[7,[7,9]],0],
    [[[[6,7],[8,1]],[[0,2],2]],[[[7,6],6],[[3,4],[9,9]]]],
    [[7,[6,[2,2]]],[[[8,8],[0,4]],[5,[7,7]]]],
    [[[[0,6],[9,2]],[8,1]],[[[0,4],2],[[5,9],[4,9]]]],
    [[[[9,1],[1,7]],[[3,1],[0,7]]],[[2,[4,9]],[9,1]]],
    [[[9,4],2],[[[2,3],3],[6,[5,7]]]],
    [[[0,8],[[0,9],2]],[[[0,7],[4,4]],7]],
    [[[5,2],4],[0,6]],
    [[3,[9,[9,2]]],[8,[1,[6,8]]]],
    [3,[7,[[8,0],[1,7]]]],
    [[[[2,4],[7,3]],[[0,7],0]],5],
    [[[[6,0],8],[1,4]],[[[3,3],[8,6]],5]],
    [[5,[5,[6,2]]],4],
    [[[0,7],[[4,1],4]],[[8,[3,2]],[7,7]]],
    [[1,[[6,5],[2,2]]],[[6,[2,8]],[1,0]]],
    [6,[4,[[2,2],[1,8]]]],
    [[[[3,3],1],[[4,1],7]],[[[5,2],7],[4,[4,7]]]],
    [[[[2,2],1],[[4,1],3]],[1,[[0,9],[3,8]]]],
    [[0,[0,4]],[[9,[7,5]],[8,[8,0]]]],
    [[[[0,3],3],[[7,3],5]],[4,[[0,1],[3,0]]]],
    [[4,8],3],
    [[[6,0],7],[[6,8],[8,6]]],
    [[[[8,5],3],[[6,2],[2,6]]],[[[2,7],5],[[3,8],[6,9]]]],
    [7,[4,2]],
    [[[[6,0],[7,8]],6],[[[4,6],6],7]],
    [[[0,[2,1]],[5,[3,8]]],[[[3,9],3],[[0,9],3]]],
    [[[8,6],[4,0]],[2,[[4,1],8]]],
    [[[0,1],[[2,0],5]],[[[0,1],[7,0]],[[1,2],[1,4]]]],
    [[[8,8],[[4,4],3]],[1,[4,1]]],
    [[[5,[0,7]],[7,5]],[[7,6],[5,5]]],
    [[[9,[1,3]],[[3,3],6]],[4,[[5,6],8]]],
    [[[9,[3,0]],[8,5]],[1,[[8,0],3]]],
    [[[3,[3,9]],[[2,4],[4,6]]],[[1,2],3]],
    [[[1,[3,1]],[3,[6,3]]],[1,[5,7]]],
    [[[[5,5],[1,5]],3],[9,[[7,4],[9,2]]]],
    [[[6,[7,1]],[[6,6],[1,6]]],7],
    [[[[1,4],0],[8,3]],[[[8,2],9],[[0,3],[9,5]]]],
    [[4,[1,[0,1]]],[[1,[7,3]],1]]
        ]

# lines = [
#     [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]],
#     [[[5,[2,8]],4],[5,[[9,9],0]]],
#     [6,[[[6,2],[5,6]],[[7,6],[4,7]]]],
#     [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]],
#     [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]],
#     [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]],
#     [[[[5,4],[7,7]],8],[[8,3],8]],
#     [[9,3],[[9,9],[6,[4,9]]]],
#     [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]],
#     [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
#     ]
solution2(lines)

a = [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
b = [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
# print(magnitude(add_vals(a, b)))
# a = [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
# a = [[[[5,0],[7,4]],[5,5]],[6,6]]
# explode_list(a)
# print(add_vals([[[[3,0],[5,3]],[4,4]],[5,5]]))

# x = to_tree([[[[[9,8],1],2],3],4])
# print(to_list(reduce_snail_fish(x)))