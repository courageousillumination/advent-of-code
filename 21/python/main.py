import functools
rolls = 1         
def get_next_dice(dice):
    global rolls
    rolls += 1 
    if dice < 100:
        return dice + 1
    else:
        return 1
[
[1, 1, 1],
[1, 1, 2],
[1, 1, 3],
[1, 2, 2],
[1, 2, 3],
[2, 2, 2],
[2, 2, 3],
[2, 3, 3],
[3, 3, 3],
]

counts = {6: 7, 5: 6, 7: 6, 8: 3, 4: 3, 9: 1, 3: 1}


MAX_SCORE = 21
@functools.lru_cache(maxsize=None)
def count_winners(player1Score, player2Score, player1Pos, player2Pos, active):
    if player1Score >= MAX_SCORE:
        return (1, 0)
    if player2Score >= MAX_SCORE:
        return (0, 1)
    if active == 0:
        a = 0
        b = 0
        for move in counts:
            new_pos = move_player(player1Pos, move)
            (p1wins, p2wins) = count_winners(player1Score + new_pos, player2Score, new_pos, player2Pos, 1)
            a += p1wins * counts[move]
            b += p2wins * counts[move]
        return (a, b)
    else:
        a = 0
        b = 0
        for move in counts:
            new_pos = move_player(player2Pos, move)
            (p1wins, p2wins) = count_winners(player1Score, player2Score + new_pos, player1Pos, new_pos, 0)
            a += p1wins * counts[move]
            b += p2wins * counts[move]
        return (a, b)



def move_player(pos, x):
    for _ in range(x):
        pos += 1
        if pos == 11:
            pos = 1
        # print(pos)
    return pos
def solution():
    player1Pos = 1
    player2Pos = 2
    player1Points = 0
    player2Points = 0

    activePlayer = 0
    diceNum = 0
    while player1Points < 1000 and player2Points < 1000:
        if activePlayer == 0:
            diceNum = get_next_dice(diceNum)
            player1Pos = move_player(player1Pos, diceNum)
            
            # player1Points += player1Pos
            if player1Points >= 1000:
                break
            diceNum = get_next_dice(diceNum)    
            player1Pos = move_player(player1Pos, diceNum)
            
            # player1Points += player1Pos
            if player1Points >= 1000:
                break
            diceNum = get_next_dice(diceNum)
            player1Pos = move_player(player1Pos, diceNum)
            
            player1Points += player1Pos
            if player1Points >= 1000:
                break

        else:
            diceNum = get_next_dice(diceNum)
            player2Pos = move_player(player2Pos, diceNum)
            
            # player2Points += player2Pos
            if player2Points >= 1000:
                break
            diceNum = get_next_dice(diceNum)    
            player2Pos = move_player(player2Pos, diceNum)
            
            # player2Points += player2Pos
            if player2Points >= 1000:
                break
            diceNum = get_next_dice(diceNum)
            player2Pos = move_player(player2Pos, diceNum)
            
            player2Points += player2Pos
            if player1Points >= 1000:
                break
        activePlayer = (activePlayer + 1) % 2
        
    r = rolls -1 
    if player1Points < player2Points:
        print(player1Points * r)
    else:
        print(player2Points * r)
    print(player1Points, player2Points, r)
    # Part 2
    res = count_winners(0, 0, 1, 2, 0)
    print(res)

solution()
   