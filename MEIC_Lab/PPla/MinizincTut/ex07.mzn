% BEST BURGER

% SOFIUM FAT CAL COST

array[1..8,1..4] of int: ingredients = [|
50,17,220,25|               % BEEF
330,9,260,15|               % BUN 
310,6,70,10|                % CHEESE 
1,2,10,9|                   % ONIONS
260,0,5,3|                  % PICKLES
3,0,4,4|                    % LETTUCE
160,0,20,2|                 % KETCHUP
3,0,9,4|];                   % TOMATO

% menos de 3000mg de sodio, menos de 150 fat, menos de 3000 calorias
% lettuce e ketchup the same, pickle and tomatos the same

array[1..8] of var 1..5: quantidades;
var int: total_cost = sum(i in 1..8)(ingredients[i,4] * quantidades[i]);

constraint quantidades[5] == quantidades[8];
constraint quantidades[5] == quantidades[8];

constraint sum(i in 1..8)(ingredients[i,1] * quantidades[i]) < 3000;
constraint sum(i in 1..8)(ingredients[i,2] * quantidades[i]) < 150;
constraint sum(i in 1..8)(ingredients[i,3] * quantidades[i]) < 3000;

solve maximize total_cost;
