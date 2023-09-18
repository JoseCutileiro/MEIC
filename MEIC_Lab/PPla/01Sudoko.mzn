include alldifferent;
include "sudoko.dzn"

int : S;
int : N = S * S;

set of int : PuzzleRange = 1..N;
set of int : SubSquareRange = 1..S;

array[1..N, 1..N] of 0..N : start; % 0 <=> empty space
array[1..N, 1..N] of var PuzzleRange : puzzle;

% encher com tabuleiro inicial
constraint forall (i,j in PuzzleRange) (
    if start[i,j] > 0 then puzzle[i,j] = start[i,j] else true endif
);

% todas as linhas diferentes
constraint forall (i in PuzzleRange) (
    alldifferent([puzzle[i,j] | j in PuzzleRange])
);

% todas as colunas diferentes
constraint forall (j in PuzzleRange) (
    alldifferent([puzzle[i,j] | i in PuzzleRange])
);

% sub  squares different
constraint forall (a,o in SubSquareRange) (
    alldifferent( [puzzle[(a-1) * S + a1, (o-1) * S + o1] | 
    a1,o1 in SubSquareRange])
);

solve satisfy; 




