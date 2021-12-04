def is_winner(board):
    for row in board:
        if row == [-1] * 5:
            return True
    for i in range(0, 5):
        vals = [row[i] for row in board]
        if vals == [-1] * 5:
            return True
    # if board[0][0] == board[1][1] == board[2][2] == board[3][3] == board[4][4]:
    #     return True
    # if board[4][0] == board[3][1] == board[2][2] == board[1][3] == board[0][4]:
    #     return True
    return False
def solution(lines):
    nums = [int(x) for x in lines[0].split(',') if x]

    boards = []
    for i in range(2, len(lines), 6):
        board = [[int(z) for z in x.strip().split(' ') if z] for x in lines[i:i+5]]
        boards.append(board)

    count_won = 0

    for num in nums:
        for k in range(0, len(boards)):
            board = boards[k]
            if (board is not None):
                
                for i in range(0, len(board)):
                    for j in range(0, len(board[i])):
                        if board[i][j] == num:
                            board[i][j] = -1
                if (is_winner(board)):
                    print("----(winner)")
                    for row in board:
                        print(row)
        
                    boards[k] = None
                    count_won += 1

                    if (count_won == len(boards)):
                        s = 0
                        for row in board:
                            for val in row:
                                if val != -1:
                                    s += val
                        print(num * s)
                        return
                else:
                    print("----")
                    for row in board:
                        print(row)
        

    
    
    # print (lines)


with open('input.txt') as f:
    lines = f.readlines()
    print(solution(lines))