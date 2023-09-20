% Magic square
% forall(i,j in 1..3 where i!=j)(a[j] != a[i]);
% array[2,3] of var float: value;
include "alldifferent.mzn";

int: N = 3;

array[1..N,1..N] of var 1..N*N: tab;
int: nbMagic = N * (N*N + 1) div 2;

constraint alldifferent([tab[i,j] | i in 1..N, j in 1..N]);

constraint forall(i in 1..N)(sum(j in 1..N)(tab[i,j]) == nbMagic);
constraint forall(i in 1..N)(sum(j in 1..N)(tab[j,i]) == nbMagic);

% diagonal principal
constraint sum(i in 1..N)(tab[i,i]) == nbMagic;

% outra diagonal
constraint sum(i in 1..N)(tab[i,N-i+1]) == nbMagic;

solve satisfy;
