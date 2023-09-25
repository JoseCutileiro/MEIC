var 1..3 : T1;
var 1..3 : T2;
var 1..3 : T3;
var {1,3} : T4;
var 1..3 : T5;

constraint T4 != 2;

constraint T1 > T3;
constraint T3 > T5;
constraint T4 > T3;
constraint T1 != T2;
constraint T2 != T4;

solve satisfy;

