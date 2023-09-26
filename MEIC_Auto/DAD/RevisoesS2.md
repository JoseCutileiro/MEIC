# Foco no Paxos

# PAXO

```
Algoritmo que resolve consenso, assumindo que o sistema irá ser
sincrono durante um periodo de tempo, não usa PFD (perfect failure detector)

    > As mensagens podem demorar o tempo que quiserem, podem ser duplicadas e 
        podem até falhar
    
Relembrar: Um pfd é apenas uma forma de simular um sistema sincrono num 
    ambiente que originalmente era assincrono

Agentes no paxos: 
    > Proposers
    > Acceptors
    > Learners

[Sistema asincrono e sem falhas bizantinas]
```

# Lideres no paxos

```
Proposers pre agree on a order to become leader
Proposers: {p1,...,pn}

p1 é o primeiro lider
Se p2 suspeita que p1 crashou -> p2 torna-se lider
[...]

Como não estamos a assumir que o detetor de falhas é perfeito, p2
pode suspeitar de p1 erradamente, por isso 

p1 é lider em p1,pn+1,p2n+1 ...
p2 é lider em p2,pn+2,p2n+2 ...
```

# Algoritmo do lider

```
Dividido em duas etapas:

    Etapa 1: 
        > Perceber o que é que os lideres anteriores andaram a fazer

    Etapa 2: 
        > Tentar obter uma maioria de nós com o valor que decidiu
    
    valor adotado:
        <VALUE; WRITE_TS; READ_TS>
    
    Inicialmente:
        <ValorProposto; 0; 0>
```

# Exemplo:

```
Por enquanto vamos ignorar o READ_TS

P1:
    Salta a "Etapa 1"
    Começa a "Etapa 2"
        > Envia "accept(my_value,1)" para todos os processos 
        > Espera por "accepted(my_value,1)" de uma maioria de processos
        > Se recebeu -> "decide(my_value)"
    
    Numa ronda em que corre bem, é simples, ele simplesmente decide o valor
    vamos agora fingir que ele crasha lá para o meio -> P2 entre na fight

P2: 
    Começa a "Etapa 1":
        > Envia "prepare(2)" para todos os nós
        > Espera por promise(my_value,WRITE_TS)" de uma maioria
        > Escolhe o valor com maior WRITE_TS dos nós (se ainda estiverem a 0 escolhe o seu)

    Repete a "Etapa 2"

Esta solução só tem um problema: Multiplos lideres concorrentes 
E aí é que irá aparecer o READ_TS
```

# Lideres concurrentes

```
READ_TS: Quando um lider executa o step 1, memoriza
qual é que foi o ultimo lider que leu o seu estado

Ou seja quando um processo recebe,
por exemplo "prepare(2)", se o READ_TS do processo 
que recebeu esta mensagem for inferior a 2, ele irá
atualizar o seu READ_TS para dois e responder. Se 
for superior a dois irá ignorar o prepare deste
lider (é um lider que está desatualizado)

Mesmo assim pode haver uma situação de LIVELOCK
```

# Apontamentos das aulas teóricas

# Sobre o projeto
```
O consenso (utilizando PAXOS) é uma operação
exigente e lenta. Por isso o objetivo é tentar reduzir
o nr de vezes que fazemos esta operação. 

Em vez de aplixar o consensus nas TM aplicamos apenas
nas LM e o consenso é distribuido quase gratuitamente
pelo sistema todo. => Mais barato

Reduzimos o nr de colisões e o nr de vezes
que temos que aplicar o paxos

Um TM tenta manter a Lease o maior tempo possivel
para reduzir o numero de vezes que o paxos
é executado.
```

# MultiPaxos
```
É baseado no paxos, mas é mais eficiente numa maneira
prática. [Mais otimizado e simplificado]
```

# Fatores não deterministas
```
Tempo 
Threads
...
```

# Atomic broadcast
```
Ordem igual para TODAS as réplicas
```

# SMR: State machine replication 

```
Objeitivos: Assegurar consistencia
de um sistema de réplicas.

Utiliza um protocolo de consensus 
Propagação de comandos
Execução deterministica
Tolerante a falhas
```

# Sistemas de coordenação

```
CHUBBY: Sistema de ficheiros distribuidos + LOCK MANAGER + PAXOS
ZOOKEPER: Semelhante

Chubby: Sistema de locks distribuido
    > dá lock
    > quem tem lock -> obrigado a enviar KEEP ALIVE
    > não envia -> Perde o privilégio

Problema: CACHING + Comunicação com periféricos -> Ex: Impressora

É importante balancear o nr de keep alive para não dar FLOOD 

O problema do caching é:
    > O cliente usa caching para ser mais rápido
        mas aqui o que está na cache pode estar desatualizado
    
O problema dos periféricos é: 
    > O cliente pede acesso a um periférico, não envia keep alive
        mas continua a utilizar o periférico. às tantas outro cliente
        também usa o periférico -> super bug
```