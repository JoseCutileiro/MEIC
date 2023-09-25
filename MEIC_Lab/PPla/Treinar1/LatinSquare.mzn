include "alldifferent.mzn";

int: N = 3;

array[1..N,1..N] of var 1..N: tab;

var int: sum_result;

% Define an array of integers from 1 to N
array[1..N] of int: numbers = [i | i in 1..N];

% Calculate the sum of the elements in the array
constraint sum(numbers) = sum_result;

% Solve the constraint problem
var int: nbMagic;

constraint nbMagic == sum_result;

% Constraint: All elements in every row must be different
% Constraint: All elements in every column must be different
constraint forall(i in 1..N)(
    all_different([tab[i, j] | j in 1..N])
);

% Constraint: All elements in every column must be different
constraint forall(j in 1..N)(
    all_different([tab[i, j] | i in 1..N])
);

constraint forall(i in 1..N)(sum(j in 1..N)(tab[i,j]) == nbMagic);
constraint forall(i in 1..N)(sum(j in 1..N)(tab[j,i]) == nbMagic);