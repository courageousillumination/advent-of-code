def get_value(v, reg):
    if v in reg:
        return reg[v]
    return int(v)


# def run_step(command, reg)
def run_program(commands, vals, initial_z=0):
    reg = {
        'w': 0,
        'x': 0,
        'y': 0,
        'z': initial_z,
    }
    for command in commands:
        if command[0] == 'inp':
            if len(vals) == 0:
                # print(reg)
                break

            reg[command[1]] = vals.pop()

        elif command[0] == 'add':
            reg[command[1]] = get_value(command[1], reg) + get_value(command[2], reg)
        elif command[0] == 'mul':
            reg[command[1]] = get_value(command[1], reg) * get_value(command[2], reg)
        elif command[0] == 'div':
            reg[command[1]] = int(get_value(command[1], reg) / get_value(command[2], reg))
        elif command[0] == 'mod':
            reg[command[1]] = get_value(command[1], reg) % get_value(command[2], reg)
        elif command[0] == 'eql':
            reg[command[1]] = 1 if get_value(command[1], reg) == get_value(command[2], reg) else 0
        else:
            print(command)
        # print(command, reg)
    return reg['z']

def reverse_solve(commands, vals):
    # Reduce this to a giant equation and find a value
    pass

# Set x to z (from the previous)
# Mod x by 26 = z % 26
# Div z by 26
# Add a constant to x
# Check if it's equal to w (the input)
# Check if it's equal to 0 (i.e. not)

# Clear y
# Add constant to y
# mul y by x (either 0 or 1)
# add 1 to y
# mul z by y (either 1 or 2)

# Clear y
# Set y to w + 5
# Multiple y by x (either 0 or 1)

# add z to y

# To make this zero at the end
# y [6, 14]
# z [-14, 6]

# OR z = 0

# Can I leave z in a zero state?



def solution(lines):
    commands = [x.strip().split(" ") for x in lines]


    chunks = []
    chunk = []
    for command in commands:
        # print(command)
        if command == ['inp', 'w']:
            chunks.append(chunk)
            chunk = []
        chunk.append(command)
    chunks.append(chunk)

    chunks = chunks[1:]

    for i in range(len(chunks)):
        chunk = chunks[i]
        # print(i)
        if ['div', 'z', '26'] in chunk:
            # print(i, "Shrink chunk")
            print([x for x in chunk if len(x) == 3 and x[0] == 'add' and x[1] == 'x' and x[2] != 'z'][0][2])
        else:
            # print(i, "Grow chunk")
            # print([x for x in chunk if len(x) == 3 and x[0] == 'add' and x[1] == 'y' and x[2] != 'w'][0])
            print([x for x in chunk if len(x) == 3 and x[0] == 'add' and x[1] == 'y' and x[2] != 'w'][2][2])
        

    # 8 + 10 - 11 = 8 + 10 -> 18 - 11 -> 7
    subChunks = chunks[0] + chunks[2] + chunks[3] + chunks[-1]

    subChunks = commands
    39999697924989

    # 12 - 6 -> max 3, 9  
    # 9 - 16 -> max 9, 2
    # 8 - 8 -> 9,9
    # 0 - 5 -> max 9, 4
    # 11 -8 -> max 6, 9
    # 10 - 11 -> max 9, 8
    # 3 - 1 -> max 7, 9


    18116121134117
    # 12 - 6 -> min 1 -> 7  
    # 9 - 16 -> min 8 -> 1
    # 8 - 8 -> 1,1
    # 0 - 5 -> min 6, 1
    # 11 -8 -> max 1, 4
    # 10 - 11 -> max 2, 1
    # 3 - 1 -> max 1, 3

    # print(subChunks)
    # 12 
    # 9
    # 8
    # -8
    # 0
    # 11
    # 10
    # -11
    # 3
    # -1
    # -8
    # -5
    # -16
    # -6

    # 12 -> 

    print("done")

    subChunks = (
        chunks[0] +
        chunks[1] + (chunks[2] + chunks[3]) +
        chunks[4] +
        chunks[5] + (chunks[6] + chunks[7]) +
        (chunks[8])
        + chunks[-5]
        + chunks[-4]
        + chunks[-3]
        + chunks[-2]
        + chunks[-1])

    # subChunks = commands
    # for i in range(9999, 0, -1):
    # i = 39999697924989
    i = 18116121134117
    vals = [int(x) for x in str(i)]
    vals.reverse()
    res = run_program(subChunks, vals)
    print(res)
    if res == 0:
        print("good")
    # 79 is the best we can do
    

    # Last iteration I need z to equal i + 6 (exactly)

    # A shrink chunk is identified by add x (amount) and the mult for the next
    # A grow chunk is defined by the add y and the mult y
    
    # vals = []
    # for i in range(9,0,-1):
    #     res = run_program(chunks[0], [i], 10)
    #     # print(res)
    #     # res = run_program(chunks[-1], [i, i], res)
    #     # print(res, i)
    #     # print(res, i)
    #     print(res)
    #     vals.append(res)

    # Chunk 1: Add 12 to input

    # Always adds the last y to the input
    
    # v1 = []
    # for i in range(9,0,-1):
    #     for v in vals:
    #         res = run_program(chunks[1], [i], v)
    #         v1.append(res)
    # print(len(v1), len(set(v1)))
    
    

    # target_z = [0]
    # next_targets = set()
    # chunks.reverse()
    # chunks = chunks[:2]
    # for chunk in chunks:
    #     for z in range(-20, 20):
    #         for i in range(1,10):
    #             final_z = run_program(chunk, [i], z)
    #             if final_z in target_z:
    #                 next_targets.add(z)
    #     target_z = [x for x in next_targets]
    #     next_targets = set()
    # print(target_z)
    # for z in range(-20, 20):
    #     for i in range(1,10):
    #         if run_program(commands, [i], z):
    #             print(i, z)
    # for command in commands:
    #     if command == ['inp', 'w']:
    #         print("###New block###")
    #     else:
    #         print(command)

    # for i in range(1, 9):
    #     for j in range(1, 9):
    #         print(i,j)
    #         run_program(commands, [i, j])
    # for i in range(99999999999999, 0, -1):
    #     # print(i)
    #     vals = [int(x) for x in str(i)][:1]
    #     if 0 in vals:
    #         continue
    #     if run_program(commands, vals):
    #         print(i)


def search(chunks, z):
    
    if len(chunks) == 0 :
        return [] if z == 0 else None

    (kind, chunk) = chunks[0]

    if kind == "grow":
        for i in range(1, 10):
            if len(chunks) > 10:
                print(i, len(chunks))
            new_z = run_program(chunk, [i], z)
            res = search(chunks[1:], new_z)
            if res is not None:
                return [i] + res
    else:
        for i in range(1, 10):
            new_z = run_program(chunk, [i], z)
            if new_z < z:
                res = search(chunks[1:], new_z)
                if res is not None:
                    return [i] + res
                return None
    return None
    
def condense_chunk(chunk):
    if ['div', 'z', '1'] in chunk:
        return (("grow", [x for x in chunk if len(x) == 3 and x[0] == 'add' and x[1] == 'y' and x[2] != 'w'][2][2]))
    else:
        return (("shrink", [x for x in chunk if len(x) == 3 and x[0] == 'add' and x[1] == 'x' and x[2] != 'z'][0][2]))

def solution2(lines):
    commands = [x.strip().split(" ") for x in lines]
    chunks = []
    chunk = []
    for command in commands:
        if command == ['inp', 'w']:
            if chunk != []:
                chunks.append(condense_chunk(chunk))
            chunk = []
        chunk.append(command)
    
    chunks.append(condense_chunk(chunk))
    # Create pairs

    relations = {}
    stack = []
    for i, (kind, amount) in enumerate(chunks):
        if kind == "grow":
            stack.append((i, amount))
        else:
            j, val = stack.pop()
            relations[j] = (i, int(val) + int(amount))
    
    # Generate a number that meets the relations
    value = [None] * 14
    for i in range(len(value)):
        if value[i] != None:
            continue
        idx2, diff = relations[i]
        if diff > 0:
            value[idx2] = 9
            value[i] = 9 - diff
        elif diff <= 0:
            value[i] = 9
            value[idx2] = 9 + diff
    print(''.join([str(x) for x in value]))

    


with open('input.txt') as f:
    lines = f.readlines()
    solution2(lines)
