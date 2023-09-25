% O que temos:

% 4000 de farinha
% 6 bananas 
% 2000 de açucar
% 500 manteiga
% 500 cacao

% BANANA
% 250 farinha
% 2 bananas
% 75 açucar
% 100 manteiga

% CACAO
% 200 farinha
% 75 cacao
% 150 açucar
% 150 manteiga

var int : nBan;
var int : nChoc;

constraint nBan >= 0;
constraint nChoc >= 0;
constraint nBan * 250 + nChoc * 200 <= 4000;
constraint nBan * 2 <= 6;
constraint nChoc * 75 <= 500;
constraint nBan * 75 + nChoc * 150 <= 2000;
constraint nBan * 100 + nChoc * 150 <= 500;

solve maximize 450 * nChoc + 400 * nBan;