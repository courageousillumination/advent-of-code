:- use_module(library(clpfd)).



validPosition(X, Y) :- X #> 20, X #< 30, Y #> -10, Y #< -5.

% validTrajectory(DX, DY, X, Y) :- 
%     validPosition(X, Y); 
%         NX is X + DX,
%          validTrajectory()