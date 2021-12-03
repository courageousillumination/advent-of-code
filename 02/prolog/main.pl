% Usage: position(X, Y, AIM, [LIST OF COMMANDS ["forward", 5]])
% Note commands need to be reversed (only matters for the second part.)

position(0,0,0, []).
position(X, Y, AIM, [["forward", D] | R]) :-  position(N, Y, AIM, R), X is N + D.
position(X, Y, AIM, [["up", D] | R])      :-  position(X, N, AIM, R), Y is N - D.
position(X, Y, AIM, [["down", D] | R])    :-  position(X, N, AIM, R), Y is N + D.

position2(0,0,0, []).
position2(X, Y, AIM, [["forward", D] | R]) :-  position2(N, M, AIM, R), X is N + D, Y is M + AIM * D.
position2(X, Y, AIM, [["up", D] | R])      :-  position2(X, Y, N, R), AIM is N - D.
position2(X, Y, AIM, [["down", D] | R])    :-  position2(X, Y, N, R), AIM is N + D.
