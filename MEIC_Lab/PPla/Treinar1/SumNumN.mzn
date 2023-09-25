int: N = 5; 
var int: sum_result;

% Define an array of integers from 1 to N
array[1..N] of int: numbers = [i | i in 1..N];

% Calculate the sum of the elements in the array
constraint sum(numbers) = sum_result;

% Solve the constraint problem
solve satisfy;