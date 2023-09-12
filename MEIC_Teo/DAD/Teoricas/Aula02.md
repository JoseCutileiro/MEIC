# Aula 2

# Consensus

```
Problema aparentemente simples, funciona como uma abstração 
para o verdadeiro problema

> N processos (N conhecido à priori)
> Cada um com um input
> Todos os processos corretos devolvem o mesmo output
> O output tem que ser um dos valores propostos
    > Não tem que ser o mais frequente
    > Todos os valores de input são bons

Solução trivial: Todos os processos dão um valor default
```

# Propriedades

1. Terminação: Todos os processos corretos, terminam
(Neste curso não iremos falar de falhas bizentinas)
2. Acordo uniforme, se dois processos decidirem, decidem o mesmo valor
3. Integridade (o valor foi proposto por (pelo menos) um dos processos)

# Porque é que isto é dificil 

```
EXEMPLO: 
URB: Uniform reliable broadcast


Interface
broadcast(m) : send a message
deliver(m) : deliver hte message to the app

URB properties:
Validity: if a correct process broadcast m every correct process will deliver m
No dupes: no message is delivered more than once
No creation: If process deliver m, m was broadcast by some process
Agreement: If process deliver m every correct processs will deliver m 

Como implementar o URB? 

P1
Broadcast(m)

P2 recebe broadcast de P1 
Broadcast(m) 

[...]

Quando receber  n-1 broadcasts -> Deliver(m)


Problema: Pode não terminar ggwp

Nos slides estão os vários algoritmos, estão bem explicados lá

Conceito a investigar: Perfect failure detection
Propriedades
Completeness: Se buga ele vai encontrar 
Acurracy: Não pode dar false positives

Como implementar?
Mandar mensagens (e.g. ping with TIMEOUTS)
```
