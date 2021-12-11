m = {
     '>': 25137,
        '}': 1197,
        ']': 57,
        ')': 3
}

m1 = {
     '>': 4,
        '}': 3,
        ']': 2,
        ')': 1
}
def solution(lines):
    lines = [x.strip() for x in lines]
    open = {
        '<': 0,
        '(': 0,
        '{': 0,
        '[': 0
    }
    total = 0
    scores = []
    for line in lines:
        open = {
            '<': 0,
            '(': 0,
            '{': 0,
            '[': 0
        }

        opened = []
        incomplete = True
        for char in line:
            if char not in '>})]':
                opened.append(char)
            else:
                expected = opened.pop()
                if expected == '(':
                    expected = ')'
                elif expected == '[':
                    expected = ']'
                elif expected == '{':
                    expected = '}'
                elif expected == '<':
                    expected = '>'
                if expected != char:
                    total += m[char]
                    incomplete = False
                    break

        if incomplete:
            closing = []
            while (len(opened) > 0):
                expected = opened.pop()
                if expected == '(':
                    expected = ')'
                elif expected == '[':
                    expected = ']'
                elif expected == '{':
                    expected = '}'
                elif expected == '<':
                    expected = '>'
                closing.append(expected)
            score = 0
            for x in closing:
                score = score * 5 + m1[x]
            scores.append(score)
            
    print(sorted(scores)[int(len(scores) / 2)])
    print(total)
with open('input.txt') as f:
    lines = f.readlines()
    print(solution(lines))