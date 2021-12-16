def to_int(bits):
    return int(''.join(str(x) for x in bits), 2)

bits = {
'0': '0000',
'1': '0001',
'2': '0010',
'3': '0011',
'4': '0100',
'5': '0101',
'6': '0110',
'7': '0111',
'8': '1000',
'9': '1001',
'A': '1010',
'B': '1011',
'C': '1100',
'D': '1101',
'E': '1110',
'F': '1111',
}

def to_bits(x):
    return [int(a) for  a in bits[x]]


def process_op(type, sub):
    print("In here", type, sub)
    if type == 0:
        return sum(sub)
    if type == 1:
        prod = 1
        for x in sub:
            prod *= x
        return prod
    if type == 2:
        return min(sub)
    if type == 3:
        return max(sub)
    if type == 5:
        return 1 if sub[0] > sub[1] else 0
    
    if type == 6:
        return 1 if sub[0] < sub[1] else 0
    
    if type == 7:
        return 1 if sub[0] == sub[1] else 0

total_version = 0
def process_packet(bits):
    print(bits)
    end = 0
    version = to_int(bits[0:3])
    print("version", version)
    global total_version
    total_version += version
    # print(total_version)
    packet_type = to_int(bits[3:6])
    print("packet type", packet_type)
    if (packet_type != 4):
        sub = bits[6]
        if sub == 0:
            
            length = to_int(bits[7:7+15])
            # print(length)
            x = 7+15
            end = 7+15+length
            sub_vals = []
            while x < end:
                a,b = process_packet(bits[x:])
                x += a
                sub_vals.append(b)
                
            return (7+15+length, process_op(packet_type, sub_vals))
        else:
            count = to_int(bits[7:7+11])
            x = 7+11
            sub_vals = []
            for i in range(0, count):
                a,b = process_packet(bits[x:])
                x += a
                sub_vals.append(b)

            return (x, process_op(packet_type, sub_vals))
    else:
        x = 6
        val = []
        # print(bits)
        while bits[x] != 0:
            val += bits[x+1:x+5]
            x += 5
        val += bits[x+1:x+5]
        # print("literal", to_int(val))
        return (x + 5, to_int(val))
    # print(version)

def solution(lines):
    v = []
    for x in lines[0]:
        v += to_bits(x)
    # v = [to_bits(x) for x in lines[0]]
    print(process_packet(v))
    # print(total_version)

with open('input.txt') as f:
    lines = f.readlines()
    solution(lines)