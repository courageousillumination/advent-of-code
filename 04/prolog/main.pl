% THis hadn't quite got there. I can mostly determine if a board has won, but some other bits are
% still elluding me...
hasBingo([-1, _, _, _, _, 
          -1, _, _, _, _,
          -1, _, _, _, _,
          -1, _, _, _, _,
          -1, _, _, _, _ ]).
hasBingo([_, -1, _, _, _, 
          _, -1, _, _, _,
          _, -1, _, _, _,
          _, -1, _, _, _,
          _, -1, _, _, _ ]).
hasBingo([_, _, -1, _, _, 
          _, _, -1, _, _,
          _, _, -1, _, _,
          _, _, -1, _, _,
          _, _, -1, _, _ ]).
hasBingo([_, _, _, -1, _, 
          _, _, _, -1, _,
          _, _, _, -1, _,
          _, _, _, -1, _,
          _, _, _, -1, _ ]).
hasBingo([_, _, _, _, -1, 
          _, _, _, _, -1,
          _, _, _, _, -1,
          _, _, _, _, -1,
          _, _, _, _, -1 ]).
hasBingo([-1, -1, -1, -1, -1, 
          _, _, _, _, _,
          _, _, _, _, _,
          _, _, _, _, _,
          _, _, _, _, _ ]).
hasBingo([_, _, _, _, _,
          -1, -1, -1, -1, -1, 
          _, _, _, _, _,
          _, _, _, _, _,
          _, _, _, _, _ ]).
hasBingo([_, _, _, _, _,
          _, _, _, _, _,
          -1, -1, -1, -1, -1,
          _, _, _, _, _,
          _, _, _, _, _]).
hasBingo([_, _, _, _, _,
          _, _, _, _, _,
          _, _, _, _, _,
          -1, -1, -1, -1, -1, 
          _, _, _, _, _ ]).
hasBingo([_, _, _, _, _,
          _, _, _, _, _,
          _, _, _, _, _,
          _, _, _, _, _,
          -1, -1, -1, -1, -1]).

board([22,13,17,11,0,
    8,2,23,4,24,
    21,9,14,16,7,
    6,10,3,18,5,
    1,12,20,15,19]).
        
board([3,15,0,2,22,
    9,18,13,17,5,
    19,8,7,25,23,
    20,11,10,24,4,
    14,21,16,12,6]).
        
board([14,21,17,24,4,
    10,16,15,9,19,
    18,8,23,26,20,
    22,11,13,6,5,
    2,0,12,3,7]).

% A board is valid if it can be constructed from a marked board
mBoard([], _, []).
mBoard([B|R], X, Out) :- mBoard(R, X, REM),  (B =\= X -> Out = [B| REM]; Out = [-1| REM]).


playMoves(B, [], B).
playMoves(B, [M | Rest], Out) :- mBoard(B, M, Marked), playMoves(Marked, Rest, Out).


solution(Moves, B) :- board(B), hasBingo(X), playMoves(B, Moves, X).