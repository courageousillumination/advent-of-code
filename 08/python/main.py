def solution(lines):
    foos = [x.split("|") for x in lines]
    foos = [[x[0].strip().split(" "), x[1].strip().split(" ")] for x in foos]
    vals = []
    for [_, z] in foos:
        vals += [x for x in z if len(x) == 2 or len(x) == 4 or len(x)==7 or len(x) == 3]
    # print(set(vals))

    total = 0

    for [left, right] in foos:
        n1 = [x for x in left if len(x) == 2][0]
        n7 = [x for x in left if len(x) == 3][0]
        n4 = [x for x in left if len(x) == 4][0]
        n8 = [x for x in left if len(x) == 7][0]

        a = [x for x in n7 if not x in n4][0]
        b = [x for x in n4 if not x in n7 and sum(1 for z in left if x in z) == 6][0]
        d = [x for x in n4 if not x in n7 and sum(1 for z in left if x in z) != 6][0]

        f = [x for x in n4 if sum(1 for z in left if x in z) == 9][0]
        c = [x for x in n1 if x != f][0]
        e = [x for x in n8 if sum(1 for z in left if x in z) == 4 and x != f and x != c and x != a and x != b and x != d][0]
        g = [x for x in n8 if x != e and x != f and x != c and x != a and x != b and x != d][0]
        
        print(('a', a), ('b', b), ('c', c) , ('d', d) , ('e', e) , ('f', f) , ('g', g))
        def apply_mapping(str):
            result = ""
            for char in str:
                if char == a:
                    result += 'a'
                if char == b:
                    result += 'b'
                if char == c:
                    result += 'c'
                if char == d:
                    result += 'd'
                if char == e:
                    result += 'e'
                if char == f:
                    result += 'f'
                if char == g:
                    result += 'g'
            return result
        
        def interpret_result(str):
            if str == 'abcdefg':
                return 8
            if str == 'abdfg':
                return 5
            if str == 'acdeg':
                return 2
            if str == 'acdfg':
                return 3
            if str == 'acf':
                return 7
            if str == 'abcdfg':
                return 9
            if str == 'abdefg':
                return 6
            if str == 'bcdf':
                return 4
            if str == 'abcefg':
                return 0
            if str == 'cf':
                return 1
            print(str)
        
        baz = ([interpret_result(''.join(sorted(apply_mapping(x)))) for x in right])
        baz_int = int(''.join([str(x) for x in baz]))
        total += baz_int
    print(total)
    # xs = [x for y in lines for x in y.split(" | ")]
    # print(count)

with open('input.txt') as f:
    lines = f.readlines()
    print(solution(lines))