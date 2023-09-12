# DAD: Desenvolvimento de aplicacoes distribuidas

## Cenas para hoje:

1. Objetivos
2. Bibliografia
3. Avaliação
4. Datas importantes
5. Apresentações nos labs? Como apresentar

## Objetivos gerais

1. Construir, planear e executar sistemas distribuidos de larga escala

### O que já falámos?

1. Consenso 
2. Sistema sincrono 

## Problema de sistema assincrono?

1. Falhou ou  está lento?

## No mestrado: 

1. Vamos melhorar os algortimos para conseguirem lidar com sistemas assincronos
2. Vamos focar em LARGE SCALE systems

# Overview dos tópicos

1. Consenso em sistemas parcialmente sincronos:
- Paxos and Multi-paxos
- Crucial para construir este tipo de sistemas

2. Serviços de coordenação 
- Chubby and zookeper 
- Sistema de ficheiro distribuidos 

3. Group communication and View synshrony
- Ter uma ideia do sistema
- Reconfigurações
- Escalar para cima ou para baixo
- Replicar 
  
4. Reconfigurar paxos

## Paxos: Serviço de consenso

# Tipos de sistemas

1. Database replication
```
Sistem as Rápidos
Sistemas fiaveis
    > Sem erros 
    > Tolerantes a falhas
(podem ser sistemas com informação sigilosa e.g: bancos)

Replicação parcial
(diferentes grupos replicam diferentes partes de dados)

Sistemas de elevada consistencia
```

2. TCC (transactional causal consistency)
```
Teorema CAP: Consistencia, availability e partition (dos 3 escolhe 2)

TCC é um modelo de consistencia mais forte que pode ser implementado sem bloquear
TCC: A + P ( não é SUPER SUPER consistente mas é consistente o suficiente)
```

3. P2P systems (são os mais escalaveis, existem vários tipos)
```
Unstructured P2P : Peer sampling
Structured P2P: chord and Pastry
```

# Bibliografia:

1. Distributed Sytems: Couloris (um bocado outdated pk esta cadeira usa cenas muito recentes)
2. Papers: Pacos, zookeper, spanner

# Avaliação: 

1. Exam: 45%
2. Projeto: 45% (grupos de 3) 
(projeto tem uma entrega intermedia que so serve para ajudar, se tiveres pior nota nao conta)
(é preciso registar para os labs)
3. Apresentação: 10% (sobre um paper escolhido por nós)

- Datas:
1. exam1: Nov 8
2. exam2: Jan 30
3. Proj: checkpoint oct6, Final: Oct27
4. Demos e discussão: 30 oct para aí 

#  Labs: 

1. .Net framework C# and gRPC

# Como apresentar um PAPER?

1. Motivação 
2. Structure of a presentation 
3. Questions

> TOP Down aproach: Intro, main, datails,conclusion 

```
O mais importante: O inicio, ser simples e apresentar bem qual é o problema 
Focar bastante  na apresentação do problema 

Terminologia correta
Trabalho relacionado: O que é que já foi feito à volta disto
O que é que o PAPER trás de novo? 
Road-Map do que é que nos resta para o resto da apresentação

Objetivo: Convencer a audiencia que o que estamos a apresentar é util e interessante
Selecionar um topico principal: Relevante mas não trivial

Para perceber os papers provavelmente vamos ter que ver as referencias

Conclusao: 
Sumario final
Identificar limitações
```