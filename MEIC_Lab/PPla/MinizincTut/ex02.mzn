include "alldifferent.mzn";

% Problem defenition: TWO + TWO = FOUR

var 0..9: O;
var 0..1: rem1;
var 0..9: R;
var 0..9: W;
var 0..1: rem2;
var 0..9: U;
var 1..9: T;
int : F = 1;

constraint 2 * O == R + 10 * rem1;
constraint 2*W + rem1 == U + 10 * rem2;
constraint 2*T + rem2 == O + 10*F;

constraint alldifferent([R,W,U,T,O,F]);

solve maximize(rem1);

