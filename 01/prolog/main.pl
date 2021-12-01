% This may be generated from the input via a script or something. It looks like it's kind of a pain
% to read them by themselves? But we could at least use this for building the real logic.


% Usage: solution([...depths], A)
solution([A, B|Rest], Count) :- solution([B|Rest], N), (B > A -> Count is 1 + N; Count is N).
solution(_, Count) :- Count is 0.

solution2([A, B, C, D | Rest], Count) :- solution2([B, C, D|Rest], N), (D > A -> Count is 1 + N; Count is N).
solution2(_, Count) :- Count is 0.