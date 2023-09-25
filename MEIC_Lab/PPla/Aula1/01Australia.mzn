var 0..2: WA;
var 0..2: NT;
var 0..2: SA;
var 0..2: Q;
var 0..2: NSW;
var 0..2: V;
var 0..2: T;

constraint WA != NT;
constraint WA != SA;

constraint SA != NT;
constraint SA != Q;
constraint SA != NSW;
constraint SA != V;

constraint NSW != Q;
constraint NSW != V;


solve satisfy; 
