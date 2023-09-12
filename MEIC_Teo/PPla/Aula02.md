# Aula 2

```
Warning: Por motivos pessoais não consegui comparecer a esta
aula. Portanto vou deixar aqui apontamentos tirados por mim próprio
```

# Crystal maze with MiniZinc

## Relembrar crystal maze: 

```
Numeros de 0 a 7 
Grafo com um dado formato (sabemos à priori)
Os nós com ligação não podem ter número consecutivo
```

## MiniZinc

```
1. Download
2. Aquilo tem um IDE integrado

Extension: .mzn
```

## Linguagem:

```

%
% Isto é um comentario
%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Variaveis às quais iremos aplicar restricoes

var 0..7: v0;
var 0..7: v1;

[...]

var 0..7: v7;

% Variaveis vi podem ser 0 a 8
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Isto é uma restrição

constraint abs(v0-v1) > 1;
constraint abs(v0-v5) > 1;

[...]

% colocar aqui todas as arestas
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

include "alldiferent.mzn";
constraint alldifferent([v0,v1,...,v7])

solve satisfy
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Clicar em run: Ele cospe uma solução

% Podes usar a command line com o seguinte comando:
% minizinc crystalMaze.mzn

% para teres todas as soluções
% crystalMaze.mzn -a

% -s (estatisticas)
```

# Claro que é massudo estar a colocar todos os vértices individualemente
# Por isso deves fazer da maneira genérica:

```mzn

include "allldifferent.mzn"

int: n;     % Vértices
int: m;     % Arestas

array[1..m,1..2] of int

array[0..n-1] of var 0..n-1: v

constraint forall(e in 1..m)(abs(v[edge[e,1]] - v[edge[e,2]]) > 1);
constraint alldifferent(v);

solve satisfy;

output ["v=\(v)"]
```

Para ver a explicação é melhor ires ao slide :/ 

# O que é então um constraint problem?

```
É um programa que gera variaveis e restricoes para representar um problema
Primeiro criamos um modelo do problema e depois PROCURA para o resolver
```