# DAD : Revisões

# Objetivos da cadeira

```
1. Perceber o problema de desenvolver
e desenhar aplicações distribuidas 

2. Estudar soluções para o problema

    > Architetura
    > Protocolos de comunicacao
    > Escalabilidade
    > Performance e dependability
```

## Tópicos a abordar: 

```
1. Paxos & MultiPaxos
2. Serviços de coordenacao
3. Comunicacao de grupo 
4. Replicação de BD
5. TCC (transactional causal consistency)
6. P2P Systems 
```

# Consensus

```

#1: O problema

1. Temos N processos
2. Cada um deles processa um input value
3. Todos os processos corretos devolvem o mesmo valor
4. O valor tem que ser um dos propostos
5. Pode ser qualquer um dos valores propostos

#2: Propriedades

1. Terminação: Todos os processos corretos EVENTUALMENTE terminam
2. Acordo uniforme: Sempre o mesmo valor decidido
3. Integridade: O valor decidido foi proposto
```

# Dificuldade deste problema? 

```
Vamos assumir que temos URB (uniform reliable broadcast)

URB 
    > Broadcast(m): Envia uma mensagem 
    > Deliver(m): Entrega a mensagem para a APP 

    > Validade: broadcast(m) <-> todos os corretos deliver(m)
    > No dupes 
    > if (deliver(m)) <-> algum processo broadcast(m)
    > if (deliver(m)) <-> todos os corretos deliver(m)

BOGUS CONSENSUS

#1: Primeira iteração 

Esperar por N valores e escolher com uma função determinista 
previamente acordada (ex: MIN) o valor

Problema: Se um processo falhar <-> DEADLOCK

#2: Segunda iteração

Esperar pelo número de processos que estão vivos, e aplicar 
a tal funcao determinista para decidir o valor

Problema: Outputs podem ser diferentes
```

# TRB: Terminating reliable broadcast

```

Ideia: Temos um Sender e vários Listeners
a ideia é muito simples, é o sender enviar VALUE 
e todos os Listeners corretos devolvem VALUE

1: O objetivo é garantir que todas as mensagens sejam 
entregues de forma confiavel

2: TRB termina e é tolerante a falhas
```

# Implmentar TRB: Consensus + (P)

```
Antes de mais explicar o que é o (P)

(P): Perfect failure detector
> Não existem falsos positivos, e se um processo
falhar, o (P) irá EVENTUALMENTE descubir

(a implemntação do TRB é um bocado estranha: Ver slides)
```

# Leader based consensus with P

```
Agora a ideia é só mostrar como teriamos consensus 
se utilizarmos (P)

> O algoritmo funciona em épocas, cada época tem um lider
> O processo N é lider se os anteriores N-1 falharem
> Por default 1 é lider

O lider envia o seu valor aos outros procesos, e os outros
aderem ao seu valor enviando ACK ao lider

O lider espera pelo ACK de todos os corretos

O lider dá commit do valor > O valor irá ser decidido não
há volta a dar
```

# Perfect failure detector

```
Só temos aqui um probleminho,assumir (P) é 
o mesmo que esconder o SINCRONISMO 
ou seja não estamos a resolver o problema
num sistema assincrono.

E ná prática um (P) é muito dificil de implmentar
é dificil destinguir um processo lento de um 
processo que falhou

Novo conceito: Unreliable failure detector

> Suspeita que um processo falhou mas pode estar errado
> Dá para resolvero o consensu assim? 
```

# FLP: Impossibilidade de consensus

```
Não existe um protocolo determinista que resolve o
consesnsus num sistema assincrono onde um ou mais
processos podem bugar lá pelo meio
```

# De (P) para PAXOS

```
Agora o objetivo é tentar esquecer o perfect failure
detector para resolver o problema num sistema assincrono

PROBLEMA 1: O lider não pode esperar pelo ACK de todos os processos
SOLUÇÃO: Esperar pelo ACK da maioria dos processos 

PROBLEMA 2: Quando um lider falha e um novo começa, o novo lider
            pode ter sido excluido da maioria do lider anterior
SOLUÇÃO: Novo lider deve perguntar aos outros procesos o que é que os
            os lideres anteriores andaram a fazer

PROBLEMA 3: Multiplos lideres em paralelo 
SOLUÇÃO: ???

Aqui aparece o paxos
```

# Paxos (asincrono, sem falhas bizantinas)

```
O paxos é um algoritmo que resolve consenso mas 
assumo sincronia suficiente durante um curto periodo de tempo 

1. As meensagens podem demorar tempo arbitratio
2. Pode haver dupes
3. Podem-se perder mensagens
4. As mensagens não podem ser corrompidas

AGENTES:
1. Os que propoem
2. Os que aceitam
3. Os que aprendem

Temos um set dos que propoeem {p1,p2,...,pn}
Pré acordo que p1 é lider
Se p2 acredita que p1 crashou -> torna-se lider
Se p3 acredita que p1 e p2 crasharam -> torna-se lider
[...]

Como não estamos a assumir que o detetor de falhas é perfeito
eles podem-se enganar, ou seja, p1 pode ser lider noutra circustância

p1 é lider em 1,n+1,2*n+1,...
p2 é lider em 2,n+2,...
...
pn é lider em n,2*n,...
```

# O que faz o lider (intuition)

```
> Cada lider tem duas etapas 
    1:: Tenta ver vestigios de atividade do passado de outros lideres,
        e escolhe um valor que é consistente com a decisão prévia
    2:: Tentar ter uma maioria a apoiar o seu valor 

    Se (2) acontecer com sucesso: GG WP 

> Cada processo mantém um tuplo com o valor adotado previamente

    <VALUE,WRITE_TS,READ_TS>

    Inicialização: <valor,0,0>
```

# Exemplo de uma execução que corre bem

```
N processos, 1 é lider

Envia ACCEPT!(1,valor)

Esperar por N/2 - 1 processos respondam ACCEPTED(1,valor)
Quando estes aceitam o valor o seu tuplo fica <A,1,0>
```

# Então e se isto não correr bem?

```
Por exemplo, P1 vai à vida.
P2 envia para os outros processos PREPARE(2) 
Espera que a maioria dos processos diga PROMISE(WRITE_TS,valor)
P2 Adota o valor mais recente escrito (se ainda tiverem o write_TS a 0 adota o seu valor)
Agora P2 volta a fazer uma execução normal
```

# Então e se ficarmos com dois lideres concurrentes?

```
Para isso é que vamos usar o READ_TS
O read ts guarda o ultimo prepare recebido

O write TS manda a ultima vez que mandámos accept


Meesmo assim fica de pé um problema: LIVELOCK (iremos ver na próxima aula)
```