% Generate counts from the input and put them in this 9 element array.
generation([0, 124, 43, 33, 55, 45,  0,  0,  0], 0).
generation([X0, X1, X2, X3, X4, X5, X6, X7, X8], N) :- generation([X8, X0, X1, X2, X3, X4, X5, O, X7], M), N is M + 1, X6 is O + X8.
solution(N, Ans) :- generation(A, N), sum_list(A, Ans).
