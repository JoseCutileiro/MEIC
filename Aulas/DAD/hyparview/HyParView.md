# HyParView: a membership protocol for reliable goosip-based broadcast

# Relembrar o gossip

1. Acesso rápido aos clientes
2. Mesmo em situações de partições
3. Sacrifica um pouco a coerencia

- Novas modificações em background (boato/rumor)
- Réplicas - Podem ter vistas divergentes
- Valores que o cliente lê são SEMPRE coerentes
- Também permite coerencia forte (mas os slides não abordam)
- Este tipo de protocolos baseia-se na forma como os virus ou os rumures se espalham pela nossa sociedade

"BACKGROUND UPDATE // PROPAGATION": Este tipo de algoritmos é aplicado normalmente a ambiente de cloud computing, large scale distributed systems e base de dados descentralizadas, dado que permite uma enorme escalabilidade e rapidez

# Protocolos gossip

Este tipo de protocolos são uma estratégia poderosa para implementar sistemas muito escaláveis e resilientes. Cada participante do protocolo mantém uma vista parcial do sistema. A confiança do protocolo depende de algumas propriedades destas vistas

1. O degree de distribuição 
2. Clustering coefficient

Muitos algoritmos tentam propor "manter vistas parciais para protocolos gossip". Para relembrar o que significa partial view neste contexto, é apenas uma estratégia usada pelos algoritmos que fazem o controlo da informação que cada nó "sabe" do sistema como um todo.

```
Manter o estado do sistema inteiro num nó pode ser dificil e pode acabar por desperdiçar muitos recursos. Assim muitos algoritmos tentam representar apenas a vista parcial (um subset de nós). A ideia é os nós em particular apenas conhecem um número pequeno de nós (neighbors), mas no geral eles conhecem o sistema completo (comunicando//gossipando)
```

Mas isto não é só coisas bonitas, existe um caso em  que este tipo de abordagens não funciona bem: Quando existem muitas falhas no sistema. Para combater este problema, o paper apresenta o HyparView. Em que a ideia é ter duas partial views distintas (com objetivos diferentes e mantidas de maneira diferente)

# Introdução: Caso standard (global view)

Num sistema gossip, quando um nó quer fazer broadcast, seleciona t nós (ao calhas). Nota: O número t é um atributo chamado fanout. Quando m nó recebe a mensagem repete este processo. Podemos ver que existe bastante redundância por aqui, multiplos nós irão receber a mesma mensagem repetidamente, mesmo assim a carga é distribuida pelo sistema de forma praticamente justa e quase sem trabalho nenhum.

# Introduçao: Partial view

No sistema acima cada nó conhece o sistema inteiro (ou seja todos conhecem todos). Como podem prever facilmente este sistema não é escalável (temos que manter todas as ligações durante o tempo inteiro). Para 'vencer' este problema muitos algoritmos usam a chamada vista parcial (em que em vez de conhecer a rede completa, cada nó sabe apenas um subset do sistema). O processo repete-se, mas em vez de tirarmos t nós do sistema ao calhas, retiramos t nós da nossa vista parcial. Isto depende de um sistema que se chama 'membership service'. 

# Membership service:
Simplificando ao máximo, este serviço permite 
1. Fazer tracking dos nós
2. Encontrar nós
3. Que nós é que estão a falhar, e o que fazer neste caso
4. Tratam de organizar os quorums
5. Tratam da elasticidade e escalabilidade do sistema
6. Segurança: Apenas nós autorizados podem juntar à festa

Alguns sistemas conhecidos de membership service são: 
1. Apache zookeper
2. Amazon elastic load balancing

# continuando...

MASSSSS...
Se um nó conhece apenas um número reduzido do sistema, fica mais vulnerável a falhas, em particular, se existirem MUITAS falhas todo o sistema fica mais vulneravel, e vai utilizar muitos dos serviços do 'membership service', este serviço pode ainda demorar muito tempo a restaurar o sistema, afetando a 'reliability' das mensagens que foram espalhadas durante a quebra. 

# Este paper: HyParView

1. Usar TCP (reliable) para fazer o gossip entre os vários pares. Assim evitamos tratar do sistema em que existem network omissions

2. Cada nó tem uma 'small symmetric active view' (tem fanout + 1 nós). Usar TCP permite que o fanout seja um numero pequeno comparando com outras que usam protocolos menos confiantes. O broadcast é feito deterministicamente by flododing the graph defined by the active view. O grafo é gerado pelo (membership sevice).

3. O TCP é usado como failure detector (dado que existem muitas mensagens a fluir, este detetor de falhas é significativamente rápido a agir)

4. Existe para além da active view uma ... podem adivinhar ... Passive view, tem multiplos backup nós, que podem passar para a active view caso haja alguma falha ou coisa do género de um membro que está na active view.

5. O protocolo de membership tem que tratar de manter a passive view, e para além disso tem que ver que membros é que podem ser 'promovidos' para a active viewassim que for necessário. Aliás, ambas as vistas parciais são mantidas pelo membership protocol

# Hybrid partial view

Vamos mostrar que este approach, não só permite usar fannouts mais pequenos (ou seja menos carga no sistema), mas também oferece mas resiliência na presença de falhas (até na presença de elevados números de falhas). Eles prometem que o protocolo permite recuperações de sistemas com falhas até 90% dos nós em apenas 4 rondas do membership. Isto é muito melhor comparativamente com as ideias anteriores. 

# Importância de saber lidar com um elevado número de falhas:

Existem algumas situações em que é importante conseguir lidar com um elevado número de falhas

1. Desastres naturais, virus 

No paper eles dizem que um virus pode mandar até 10 milhoes de nós  num espaço de dias

# Related work

## Vistas parciais

Cada nós tem um conjunto de n nós (n == fannout), representação de nós (ip,port). O protocolo de membership tem responsabilidade de inicializar os nós e de manter a vista parcial de cada nó durante o periodo de execução. A vista parcial pode ir mudando (devido a falhas, bloqueios, mais nós, menos nós ...)

1. MANTER VISTA PARCIAL

```
Duas estratégias:
    > Reactive stategy: Só muda em caso de evento externo (adicionar ou remover nós)

    > Cyclic stategy: Atualizar a vista de x em x tempos 

    O reactive stategy depende de um failure detector, se tiveres um detetor bom o reactive é melhor, caso contratio o cyclic é melhor.
```

# Propriedades das partial views

Nota: as partial views são grafos COM DIREÇÃO

De modo a que funcione, as partial views dependem de algumas coisas:

1. Conetividade: Permitir que o broadcast seja mesmo um broadcast (não existem nós isolados)
2. Degree distribution: Fazer com que seja bem distribuido
    > in degree (os que o conhecem) \
    > out degree (os que ele conhece)
3. Average path lenght: A média dos caminhos entre todos os nós, cada caminho é medido com o número de nós intermédios necessários para que a comunicação se dê entre os dois nós.
4. Clustering coefficient (valor entre 0 e 1), número de egdes entre o neighbor e o maximo de edges entre esses neighbors. O clustering coefficient é a média desses valores
5. Accuracy: O numero de nós que não falhou / o numero de neighbors total de esse nó

# Membership and gossip protocols

1. Scamp: é um reactive membership protocol, mantém duas vistas, a PARTIAL e a INVIEW (a inview é os que ele recebe mensagem). O scamp permite que o tamanho da PARTIAL não seja fixo. (normalmente log n). Para atualizar a partial view utilizam um protocolo de subscrição => corre quando um novo processo se junta ao sistema. De modo a recuperar os nós enviam um «a espécie de ping que eles chamam de heartbeat que é lançado periodicamente para todos os nós na partial view. Se um nó não receber o hearbeat durante x tempos, assumimos que está isolado e fazemos com que se junte novamente.

2. Cyclon: é um cyclic membership prrotocol, que corre o que chamam de shufflle passado um dado intervalo de tempo. 

3. NeEM (network friendly epidemic multicast), usa TCP para espalhar a informação, isto evita as perdas devido a congestão. Neste paper dependemm de TCP para mascarar network omissions e para failure detector, portanto o trabalho é complementar ao NeEM

4. CREW flash dissemination: muitos download de ficheiros em simultanio para muita gente. Usa TCP, mantém uma cache de conecçoes abertas (usa random walk), isto diminui o tempo necessário para abrir uma nova ligação -> pode ser usado no HyParView para a passive view.

# RELIABITY NO GOSSIP: 

```
100% -> significa que a mensagem chegou a todos os nós ativos (é o mesmo que um boradcast atómico)
```

# Motivação: 

Estes gajos começaram a trabalhar nisto por dois motivos

1. O fanout de um gossip protocol depende do objetivo, tanto o nivel de resistencia a falhas que se quer, como o nivel de reliability que se quer. O objetivo é escolher boas views, e usar o TCP (deste modo deve ser possivel usar um fanout mais pequeno)

# Gráficos I 

```
Para entregar 50 mensagens, numa network de 10k nós

Cyclon: Precisa de fanout de 6 para alcançar 99.9%

Scamp: Precisa de fanout de 6 para alcançar 99%

Eles irão mostrar que com o aprouach deles consegue m mais reliability com um valor perto de log(n) para o fanout
```

# Gráficos II

```
Num sistema em que 50% dos nós estão falhados, estes protocolos não conseguem ultrapassar os 85% (a reliability é completamnete perdida), e isto pode ser inaceitável em vários sistemas que usamos hoje me dia
```

# HyParView

E é aqui que aparece o HyParView

# Relembrar:

Manter duas vistas 

1. Active view (fanout + 1): Dado que os links são simetricos e cada nó deve evitar depender de cada mensagem

2. Passive view (maior) Que assegura a conetividade mesmo com BUÉ da falhas (deve ser maior que log(n)) (o overhead desta view é pouco dado que não é para manter as conexoes abertas)

3. A active view serve para a disseminação da mensagem (é simétrica: Ou seja se p está na active view de q então q está na active view de p). Assumimos o TCP como protocol de transporte, permite com que a active view seja pequena. Sempre que queremos fazer broadcast, lançamos para todos menos para o que fez a mensagem, aqui o gossip também é deterministico. Mas o overlay aqui é criado de forma random -> Utiliza um protocolo de membership

# Protocol de membership usado:

Usamos uma reactive strategy para manter a active view. Os nodes podem dar join a esta view quando se conectam ao sistema, e removidos quando falham. A cada mensagem, o overlay* é testado implicitamente 
\
*overlay: Topologia da rede (trocando por miudos)
\
A passive view não é usada para fazer a disseminação da mensagem, é apenas manter uma lista de nós que podem substituir os nós da active view em caso de falhas, a passive view utiliza uma estratégia CYCLIC (periodicamente -> shuffle in the house). Para além do shuffle normal eles fazem com que a probabilidade de ter nós ativos na passivew view seja grande (isto faz com que todos os nós que falharam sejam removidos da passive view automaticamente passado um dado numero de epocas)

# Mecanismos de join (join request)

1. Quando um nó decide juntar ao overlay, tem que conhecer um nó que já pertence ao overlay (contact node). 

2. Para isto o novo node (n) tem que estabelecer uma conecção TCP com o seu contact node (c). 
\
Basicamente n -----> c (JOIN REQUEST)

## O que faz o contact node?

1. Adiciona n à sua active view (mesmo que tenha que dar drop de um nó random qualquer, neste  caso vai ter que enviar DISCONNECT apra o nó que quer dropar da active view)

2. Vai depois enviar um FORWARD JOIN com o novo nó (este request é propagado no overlay utilizando random walk* + um parametro*)

3. Para além disto ainda tens que fazer duas configuration parametres 
   1. ACTIVE RANDOM WALK LENGTH (ARWL): nr de hops o forward join propagou
   2. PASSIVE RANDOM WALK LENGTH (PRWL): quando é que o novo nó foi inserido na passive view

NOTAS:

1. Random walk: A ideia é explorar  a topologia da rede de forma estocástica/aleatória

2. Parametro: time to live -> inicialmente começa a ARWL e vai decrementando a cada hop

3. VER O ALGORITMO I no paper para perceber, o texto está um bocado confuso
