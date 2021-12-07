def solution(lines):
    levels = [int(x) for x in lines[0].split(',')]
    min_cost = None
    for i in range(0, max(levels)):
        total_cost = sum([(sum(z for z in range(1,abs(y - i)+1))) for y in levels])
        if min_cost is None or total_cost < min_cost:
            min_cost = total_cost
            print(i, total_cost)


with open('input.txt') as f:
    lines = f.readlines()
    print(solution(lines))