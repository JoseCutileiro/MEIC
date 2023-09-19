# Teorica de segunda

```
Bibliografia recomendada: Constraint programming - Rina Detcher
Quinta feira: Lab do projeto
Instancias para correr o projeto - Fenix
```

# Inferencias:

```
Vamos usar inferencias para reduzir o espaço de procura

Exemplo: 

A = 0 ou 1
B = 0 ou 1
C = 0 ou 1

A != B
A != C

Inferencia: B == C

O que é que ganhamos com isto? 

Espaço de procura original fica reduzido
(não temos que procurar em casos em que B != C)
```

## Conclusões
```
+ constraints = - espaço de procura
equivalentes <-> mesmo espaço de solução
```

# CSP Inconsistente

```
Um CSP inconsistente é um CSP cujo espaço de solução
é vazio

exemplo: 
A == B /\ B != A
```

# Como fazer inferências?

```
Fazer inferencias é uma coisa muito lenta

O nosso objetivo é diminuir o espaço de procura, fazendo
um problema equivalente mas com RESTICOES mais explicitas

Repara que, as cosntraints podem ser tão explicitas que nos levam
diretamente à solução sem usar sequer procura, mas no geral isto é muito
complicado. Exigindo um número exponencial de constraints

Soluçáo parcial > Usada na procura, é basicamente escolher um subset do 
set original, atribuir valores possiveis, para depois fazer crever a arvore de procura

```

# Consistency enforcing algorithms

``` 

Técnica usada: ARC Consistency
    > baseado em pares de variaveis
    > ver se há valores de dominio useless

Técnica usada: Path consistency
    É o mesmo conceito mas aplicado a trios de variaveis

Depois tens o caso genérico
    i-consistency 
```

# Arc consistency

```
No lab vamos usar este algoritmo à mão, por enquanto vamos focar em perceber 
como é que isto funciona

VARIAVEL: É um não arc consistency com as outras variaveis
CONSTRAINT: É ou não arc consistency para uma dada variavel 

e.g. INTRO

X : Dominio é 1,2,3
Y : Dominio é 1,2,3
Constraint: Rxt = {X < Y}

Rxy não é arc.consistent relativo a x: O valor 3 não tem valor no Dy
Rxy não é arc.consistent relativo a y: O valor 1 não tem valor no Dx

CONCLUSÃO: Diminuir o dominio para
X {1,2}
Y {2,3}
```

# O método: REVISE 
```
Complexidade: k*k onde k é o tamanho do dominio

Sejam x e y duas variaveis com dominios (diferentes ou não)

void Revise(x,y) {
    vamos a todos os valores xi e vemos se pelo menos uma 
    restrição que implique x e y mantém esse valor de pé

        Se houver -> mantém
        Se não houver -> retira do dominio de x
}

Repara que revise não funciona nos dois sentidos

Para veres se um dado arco (x,y) é arc consistency ten
Tens que fazer revise(x,y) + revise(y,x) 
e o dominio final tem que ser igual ao inicial
```

 


