from collections import defaultdict
def optimized(lines):
    template = lines[0].strip()
    rules = [x.strip().split(" -> ") for x in lines[2:]]
    rules = {x: y for [x,y] in rules}
    print(rules)
    # Map from pairs -> pairs
    pairs = {}
    for i in range(len(template)-1):
        val = template[i:i+2]
        if val in pairs:
            pairs[val] += 1
        else:
            pairs[val] = 1

    last_pair = template[-2:]
    for _ in range(0, 40):
        new_pairs = defaultdict(lambda: 0)
        for x in pairs:
            if x in rules:
                new_pairs[x[0] + rules[x]] += pairs[x]
                new_pairs[rules[x] + x[1]] += pairs[x]
            else:
                new_pairs[x] += pairs[x]
        pairs = new_pairs
        if last_pair in rules:
            last_pair = rules[last_pair] + last_pair[1]

    final_count = defaultdict(lambda: 0)
    for x in pairs:
       
        final_count[x[0]] += pairs[x]
    final_count[last_pair[1]] += 1
    z = (sorted([(final_count[x], x) for x in final_count]))
    print(z[-1][0] - z[0][0]) # Could be off by one in either direction

def solution(lines):
   template = lines[0].strip()
   rules = [x.strip().split(" -> ") for x in lines[2:]]
   
   for _ in range(0, 40):
    print(_)
    next = ""
    for i in range(len(template)-1):
        pair = template[i:i+2]
        found_rule = False
        for [a, b] in rules:
            # print(a)
            if a == pair:
                next += template[i]
                next += b
                found_rule = True
                break
        if not found_rule:
            next += template[i]
            
    next += template[-1]
    template = next
   res = {}
   for x in template:
       if x in res:
           res[x] += 1
       else:
           res[x] = 1
   print(res)
#    print(next)

with open('input.txt') as f:
    lines = f.readlines()
    optimized(lines)