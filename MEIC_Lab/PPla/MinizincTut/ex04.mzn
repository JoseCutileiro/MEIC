% MORE ABOUT ARRAYS

% array[v1,v2,..,vn] of [var] type: NOME;
%
% e.g:
% 
% array[1..19] of string: townsname;
% array[2,3] of var float: value;

% VALUE IS SOMETHING LIKE THIS:

% 2 2 2
% 3 3 3

% writing:

% value[1,2] = 1.2;
% value = [|2,2,2|3,3,3];
% value = array2d(1..2,1..3,[2,2,2,3,3,3]);

% Constraint no array: FORALL

% são iguais
% forall ([EXPRESSION | GENERATOR WHERE BOOLEAN])
% FORALL (GENERATOR WHERE BOLEAN)(EXPRESSION)

% e.g
% forall([a[j] != a[i] | i,j in 1..3 where i!=j]);
% forall(i,j in 1..3 where i!=j)(a[j] != a[i]);

array[1..10] of var 0..9: a;

constraint forall(i,j in 1..10 where i > j)(a[j] > a[i]);

solve satisfy;

