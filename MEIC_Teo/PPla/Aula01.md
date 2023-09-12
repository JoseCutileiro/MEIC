# PPla: Procura e planeamento 

# Aula 1
```
Warning: Por motivos pessoais não consegui comparecer a esta
aula. Portanto vou deixar aqui apontamentos tirados por mim próprio
```

# SLIDE_01: pp-intro.pdf

## Avaliação: 

```
50% projeto 
50% exam

As inscrições para os agrupamentos já estão abertas
```

## Material para o curso:

```
>>> Bibliografia:
• Constraint Processing: Rina Dechter 2003 Elsevier Morgan Kaufmann
• Principles of Constraint Programming: Krzysztof Apt 2003 Cambridge University Press
• Automated Planning and Acting: Malik Ghallab, Dana Nau and Paolo Traverso 2016 
Cambridge University Press
• Automated Planning – theory and practice: Malik Ghallab, Dana Nau and Paolo 
Traverso 2004 Elsevier

>>> Slides

>>> Fazer os exercicios em casa

>>> Muito material na net
```

## Definições:

```
O que é procura e planeamento?

Procura [Verbo] - Tentar encontrar algo
Plano [Nome] - Como alcançar algo

=========================================

SEARCH: No contexto de AI? 
> Como navegar do estado inicial para o estado objetivo, navegando 
entre estados intermediários

PLANNING: No contecto de AI? 
> Explorar o processo de utilizar técnicas autonomas para planear e organizar problemas

O planeamento pode ser resolvido com a procura

```

# Revisões e cenas (resumo)

Informação completa: https://towardsdatascience.com/ai-search-algorithms-every-data-scientist-should-know-ed0968a43a7a

## Conceitos chave: 


1. Estado, Estado inicial, Estado objetivo, Intermédio
2. Transição
3. Espaço de procura (coleção de estados)

## Algoritmos clássicos de procura não informada:

1. DFS
2. IDFS 
3. BFS

```
Nota: Procura não informada, não existe informarção acerca do custo de 
navegar entre os estados
```

## Algoritmos clássicos de procura informada:

1. UCF
2. A*
3. IDA* 

```
Nota: Procura informada, temos ideia ou a certeza do custo 
de navegar entre os estados
```

## Procura local:

1. Hill Climbing
2. Simulated annealing
3. GSAT
4. Procura genética
5. Beam search (procura lazer)
6. Procura de monte carlo
7. Procura de Las Vegas
8. Procura de Atlantic city

# Resolver problemas com PROCURA

```
Nesta aula, codificamos problemas de procura como CSPs
(constraint satisfaction problems)
```

# Crystal maze

## PUZZLE (exemplo)

```
Temos um grafo com 8 nós 
temos que garantir que nenhum nó tem uma
ligação com um número consecutivo

Problema + Tentativa
```

```
Heuristica: 
Meter nos nós com mais ligações  os números com menos restrições
(1 e 8 neste caso)

Inferência e propagação 
```

```
Este puzzle é NP completo
```

# CSP: Constraint satisfaction problem

```
Um CSP é um triplo <V,D,C> onde:
> V é um set de variaveis
> D (dominio)
> C (conjunto de restricões)

Objetivo: Encontrar os V que satisfazem a todas as C dado D
```

```
Mas isto é assim tão dificil?

Imaginemos
    n variavies
    cada uma com m possibilidades de valores (dominio)
    quantos estados podemos considerar?

    n^m estados 

Mais exemplos de problemas CSP
> Sudoko
> Scotsman
> Exam timetable
```

# MiniZinc: CSP solver

MiniZinc: https://towardsdatascience.com/ai-search-algorithms-every-data-scientist-should-know-ed0968a43a7a

