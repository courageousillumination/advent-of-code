openingCharacter('(').
openingCharacter('[').
openingCharacter('{').
openingCharacter('<').

closes('(', ')').
closes('[', ']').
closes('{', '}').
closes('<', '>').

% Rem will be the remaining bits to parse, Err will be an error character
% if encountered.
validSequence([], Acc, Rem, _) :- Rem = Acc.
validSequence([X | T], Acc, Rem, Err) :-
    openingCharacter(X), validSequence(T, [X | Acc], Rem, Err).
validSequence([X | T], [AccX | AccT], Rem, Err) :- 
    closes(AccX, X), validSequence(T, AccT, Rem, Err).
validSequence([X | _], _, _, Err) :- Err = X.

solution(X, Rem, Err) :- atom_chars(X, Y), validSequence(Y, [], Rem, Err).