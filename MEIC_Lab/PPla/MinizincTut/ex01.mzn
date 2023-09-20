include "alldifferent.mzn";

var 0..9: a;
var 0..9: b;
var 0..9: c;

constraint a + b == c;

constraint alldifferent([a,b,c]);

solve satisfy;
